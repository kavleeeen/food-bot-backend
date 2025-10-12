# Food Bot Codebase Context & Architecture

## Overview

This is a comprehensive food recommendation chatbot built with Flask, Firebase Firestore, and LangChain agents. The system helps Indian users make food decisions by providing personalized meal recommendations, recipes, and dietary preference management.

## Architecture Evolution

### Phase 1: Custom Orchestration (Original)
- **Manager Agent**: Custom orchestration with manual intent analysis
- **Direct LLM calls**: Manual routing and tool invocation
- **Simple memory**: In-memory chat history
- **Manual error handling**: Custom try-catch blocks

### Phase 2: LangGraph Agents (Current)
- **Enhanced LangGraph Agent**: Automatic tool selection and reasoning
- **Persistent memory**: Thread-based conversation tracking
- **Built-in error handling**: Automatic retry logic
- **Multi-step reasoning**: Iterative problem solving

## Project Structure

```
foodbot/
├── app.py                          # Main Flask API server
├── firebase_config.py              # Firebase initialization and database client
├── firebase.json                   # Firebase service account credentials
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── services/                       # Service layer architecture
│   ├── __init__.py
│   ├── auth_service.py            # JWT authentication service
│   ├── chat_service.py            # Chat orchestration service
│   ├── preference_service.py      # User preference management
│   └── agents/                    # AI agent implementations
│       ├── __init__.py
│       ├── manager_agent.py       # Original custom orchestration
│       ├── langgraph_agent.py     # Basic LangGraph implementation
│       ├── enhanced_langgraph_agent.py  # Advanced LangGraph with memory
│       └── tools/                 # LangChain tools
│           ├── __init__.py
│           ├── preference_tools.py    # Preference management tools
│           ├── recommendation_tools.py # Food recommendation tools
│           └── recipe_tools.py        # Recipe generation tools
├── data/                          # Data storage
│   └── recipes/                   # Recipe data (migrated to Firestore)
├── documentation/                 # API and implementation docs
│   ├── FRONTEND_API_GUIDE.md     # Frontend integration guide
│   ├── FRONTEND_PHASE2_GUIDE.md  # Phase 2 frontend guide
│   ├── API_REFERENCE.md          # Complete API documentation
│   └── diff.md                   # LangChain agents comparison
└── test_*.py                     # Test scripts
```

## Core Components

### 1. Flask API Server (`app.py`)

**Purpose**: Main entry point for the application, handles HTTP requests and routes them to appropriate services.

**Key Features**:
- JWT authentication middleware
- CORS support for frontend integration
- Error handling and logging
- Environment variable management

**API Endpoints**:
```python
# Authentication
POST /api/auth/register     # User registration
POST /api/auth/login        # User login
GET  /api/auth/profile      # Get user profile

# Chat & Recommendations
POST /api/chat              # Send message to AI agent
GET  /api/preferences       # Get user preferences
PUT  /api/preferences       # Update user preferences
```

**Dependencies**:
- Flask for web framework
- Firebase for database
- JWT for authentication
- LangChain for AI agents

### 2. Firebase Configuration (`firebase_config.py`)

**Purpose**: Manages Firebase initialization and provides database client.

**Key Features**:
- Service account authentication
- Database connection management
- Error handling for Firebase operations
- Thread-safe database access

**Database Structure**:
```
food-bot (Firestore Database)
├── users/                    # User accounts
│   └── {user_id}/
│       ├── email: string
│       ├── password_hash: string
│       ├── created_at: timestamp
│       └── preferences: object
└── recipes/                  # Recipe collection
    └── {recipe_id}/
        ├── name: string
        ├── cuisine: string
        ├── ingredients: array
        ├── instructions: string
        └── macros: object
```

### 3. Service Layer Architecture

#### Authentication Service (`auth_service.py`)

**Purpose**: Handles user authentication, registration, and JWT token management.

**Key Methods**:
```python
def hash_password(password: str) -> str
def verify_password(password: str, hashed: str) -> bool
def generate_token(user_id: str) -> str
def verify_token(token: str) -> dict
def register_user(email: str, password: str) -> dict
def login_user(email: str, password: str) -> dict
def get_user_profile(user_id: str) -> dict
```

