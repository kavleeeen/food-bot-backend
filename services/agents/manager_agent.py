"""
Manager Agent for Food Bot
Coordinates preference collection and food recommendations using direct orchestration
"""

from langchain.chat_models import init_chat_model
from services.preference_service import PreferenceService
from services.agents.tools.recommendation_tools import generate_food_recommendation
from services.agents.tools.recipe_tools import generate_detailed_recipe, suggest_recipe_variations
import os

class ManagerAgent:
    def __init__(self):
        # Use universal initialization as per LangChain docs
        self.llm = init_chat_model(
            "gemini-2.5-flash",
            model_provider="google_genai",
            temperature=0.3,  # Lower temperature for more consistent intent detection
            google_api_key=os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
        )
        
        # Initialize services
        self.preference_service = PreferenceService()
        
        # System prompt for Indian context
        self.system_prompt = """You are a helpful food recommendation assistant designed specifically for Indian users. Your primary goal is to eliminate decision fatigue by providing simple, nutritious meal suggestions that users can easily make or ask someone to prepare.

Key Principles:
1. SIMPLICITY FIRST: Recommend easy-to-make, everyday meals that don't require complex cooking
2. NUTRITIONAL BALANCE: Focus on balanced meals with proper macros (carbs, protein, vegetables)
3. INDIAN CONTEXT: Understand Indian food culture - both traditional and modern (pizza, pasta, etc. are common in India)
4. DECISION FATIGUE: Make choices for users - don't overwhelm with too many options
5. PRACTICAL: Consider if the meal can be made at home or ordered easily
6. CRISP & MINIMAL: Keep responses short, direct, and to the point

Demographic: Indian users who want quick, nutritious meal decisions without overthinking."""
    
    def _analyze_user_intent(self, user_message: str, user_preferences: dict) -> str:
        """Analyze user message using Gemini 2.5 Flash to determine intent"""
        print(f"🔍 INTENT ANALYSIS: Analyzing message with Gemini: {user_message}")
        
        # Create context about user preferences
        prefs_context = "None" if not user_preferences else str(user_preferences)
        
        # Create intent analysis prompt
        intent_prompt = f"""
You are an intent analysis assistant for a food recommendation system. Analyze the user's message and determine their intent.

USER MESSAGE: "{user_message}"
USER PREFERENCES: {prefs_context}

INTENT OPTIONS:
- preferences: User is providing or updating their dietary preferences, restrictions, allergies, or food preferences
- recommendations: User wants meal suggestions, food recommendations, or is asking what to eat
- recipe: User wants detailed recipe, cooking instructions, or recipe variations for a specific dish
- chat: General conversation, greetings, or unclear intent

RULES:
1. If user mentions dietary info (vegetarian, vegan, allergies, cuisine preferences) → preferences
2. If user asks for food suggestions, recommendations, or what to eat → recommendations  
3. If user asks for recipe, cooking instructions, how to make, ingredients, or recipe variations → recipe
4. If user has complete preferences and asks general food questions → recommendations
5. If user just greets or has unclear intent → chat

RESPOND WITH ONLY ONE WORD: preferences, recommendations, recipe, or chat
"""
        
        try:
            print(f"🤖 INTENT ANALYSIS: Sending prompt to Gemini 2.5 Flash")
            response = self.llm.invoke(intent_prompt)
            intent = response.content.strip().lower()
            
            # Validate the response
            valid_intents = ["preferences", "recommendations", "recipe", "chat"]
            if intent not in valid_intents:
                print(f"⚠️ INTENT ANALYSIS: Invalid response '{intent}', defaulting to chat")
                intent = "chat"
            
            print(f"🎯 INTENT ANALYSIS: Gemini detected intent: {intent}")
            return intent
            
        except Exception as e:
            print(f"❌ INTENT ANALYSIS: Error with Gemini, falling back to keyword matching: {e}")
            
            # Fallback to simple keyword matching
            message_lower = user_message.lower()
            
            # Preference-related keywords
            preference_keywords = [
                "vegetarian", "vegan", "gluten-free", "allergies", "allergic", 
                "indian", "italian", "chinese", "mexican", "cuisine", "food type",
                "dietary", "restrictions", "preferences", "like", "dislike"
            ]
            
            # Recommendation keywords
            recommendation_keywords = [
                "what should i eat", "recommend", "suggestion", "meal", "food",
                "hungry", "eat", "lunch", "dinner", "breakfast", "snack"
            ]
            
            # Check for preference intent
            if any(keyword in message_lower for keyword in preference_keywords):
                print("🎯 INTENT: User wants to provide/update preferences")
                return "preferences"
            
            # Check for recommendation intent
            elif any(keyword in message_lower for keyword in recommendation_keywords):
                print("🎯 INTENT: User wants meal recommendations")
                return "recommendations"
            
            # Check if user has complete preferences for recommendations
            elif user_preferences and len(user_preferences.get("restrictions", [])) > 0:
                print("🎯 INTENT: User has preferences, defaulting to recommendations")
                return "recommendations"
            
            # Default to chat
            else:
                print("🎯 INTENT: General chat")
                return "chat"
    
    def _collect_preferences(self, user_id: str, user_message: str) -> str:
        """Collect user preferences based on their message"""
        print(f"📝 PREFERENCE COLLECTION: Processing for user {user_id}")
        
        saved_preferences = []
        message_lower = user_message.lower()
        
        # Check for "no allergies" case
        no_allergies_indicators = ["no allergies", "no allergic", "not allergic", "no food allergies"]
        if any(indicator in message_lower for indicator in no_allergies_indicators):
            print("🔍 PREFERENCE: User mentioned no allergies, saving as 'none'")
            self.preference_service.add_preference(user_id, "allergies", "none")
            saved_preferences.append("allergies: none")
        
        # Check for other preference indicators
        preference_indicators = {
            "vegetarian": "restrictions",
            "vegan": "restrictions", 
            "gluten-free": "restrictions",
            "allergies": "allergies",
            "allergic": "allergies",
            "indian": "cuisine_preferences",
            "italian": "cuisine_preferences",
            "chinese": "cuisine_preferences",
            "mexican": "cuisine_preferences"
        }
        
        for indicator, pref_type in preference_indicators.items():
            if indicator.lower() in message_lower:
                print(f"🔍 PREFERENCE: User mentioned '{indicator}', saving as {pref_type}")
                self.preference_service.add_preference(user_id, pref_type, indicator)
                saved_preferences.append(f"{pref_type}: {indicator}")
        
        if saved_preferences:
            return f"Saved preferences: {', '.join(saved_preferences)}"
        else:
            return "No specific preferences detected in message"
    
    def _handle_recipe_request(self, user_message: str, user_preferences: dict) -> str:
        """Handle recipe requests using Gemini directly"""
        print(f"🍳 RECIPE HANDLER: Processing recipe request: {user_message}")
        
        # Extract meal name from the message using better logic
        message_lower = user_message.lower()
        meal_name = ""
        
        # Common patterns to extract meal names
        patterns = [
            "recipe for",
            "how to make",
            "cooking instructions for",
            "ingredients for",
            "variations for",
            "recipe of",
            "how to cook"
        ]
        
        # Try to extract meal name using different patterns
        for pattern in patterns:
            if pattern in message_lower:
                # Extract text after the pattern
                parts = message_lower.split(pattern)
                if len(parts) > 1:
                    after_pattern = parts[1].strip()
                    # Clean up the meal name
                    meal_name = after_pattern.replace("?", "").replace(".", "").strip()
                    break
        
        # If no pattern matched, try to extract from the whole message
        if not meal_name:
            # Remove common recipe words and get the remaining text
            recipe_words = ["recipe", "how", "to", "make", "cook", "cooking", "instructions", "ingredients", "variations", "for", "of", "the", "a", "an"]
            words = message_lower.split()
            filtered_words = [word for word in words if word not in recipe_words]
            if filtered_words:
                meal_name = " ".join(filtered_words).strip()
        
        print(f"🍳 RECIPE HANDLER: Extracted meal name: '{meal_name}'")
        
        # If no specific meal mentioned, ask for clarification
        if not meal_name or len(meal_name) < 3:
            return "I'd be happy to help you with a recipe! Which dish would you like the recipe for? Just tell me the name of the meal you want to cook."
        
        # Check if user wants variations
        if any(word in message_lower for word in ["variation", "variations", "different", "alternative"]):
            print(f"🔄 RECIPE HANDLER: User wants variations for: {meal_name}")
            return suggest_recipe_variations(meal_name, user_preferences)
        else:
            print(f"🍳 RECIPE HANDLER: User wants detailed recipe for: {meal_name}")
            return generate_detailed_recipe(meal_name, user_preferences, user_message)
    
    def _handle_general_chat(self, user_message: str) -> str:
        """Handle general conversation when user intent is not clear"""
        print(f"💬 GENERAL CHAT: Handling message: {user_message}")
        
        # Simple responses for common greetings
        greetings = {
            "hello": "Hi! I'm here to help you decide what to eat. What are you in the mood for?",
            "hi": "Hello! Ready to find your next meal? Just tell me what you're craving!",
            "hey": "Hey there! Let's figure out what delicious food you should have today!",
            "thanks": "You're welcome! Happy to help with your food decisions!",
            "thank you": "You're welcome! Hope you enjoy your meal!",
        }
        
        message_lower = user_message.lower().strip()
        for greeting, response in greetings.items():
            if greeting in message_lower:
                return response
        
        # Default response
        return "I'd love to help you decide what to eat! Do you have any dietary preferences I should know about?"
    
    def process_message(self, user_id: str, message: str, chat_history: list = None):
        """Process user message using direct orchestration"""
        try:
            print(f"🤖 MANAGER AGENT: Starting orchestration for user {user_id}")
            print(f"📝 MANAGER AGENT: Message: {message}")
            
            # Get user preferences for context
            preferences = self.preference_service.get_user_preferences(user_id)
            print(f"📊 MANAGER AGENT: User preferences: {preferences}")
            
            # Step 1: Analyze user intent
            intent = self._analyze_user_intent(message, preferences)
            print(f"🎯 MANAGER AGENT: Detected intent: {intent}")
            
            # Step 2: Route to appropriate handler based on intent
            if intent == "preferences":
                # User is providing preferences
                preference_result = self._collect_preferences(user_id, message)
                print(f"📝 MANAGER AGENT: Preference collection result: {preference_result}")
                
                # Get updated preferences after saving
                updated_preferences = self.preference_service.get_user_preferences(user_id)
                missing_preferences = self.preference_service.get_missing_mandatory_preferences(updated_preferences or {})
                print(f"📊 MANAGER AGENT: Updated preferences: {updated_preferences}")
                print(f"🔍 MANAGER AGENT: Missing preferences: {missing_preferences}")
                
                # Check if we need to ask for more preferences
                if len(missing_preferences) > 0:
                    if "restrictions" in missing_preferences:
                        response = "I'd love to help you decide what to eat! First, do you have any dietary restrictions? Like vegetarian, vegan, or any foods you avoid?"
                    elif "allergies" in missing_preferences:
                        restrictions = updated_preferences.get("restrictions", []) if updated_preferences else []
                        response = f"Got it! Do you have any food allergies I should know about? This helps me suggest safe options."
                    elif "cuisine_preferences" in missing_preferences:
                        restrictions = updated_preferences.get("restrictions", []) if updated_preferences else []
                        allergies = updated_preferences.get("allergies", []) if updated_preferences else []
                        response = f"Perfect! Last question - what type of food are you in the mood for? Indian, Italian, Chinese, or anything specific?"
                    else:
                        response = "I'd love to help you decide what to eat! Do you have any dietary preferences I should know about?"
                else:
                    # All preferences collected, provide recommendations
                    response = generate_food_recommendation.invoke({
                        "preferences": updated_preferences,
                        "user_message": message
                    })
                
            elif intent == "recommendations":
                # User wants recommendations
                if preferences and len(preferences.get("restrictions", [])) > 0:
                    response = generate_food_recommendation.invoke({
                        "preferences": preferences,
                        "user_message": message
                    })
                else:
                    response = "I'd love to help you decide what to eat! First, do you have any dietary restrictions? Like vegetarian, vegan, or any foods you avoid?"
            
            elif intent == "recipe":
                # User wants recipe
                response = self._handle_recipe_request(message, preferences)
            
            else:  # intent == "chat"
                # General conversation
                response = self._handle_general_chat(message)
            
            print(f"✅ MANAGER AGENT: Final response: {response}")
            return response
            
        except Exception as e:
            print(f"❌ MANAGER AGENT: Error in orchestration: {e}")
            import traceback
            traceback.print_exc()
            return "Sorry, I'm having trouble processing your request right now."
