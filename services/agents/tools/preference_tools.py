"""
LangChain Tools for Preference Management
"""

from langchain.tools import tool
from services.preference_service import PreferenceService

preference_service = PreferenceService()

@tool
def read_user_preferences(user_id: str) -> dict:
    """Read user's current food preferences from database"""
    print(f"🔧 PREFERENCE TOOL: Reading preferences for user {user_id}")
    result = preference_service.get_user_preferences(user_id)
    print(f"📊 PREFERENCE TOOL: Retrieved preferences: {result}")
    return result

@tool
def update_user_preferences(user_id: str, preferences: dict) -> bool:
    """Update user's food preferences in database"""
    return preference_service.update_user_preferences(user_id, preferences)

@tool
def add_single_preference(user_id: str, preference_type: str, value: str) -> bool:
    """Add a single preference to user's existing preferences"""
    return preference_service.add_preference(user_id, preference_type, value)

@tool
def check_missing_mandatory_preferences(preferences: dict = None) -> list:
    """Check which mandatory preferences are missing (restrictions, allergies, cuisine_preferences)"""
    if preferences is None:
        preferences = {}
    return preference_service.get_missing_mandatory_preferences(preferences)

@tool
def has_complete_preferences(preferences: dict = None) -> bool:
    """Check if user has all mandatory preferences"""
    if preferences is None:
        preferences = {}
    return preference_service.has_complete_preferences(preferences)
