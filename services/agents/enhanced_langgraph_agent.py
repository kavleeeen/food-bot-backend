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
from services.chat_history_service import ChatHistoryService
from services.agents.tools.preference_tools import (
    read_user_preferences,
    update_user_preferences,
    add_single_preference,
    check_missing_mandatory_preferences,
    has_complete_preferences
)
from services.agents.tools.recommendation_tools import generate_food_recommendation
from services.agents.tools.recipe_tools import generate_detailed_recipe, suggest_recipe_variations
from services.agents.tools.greeting_tools import (
    detect_and_respond_to_greeting, get_greeting_suggestions
)
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
        self.chat_history_service = ChatHistoryService()
        
        # Define tools for the agent
        self.tools = [
            detect_and_respond_to_greeting,
            get_greeting_suggestions,
            read_user_preferences,
            update_user_preferences,
            add_single_preference,
            check_missing_mandatory_preferences,
            has_complete_preferences,
            generate_food_recommendation,
            generate_detailed_recipe,
            suggest_recipe_variations
        ]
        
        # Create the agent
        self.agent = create_react_agent(
            self.llm,
            self.tools
        )
        
        # Wrap with message history using persistent storage (database-only)
        self.agent_with_memory = RunnableWithMessageHistory(
            self.agent,
            self._get_session_history,
            input_messages_key="messages",
            history_messages_key="chat_history"
        )
        
        print("✅ ENHANCED LANGGRAPH AGENT: Agent initialized successfully")
    
    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session from persistent storage (database-only)"""
        print(f"💾 MESSAGES: Loading conversation history for session {session_id} from database")
        # Load directly from database (session_id is actually user_id in this context)
        return self.chat_history_service.get_langchain_history(session_id)
    
    def _get_user_context(self, user_id: str, session_id: str = None) -> str:
        """Get user context including preferences and session-specific conversation history"""
        try:
            context_parts = []
            
            # Include user preferences as context (only if they exist)
            preferences = self.preference_service.get_user_preferences(user_id)
            if preferences and any(preferences.values()):
                context_parts.append("USER PREFERENCES (from all previous sessions):")
                if preferences.get("restrictions") and preferences.get("restrictions") != ["none"]:
                    context_parts.append(f"- Dietary restrictions: {', '.join(preferences['restrictions'])}")
                if preferences.get("allergies") and "none" not in preferences.get("allergies", []):
                    context_parts.append(f"- Allergies: {', '.join(preferences['allergies'])}")
                if preferences.get("cuisine_preferences") and preferences.get("cuisine_preferences") != ["none"]:
                    context_parts.append(f"- Preferred cuisines: {', '.join(preferences['cuisine_preferences'])}")
                if preferences.get("spice_level") and preferences.get("spice_level") != "none":
                    context_parts.append(f"- Spice level preference: {preferences['spice_level']}")
                if preferences.get("custom_preferences"):
                    context_parts.append(f"- Custom preferences: {', '.join(preferences['custom_preferences'])}")
            # Note: Don't mention missing preferences here - let the agent ask contextually
            
            # Get session-specific conversation history only
            if session_id and session_id != "default":
                # Check if this is a new session
                session_exists = self.chat_history_service.session_exists(user_id, session_id)
                if session_exists:
                    context_parts.append(f"\nCURRENT SESSION CONTEXT (Session: {session_id[:8]}...):")
                    # Get only messages from this specific session
                    history = self.chat_history_service.get_conversation_history(user_id, session_id, limit=10)
                    if history:
                        for msg in history[-5:]:  # Last 5 messages from this session
                            if msg.get("user_message"):
                                context_parts.append(f"- User said: \"{msg['user_message'][:100]}...\"")
                            if msg.get("assistant_response"):
                                context_parts.append(f"- Assistant responded: \"{msg['assistant_response'][:100]}...\"")
                    else:
                        context_parts.append("- No previous messages in this session")
                else:
                    context_parts.append(f"\nCURRENT SESSION CONTEXT (New Session: {session_id[:8]}...):")
                    context_parts.append("- This is a new session, no previous conversation context")
            else:
                # Default session - get recent history
                context_parts.append(f"\nCURRENT SESSION CONTEXT (Default Session):")
                history = self.chat_history_service.get_conversation_history(user_id, None, limit=5)
                if history:
                    for msg in history[-3:]:  # Last 3 messages
                        if msg.get("user_message"):
                            context_parts.append(f"- User said: \"{msg['user_message'][:100]}...\"")
                        if msg.get("assistant_response"):
                            context_parts.append(f"- Assistant responded: \"{msg['assistant_response'][:100]}...\"")
                else:
                    context_parts.append("- No previous conversation context")
            
            if context_parts:
                return "\n".join(context_parts)
            else:
                return "This is a new user with no previous preferences or conversation history."
                
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error getting user context: {e}")
            return "Unable to retrieve user context."
    
    
    
    def process_message(self, user_id: str, message: str, chat_history: list = None, session_id: str = None):
        """Process user message using Enhanced LangGraph agent with memory and session support"""
        try:
            print(f"🤖 ENHANCED LANGGRAPH AGENT: Processing message for user {user_id}")
            print(f"📝 ENHANCED LANGGRAPH AGENT: Message: {message}")
            print(f"🆔 ENHANCED LANGGRAPH AGENT: Session ID: {session_id or 'default'}")
            
            # Determine if this is a new or existing session
            is_new_session = True
            if session_id and session_id != "default":
                is_new_session = not self.chat_history_service.session_exists(user_id, session_id)
                print(f"🆕 ENHANCED LANGGRAPH AGENT: New session: {is_new_session}")
            
            # Get tool names safely
            tool_names = []
            for tool in self.tools:
                if hasattr(tool, 'name'):
                    tool_names.append(tool.name)
                elif hasattr(tool, '__name__'):
                    tool_names.append(tool.__name__)
                else:
                    tool_names.append(str(type(tool).__name__))
            print(f"🔧 ENHANCED LANGGRAPH AGENT: Available tools: {tool_names}")
            
            # Get user context (preferences + session-specific history)
            user_context = self._get_user_context(user_id, session_id)
            
            # Add session context to system message
            session_context = ""
            if is_new_session:
                session_context = f"\n🆕 NEW SESSION: This is a new conversation session. User preferences from previous sessions are included above, but conversation context is fresh."
            else:
                session_context = f"\n🔄 EXISTING SESSION: This is an existing conversation session. Use the session context above to maintain conversation flow."
            
            system_context = f"""You are a helpful food recommendation assistant designed specifically for Indian users. Your primary goal is to eliminate decision fatigue by providing simple, nutritious meal suggestions.

                Key Principles:
                1. USER-FIRST: Always prioritize what the user is asking for - help them immediately
                2. CONVERSATIONAL: Be friendly and helpful, ask questions to understand what they need
                3. SIMPLICITY FIRST: When recommending, suggest easy-to-make, everyday meals
                4. NUTRITIONAL BALANCE: Focus on balanced meals with proper macros when giving recommendations
                5. INDIAN CONTEXT: Understand Indian food culture - both traditional and modern
                6. DECISION FATIGUE: Help users make choices without overwhelming them
                7. PRACTICAL: Consider if meals can be made at home or ordered easily
                8. CRISP & MINIMAL: Keep responses short, direct, and to the point

                {user_context}{session_context}

                PRIORITY WORKFLOW:
                1. **IMMEDIATE HELP**: If user asks for food recommendations, recipes, or variations - provide them immediately using the appropriate tool
                2. **PREFERENCE COLLECTION**: Only ask about preferences as a follow-up question AFTER helping with their main request
                3. **CONTEXTUAL PREFERENCES**: If you need specific preferences to give better recommendations, ask for them in context (e.g., "For better recommendations, do you have any dietary restrictions?")

                You have access to tools for:
                - Responding to greetings (use when user greets you)
                - Reading and updating user preferences (use as follow-up, not priority)
                - Generating food recommendations (use immediately when requested)
                - Creating detailed recipes (use immediately when requested)
                - Suggesting recipe variations (use immediately when requested)

                TOOL USAGE PRIORITY:
                1. **HIGH PRIORITY**: generate_food_recommendation, generate_detailed_recipe, suggest_recipe_variations
                2. **MEDIUM PRIORITY**: read_user_preferences (only if needed for better recommendations)
                3. **LOW PRIORITY**: update_user_preferences, add_single_preference (as follow-up questions)

                EXAMPLES:
                - User: "I want lunch recommendations" → Use generate_food_recommendation tool immediately
                - User: "How to make biryani?" → Use generate_detailed_recipe tool immediately
                - User: "Variations of dal?" → Use suggest_recipe_variations tool immediately
                - After helping: "For better future recommendations, do you have any dietary restrictions?" """

            # Prepare input for the agent
            input_data = {
                "messages": [
                    SystemMessage(content=system_context),
                    HumanMessage(content=message)
                ]
            }
            
            # Configuration for memory with session support
            effective_session_id = f"{user_id}_{session_id}" if session_id else user_id
            config = RunnableConfig(
                configurable={"session_id": effective_session_id}
            )
            
            # Execute the agent with memory
            print("🚀 ENHANCED LANGGRAPH AGENT: Executing agent with memory...")
            print("=" * 80)
            print("🔍 LANGGRAPH DEBUG: Starting agent execution...")
            print("=" * 80)
            
            # Enable debug mode for more detailed output
            config_with_debug = RunnableConfig(
                configurable={"session_id": user_id},
                # Add debug configuration
                debug=True
            )
            
            # Add execution tracing
            print("🔍 LANGGRAPH DEBUG: About to invoke agent...")
            print("🔍 LANGGRAPH DEBUG: Input data:", input_data)
            print("🔍 LANGGRAPH DEBUG: Config:", config_with_debug)
            
            result = self.agent_with_memory.invoke(input_data, config=config_with_debug)
            
            print("🔍 LANGGRAPH DEBUG: Agent execution completed")
            print("🔍 LANGGRAPH DEBUG: Result type:", type(result))
            print("🔍 LANGGRAPH DEBUG: Result keys:", result.keys() if isinstance(result, dict) else "Not a dict")
            print("=" * 80)
            
            # Extract response
            if "messages" in result and result["messages"]:
                response = result["messages"][-1].content
                print(f"📤 ENHANCED LANGGRAPH AGENT: Response: {response}")
                
                
                # Save conversation to database with session support
                self.chat_history_service.save_message(user_id, message, response, session_id)
                
                return response
            else:
                print("⚠️ ENHANCED LANGGRAPH AGENT: No response generated")
                error_response = "I'm having trouble processing your request. Please try again."
                
                # Save error message to database with session support
                self.chat_history_service.save_message(user_id, message, error_response, session_id)
                
                return error_response
                
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error processing message: {e}")
            import traceback
            traceback.print_exc()
            return "Sorry, I'm having trouble processing your request right now."
    
    def get_conversation_history(self, user_id: str, session_id: str = None) -> list:
        """Get conversation history for a user from database, optionally filtered by session"""
        try:
            # Get from database with session filter
            history = self.chat_history_service.get_conversation_history(user_id, session_id)
            
            # Format for API response
            formatted_history = []
            for message in history:
                formatted_history.append({
                    "user": message.get("user_message", ""),
                    "assistant": message.get("assistant_response", ""),
                    "timestamp": message.get("created_at", ""),
                    "session_id": message.get("session_id", "default"),
                    "id": message.get("id", "")
                })
            
            return formatted_history
            
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error getting conversation history: {e}")
            return []
    
    def clear_conversation_history(self, user_id: str, session_id: str = None):
        """Clear conversation history for a user from database, optionally filtered by session"""
        try:
            # Clear from database with session filter
            success = self.chat_history_service.clear_conversation_history(user_id, session_id)
            
            if success:
                print(f"🗑️ ENHANCED LANGGRAPH AGENT: Cleared history for user {user_id} in session {session_id}")
            else:
                print(f"⚠️ ENHANCED LANGGRAPH AGENT: Failed to clear history for user {user_id} in session {session_id}")
                
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error clearing history: {e}")
    
    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get conversation summary for a user"""
        return self.chat_history_service.get_conversation_summary(user_id)
    
    def search_conversation(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """Search through conversation history"""
        return self.chat_history_service.search_conversation(user_id, query)
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user"""
        return self.chat_history_service.get_user_sessions(user_id)
    
    def create_session(self, user_id: str, session_name: str = None) -> str:
        """Create a new session for a user"""
        return self.chat_history_service.create_session(user_id, session_name)
    
    def delete_session(self, user_id: str, session_id: str) -> bool:
        """Delete a specific session and all its messages"""
        return self.chat_history_service.delete_session(user_id, session_id)
    
    def has_user_shared_info(self, user_id: str) -> Dict[str, Any]:
        """Check if user has shared any information before (preferences, conversations, etc.)"""
        try:
            # Check preferences
            preferences = self.preference_service.get_user_preferences(user_id)
            has_preferences = preferences and any(preferences.values())
            
            # Check conversation history
            all_history = self.chat_history_service.get_conversation_history(user_id, limit=1)
            has_conversations = len(all_history) > 0
            
            # Check sessions
            sessions = self.chat_history_service.get_user_sessions(user_id)
            has_sessions = len(sessions) > 0
            
            # Get summary of what they've shared
            shared_info = {
                "has_shared_info": has_preferences or has_conversations or has_sessions,
                "has_preferences": has_preferences,
                "has_conversations": has_conversations,
                "has_sessions": has_sessions,
                "preferences_summary": self._get_preferences_summary(preferences) if has_preferences else None,
                "conversation_count": len(all_history),
                "session_count": len(sessions),
                "last_activity": sessions[0].get('last_activity') if sessions else None
            }
            
            return shared_info
            
        except Exception as e:
            print(f"❌ ENHANCED LANGGRAPH AGENT: Error checking user shared info: {e}")
            return {
                "has_shared_info": False,
                "has_preferences": False,
                "has_conversations": False,
                "has_sessions": False,
                "error": str(e)
            }
    
    def _get_preferences_summary(self, preferences: dict) -> str:
        """Get a summary of user preferences"""
        if not preferences:
            return "No preferences set"
        
        summary_parts = []
        if preferences.get("restrictions"):
            summary_parts.append(f"Dietary: {', '.join(preferences['restrictions'])}")
        if preferences.get("allergies") and "none" not in preferences.get("allergies", []):
            summary_parts.append(f"Allergies: {', '.join(preferences['allergies'])}")
        if preferences.get("cuisine_preferences"):
            summary_parts.append(f"Cuisines: {', '.join(preferences['cuisine_preferences'])}")
        
        return "; ".join(summary_parts) if summary_parts else "Basic preferences set"
    
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent configuration"""
        return {
            "agent_type": "Enhanced LangGraph Agent with Database-Only Chat History",
            "tools_count": len(self.tools),
            "tools": [tool.name if hasattr(tool, 'name') else str(type(tool).__name__) for tool in self.tools],
            "memory_enabled": True,
            "persistent_storage": True,
            "storage_type": "Database-only (no in-memory cache)",
            "chat_history_service": "Firebase Firestore Messages Collection"
        }
