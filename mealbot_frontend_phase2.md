# MealBot Frontend API Guide - Phase 2

## Overview
This guide covers the enhanced MealBot API with AI-powered food recommendations, preference management, and intelligent conversation handling using LangChain agents.

## Base URL
```
http://localhost:5003
```

## New Features in Phase 2

### 🤖 **AI Agent System**
- **Manager Agent**: Coordinates preference collection and food recommendations
- **Context-Aware Chat**: Maintains conversation context within chat sessions
- **Intelligent Routing**: Automatically determines when to collect preferences vs. provide recommendations

### 🍽️ **Preference Management**
- **Flexible Schema**: Supports any type of food preference
- **Mandatory Preferences**: Tracks essential preferences (dietary restrictions, allergies, cuisine)
- **Conversational Collection**: Natural preference gathering through chat

### 🎯 **Smart Recommendations**
- **Context-Aware**: Considers user preferences and conversation history
- **Progressive Detail**: Basic recommendations first, detailed info on request
- **Personalized**: Adapts to individual user preferences

## API Endpoints

### 1. Enhanced Chat with AI Agent
**Endpoint:** `POST /api/chat`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "string"
}
```

**Success Response (200):**
```json
{
  "message": "AI agent response",
  "user_message": "User's original message",
  "timestamp": "2025-10-11T14:39:47.611850"
}
```

**Use Cases:**
- **First-time users**: Agent will collect preferences conversationally
- **Preference updates**: Agent can update preferences based on conversation
- **Food recommendations**: Get personalized meal suggestions
- **Detailed recipes**: Ask for cooking instructions, macros, etc.

**Example Conversations:**

*Initial Chat:*
```
User: "I'm hungry, what should I eat?"
Agent: "I'd love to recommend some great meals! First, do you have any dietary restrictions like vegetarian or vegan?"
```

*Preference Collection:*
```
User: "I'm vegetarian and allergic to nuts"
Agent: "Great! What type of cuisines do you enjoy? Italian, Indian, Mexican, etc.?"
```

*Recommendations:*
```
User: "I like Italian food"
Agent: "Perfect! Here are some great vegetarian Italian options:
- Pasta with Marinara Sauce (Vegetarian, Italian)
- Margherita Pizza (Vegetarian, Italian)
- Caprese Salad (Vegetarian, Italian)"
```

*Detailed Information:*
```
User: "Tell me more about the pasta recipe"
Agent: "Here's the detailed recipe for Pasta with Marinara Sauce:
[Detailed recipe with ingredients, instructions, macros, cooking time]"
```

### 2. Get User Preferences
**Endpoint:** `GET /api/preferences`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "preferences": {
    "likes": ["pasta", "spicy food", "italian cuisine"],
    "dislikes": ["mushrooms", "seafood"],
    "restrictions": ["vegetarian", "no red food"],
    "allergies": ["nuts", "dairy"],
    "custom": ["prefer warm meals", "love garlic"]
  },
  "timestamp": "2025-10-11T14:39:47.611850"
}
```

**Use Cases:**
- Display current preferences in user profile
- Check what preferences are already set
- Debug preference-related issues

### 3. Update User Preferences
**Endpoint:** `PUT /api/preferences`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "preferences": {
    "likes": ["pasta", "spicy food"],
    "dislikes": ["mushrooms"],
    "restrictions": ["vegetarian"],
    "allergies": ["nuts"],
    "custom": ["prefer warm meals"]
  }
}
```

**Success Response (200):**
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "likes": ["pasta", "spicy food"],
    "dislikes": ["mushrooms"],
    "restrictions": ["vegetarian"],
    "allergies": ["nuts"],
    "custom": ["prefer warm meals"]
  },
  "timestamp": "2025-10-11T14:39:47.611850"
}
```

**Use Cases:**
- Direct preference updates from settings page
- Bulk preference updates
- Preference management outside of chat

## Preference Schema

### **Flexible Structure**
The preference system uses a flexible schema that can accommodate any type of food preference:

```json
{
  "preferences": {
    "likes": ["array of liked foods/cuisines"],
    "dislikes": ["array of disliked foods"],
    "restrictions": ["dietary restrictions like vegetarian, vegan"],
    "allergies": ["food allergies"],
    "custom": ["any other preferences like 'no red food'"]
  }
}
```

### **Mandatory Preferences (First 3)**
The system tracks these as essential for recommendations:
1. **Dietary restrictions** (vegetarian, vegan, gluten-free, etc.)
2. **Allergies** (nuts, dairy, shellfish, etc.)
3. **Cuisine preferences** (Italian, Indian, Mexican, etc.)

## Frontend Implementation Guidelines

### **Chat Interface Enhancements**
1. **Context Awareness**: The chat maintains context within a session
2. **Progressive Disclosure**: Show basic recommendations first, details on request
3. **Preference Indicators**: Show when preferences are being collected
4. **Loading States**: Handle agent processing time

### **Preference Management UI**
1. **Preference Display**: Show current preferences in user profile
2. **Direct Updates**: Allow manual preference updates
3. **Preference Validation**: Show which mandatory preferences are missing
4. **Flexible Input**: Allow custom preference entries

### **State Management**
1. **Chat History**: Maintain conversation context
2. **User Preferences**: Cache and sync with backend
3. **Loading States**: Handle agent processing
4. **Error Handling**: Graceful degradation for agent failures

### **User Experience Flow**
1. **First Visit**: Agent collects preferences conversationally
2. **Regular Use**: Get personalized recommendations
3. **Preference Updates**: Natural conversation or direct updates
4. **Detailed Info**: Ask follow-up questions for recipes, macros

## Error Handling

### **Agent Errors**
- **Retry Logic**: 3 attempts for Gemini failures
- **Fallback Messages**: "Sorry, Gemini seems to have an issue"
- **Graceful Degradation**: Basic responses when agent fails

### **Preference Errors**
- **Validation**: Handle invalid preference formats
- **Database Errors**: Retry or show user-friendly messages
- **Network Issues**: Offline preference caching

## Security Considerations

1. **Input Sanitization**: Clean user inputs before processing
2. **Preference Validation**: Basic validation for preference data
3. **Rate Limiting**: Prevent abuse of agent endpoints
4. **Data Privacy**: Secure storage of personal preferences

## Testing

### **Test Scenarios**
1. **New User Flow**: Complete preference collection
2. **Existing User**: Direct recommendations
3. **Preference Updates**: Modify existing preferences
4. **Error Handling**: Agent failures and recovery
5. **Context Maintenance**: Multi-turn conversations

### **Test Data**
Use the existing test user or create new ones:
- **Email:** test@example.com
- **Password:** TestPass123

## Migration from Phase 1

### **Backward Compatibility**
- All Phase 1 endpoints remain unchanged
- Chat endpoint enhanced but maintains same interface
- New endpoints are additive

### **Frontend Updates Needed**
1. **Chat Interface**: Update to handle agent responses
2. **Preference Management**: Add preference UI components
3. **State Management**: Add preference and context state
4. **Error Handling**: Update for agent-specific errors

## Support

For API issues or questions:
1. Check server logs for agent processing details
2. Verify Gemini API key configuration
3. Test preference endpoints independently
4. Contact backend team for agent-specific issues

