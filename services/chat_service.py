"""
Chat Service
Handles AI chat functionality using LangGraph Agent
"""

# from services.agents.enhanced_langgraph_agent import EnhancedFoodBotAgent
from datetime import datetime

class ChatService:
    def __init__(self):
        # self.langgraph_agent = EnhancedFoodBotAgent()
        self.langgraph_agent = None
        print("✅ CHAT SERVICE: Initialized without LangGraph Agent (temporarily disabled)")
    
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
    
    def get_conversation_history(self, user_id: str):
        """Get conversation history for a user"""
        return self.langgraph_agent.get_conversation_history(user_id)
    
    def clear_conversation_history(self, user_id: str):
        """Clear conversation history for a user"""
        self.langgraph_agent.clear_conversation_history(user_id)
    
    def get_agent_info(self):
        """Get information about the agent"""
        return self.langgraph_agent.get_agent_info()
