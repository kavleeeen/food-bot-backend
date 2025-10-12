# 🍽️ Food Bot Backend

An intelligent food recommendation chatbot backend built with Flask, Firebase Firestore, and LangChain agents. Designed specifically for Indian users to eliminate decision fatigue by providing personalized meal suggestions, recipes, and dietary preference management.

## 🌟 Features

### Core Functionality
- 🤖 **AI-Powered Chat**: LangGraph-based conversational agent with persistent memory
- 🍛 **Food Recommendations**: Personalized meal suggestions based on user preferences
- 📖 **Recipe Generation**: Detailed recipes with ingredients, instructions, and nutritional info
- 🔄 **Recipe Variations**: Creative variations and modifications for existing recipes
- 👋 **Smart Greetings**: Context-aware greeting detection and responses

### User Management
- 🔐 **JWT Authentication**: Secure user registration and login
- 👤 **User Profiles**: Comprehensive user preference management
- 📊 **Session Management**: Multi-session conversation tracking
- 💾 **Persistent Storage**: Firebase Firestore for reliable data storage

### Preference System
- 🥗 **Dietary Restrictions**: Vegetarian, vegan, gluten-free, etc.
- 🚫 **Allergy Management**: Comprehensive allergy tracking
- 🌶️ **Cuisine Preferences**: Indian, Italian, Chinese, and more
- ⚙️ **Custom Preferences**: Flexible preference system

## 🏗️ Architecture

```
food-bot-backend/
├── app.py                          # Main Flask application
├── firebase_config.py              # Firebase configuration
├── requirements.txt                # Python dependencies
├── services/
│   ├── auth_service.py            # Authentication logic
│   ├── chat_service.py            # Chat orchestration
│   ├── chat_history_service.py    # Message storage & retrieval
│   ├── preference_service.py      # User preference management
│   └── agents/
│       ├── enhanced_langgraph_agent.py  # Main AI agent
│       └── tools/
│           ├── greeting_tools.py        # Greeting detection
│           ├── preference_tools.py      # Preference management
│           ├── recipe_tools.py          # Recipe generation
│           └── recommendation_tools.py  # Food recommendations
└── API_REFERENCE.md               # Complete API documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Firebase project with Firestore enabled
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd food-bot-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   export JWT_SECRET_KEY="your-jwt-secret-key"
   export GEMINI_API_KEY="your-gemini-api-key"
   export FIREBASE_PROJECT_ID="your-firebase-project-id"
   export FIREBASE_DATABASE_ID="your-firestore-database-id"
   export FIREBASE_KEY_FILE="path/to/firebase-service-account.json"
   ```

4. **Configure Firebase**
   - Download your Firebase service account key
   - Place it in the project root as `firebase.json`
   - Ensure Firestore is enabled in your Firebase project

5. **Start the server**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5001`

## 📡 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (protected)

### Chat & Recommendations
- `POST /api/chat` - Send message to food bot
- `GET /api/chat/history` - Get conversation history
- `DELETE /api/chat/history` - Clear conversation history

### Preferences
- `GET /api/preferences` - Get user preferences
- `PUT /api/preferences` - Update user preferences

### Sessions
- `GET /api/sessions` - Get user sessions
- `POST /api/sessions` - Create new session
- `DELETE /api/sessions/<session_id>` - Delete session

### Health & Info
- `GET /api/health` - Health check
- `GET /api/agent/info` - Get agent information

## 💬 Usage Examples

### 1. Register and Login
```bash
# Register
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "foodie123",
    "email": "user@example.com",
    "password": "SecurePass123"
  }'

# Login
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### 2. Chat with Food Bot
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "message": "I want lunch recommendations",
    "session_id": "optional-session-id"
  }'
```

### 3. Set Preferences
```bash
curl -X PUT http://localhost:5001/api/preferences \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "restrictions": ["vegetarian"],
    "allergies": ["nuts"],
    "cuisine_preferences": ["indian", "italian"]
  }'
```

## 🤖 AI Agent Behavior

### User-First Approach
The AI agent prioritizes user requests over preference collection:

1. **Immediate Help**: Provides food recommendations, recipes, or variations when requested
2. **Contextual Preferences**: Asks for preferences only when needed for better recommendations
3. **Follow-up Questions**: Collects preferences as natural follow-up, not as barriers

### Tool Priority System
- **HIGH PRIORITY**: Food recommendations, recipe generation, recipe variations
- **MEDIUM PRIORITY**: Reading existing preferences (when needed)
- **LOW PRIORITY**: Preference updates (as follow-up questions)

### Example Conversation Flow
```
User: "I want lunch recommendations"
Bot: [Provides immediate recommendations]
Bot: "For better future recommendations, do you have any dietary restrictions?"

User: "How to make biryani?"
Bot: [Provides detailed recipe immediately]
Bot: "Would you like variations of this recipe?"
```

## 🗄️ Database Schema

### Messages Collection
```json
{
  "user_id": "string",
  "session_id": "string",
  "user_message": "string",
  "assistant_response": "string",
  "message_length": "number",
  "response_length": "number",
  "timestamp": "datetime",
  "created_at": "string",
  "message_type": "conversation",
  "metadata": {
    "user_message_tokens": "number",
    "assistant_response_tokens": "number",
    "is_greeting": "boolean",
    "contains_food_keywords": "boolean",
    "session_created_at": "string"
  }
}
```

### User Sessions Collection
```json
{
  "user_id": "string",
  "session_id": "string",
  "session_name": "string",
  "created_at": "string",
  "status": "active",
  "metadata": {
    "message_count": "number",
    "total_tokens": "number",
    "food_related_messages": "number",
    "greeting_messages": "number",
    "last_activity": "string"
  }
}
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Required |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `FIREBASE_PROJECT_ID` | Firebase project ID | `food-recommend-39842` |
| `FIREBASE_DATABASE_ID` | Firestore database ID | `food-bot` |
| `FIREBASE_KEY_FILE` | Path to Firebase service account key | `firebase.json` |

### Firebase Setup
1. Create a Firebase project
2. Enable Firestore Database
3. Create a service account and download the key
4. Place the key file in your project root

## 🧪 Testing

### Health Check
```bash
curl -X GET http://localhost:5001/api/health
```

### Agent Information
```bash
curl -X GET http://localhost:5001/api/agent/info \
  -H "Authorization: Bearer <your_jwt_token>"
```

## 📚 Documentation

- **[API Reference](API_REFERENCE.md)** - Complete API documentation with examples
- **[Codebase Overview](codebase.md)** - Detailed technical documentation

## 🛠️ Development

### Project Structure
- **Flask App** (`app.py`): Main application with all API endpoints
- **Services**: Business logic separated into focused modules
- **Agents**: AI agent implementation with LangChain tools
- **Tools**: Specialized functions for different capabilities

### Key Technologies
- **Flask**: Web framework
- **Firebase Firestore**: Database
- **LangChain**: AI agent framework
- **Google Gemini**: LLM for responses
- **JWT**: Authentication
- **bcrypt**: Password hashing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the [API Reference](API_REFERENCE.md)
2. Review the [Codebase Documentation](codebase.md)
3. Open an issue on GitHub

---

**Built with ❤️ for food lovers who want to eliminate decision fatigue!** 🍽️