**Security Features**:
- bcrypt password hashing
- JWT token with 30-day expiration
- Input validation and sanitization

#### Chat Service (`chat_service.py`)

**Purpose**: Orchestrates AI chat functionality using LangGraph agents.

**Key Methods**:
```python
def send_message(user_id: str, message: str) -> dict
def get_conversation_history(user_id: str) -> list
def clear_conversation_history(user_id: str) -> None
def get_agent_info() -> dict
```

**Architecture**:
- Uses Enhanced LangGraph Agent for AI processing
- Maintains conversation context
- Handles error recovery and logging

#### Preference Service (`preference_service.py`)

**Purpose**: Manages user food preferences and dietary restrictions.

**Key Methods**:
```python
def get_user_preferences(user_id: str) -> dict
def update_user_preferences(user_id: str, preferences: dict) -> bool
def add_preference(user_id: str, pref_type: str, value: str) -> bool
def get_missing_mandatory_preferences(preferences: dict) -> list
def has_complete_preferences(preferences: dict) -> bool
```

**Preference Schema**:
```json
{
  "restrictions": ["vegetarian", "vegan", "gluten-free"],
  "allergies": ["nuts", "dairy", "none"],
  "cuisine_preferences": ["indian", "italian", "chinese"],
  "spice_level": "medium",
  "custom_preferences": []
}
```

### 4. AI Agent Implementations

#### Manager Agent (`manager_agent.py`) - Original Implementation

**Purpose**: Custom orchestration approach with manual intent analysis and routing.

**Architecture**:
```python
class ManagerAgent:
    def __init__(self):
        self.llm = init_chat_model("gemini-2.5-flash")
        self.preference_service = PreferenceService()
    
    def process_message(self, user_id: str, message: str, chat_history: list):
        # 1. Analyze user intent
        intent = self._analyze_user_intent(message, preferences)
        
        # 2. Route to appropriate handler
        if intent == "preferences":
            return self._collect_preferences(user_id, message)
        elif intent == "recommendations":
            return self._handle_food_recommendations(message, preferences)
        elif intent == "recipe":
            return self._handle_recipe_request(message, preferences)
        else:
            return self._handle_general_chat(message)
```

**Limitations**:
- Manual intent analysis and routing
- Single-pass processing
- Basic error handling
- No persistent memory

#### Enhanced LangGraph Agent (`enhanced_langgraph_agent.py`) - Current Implementation

**Purpose**: Advanced agent using LangGraph framework with automatic tool selection and reasoning.

**Architecture**:
```python
class EnhancedFoodBotAgent:
    def __init__(self):
        self.llm = init_chat_model("gemini-2.5-flash")
        self.tools = [preference_tools, recommendation_tools, recipe_tools]
        self.agent = create_react_agent(self.llm, self.tools)
        self.agent_with_memory = RunnableWithMessageHistory(
            self.agent, self._get_session_history
        )
    
    def process_message(self, user_id: str, message: str, chat_history: list):
        # Automatic tool selection and execution
        result = self.agent_with_memory.invoke(input_data, config=config)
        return result["messages"][-1].content
```

**Advantages**:
- Automatic tool selection based on context
- Multi-step reasoning and iteration
- Persistent conversation memory
- Built-in error handling and retry logic
- Standardized LangChain patterns

### 5. LangChain Tools

#### Preference Tools (`preference_tools.py`)

**Purpose**: LangChain tools for managing user preferences.

**Tools**:
```python
@tool
def read_user_preferences(user_id: str) -> dict
@tool
def update_user_preferences(user_id: str, preferences: dict) -> bool
@tool
def add_single_preference(user_id: str, preference_type: str, value: str) -> bool
@tool
def check_missing_mandatory_preferences(preferences: dict) -> list
@tool
def has_complete_preferences(preferences: dict) -> bool
```

#### Recommendation Tools (`recommendation_tools.py`)

**Purpose**: Tools for generating food recommendations and detailed recipes.

**Tools**:
```python
@tool
def generate_food_recommendation(preferences: dict, user_message: str) -> str
@tool
def generate_detailed_recipe(food_name: str, preferences: dict) -> str
```

**Features**:
- Indian demographic targeting
- Nutritional balance focus
- Practical cooking advice
- Concise output (under 100 words)

