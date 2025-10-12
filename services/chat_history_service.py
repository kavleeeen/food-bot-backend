"""
Chat History Service for persistent conversation storage
Stores and retrieves chat history from Firebase Firestore
"""

from firebase_admin import firestore
from datetime import datetime
from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
import json
from firebase_config import firebase_config

class ChatHistoryService:
    def __init__(self):
        """Initialize the chat history service with Firebase connection"""
        self.db = firebase_config.get_db()
        self.messages_collection = "messages"
        self.sessions_collection = "user_sessions"
    
    def save_message(self, user_id: str, message: str, response: str, session_id: str = None, timestamp: datetime = None) -> bool:
        """Save a single message exchange to the messages table with comprehensive metadata"""
        try:
            if timestamp is None:
                timestamp = datetime.now()
            
            # Create comprehensive message document
            message_doc = {
                "user_id": user_id,
                "session_id": session_id or "default",
                "user_message": message,
                "assistant_response": response,
                "message_length": len(message),
                "response_length": len(response),
                "timestamp": timestamp,
                "created_at": timestamp.isoformat(),
                "message_type": "conversation",
                "metadata": {
                    "user_message_tokens": len(message.split()),
                    "assistant_response_tokens": len(response.split()),
                    "is_greeting": self._is_greeting(message),
                    "contains_food_keywords": self._contains_food_keywords(message),
                    "session_created_at": timestamp.isoformat()
                }
            }
            
            # Add to messages collection
            doc_ref = self.db.collection(self.messages_collection).add(message_doc)
            print(f"💾 MESSAGES: Saved message for user {user_id} in session {session_id}")
            return True
            
        except Exception as e:
            print(f"❌ MESSAGES: Error saving message: {e}")
            return False
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greeting_keywords = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste", "namaskar"]
        message_lower = message.lower().strip()
        return any(greeting in message_lower for greeting in greeting_keywords)
    
    def _contains_food_keywords(self, message: str) -> bool:
        """Check if message contains food-related keywords"""
        food_keywords = [
            "food", "meal", "lunch", "dinner", "breakfast", "recipe", "cook", "eat", "hungry",
            "vegetarian", "vegan", "spicy", "sweet", "salty", "healthy", "nutrition",
            "dal", "rice", "curry", "biryani", "paneer", "chicken", "fish", "vegetables"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in food_keywords)
    
    def get_conversation_history(self, user_id: str, session_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history for a user from the messages table, optionally filtered by session"""
        try:
            # Query messages for the user, optionally filtered by session
            query = self.db.collection(self.messages_collection).where("user_id", "==", user_id)
            
            if session_id:
                query = query.where("session_id", "==", session_id)
            
            messages_query = query.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
            messages = messages_query.stream()
            
            # Convert to list and reverse to get chronological order
            history = []
            for doc in messages:
                message_data = doc.to_dict()
                history.append({
                    "id": doc.id,
                    "session_id": message_data.get("session_id", "default"),
                    "user_message": message_data.get("user_message", ""),
                    "assistant_response": message_data.get("assistant_response", ""),
                    "timestamp": message_data.get("timestamp"),
                    "created_at": message_data.get("created_at", ""),
                    "message_length": message_data.get("message_length", 0),
                    "response_length": message_data.get("response_length", 0),
                    "message_type": message_data.get("message_type", "conversation"),
                    "metadata": message_data.get("metadata", {})
                })
            
            # Reverse to get chronological order (oldest first)
            history.reverse()
            
            print(f"📚 MESSAGES: Retrieved {len(history)} messages for user {user_id} in session {session_id}")
            return history
            
        except Exception as e:
            print(f"❌ MESSAGES: Error retrieving history: {e}")
            return []
    
    def get_langchain_history(self, user_id: str, session_id: str = None, limit: int = 20) -> ChatMessageHistory:
        """Get conversation history in LangChain format for the agent, optionally filtered by session"""
        try:
            history = self.get_conversation_history(user_id, session_id, limit)
            chat_history = ChatMessageHistory()
            
            for message in history:
                # Add user message
                if message.get("user_message"):
                    chat_history.add_user_message(message["user_message"])
                
                # Add assistant message
                if message.get("assistant_response"):
                    chat_history.add_ai_message(message["assistant_response"])
            
            print(f"🔄 MESSAGES: Converted {len(history)} messages to LangChain format for session {session_id}")
            return chat_history
            
        except Exception as e:
            print(f"❌ MESSAGES: Error converting to LangChain format: {e}")
            return ChatMessageHistory()
    
    def clear_conversation_history(self, user_id: str, session_id: str = None) -> bool:
        """Clear conversation history for a user, optionally filtered by session"""
        try:
            # Query messages for the user, optionally filtered by session
            query = self.db.collection(self.messages_collection).where("user_id", "==", user_id)
            
            if session_id:
                query = query.where("session_id", "==", session_id)
            
            messages = query.stream()
            
            # Delete each message
            deleted_count = 0
            for doc in messages:
                doc.reference.delete()
                deleted_count += 1
            
            print(f"🗑️ MESSAGES: Cleared {deleted_count} messages for user {user_id} in session {session_id}")
            return True
            
        except Exception as e:
            print(f"❌ MESSAGES: Error clearing history: {e}")
            return False
    
    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation for a user"""
        try:
            history = self.get_conversation_history(user_id, limit=100)
            
            if not history:
                return {
                    "total_messages": 0,
                    "first_message": None,
                    "last_message": None,
                    "conversation_duration": None
                }
            
            first_message = history[0]
            last_message = history[-1]
            
            # Calculate conversation duration
            if first_message.get("timestamp") and last_message.get("timestamp"):
                duration = last_message["timestamp"] - first_message["timestamp"]
                duration_str = str(duration)
            else:
                duration_str = None
            
            return {
                "total_messages": len(history),
                "first_message": first_message.get("created_at"),
                "last_message": last_message.get("created_at"),
                "conversation_duration": duration_str,
                "recent_topics": self._extract_recent_topics(history[-10:])  # Last 10 messages
            }
            
        except Exception as e:
            print(f"❌ CHAT HISTORY: Error getting summary: {e}")
            return {"error": str(e)}
    
    def _extract_recent_topics(self, recent_messages: List[Dict[str, Any]]) -> List[str]:
        """Extract topics from recent messages (simple keyword extraction)"""
        topics = set()
        food_keywords = [
            "food", "meal", "lunch", "dinner", "breakfast", "recipe", "cook", "eat",
            "vegetarian", "vegan", "spicy", "sweet", "salty", "healthy", "nutrition",
            "dal", "rice", "curry", "biryani", "paneer", "chicken", "fish"
        ]
        
        for message in recent_messages:
            text = (message.get("user_message", "") + " " + message.get("assistant_response", "")).lower()
            for keyword in food_keywords:
                if keyword in text:
                    topics.add(keyword)
        
        return list(topics)[:5]  # Return top 5 topics
    
    def search_conversation(self, user_id: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search through conversation history for specific topics"""
        try:
            history = self.get_conversation_history(user_id, limit=100)
            query_lower = query.lower()
            
            matching_messages = []
            for message in history:
                user_msg = message.get("user_message", "").lower()
                assistant_msg = message.get("assistant_response", "").lower()
                
                if query_lower in user_msg or query_lower in assistant_msg:
                    matching_messages.append(message)
            
            print(f"🔍 CHAT HISTORY: Found {len(matching_messages)} messages matching '{query}'")
            return matching_messages[:limit]
            
        except Exception as e:
            print(f"❌ CHAT HISTORY: Error searching conversation: {e}")
            return []
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user from the messages table"""
        try:
            # Query all messages for the user
            messages_query = (
                self.db.collection(self.messages_collection)
                .where("user_id", "==", user_id)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
            )
            
            messages = messages_query.stream()
            
            # Group by session_id and get session info
            sessions = {}
            for doc in messages:
                message_data = doc.to_dict()
                session_id = message_data.get("session_id", "default")
                
                if session_id not in sessions:
                    sessions[session_id] = {
                        "session_id": session_id,
                        "message_count": 0,
                        "first_message": None,
                        "last_message": None,
                        "last_activity": None,
                        "total_tokens": 0,
                        "food_related_messages": 0,
                        "greeting_messages": 0
                    }
                
                sessions[session_id]["message_count"] += 1
                
                # Add token counts
                metadata = message_data.get("metadata", {})
                sessions[session_id]["total_tokens"] += metadata.get("user_message_tokens", 0) + metadata.get("assistant_response_tokens", 0)
                
                # Count special message types
                if metadata.get("contains_food_keywords", False):
                    sessions[session_id]["food_related_messages"] += 1
                if metadata.get("is_greeting", False):
                    sessions[session_id]["greeting_messages"] += 1
                
                if not sessions[session_id]["first_message"]:
                    sessions[session_id]["first_message"] = message_data.get("created_at")
                
                if not sessions[session_id]["last_message"]:
                    sessions[session_id]["last_message"] = message_data.get("created_at")
                    sessions[session_id]["last_activity"] = message_data.get("timestamp")
            
            # Convert to list and sort by last activity
            session_list = list(sessions.values())
            session_list.sort(key=lambda x: x["last_activity"] or datetime.min, reverse=True)
            
            print(f"📋 MESSAGES: Found {len(session_list)} sessions for user {user_id}")
            return session_list
            
        except Exception as e:
            print(f"❌ MESSAGES: Error getting user sessions: {e}")
            return []
    
    def create_session(self, user_id: str, session_name: str = None) -> str:
        """Create a new session for a user"""
        try:
            import uuid
            session_id = str(uuid.uuid4())
            
            # Create a session document with enhanced metadata
            session_doc = {
                "user_id": user_id,
                "session_id": session_id,
                "session_name": session_name or f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "created_at": datetime.now().isoformat(),
                "status": "active",
                "metadata": {
                    "message_count": 0,
                    "total_tokens": 0,
                    "food_related_messages": 0,
                    "greeting_messages": 0,
                    "last_activity": datetime.now().isoformat()
                }
            }
            
            # Save session metadata
            self.db.collection(self.sessions_collection).add(session_doc)
            
            print(f"🆕 MESSAGES: Created new session {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            print(f"❌ MESSAGES: Error creating session: {e}")
            return None
    
    def delete_session(self, user_id: str, session_id: str) -> bool:
        """Delete a specific session and all its messages"""
        try:
            # Clear all messages in the session
            success = self.clear_conversation_history(user_id, session_id)
            
            # Delete session metadata (if exists)
            try:
                sessions_query = (
                    self.db.collection(self.sessions_collection)
                    .where("user_id", "==", user_id)
                    .where("session_id", "==", session_id)
                )
                
                sessions = sessions_query.stream()
                for doc in sessions:
                    doc.reference.delete()
            except:
                pass  # Session metadata might not exist
            
            print(f"🗑️ MESSAGES: Deleted session {session_id} for user {user_id}")
            return success
            
        except Exception as e:
            print(f"❌ MESSAGES: Error deleting session: {e}")
            return False
    
    def session_exists(self, user_id: str, session_id: str) -> bool:
        """Check if a session exists for a user"""
        try:
            # Check if there are any messages in this session
            messages_query = self.db.collection(self.messages_collection).where("user_id", "==", user_id).where("session_id", "==", session_id).limit(1)
            messages = list(messages_query.stream())
            
            # Also check session metadata
            session_doc_ref = self.db.collection(self.sessions_collection).document(f"{user_id}_{session_id}")
            session_doc = session_doc_ref.get()
            
            exists = len(messages) > 0 or session_doc.exists
            print(f"🔍 MESSAGES: Session {session_id} exists for user {user_id}: {exists}")
            return exists
            
        except Exception as e:
            print(f"❌ MESSAGES: Error checking session existence: {e}")
            return False
