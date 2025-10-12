#!/usr/bin/env python3
"""
Simple Flask app with register and login functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
import os
from firebase_config import firebase_config
from services.auth_service import AuthService
from services.chat_service import ChatService
from services.preference_service import PreferenceService

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize services
auth_service = AuthService()
chat_service = ChatService()
preference_service = PreferenceService()

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            current_user_id = auth_service.verify_token(token)
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    print("🔔 REGISTER REQUEST RECEIVED")
    
    try:
        data = request.get_json()
        print(f"📦 Request Data: {data}")
        
        if not data:
            print("❌ No request body provided")
            return jsonify({"error": "Request body is required"}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        print(f"👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"🔒 Password: {'*' * len(password) if password else 'None'}")
        
        if not all([username, email, password]):
            print("❌ Missing required fields")
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        # Use auth service to register user
        user_data = auth_service.register_user(username, email, password)
        
        response = {
            "message": "User registered successfully",
            "user": {
                "id": user_data["user_id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "created_at": user_data["created_at"].isoformat()
            }
        }
        print(f"📤 Response: {response}")
        
        return jsonify(response), 201
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Registration failed"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    print("🔔 LOGIN REQUEST RECEIVED")
    
    try:
        data = request.get_json()
        print(f"📦 Request Data: {data}")
        
        if not data:
            print("❌ No request body provided")
            return jsonify({"error": "Request body is required"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        print(f"📧 Email: {email}")
        print(f"🔒 Password: {'*' * len(password) if password else 'None'}")
        
        if not all([email, password]):
            print("❌ Missing required fields")
            return jsonify({"error": "Email and password are required"}), 400
        
        # Use auth service to login user
        login_data = auth_service.login_user(email, password)
        
        response = {
            "message": "Login successful",
            "user": {
                "id": login_data["user"]["id"],
                "username": login_data["user"]["username"],
                "email": login_data["user"]["email"],
                "created_at": login_data["user"]["created_at"].isoformat() if hasattr(login_data["user"]["created_at"], 'isoformat') else str(login_data["user"]["created_at"])
            },
            "token": login_data["token"],
            "expires_in": login_data["expires_in"]
        }
        print(f"📤 Response: {response}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    """Get user profile (protected endpoint)"""
    print(f"🔔 PROFILE REQUEST RECEIVED for user: {current_user_id}")
    
    try:
        # Use auth service to get user profile
        user_data = auth_service.get_user_profile(current_user_id)
        
        response = {
            "user": {
                "id": user_data["id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "created_at": user_data["created_at"].isoformat() if hasattr(user_data["created_at"], 'isoformat') else str(user_data["created_at"])
            }
        }
        print(f"📤 Response: {response}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to get profile"}), 500

@app.route('/api/chat', methods=['POST'])
@token_required
def chat(current_user_id):
    """Chat with Gemini AI"""
    print(f"🔔 CHAT REQUEST RECEIVED from user: {current_user_id}")
    
    try:
        data = request.get_json()
        print(f"📦 Request Data: {data}")
        
        if not data:
            print("❌ No request body provided")
            return jsonify({"error": "Request body is required"}), 400
        
        message = data.get('message')
        
        if not message:
            print("❌ No message provided")
            return jsonify({"error": "Message is required"}), 400
        
        # Use chat service to send message with user context
        response_data = chat_service.send_message(current_user_id, message)
        
        print(f"📤 Response: {response_data}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Chat failed"}), 500

@app.route('/api/preferences', methods=['GET'])
@token_required
def get_preferences(current_user_id):
    """Get user preferences"""
    print(f"🔔 PREFERENCES REQUEST RECEIVED for user: {current_user_id}")
    
    try:
        preferences = preference_service.get_user_preferences(current_user_id)
        
        response = {
            "preferences": preferences,
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"📤 Response: {response}")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to get preferences"}), 500

@app.route('/api/preferences', methods=['PUT'])
@token_required
def update_preferences(current_user_id):
    """Update user preferences"""
    print(f"🔔 UPDATE PREFERENCES REQUEST RECEIVED for user: {current_user_id}")
    
    try:
        data = request.get_json()
        print(f"📦 Request Data: {data}")
        
        if not data:
            print("❌ No request body provided")
            return jsonify({"error": "Request body is required"}), 400
        
        preferences = data.get('preferences')
        
        if not preferences:
            print("❌ No preferences provided")
            return jsonify({"error": "Preferences are required"}), 400
        
        # Update preferences
        success = preference_service.update_user_preferences(current_user_id, preferences)
        
        if success:
            response = {
                "message": "Preferences updated successfully",
                "preferences": preferences,
                "timestamp": datetime.utcnow().isoformat()
            }
            print(f"📤 Response: {response}")
            return jsonify(response), 200
        else:
            return jsonify({"error": "Failed to update preferences"}), 500
        
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to update preferences"}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    # Get users count from Firestore
    print("📊 HEALTH: Getting users count from Firestore...")
    try:
        all_users = auth_service.users_collection.get()
        users_count = len(all_users)
        print(f"✅ HEALTH: Successfully retrieved {users_count} users from Firestore")
    except Exception as e:
        print(f"❌ HEALTH: Error getting users count: {e}")
        users_count = 0
    
    return jsonify({
        "status": "healthy",
        "message": "Simple Auth API with Firebase is running",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "Firebase Firestore",
        "users_count": users_count
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Auth API Server...")
    print("🌐 Server running on http://localhost:5003")
    print("📋 Available endpoints:")
    print("   🔐 Authentication:")
    print("     POST /api/register - Register new user")
    print("     POST /api/login - Login user")
    print("     GET  /api/profile - Get user profile (requires auth)")
    print("   💬 Chat:")
    print("     POST /api/chat - Chat with AI Agent (requires auth)")
    print("   🍽️  Preferences:")
    print("     GET  /api/preferences - Get user preferences (requires auth)")
    print("     PUT  /api/preferences - Update user preferences (requires auth)")
    print("   🔧 System:")
    print("     GET  /api/health - Health check")
    print("=" * 60)
    print("🎧 Server is now listening on http://localhost:5003")
    print("📡 Ready to accept requests!")
    print("=" * 60)
    
    app.run(debug=True, port=5003)