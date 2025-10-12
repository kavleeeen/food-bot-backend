# Simple Auth API

A minimal Flask API with user registration and login functionality using JWT authentication.

## Features

- ✅ User Registration
- ✅ User Login
- ✅ JWT Token Authentication
- ✅ Password Hashing (bcrypt)
- ✅ Protected Profile Endpoint
- ✅ Health Check

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables (optional):
   ```bash
   export JWT_SECRET_KEY="your-secret-key-here"
   ```

3. Start the server:
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5001`

## API Endpoints

### Register User
```bash
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Login User
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Get Profile (Protected)
```bash
curl -X GET http://localhost:5001/api/profile \
  -H "Authorization: Bearer <your_jwt_token>"
```

### Health Check
```bash
curl -X GET http://localhost:5001/api/health
```

## Response Examples

### Register Response
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00.000000"
  }
}
```

### Login Response
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00.000000"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 3600
}
```

## Notes

- Uses in-memory storage (data is lost when server restarts)
- JWT tokens expire after 1 hour
- Passwords are hashed using bcrypt
- CORS is enabled for frontend integration