#!/usr/bin/env python3
"""
Test script for LangGraph Agent implementation
"""

import os
from dotenv import load_dotenv
from services.agents.enhanced_langgraph_agent import EnhancedFoodBotAgent

# Load environment variables
load_dotenv()

def test_langgraph_agent():
    """Test the Enhanced LangGraph Agent"""
    try:
        print("🧪 TESTING: Creating Enhanced LangGraph Agent...")
        agent = EnhancedFoodBotAgent()
        print("✅ Agent created successfully")
        
        # Test cases
        test_cases = [
            "I am hungry and want something healthy",
            "I want food recommendations",
            "I am vegetarian and like Indian food",
            "How to make dal chawal?",
            "Can you give me variations for biryani?"
        ]
        
        for i, message in enumerate(test_cases, 1):
            print(f"\n🧪 TEST {i}: '{message}'")
            result = agent.process_message(
                user_id="test_user_123",
                message=message,
                chat_history=[]
            )
            print(f"📤 RESULT: {result[:200]}...")
        
        # Test agent info
        print(f"\n📊 AGENT INFO: {agent.get_agent_info()}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_langgraph_agent()

