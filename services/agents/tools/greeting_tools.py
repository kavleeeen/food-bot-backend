"""
LangChain Tools for Greeting and General Conversation
"""

# from langchain.tools import tool
import random

# Pre-stored greeting messages
GREETING_MESSAGES = [
    "Hello! I'm your personal food recommendation assistant. I'm here to help you discover delicious and nutritious Indian meals. What can I help you with today?",
    "Hi there! Welcome to your food companion. I specialize in suggesting simple, healthy Indian meals that are easy to make or order. How can I assist you?",
    "Hey! Great to meet you! I'm your food recommendation buddy, focused on helping you find the perfect Indian meal. What brings you here today?",
    "Hello! I'm excited to help you with your food choices. I specialize in Indian cuisine and can suggest meals based on your preferences. What would you like to know?",
    "Hi! I'm your food recommendation assistant, here to make your meal decisions easier. I love helping people discover tasty Indian food. How can I help you today?",
    "Hey there! Welcome! I'm your personal food guide, specializing in Indian cuisine. I'm here to help you find the perfect meal. What can I do for you?",
    "Hello! I'm your food recommendation assistant, designed to help you with simple, nutritious Indian meal suggestions. What kind of food adventure are we going on today?",
    "Hi! Great to see you! I'm your food companion, here to help you discover amazing Indian meals that are both delicious and easy to prepare. How can I assist you?",
    "Hey! I'm your food recommendation assistant, passionate about helping you find the perfect Indian meal. What brings you here today?",
    "Hello there! I'm your food buddy, specialized in Indian cuisine recommendations. I'm here to make your meal planning easier. What can I help you with?"
]

# Keywords that indicate greeting intent
GREETING_KEYWORDS = [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
    "greetings", "howdy", "what's up", "how are you", "nice to meet you",
    "good day", "hi there", "hey there", "hello there", "greetings"
]

# @tool
def detect_and_respond_to_greeting(user_message: str) -> str:
    """Detect if user is greeting and respond with a shuffled greeting message"""
    print("=" * 60)
    print("🔧 GREETING TOOL: detect_and_respond_to_greeting CALLED!")
    print(f"🔧 GREETING TOOL: User message: {user_message}")
    
    # Convert message to lowercase for checking
    message_lower = user_message.lower().strip()
    
    # Check if message contains greeting keywords
    is_greeting = any(keyword in message_lower for keyword in GREETING_KEYWORDS)
    
    if is_greeting:
        # Select a random greeting message
        selected_greeting = random.choice(GREETING_MESSAGES)
        print(f"🎯 GREETING TOOL: Greeting detected! Selected message: {selected_greeting[:50]}...")
        print("=" * 60)
        return selected_greeting
    else:
        print("❌ GREETING TOOL: No greeting detected")
        print("=" * 60)
        return "NOT_A_GREETING"

# @tool
def get_greeting_suggestions() -> str:
    """Get suggestions for what users can ask about"""
    suggestions = [
        "🍽️ **Food Recommendations**: Ask me to suggest meals based on your preferences",
        "📝 **Recipe Details**: Request detailed recipes for specific dishes",
        "🔄 **Recipe Variations**: Ask for variations of your favorite recipes",
        "⚙️ **Preferences**: Tell me about your dietary restrictions, allergies, or cuisine preferences",
        "🍳 **Cooking Tips**: Ask for cooking advice or techniques",
        "🕐 **Meal Planning**: Get help with breakfast, lunch, dinner, or snack ideas",
        "🌶️ **Spice Levels**: Discuss your spice tolerance and preferences",
        "🏠 **Home vs Order**: Get suggestions for both home cooking and ordering options"
    ]
    
    response = "Here are some things you can ask me about:\n\n" + "\n".join(suggestions)
    print("=" * 60)
    print("🔧 GREETING TOOL: get_greeting_suggestions CALLED!")
    print(f"🔧 GREETING TOOL: Returning suggestions")
    print("=" * 60)
    return response