#### Recipe Tools (`recipe_tools.py`)

**Purpose**: Specialized tools for recipe generation and variations.

**Tools**:
```python
@tool
def generate_detailed_recipe(meal_name: str, user_preferences: dict) -> str
@tool
def suggest_recipe_variations(meal_name: str, user_preferences: dict) -> str
```

**Features**:
- Step-by-step cooking instructions
- Ingredient quantities for 2-3 people
- Cooking time estimates
- Nutritional information
- Recipe variations (quick, healthy, fusion, seasonal)

## Data Flow

### 1. User Registration/Login Flow

```
User → POST /api/auth/register → AuthService → Firebase → JWT Token → User
```

### 2. Chat Message Flow

```
User → POST /api/chat → ChatService → LangGraph Agent → Tools → Firebase → Response
```

### 3. Preference Collection Flow

```
User Message → Intent Analysis → Preference Tools → Firebase → Updated Preferences
```

### 4. Recommendation Generation Flow

```
User Request → Preference Retrieval → Recommendation Tools → Gemini API → Formatted Response
```

## Key Features

### 1. Intelligent Intent Analysis

The system automatically detects user intent:
- **Preferences**: Dietary restrictions, allergies, cuisine preferences
- **Recommendations**: Food suggestions and meal ideas
- **Recipes**: Cooking instructions and recipe variations
- **Chat**: General conversation and greetings

### 2. Conversational Preference Collection

The agent collects user preferences through natural conversation:
- Asks for dietary restrictions first
- Collects allergy information
- Determines cuisine preferences
- Stores preferences in Firebase

### 3. Personalized Recommendations

Based on user preferences, the system provides:
- 3 meal suggestions per request
- Nutritional balance focus
- Indian demographic targeting
- Practical cooking advice

### 4. Recipe Generation

The system can generate:
- Detailed cooking instructions
- Ingredient lists with quantities
- Cooking time estimates
- Nutritional information
- Recipe variations

### 5. Memory and Context

The LangGraph agent maintains:
- Conversation history per user
- Context across multiple messages
- Preference state management
- Session-based memory

## Environment Configuration

### Required Environment Variables

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=food-recommend-39842
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=your_cert_url

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key

# Server Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Chat Endpoints

#### Send Message
```http
POST /api/chat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "message": "I want food recommendations"
}
```

### Preference Endpoints

#### Get Preferences
```http
GET /api/preferences
Authorization: Bearer <jwt_token>
```

#### Update Preferences
```http
PUT /api/preferences
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "restrictions": ["vegetarian"],
  "allergies": ["nuts"],
  "cuisine_preferences": ["indian", "italian"]
}
```

## Testing

### Test Scripts

1. **`test_langgraph_agent.py`**: Tests the LangGraph agent implementation
2. **`test_manager_agent.py`**: Tests the original manager agent
3. **`test_*.py`**: Various component tests

### Running Tests

```bash
# Test LangGraph agent
python test_langgraph_agent.py

# Test specific components
python -m pytest test_*.py
```

## Deployment Considerations

### Production Requirements

1. **Environment Variables**: All sensitive data in environment variables
2. **Database**: Firebase Firestore for production data
3. **Authentication**: JWT tokens with proper expiration
4. **Error Handling**: Comprehensive error logging and recovery
5. **Monitoring**: Application performance and error tracking

### Scaling Considerations

1. **Database**: Firebase Firestore scales automatically
2. **Memory**: LangGraph agent memory can be moved to Redis
3. **API**: Flask can be deployed with Gunicorn or similar
4. **Load Balancing**: Multiple instances can be deployed

## Future Enhancements

### Planned Features

1. **Advanced Memory**: Redis-based conversation storage
2. **User Profiles**: Extended user preference management
3. **Recipe Database**: Integration with external recipe APIs
4. **Nutritional Analysis**: Advanced macro and micronutrient tracking
5. **Meal Planning**: Weekly meal plan generation
6. **Shopping Lists**: Automatic ingredient list generation

### Technical Improvements

1. **Caching**: Redis caching for frequently accessed data
2. **Rate Limiting**: API rate limiting and throttling
3. **Monitoring**: Application performance monitoring
4. **Testing**: Comprehensive test coverage
5. **Documentation**: API documentation with Swagger/OpenAPI

