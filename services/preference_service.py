"""
Preference Service
Handles user food preferences management
"""

from firebase_config import firebase_config
from datetime import datetime

class PreferenceService:
    def __init__(self):
        self.db = firebase_config.get_db()
        self.users_collection = self.db.collection('users')
    
    def get_user_preferences(self, user_id):
        """Get user preferences from database"""
        try:
            user_doc = self.users_collection.document(user_id).get()
            if not user_doc.exists:
                return None
            
            user_data = user_doc.to_dict()
            return user_data.get('preferences', {})
        except Exception as e:
            print(f"❌ PREFERENCE SERVICE: Error getting preferences: {e}")
            return {}
    
    def update_user_preferences(self, user_id, preferences):
        """Update user preferences in database"""
        try:
            user_doc_ref = self.users_collection.document(user_id)
            
            # Check if user document exists
            user_doc = user_doc_ref.get()
            if not user_doc.exists:
                # Create user document with basic info and preferences
                user_data = {
                    'username': f'user_{user_id}',
                    'email': f'user_{user_id}@example.com',
                    'preferences': preferences,
                    'preferences_updated_at': datetime.utcnow(),
                    'created_at': datetime.utcnow()
                }
                user_doc_ref.set(user_data)
                print(f"✅ PREFERENCE SERVICE: Created user document with preferences for user {user_id}")
            else:
                # Update existing user document
                user_doc_ref.update({
                    'preferences': preferences,
                    'preferences_updated_at': datetime.utcnow()
                })
                print(f"✅ PREFERENCE SERVICE: Updated preferences for user {user_id}")
            return True
        except Exception as e:
            print(f"❌ PREFERENCE SERVICE: Error updating preferences: {e}")
            return False
    
    def add_preference(self, user_id, preference_type, value):
        """Add a single preference to user's existing preferences"""
        try:
            current_preferences = self.get_user_preferences(user_id)
            if not current_preferences:
                current_preferences = {
                    "likes": [],
                    "dislikes": [],
                    "restrictions": [],
                    "allergies": [],
                    "cuisine_preferences": [],
                    "custom": []
                }
            
            # Add to appropriate category
            if preference_type in current_preferences:
                if isinstance(current_preferences[preference_type], list):
                    if value not in current_preferences[preference_type]:
                        current_preferences[preference_type].append(value)
                else:
                    current_preferences[preference_type] = value
            else:
                # Add to custom if type doesn't exist
                if "custom" not in current_preferences:
                    current_preferences["custom"] = []
                current_preferences["custom"].append(f"{preference_type}: {value}")
            
            return self.update_user_preferences(user_id, current_preferences)
        except Exception as e:
            print(f"❌ PREFERENCE SERVICE: Error adding preference: {e}")
            return False
    
    def get_missing_mandatory_preferences(self, preferences):
        """Check which mandatory preferences are missing"""
        mandatory_fields = ["restrictions", "allergies", "cuisine_preferences"]
        missing = []
        
        for field in mandatory_fields:
            if not preferences.get(field) or len(preferences.get(field, [])) == 0:
                missing.append(field)
        
        return missing
    
    def has_complete_preferences(self, preferences):
        """Check if user has all mandatory preferences"""
        return len(self.get_missing_mandatory_preferences(preferences)) == 0
