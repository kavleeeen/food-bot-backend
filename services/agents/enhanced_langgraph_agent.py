"""
Enhanced LangGraph-based Food Bot Agent with Memory
Uses LangChain agents framework with persistent memory and better tool integration
"""

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig
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
from typing import Dict, Any, List
import json

class EnhancedFoodBotAgent:
    def __init__(self):
        """Initialize the Enhanced LangGraph-based Food Bot Agent with Memory"""
        print("🤖 ENHANCED LANGGRAPH AGENT: Initializing Food Bot Agent...")
        
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
        
        # Create memory store for conversation persistence
        self.memory_store = {}
        
        # Create the agent
        self.agent = create_react_agent(
            self.llm,
            self.tools
        )
        
        # Wrap with message history
        self.agent_with_memory = RunnableWithMessageHistory(
            self.agent,
            self._get_session_history,
            input_messages_key="messages",
            history_messages_key="chat_history"
        )
        
        print("✅ ENHANCED LANGGRAPH AGENT: Agent initialized successfully")
    
    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session"""
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ChatMessageHistory()
        return self.memory_store[session_id]
    
    def process_message(self, user_id: str, message: str, chat_history: list = None):
        """Process user message using Enhanced LangGraph agent with memory"""
        try:
            print(f"🤖 ENHANCED LANGGRAPH AGENT: Processing message for user {user_id}")
            print(f"📝 ENHANCED LANGGRAPH AGENT: Message: {message}")
            
            # Create system message with context
            system_context = """You are a helpful food recommendation assistant designed specifically for Indian users. Your primary goal is to eliminate decision fatigue by providing simple, nutritious meal suggestions.

Key Principles:
1. SIMPLICITY FIRST: Recommend easy-to-make, everyday meals
2. NUTRITIONAL BALANCE: Focus on balanced meals with proper macros
3. INDIAN CONTEXT: Understand Indian food culture - both traditional and modern
4. DECISION FATIGUE: Make choices for users - don't overwhelm with options
5. PRACTICAL: Consider if the meal can be made at home or ordered easily
6. CRISP & MINIMAL: Keep responses short, direct, and to the point

You have access to tools for:
- Reading and updating user preferences
- Generating food recommendations
- Creating detailed recipes
- Suggesting recipe variations

Always use the appropriate tools based on what the user is asking for."""

            # Prepare input for the agent
            input_data = {
                "messages": [
                    SystemMessage(content=system_context),
                    HumanMessage(content=message)
                ]
            }
            
            # Configuration for memory
            config = RunnableConfig(
                configurable={"session_id": user_id}
            )
            
            # Execute the agent with memory
            print("🚀 ENHANCED LANGGRAPH AGENT: Executing agent with memory...")
            result = self.agent_with_memory.invoke(input_data, config=config)
            
            # Extract response
            if "messages" in result and result["messages"]:
                response = result["messages"][-1].content
                print(f"📤 ENHANCED LANGGRAPH AGENT: Response: {response}")
                return response
            else:
                print("⚠️ ENHANCED LANGGRAPH AGENT: No response generated")
                return "I'm having trouble processing your request. Please try again."
                
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error processing message: {e}")
            import traceback
            traceback.print_exc()
            return "Sorry, I'm having trouble processing your request right now."
    
    def get_conversation_history(self, user_id: str) -> list:
        """Get conversation history for a user"""
        if user_id in self.memory_store:
            history = self.memory_store[user_id].messages
            formatted_history = []
            for msg in history:
                if isinstance(msg, HumanMessage):
                    formatted_history.append({"user": msg.content})
                elif isinstance(msg, AIMessage):
                    formatted_history.append({"assistant": msg.content})
            return formatted_history
        return []
    
    def clear_conversation_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.memory_store:
            self.memory_store[user_id].clear()
            print(f"🗑️ ENHANCED LANGGRAPH AGENT: Cleared history for user {user_id}")
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent configuration"""
        return {
            "agent_type": "Enhanced LangGraph Agent",
            "tools_count": len(self.tools),
            "tools": [getattr(tool, 'name', tool.__name__) for tool in self.tools],
            "memory_enabled": True,
            "active_sessions": len(self.memory_store)
        }