## Migration from Custom Orchestration to LangGraph

### Benefits of Migration

1. **Reduced Complexity**: Single agent instead of custom orchestration
2. **Better Reliability**: Built-in error handling and retry logic
3. **Enhanced Capabilities**: Multi-step reasoning and iteration
4. **Improved Maintainability**: Standardized LangChain patterns
5. **Better User Experience**: Context-aware responses and memory

### Migration Steps

1. **Tool Migration**: Convert functions to LangChain tools
2. **Agent Implementation**: Create LangGraph agent with tools
3. **Memory Management**: Implement persistent conversation storage
4. **Testing**: Comprehensive testing of new implementation
5. **Deployment**: Gradual rollout with fallback options

## LangGraph Implementation: Step-by-Step Breakdown

### How LangGraph Works in This System

LangGraph is a framework that creates intelligent agents that can reason, use tools, and maintain memory. Here's exactly what happens when a user sends a message:

#### 1. Agent Initialization (`enhanced_langgraph_agent.py` lines 28-72)

```python
# Lines 28-38: Initialize the LLM (Gemini 2.5 Flash)
self.llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai",
    temperature=0.7,
    google_api_key=os.getenv('GEMINI_API_KEY')
)

# Lines 44-53: Define available tools
self.tools = [
    read_user_preferences,           # Tool 1: Read user preferences from database
    update_user_preferences,         # Tool 2: Update user preferences
    add_single_preference,           # Tool 3: Add single preference
    check_missing_mandatory_preferences, # Tool 4: Check what's missing
    has_complete_preferences,        # Tool 5: Check if complete
    generate_food_recommendation,    # Tool 6: Generate food suggestions
    generate_detailed_recipe,        # Tool 7: Create detailed recipes
    suggest_recipe_variations        # Tool 8: Suggest variations
]

# Lines 59-62: Create the ReAct agent
self.agent = create_react_agent(
    self.llm,    # The language model
    self.tools   # Available tools
)

# Lines 65-70: Add memory capability
self.agent_with_memory = RunnableWithMessageHistory(
    self.agent,                    # The base agent
    self._get_session_history,     # Memory function
    input_messages_key="messages",
    history_messages_key="chat_history"
)
```

#### 2. Message Processing Flow (`enhanced_langgraph_agent.py` lines 80-135)

When a user sends a message, here's the step-by-step process:

**Step 1: Message Reception (lines 80-85)**
```python
def process_message(self, user_id: str, message: str, chat_history: list = None):
    print(f"🤖 ENHANCED LANGGRAPH AGENT: Processing message for user {user_id}")
    print(f"📝 ENHANCED LANGGRAPH AGENT: Message: {message}")
```

**Step 2: System Context Creation (lines 86-103)**
```python
# Create system message with context
system_context = """You are a helpful food recommendation assistant designed specifically for Indian users. Your primary goal is to eliminate decision fatigue by providing simple, nutritious meal suggestions.

Key Principles:
1. SIMPLICITY FIRST: Recommend easy-to-make, everyday meals
2. NUTRITIONAL BALANCE: Focus on balanced meals with proper macros
3. INDIAN CONTEXT: Understand Indian food culture - both traditional and modern
4. DECISION FATIGUE: Make choices for users - don't overwhelm with options
5. PRACTICAL: Consider if the meal can be made at home or ordered easily
6. CRISP & MINIMAL: Keep responses short, direct, and to the point

You have access to tools for:
- Reading and updating user preferences
- Generating food recommendations
- Creating detailed recipes
- Suggesting recipe variations

Always use the appropriate tools based on what the user is asking for."""
```

**Step 3: Input Preparation (lines 105-111)**
```python
# Prepare input for the agent
input_data = {
    "messages": [
        SystemMessage(content=system_context),  # System instructions
        HumanMessage(content=message)           # User's message
    ]
}
```

**Step 4: Memory Configuration (lines 113-116)**
```python
# Configuration for memory
config = RunnableConfig(
    configurable={"session_id": user_id}  # Each user gets their own memory session
)
```

**Step 5: Agent Execution (lines 118-120)**
```python
# Execute the agent with memory
print("🚀 ENHANCED LANGGRAPH AGENT: Executing agent with memory...")
result = self.agent_with_memory.invoke(input_data, config=config)
```

