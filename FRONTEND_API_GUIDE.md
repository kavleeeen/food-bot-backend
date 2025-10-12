# Frontend API Integration Guide

## Overview
This guide provides everything a frontend engineer needs to implement user authentication and AI chat functionality using the Food Bot API.

## Base URL
```
http://localhost:5003
```

## API Endpoints

### 1. User Registration
**Endpoint:** `POST /api/register`

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

### 2. User Login
**Endpoint:** `POST /api/login`

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
    "created_at": "2025-10-11T14:39:47.611850+00:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 2592000
}
```

**Error Responses:**
- `400` - Missing required fields
- `401` - Invalid credentials
- `500` - Server error

### 3. Get User Profile (Protected)
**Endpoint:** `GET /api/profile`

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
    "created_at": "2025-10-11T14:39:47.611850+00:00"
  }
}
```

**Error Responses:**
- `401` - Missing or invalid token
- `404` - User not found
- `500` - Server error

### 4. Chat with AI (Protected)
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
  "message": "AI response text here",
  "user_message": "User's original message",
  "timestamp": "2025-10-11T14:39:47.611850"
}
```

**Error Responses:**
- `400` - Missing message
- `401` - Missing or invalid token
- `500` - Server error

### 5. Health Check
**Endpoint:** `GET /api/health`

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

## Frontend Implementation Guidelines

### Authentication Flow
1. **Registration:**
   - Send POST request to `/api/register` with username, email, password
   - On success, automatically log the user in
   - Store JWT token and user data in localStorage/sessionStorage

2. **Login:**
   - Send POST request to `/api/login` with email and password
   - Store JWT token and user data on successful response
   - Redirect to protected area of application

3. **Protected Routes:**
   - Check for JWT token in localStorage before accessing protected endpoints
   - Include `Authorization: Bearer <token>` header in all protected API calls
   - Handle token expiration (3600 seconds = 1 hour)

4. **Logout:**
   - Remove JWT token and user data from storage
   - Redirect to login page

### Chat Implementation
1. **Message Sending:**
   - Send POST request to `/api/chat` with message in request body
   - Include JWT token in Authorization header
   - Display AI response in chat interface

2. **Error Handling:**
   - Handle network errors gracefully
   - Show appropriate error messages for different HTTP status codes
   - Implement retry logic for failed requests

### State Management
- Store authentication state (user data, token, login status)
- Manage chat history and conversation state
- Handle loading states for API calls
- Implement proper error state management

### UI Components Needed
- **Authentication:**
  - Login form (email, password)
  - Registration form (username, email, password)
  - Logout button/functionality

- **Chat Interface:**
  - Message input field
  - Chat messages display area
  - Loading indicators for AI responses
  - Error message display

### Security Considerations
1. **Token Storage:** Use `httpOnly` cookies in production instead of localStorage
2. **HTTPS:** Always use HTTPS in production
3. **Token Expiration:** Implement automatic token refresh or re-login flow
4. **Input Validation:** Validate all inputs on frontend before sending to API
5. **Error Messages:** Don't expose sensitive information in error messages

### Error Handling
Common error scenarios to handle:

- **Network errors:** Show "Connection failed" message
- **Validation errors:** Display field-specific error messages
- **Authentication errors:** Redirect to login page
- **Chat errors:** Show error message in chat interface
- **Server errors:** Show generic "Something went wrong" message

### Testing
Use these test credentials after registration:
- **Email:** test@example.com
- **Password:** TestPass123

### CORS Configuration
The API has CORS enabled for frontend integration. If you encounter CORS issues, ensure your frontend is running on a proper domain (not `file://` protocol).

### Environment Setup
Create a `.env` file in your React project with:
```
REACT_APP_API_BASE_URL=http://localhost:5003
```

### API Service Structure
Organize your API calls in a dedicated service file:
- `authService.js` - Handle authentication endpoints
- `chatService.js` - Handle chat endpoints
- `apiClient.js` - Base API client with token management

### Support
For API issues or questions, check the server logs or contact the backend team.