"""
LangChain Tools for Preference Management
"""

# from langchain.tools import tool
from services.preference_service import PreferenceService

preference_service = PreferenceService()

# @tool
def read_user_preferences(user_id: str) -> dict:
    """Read user's current food preferences from database"""
    print("=" * 60)
    print("🔧 PREFERENCE TOOL: read_user_preferences CALLED!")
    print(f"🔧 PREFERENCE TOOL: Reading preferences for user {user_id}")
    result = preference_service.get_user_preferences(user_id)
    print(f"📊 PREFERENCE TOOL: Retrieved preferences: {result}")
    print("=" * 60)
    return result

# @tool
def update_user_preferences(user_id: str, preferences: dict) -> bool:
    """Update user's food preferences in database"""
    print("=" * 60)
    print("🔧 PREFERENCE TOOL: update_user_preferences CALLED!")
    print(f"🔧 PREFERENCE TOOL: Updating preferences for user {user_id}")
    print(f"📝 PREFERENCE TOOL: New preferences: {preferences}")
    result = preference_service.update_user_preferences(user_id, preferences)
    print(f"✅ PREFERENCE TOOL: Update result: {result}")
    print("=" * 60)
    return result

# @tool
def add_single_preference(user_id: str, preference_type: str, value: str) -> bool:
    """Add a single preference to user's existing preferences"""
    print("=" * 60)
    print("🔧 PREFERENCE TOOL: add_single_preference CALLED!")
    print(f"🔧 PREFERENCE TOOL: Adding single preference for user {user_id}")
    print(f"📝 PREFERENCE TOOL: Type: {preference_type}, Value: {value}")
    result = preference_service.add_preference(user_id, preference_type, value)
    print(f"✅ PREFERENCE TOOL: Add result: {result}")
    print("=" * 60)
    return result

# @tool
def check_missing_mandatory_preferences(preferences: dict = None) -> list:
    """Check which mandatory preferences are missing (restrictions, allergies, cuisine_preferences)"""
    print("=" * 60)
    print("🔧 PREFERENCE TOOL: check_missing_mandatory_preferences CALLED!")
    print(f"🔧 PREFERENCE TOOL: Checking missing mandatory preferences")
    print(f"📝 PREFERENCE TOOL: Current preferences: {preferences}")
    if preferences is None:
        preferences = {}
    result = preference_service.get_missing_mandatory_preferences(preferences)
    print(f"📊 PREFERENCE TOOL: Missing preferences: {result}")
    print("=" * 60)
    return result

# @tool
def has_complete_preferences(preferences: dict = None) -> bool:
    """Check if user has all mandatory preferences"""
    print("=" * 60)
    print("🔧 PREFERENCE TOOL: has_complete_preferences CALLED!")
    print(f"🔧 PREFERENCE TOOL: Checking if preferences are complete")
    print(f"📝 PREFERENCE TOOL: Current preferences: {preferences}")
    if preferences is None:
        preferences = {}
    result = preference_service.has_complete_preferences(preferences)
    print(f"📊 PREFERENCE TOOL: Complete preferences: {result}")
    print("=" * 60)
    return result
