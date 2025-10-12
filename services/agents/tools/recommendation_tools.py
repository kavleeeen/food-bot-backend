"""
LangChain Tools for Food Recommendations
"""

from langchain.tools import tool
from langchain.chat_models import init_chat_model
import os

# Initialize Gemini using universal initialization
model = init_chat_model(
    "gemini-2.0-flash-exp",
    model_provider="google_genai",
    temperature=0.7,
    google_api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyCsiox7IZixwTIpEe8cw95dGJxZrdtSx0U')
)

@tool
def generate_food_recommendation(preferences: dict, user_message: str = "") -> str:
    """Generate food recommendations based on user preferences and context"""
    try:
        print("=" * 60)
        print("🔧 RECOMMENDATION TOOL: generate_food_recommendation CALLED!")
        print(f"🔧 RECOMMENDATION TOOL: Generating recommendation with preferences: {preferences}")
        print(f"📝 RECOMMENDATION TOOL: User message: {user_message}")
        
        # Create context from preferences
        context = f"User preferences: {preferences}\n"
        if user_message:
            context += f"User message: {user_message}\n"
        
        prompt = f"""
        You are a food recommendation assistant for Indian users. Your goal is to eliminate decision fatigue by providing simple, nutritious meal suggestions.

        Based on the user's food preferences and message, provide exactly 3 food recommendations that are:
        1. EASY TO MAKE: Simple recipes or easy to order
        2. NUTRITIONALLY BALANCED: Good mix of carbs, protein, vegetables
        3. PRACTICAL: Can be made at home or ordered easily in India
        4. POPULAR: Common in Indian households (both traditional and modern)

        {context}
        
        Format each recommendation as:
        1. **Meal Name**  - Brief description
        2. **Meal Name**  - Brief description
        3. **Meal Name**  - Brief description

        For each meal, briefly mention why it's good (nutritional benefit, ease of preparation in not more than 6 words).

        Keep it conversational and helpful. Always provide exactly 3 numbered suggestions.
        Keep your response crisp and minimal.
        """
        
        print(f"🤖 RECOMMENDATION TOOL: Sending prompt to Gemini: {prompt}")
        response = model.invoke(prompt)
        print(f"📤 RECOMMENDATION TOOL: Gemini response: {response.content}")
        print("=" * 60)
        return response.content
    except Exception as e:
        print(f"❌ RECOMMENDATION TOOL: Error generating recommendation: {e}")
        return "Sorry, I'm having trouble generating recommendations right now."

@tool
def generate_detailed_recipe(food_name: str, preferences: dict) -> str:
    """Generate recipe, macros, and cooking instructions for a specific food"""
    try:
        print(f"🔧 RECIPE TOOL: Generating detailed recipe for {food_name}")
        print(f"📝 RECIPE TOOL: User preferences: {preferences}")
        context = f"Food: {food_name}\nUser preferences: {preferences}\n"
        
        prompt = f"""
        You are a food recommendation assistant for Indian users. Provide information for: {food_name}
        
        Include:
        1. SIMPLE INGREDIENTS: Easy-to-find ingredients in India
        2. STEP-BY-STEP INSTRUCTIONS: Clear, simple cooking steps
        3. NUTRITIONAL INFO: Basic macros (calories, protein, carbs, fat)
        4. COOKING TIME: How long it takes
        5. SERVING SUGGESTIONS: What to serve with it
        6. COOKING TIPS: Simple tips for success
        
        {context}
        
        Make it practical and easy to follow. Consider Indian cooking methods and available ingredients.
        Focus on simplicity and nutritional balance. Keep recipe not more than 100 words.
        """
        
        print(f"🤖 RECOMMENDATION TOOL: Sending detailed recipe prompt: {prompt}")
        response = model.invoke(prompt)
        print(f"📤 RECOMMENDATION TOOL: Detailed recipe response: {response.content}")
        return response.content
    except Exception as e:
        print(f"❌ RECOMMENDATION TOOL: Error generating detailed recipe: {e}")
        return "Sorry, I'm having trouble generating detailed information right now."
