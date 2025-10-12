"""
Authentication Service
Handles user registration, login, and profile operations
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from firebase_config import firebase_config
import os

class AuthService:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
        self.jwt_expires = 2592000  # 30 days (1 month)
        self.db = firebase_config.get_db()
        self.users_collection = self.db.collection('users')
    
    def hash_password(self, password):
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password, hashed):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def generate_token(self, user_id):
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expires)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def register_user(self, username, email, password):
        """Register a new user"""
        print("🔍 Checking if user already exists in Firestore...")
        print(f"📧 FIRESTORE: Searching for email: {email}")
        
        try:
            existing_user = self.users_collection.where('email', '==', email).get()
            print(f"📊 FIRESTORE: Found {len(existing_user)} existing users with this email")
            if existing_user:
                print("❌ Email already registered")
                raise ValueError("Email already registered")
        except Exception as e:
            print(f"❌ FIRESTORE: Error checking existing user: {e}")
            raise Exception("Database connection failed")
        
        # Create user in Firestore
        print("💾 Creating user in Firestore...")
        hashed_password = self.hash_password(password)
        created_at = datetime.utcnow()
        
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': created_at
        }
        
        # Add user to Firestore
        print("📝 FIRESTORE: Creating new document...")
        try:
            doc_ref = self.users_collection.document()
            print(f"🆔 FIRESTORE: Generated document ID: {doc_ref.id}")
            
            print("💾 FIRESTORE: Setting document data...")
            doc_ref.set(user_data)
            user_id = doc_ref.id
            
            print(f"✅ User registered successfully in Firestore: {user_id}")
            print(f"📊 FIRESTORE: Document created with data: {user_data}")
            
            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "created_at": created_at
            }
        except Exception as e:
            print(f"❌ FIRESTORE: Error creating user: {e}")
            raise Exception("Failed to create user in database")
    
    def login_user(self, email, password):
        """Login user and return user data with token"""
        print("🔍 Checking if user exists in Firestore...")
        print(f"📧 FIRESTORE: Searching for email: {email}")
        
        try:
            user_docs = self.users_collection.where('email', '==', email).get()
            print(f"📊 FIRESTORE: Found {len(user_docs)} users with this email")
            if not user_docs:
                print("❌ User not found")
                raise ValueError("Invalid credentials")
            
            user_doc = user_docs[0]
            print(f"🆔 FIRESTORE: User document ID: {user_doc.id}")
            user = user_doc.to_dict()
            user['id'] = user_doc.id
            print(f"👤 FIRESTORE: User data retrieved: {list(user.keys())}")
        except Exception as e:
            print(f"❌ FIRESTORE: Error finding user: {e}")
            raise Exception("Database connection failed")
        
        # Verify password
        if not self.verify_password(password, user['password']):
            print("❌ Invalid password")
            raise ValueError("Invalid credentials")
        
        # Generate token
        token = self.generate_token(user['id'])
        print(f"✅ Login successful, token generated")
        
        return {
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "created_at": user['created_at']
            },
            "token": token,
            "expires_in": self.jwt_expires
        }
    
    def get_user_profile(self, user_id):
        """Get user profile by ID"""
        print(f"🔍 Looking for user with ID: {user_id}")
        print(f"📝 FIRESTORE: Getting document with ID: {user_id}")
        
        try:
            user_doc = self.users_collection.document(user_id).get()
            
            print(f"📊 FIRESTORE: Document exists: {user_doc.exists}")
            if not user_doc.exists:
                print("❌ User not found")
                raise ValueError("User not found")
            
            user = user_doc.to_dict()
            user['id'] = user_doc.id
            print(f"👤 FIRESTORE: User data retrieved: {list(user.keys())}")
            
            return {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "created_at": user['created_at']
            }
        except Exception as e:
            print(f"❌ FIRESTORE: Error getting user profile: {e}")
            raise Exception("Database connection failed")
    
    def verify_token(self, token):
        """Verify JWT token and return user_id"""
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return data['user_id']
        except:
            raise ValueError("Token is invalid")
