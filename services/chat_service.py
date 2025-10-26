"""
Chat Service
Handles AI chat functionality using LangGraph Agent
"""

from services.agents.enhanced_langgraph_agent import EnhancedFoodBotAgent
from datetime import datetime

class ChatService:
    def __init__(self):
        self.langgraph_agent = EnhancedFoodBotAgent()
        print("✅ CHAT SERVICE: Initialized with LangGraph Agent")
    
    def send_message(self, user_id: str, message: str, session_id: str = None):
        """Send message to LangGraph Agent and return response with session support"""
        print(f"💬 User {user_id} message: {message}")
        print(f"🆔 Session ID: {session_id or 'default'}")
        
        try:
            if self.langgraph_agent is None:
                # Return a simple response when LangGraph agent is disabled
                ai_response = "Hello! I'm your food recommendation assistant. The AI features are temporarily disabled, but I can still help you with basic functionality. Please try again later when the full AI system is restored."
                print(f"🤖 Simple Response: {ai_response}")
                return {
                    "message": ai_response,
                    "user_message": message,
                    "session_id": session_id or "default",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Get chat history for context (session-specific)
            chat_history = self.langgraph_agent.get_conversation_history(user_id, session_id)
            
            # Process message with LangGraph agent
            print("🤖 Processing with LangGraph Agent...")
            ai_response = self.langgraph_agent.process_message(user_id, message, chat_history, session_id)
            
            print(f"🤖 AI Response: {ai_response}")
            return {
                "message": ai_response,
                "user_message": message,
                "session_id": session_id or "default",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"❌ CHAT SERVICE: Error processing message: {e}")
            import traceback
            traceback.print_exc()
            return {
                "message": "Sorry, I'm having trouble processing your request right now.",
                "user_message": message,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    
    def get_agent_info(self):
        """Get information about the agent"""
        if self.langgraph_agent is None:
            return {"status": "disabled", "message": "LangGraph agent is temporarily disabled"}
        return self.langgraph_agent.get_agent_info()
    
    def create_session(self, user_id: str, session_name: str = None):
        """Create a new session for the user"""
        print(f"🆕 CHAT SERVICE: Creating session for user {user_id}")
        
        if self.langgraph_agent is None:
            # Generate a simple session ID when LangGraph agent is disabled
            import uuid
            session_id = str(uuid.uuid4())
            print(f"🆔 CHAT SERVICE: Generated session ID: {session_id}")
            return session_id
        
        # Use LangGraph agent's create_session method when available
        return self.langgraph_agent.create_session(user_id, session_name)
    
    def get_conversation_history(self, user_id: str, session_id: str = None):
        """Get conversation history for a user"""
        if self.langgraph_agent is None:
            return []
        return self.langgraph_agent.get_conversation_history(user_id, session_id)
    
    def clear_conversation_history(self, user_id: str, session_id: str = None):
        """Clear conversation history for a user"""
        if self.langgraph_agent is None:
            return True
        return self.langgraph_agent.clear_conversation_history(user_id, session_id)
    
    def get_conversation_summary(self, user_id: str):
        """Get conversation summary for a user"""
        if self.langgraph_agent is None:
            return "AI features are temporarily disabled"
        return self.langgraph_agent.get_conversation_summary(user_id)
    
    def search_conversation(self, user_id: str, query: str):
        """Search conversation history"""
        if self.langgraph_agent is None:
            return []
        return self.langgraph_agent.search_conversation(user_id, query)
    
    def get_user_sessions(self, user_id: str):
        """Get all sessions for a user"""
        if self.langgraph_agent is None:
            return []
        return self.langgraph_agent.get_user_sessions(user_id)
    
    def delete_session(self, user_id: str, session_id: str):
        """Delete a session"""
        if self.langgraph_agent is None:
            return True
        return self.langgraph_agent.delete_session(user_id, session_id)
    
    def has_user_shared_info(self, user_id: str):
        """Check if user has shared information"""
        if self.langgraph_agent is None:
            return {"has_shared_info": False, "message": "AI features are temporarily disabled"}
        return self.langgraph_agent.has_user_shared_info(user_id)
