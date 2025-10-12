# 🚀 Food Bot API Reference

## Overview
Complete API documentation for the Food Bot system with intelligent food recommendations, preference management, and conversational AI.

## Base URL
```
http://localhost:5003
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

---

## 📋 API Endpoints

### 1. User Registration
**Endpoint:** `POST /api/register`

**Description:** Register a new user account

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "H4DhNcCtY1pliOBmt1m2",
    "username": "test_user",
    "email": "test@example.com",
    "created_at": "2025-10-11T14:39:47.611850"
  }
}
```

**Error Responses:**
- `400` - Missing required fields or email already exists
- `500` - Server error

**Example cURL:**
```bash
curl -X POST http://localhost:5003/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

---

### 2. User Login
**Endpoint:** `POST /api/login`

**Description:** Authenticate user and get JWT token

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "H4DhNcCtY1pliOBmt1m2",
    "username": "test_user",
    "email": "test@example.com",
    "created_at": "2025-10-11T14:39:47.611850"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 2592000
}
```

**Error Responses:**
- `400` - Missing email or password
- `401` - Invalid credentials
- `500` - Server error

**Example cURL:**
```bash
curl -X POST http://localhost:5003/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

---

### 3. Get User Profile
**Endpoint:** `GET /api/profile`

**Description:** Get current user's profile information

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "user": {
    "id": "H4DhNcCtY1pliOBmt1m2",
    "username": "test_user",
    "email": "test@example.com",
    "created_at": "2025-10-11T14:39:47.611850"
  }
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `404` - User not found
- `500` - Server error

**Example cURL:**
```bash
curl -X GET http://localhost:5003/api/profile \
  -H "Authorization: Bearer <jwt_token>"
```

---

### 4. AI Chat
**Endpoint:** `POST /api/chat`

**Description:** Send message to AI agent for food recommendations and preference collection. Supports session-based conversation context for isolated conversations.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "string",
  "session_id": "string (optional)"
}
```

**Parameters:**
- `message` (required): The user's message to the AI agent
- `session_id` (optional): Session ID for conversation context. If not provided, uses "default" session

**Success Response (200):**
```json
{
  "message": "AI agent response text",
  "user_message": "User's original message",
  "session_id": "session_id_used",
  "timestamp": "2025-10-11T15:53:45.506567"
}
```

**Error Responses:**
- `400` - Missing message or request body
- `401` - Missing or invalid token
- `500` - Server error

**Example cURL:**
```bash
# Basic chat without session
curl -X POST http://localhost:5003/api/chat \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "I'\''m hungry, what should I eat?"}'

# Chat with specific session
curl -X POST http://localhost:5003/api/chat \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "I'\''m hungry, what should I eat?", "session_id": "uuid-string"}'
```

**Example Conversations:**
```json
// First message - AI asks for preferences
{
  "message": "I'm hungry!",
  "user_message": "I'm hungry!",
  "timestamp": "2025-10-11T15:53:45.506567"
}

// User responds with preferences
{
  "message": "Great! I've noted that you're vegetarian and avoid nuts. Here are some recommendations...",
  "user_message": "I'm vegetarian and allergic to nuts",
  "timestamp": "2025-10-11T15:54:12.123456"
}

// User says no preferences
{
  "message": "Perfect! Here are some general recommendations: Pizza, Sushi, Tacos, Pasta Carbonara",
  "user_message": "I have no dietary restrictions",
  "timestamp": "2025-10-11T15:54:30.789012"
}
```

---

### 5. Session Management

#### Create New Session
**Endpoint:** `POST /api/sessions`

