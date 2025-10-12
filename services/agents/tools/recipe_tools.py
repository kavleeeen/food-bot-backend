"""
Recipe Generation using Gemini API directly
"""

import google.generativeai as genai
import os

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCsiox7IZixwTIpEe8cw95dGJxZrdtSx0U')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_detailed_recipe(meal_name: str, user_preferences: dict = None, user_message: str = "") -> str:
    """Generate detailed recipe with ingredients, instructions, and nutritional info for a specific meal"""
    try:
        print(f"🍳 RECIPE TOOL: Generating detailed recipe for: {meal_name}")
        
        # Create context from preferences
        context = ""
        if user_preferences:
            restrictions = user_preferences.get("restrictions", [])
            allergies = user_preferences.get("allergies", [])
            cuisine_preferences = user_preferences.get("cuisine_preferences", [])
            
            if restrictions:
                context += f"Dietary restrictions: {', '.join(restrictions)}\n"
            if allergies and "none" not in allergies:
                context += f"Allergies: {', '.join(allergies)}\n"
            if cuisine_preferences:
                context += f"Preferred cuisines: {', '.join(cuisine_preferences)}\n"
        
        if user_message:
            context += f"User request: {user_message}\n"
        
        prompt = f"""
        You are a recipe expert for Indian users. Generate a concise recipe for the requested meal.

        MEAL: {meal_name}
        
        {context}
        
        Provide a SHORT recipe (under 100 words) with:
        1. Key ingredients (quantities for 2-3 people)
        2. Prep & cook time
        3. Main cooking steps (3-4 steps max)
        4. Basic nutritional info
        
        Requirements:
        - Use common Indian ingredients
        - Keep it simple and practical
        - Consider dietary preferences
        - Be concise but complete
        
        Format: Brief, clear, under 100 words total.
        """
        
        print(f"🤖 RECIPE TOOL: Sending prompt to Gemini: {prompt}")
        response = model.generate_content(prompt)
        print(f"📤 RECIPE TOOL: Gemini response: {response.text}")
        return response.text
        
    except Exception as e:
        print(f"❌ RECIPE TOOL: Error generating recipe: {e}")
        return f"Sorry, I couldn't generate the recipe for {meal_name} right now. Please try again later."

def suggest_recipe_variations(meal_name: str, user_preferences: dict = None) -> str:
    """Suggest variations and modifications for a specific meal recipe"""
    try:
        print(f"🔄 RECIPE VARIATIONS: Suggesting variations for: {meal_name}")
        
        # Create context from preferences
        context = ""
        if user_preferences:
            restrictions = user_preferences.get("restrictions", [])
            allergies = user_preferences.get("allergies", [])
            cuisine_preferences = user_preferences.get("cuisine_preferences", [])
            
            if restrictions:
                context += f"Dietary restrictions: {', '.join(restrictions)}\n"
            if allergies and "none" not in allergies:
                context += f"Allergies: {', '.join(allergies)}\n"
            if cuisine_preferences:
                context += f"Preferred cuisines: {', '.join(cuisine_preferences)}\n"
        
        prompt = f"""
        You are a creative cooking expert for Indian users. Suggest variations for the given meal.

        MEAL: {meal_name}
        
        {context}
        
        Provide 3-4 variations (under 100 words total):
        1. **QUICK VERSION** - Faster prep
        2. **HEALTHY VERSION** - More nutritious
        3. **FUSION VERSION** - Mix cuisines
        4. **SEASONAL VERSION** - Adapt for seasons
        
        For each: Key changes, why different, when to use.
        Keep practical for Indian kitchens.
        Be concise and clear.
        """
        
        print(f"🤖 RECIPE VARIATIONS: Sending prompt to Gemini: {prompt}")
        response = model.generate_content(prompt)
        print(f"📤 RECIPE VARIATIONS: Gemini response: {response.text}")
        return response.text
        
    except Exception as e:
        print(f"❌ RECIPE VARIATIONS: Error suggesting variations: {e}")
        return f"Sorry, I couldn't suggest variations for {meal_name} right now. Please try again later."
