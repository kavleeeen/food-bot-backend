"""
LangGraph-based Food Bot Agent
Uses LangChain agents framework for better orchestration and reasoning
"""

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from services.preference_service import PreferenceService
from services.agents.tools.preference_tools import (
    read_user_preferences,
    update_user_preferences,
    add_single_preference,
    check_missing_mandatory_preferences,
    has_complete_preferences
)
from services.agents.tools.recommendation_tools import generate_food_recommendation
from services.agents.tools.recipe_tools import generate_detailed_recipe, suggest_recipe_variations
import os
from typing import Dict, Any

class FoodBotAgent:
    def __init__(self):
        """Initialize the LangGraph-based Food Bot Agent"""
        print("🤖 LANGGRAPH AGENT: Initializing Food Bot Agent...")
        
        # Initialize LLM
        self.llm = init_chat_model(
            "gemini-2.5-flash",
            model_provider="google_genai",
            temperature=0.7,
            google_api_key=os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
        )
        
        # Initialize services
        self.preference_service = PreferenceService()
        
        # Define tools for the agent
        self.tools = [
            read_user_preferences,
            update_user_preferences,
            add_single_preference,
            check_missing_mandatory_preferences,
            has_complete_preferences,
            generate_food_recommendation,
            generate_detailed_recipe,
            suggest_recipe_variations
        ]
        
        # Create memory checkpointer for conversation persistence
        from langchain_core.runnables.history import RunnableWithMessageHistory
        from langchain_community.chat_message_histories import ChatMessageHistory
        
        # Create the agent with memory
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            checkpointer=None  # We'll add memory later
        )
        
        print("✅ LANGGRAPH AGENT: Agent initialized successfully")
    
    def process_message(self, user_id: str, message: str, chat_history: list = None):
        """Process user message using LangGraph agent"""
        try:
            print(f"🤖 LANGGRAPH AGENT: Processing message for user {user_id}")
            print(f"📝 LANGGRAPH AGENT: Message: {message}")
            
            # Prepare input for the agent
            input_data = {
                "messages": [HumanMessage(content=message)]
            }
            
            # Add chat history if provided
            if chat_history:
                messages = []
                for entry in chat_history:
                    if "user" in entry:
                        messages.append(HumanMessage(content=entry["user"]))
                    if "assistant" in entry:
                        messages.append(AIMessage(content=entry["assistant"]))
                messages.append(HumanMessage(content=message))
                input_data["messages"] = messages
            
            # Execute the agent
            print("🚀 LANGGRAPH AGENT: Executing agent...")
            result = self.agent.invoke(input_data)
            
            # Extract response
            if "messages" in result and result["messages"]:
                response = result["messages"][-1].content
                print(f"📤 LANGGRAPH AGENT: Response: {response}")
                return response
            else:
                print("⚠️ LANGGRAPH AGENT: No response generated")
                return "I'm having trouble processing your request. Please try again."
                
        except Exception as e:
            print(f"❌ LANGGRAPH AGENT: Error processing message: {e}")
            import traceback
            traceback.print_exc()
            return "Sorry, I'm having trouble processing your request right now."
    
    def get_conversation_history(self, user_id: str) -> list:
        """Get conversation history for a user"""
        # This would be implemented with persistent storage
        # For now, return empty list
        return []
    
    def save_conversation(self, user_id: str, user_message: str, assistant_response: str):
        """Save conversation to persistent storage"""
        # This would be implemented with persistent storage
        # For now, just log
        print(f"💾 LANGGRAPH AGENT: Saving conversation for user {user_id}")
        pass