#### 3. LangGraph's ReAct Pattern (Automatic Tool Selection)

LangGraph uses the ReAct (Reasoning + Acting) pattern. Here's what happens internally:

1. **Reasoning**: The LLM analyzes the user's message and decides what tools to use
2. **Acting**: The agent calls the appropriate tools
3. **Observing**: The agent sees the tool results
4. **Iterating**: If needed, it calls more tools or provides a final response

**Example Flow:**
- User: "I want food recommendations"
- Agent thinks: "I need to check user preferences first, then generate recommendations"
- Agent calls: `read_user_preferences(user_id)`
- Agent gets: `{"restrictions": ["vegetarian"], "allergies": ["nuts"]}`
- Agent calls: `generate_food_recommendation(preferences, user_message)`
- Agent gets: "3 vegetarian meal suggestions"
- Agent responds: "Here are 3 great vegetarian options..."

#### 4. Memory Management (`enhanced_langgraph_agent.py` lines 74-78)

```python
def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
    """Get or create chat history for a session"""
    if session_id not in self.memory_store:
        self.memory_store[session_id] = ChatMessageHistory()  # Create new memory
    return self.memory_store[session_id]  # Return existing memory
```

**Memory Features:**
- Each user gets their own conversation memory
- Previous messages are automatically included in context
- Agent can reference earlier parts of the conversation
- Memory persists across multiple API calls

#### 5. Tool Execution Examples

**Preference Tool (`preference_tools.py` lines 10-16):**
```python
@tool
def read_user_preferences(user_id: str) -> dict:
    """Read user's current food preferences from database"""
    print(f"🔧 PREFERENCE TOOL: Reading preferences for user {user_id}")
    result = preference_service.get_user_preferences(user_id)
    print(f"📊 PREFERENCE TOOL: Retrieved preferences: {result}")
    return result
```

**Recommendation Tool (`recommendation_tools.py` lines 17-57):**
```python
@tool
def generate_food_recommendation(preferences: dict, user_message: str = "") -> str:
    """Generate food recommendations based on user preferences and context"""
    # Creates context from preferences
    context = f"User preferences: {preferences}\n"
    if user_message:
        context += f"User message: {user_message}\n"
    
    # Sends detailed prompt to Gemini
    prompt = f"""You are a food recommendation assistant for Indian users..."""
    
    # Gets response from Gemini
    response = model.invoke(prompt)
    return response.content
```

#### 6. Response Extraction (`enhanced_langgraph_agent.py` lines 122-129)

```python
# Extract response
if "messages" in result and result["messages"]:
    response = result["messages"][-1].content  # Get the last message (AI response)
    print(f"📤 ENHANCED LANGGRAPH AGENT: Response: {response}")
    return response
else:
    print("⚠️ ENHANCED LANGGRAPH AGENT: No response generated")
    return "I'm having trouble processing your request. Please try again."
```

### Key Advantages of LangGraph Implementation

1. **Automatic Tool Selection**: No manual routing - the agent decides which tools to use
2. **Multi-step Reasoning**: Can call multiple tools in sequence
3. **Memory Persistence**: Remembers conversation context
4. **Error Handling**: Built-in retry logic and error recovery
5. **Standardized Patterns**: Uses LangChain's proven patterns

### Memory and Context Flow

```
User Message → System Context + User Message → LangGraph Agent
     ↓
Agent analyzes message and decides on tools
     ↓
Agent calls tools (e.g., read_user_preferences)
     ↓
Tools return data (e.g., user preferences)
     ↓
Agent calls more tools if needed (e.g., generate_food_recommendation)
     ↓
Agent gets final tool result
     ↓
Agent formats response using LLM
     ↓
Response sent back to user
     ↓
Conversation stored in memory for next interaction
```

## Conclusion

The food bot codebase represents a modern, scalable approach to AI-powered food recommendations. The migration from custom orchestration to LangGraph agents provides significant improvements in reliability, maintainability, and user experience. The modular architecture allows for easy extension and customization while maintaining clean separation of concerns.

The system successfully addresses the core problem of decision fatigue in food choices by providing personalized, context-aware recommendations through natural conversation, making it an effective solution for Indian users seeking quick, nutritious meal decisions.