**Description:** Create a new conversation session for the user

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_name": "string (optional)"
}
```

**Success Response (200):**
```json
{
  "session_id": "uuid-string",
  "session_name": "My Food Session",
  "created_at": "2025-10-11T14:39:47.611850"
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `500` - Server error

**Example cURL:**
```bash
curl -X POST http://localhost:5003/api/sessions \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"session_name": "Food Planning Session"}'
```

#### Get User Sessions
**Endpoint:** `GET /api/sessions`

**Description:** Get all sessions for the current user

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "sessions": [
    {
      "session_id": "uuid-string",
      "session_name": "My Food Session",
      "message_count": 5,
      "last_activity": "2025-10-11T14:39:47.611850"
    }
  ]
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `500` - Server error

#### Get Session History
**Endpoint:** `GET /api/sessions/{session_id}/history`

**Description:** Get chat history for a specific session

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "history": [
    {
      "user": "User message",
      "assistant": "AI response",
      "timestamp": "2025-10-11T14:39:47.611850",
      "session_id": "uuid-string"
    }
  ]
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `404` - Session not found
- `500` - Server error

#### Delete Session
**Endpoint:** `DELETE /api/sessions/{session_id}`

**Description:** Delete a specific session and all its messages

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "message": "Session deleted successfully"
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `404` - Session not found
- `500` - Server error

#### Clear Session History
**Endpoint:** `DELETE /api/sessions/{session_id}/history`

**Description:** Clear chat history for a specific session (keeps session)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "message": "Session history cleared successfully"
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `404` - Session not found
- `500` - Server error

---

### 6. Get User Preferences
**Endpoint:** `GET /api/preferences`

**Description:** Get current user's food preferences

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
{
  "preferences": {
    "restrictions": ["vegetarian"],
    "allergies": ["nuts"],
    "cuisine_preferences": ["italian", "indian"],
    "likes": ["pasta", "spicy food"],
    "dislikes": ["mushrooms"],
    "custom": ["prefer warm meals"]
  },
  "timestamp": "2025-10-11T15:53:48.088217"
}
```

**Empty Preferences Response:**
```json
{
  "preferences": null,
  "timestamp": "2025-10-11T15:53:48.088217"
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `500` - Server error

**Example cURL:**
```bash
curl -X GET http://localhost:5003/api/preferences \
  -H "Authorization: Bearer <jwt_token>"
```

---

### 7. Update User Preferences
**Endpoint:** `PUT /api/preferences`

**Description:** Update user's food preferences

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "preferences": {
    "restrictions": ["vegetarian", "gluten-free"],
    "allergies": ["nuts", "shellfish"],
    "cuisine_preferences": ["italian", "indian", "mexican"],
    "likes": ["pasta", "spicy food", "seafood"],
    "dislikes": ["mushrooms", "olives"],
    "custom": ["prefer warm meals", "no raw fish"]
  }
}
```

**Success Response (200):**
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "restrictions": ["vegetarian", "gluten-free"],
    "allergies": ["nuts", "shellfish"],
    "cuisine_preferences": ["italian", "indian", "mexican"],
    "likes": ["pasta", "spicy food", "seafood"],
    "dislikes": ["mushrooms", "olives"],
    "custom": ["prefer warm meals", "no raw fish"]
  },
  "timestamp": "2025-10-11T15:53:48.088217"
}
```

**Error Responses:**
- `400` - Missing request body or preferences
- `401` - Missing or invalid token
- `500` - Server error

**Example cURL:**
```bash
curl -X PUT http://localhost:5003/api/preferences \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "preferences": {
      "restrictions": ["vegetarian"],
      "allergies": ["nuts"],
      "cuisine_preferences": ["italian"]
    }
  }'
```

---

### 8. Health Check
**Endpoint:** `GET /api/health`

**Description:** Check API health and database connectivity

**Success Response (200):**
```json
{
  "status": "healthy",
  "message": "Simple Auth API with Firebase is running",
  "timestamp": "2025-10-11T14:39:56.781789",
  "database": "Firebase Firestore",
  "users_count": 1
}
```

**Error Response (500):**
```json
{
  "status": "unhealthy",
  "message": "Database connection failed",
  "timestamp": "2025-10-11T14:39:56.781789",
  "database": "Firebase Firestore",
  "users_count": 0
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:5003/api/health
```

---

## 📊 Data Models

### User Object
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "string (ISO 8601)"
}
```

### Preferences Object
```json
{
  "restrictions": ["string"],
  "allergies": ["string"],
  "cuisine_preferences": ["string"],
  "likes": ["string"],
  "dislikes": ["string"],
  "custom": ["string"]
}
```

### Chat Message Object
```json
{
  "message": "string",
  "user_message": "string",
  "timestamp": "string (ISO 8601)"
}
```

---

## 🔧 Error Handling

### Standard Error Response Format
```json
{
  "error": "string"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (missing/invalid data)
- `401` - Unauthorized (invalid/missing token)
- `404` - Not Found
- `500` - Internal Server Error

---

## 🚀 Quick Start Examples

### Complete User Flow
```bash
# 1. Register user
curl -X POST http://localhost:5003/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# 2. Login and get token
TOKEN=$(curl -X POST http://localhost:5003/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' | jq -r '.token')

# 3. Start chat
curl -X POST http://localhost:5003/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I'\''m hungry!"}'

# 4. Check preferences
curl -X GET http://localhost:5003/api/preferences \
  -H "Authorization: Bearer $TOKEN"

# 5. Update preferences
curl -X PUT http://localhost:5003/api/preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"preferences": {"restrictions": ["vegetarian"], "allergies": ["nuts"]}}'
```

---

## 📝 Notes

### Authentication
- JWT tokens expire after 30 days (2592000 seconds)
- Include token in Authorization header for protected endpoints
- Token format: `Bearer <jwt_token>`

### Chat Behavior
- AI automatically collects missing preferences conversationally
- Supports "no preferences" responses (saves as "none")
- Maintains conversation context within chat sessions
- Provides food recommendations based on collected preferences

### Preferences
- All preference fields are arrays of strings
- `restrictions`, `allergies`, `cuisine_preferences` are mandatory for recommendations
- `likes`, `dislikes`, `custom` are optional
- Supports any custom preference text

### Rate Limiting
- No rate limiting currently implemented
- Consider implementing for production use

---

## 🔄 API Versioning

**Current Version:** v1.0
**Base URL:** `http://localhost:5003`

No versioning in URL path currently. All endpoints are at root level.

---

*Last Updated: 2025-10-11*
*Generated from: app.py, services/*.py*
