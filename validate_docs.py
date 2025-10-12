#!/usr/bin/env python3
"""
Documentation Validator
Validates that all documentation is current and consistent
"""

import os
import re
from datetime import datetime

def check_api_endpoints():
    """Check if all API endpoints are documented"""
    print("🔍 Checking API endpoints...")
    
    # Extract endpoints from app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find all route definitions
    route_pattern = r'@app\.route\([\'"]([^\'"]+)[\'"],\s*methods=\[([^\]]+)\]\)'
    routes = re.findall(route_pattern, content)
    
    endpoints = []
    for route, methods in routes:
        methods = [m.strip().strip("'\"") for m in methods.split(',')]
        endpoints.append((route, methods))
    
    # Check if all endpoints are in API_REFERENCE.md
    with open('API_REFERENCE.md', 'r') as f:
        api_docs = f.read()
    
    missing = []
    for route, methods in endpoints:
        if route not in api_docs:
            missing.append((route, methods))
    
    if missing:
        print(f"❌ Missing documentation for {len(missing)} endpoints:")
        for route, methods in missing:
            print(f"  - {methods[0]} {route}")
        return False
    else:
        print(f"✅ All {len(endpoints)} endpoints are documented")
        return True

def check_response_formats():
    """Check if response formats are documented"""
    print("🔍 Checking response formats...")
    
    # This is a basic check - in a real implementation, you'd parse the actual responses
    with open('API_REFERENCE.md', 'r') as f:
        content = f.read()
    
    # Check for common response patterns
    required_patterns = [
        r'"message":\s*"string"',
        r'"timestamp":\s*"string \(ISO 8601\)"',
        r'"error":\s*"string"'
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if not re.search(pattern, content):
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"❌ Missing response format patterns: {missing_patterns}")
        return False
    else:
        print("✅ Response formats are properly documented")
        return True

def check_examples():
    """Check if examples are present"""
    print("🔍 Checking examples...")
    
    with open('API_REFERENCE.md', 'r') as f:
        content = f.read()
    
    # Check for cURL examples
    curl_examples = re.findall(r'```bash\ncurl[^`]+```', content)
    
    if len(curl_examples) < 5:  # Should have at least 5 examples
        print(f"❌ Only {len(curl_examples)} cURL examples found, expected at least 5")
        return False
    else:
        print(f"✅ Found {len(curl_examples)} cURL examples")
        return True

def check_timestamps():
    """Check if documentation is recent"""
    print("🔍 Checking timestamps...")
    
    with open('API_REFERENCE.md', 'r') as f:
        content = f.read()
    
    # Extract last updated date
    timestamp_match = re.search(r'\*Last Updated: (\d{4}-\d{2}-\d{2})\*', content)
    
    if not timestamp_match:
        print("❌ No timestamp found in API_REFERENCE.md")
        return False
    
    last_updated = timestamp_match.group(1)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if last_updated != today:
        print(f"⚠️  Documentation last updated on {last_updated}, today is {today}")
        print("   Consider running: python update_docs.py")
        return False
    else:
        print(f"✅ Documentation is current (updated {last_updated})")
        return True

def main():
    """Main validation function"""
    print("🚀 Documentation Validator")
    print("=" * 40)
    
    checks = [
        ("API Endpoints", check_api_endpoints),
        ("Response Formats", check_response_formats),
        ("Examples", check_examples),
        ("Timestamps", check_timestamps)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 {name}")
        if check_func():
            passed += 1
        else:
            print(f"❌ {name} check failed")
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All documentation checks passed!")
        return True
    else:
        print("⚠️  Some documentation checks failed!")
        print("\n💡 To fix issues, run:")
        print("   python update_docs.py")
        return False

if __name__ == "__main__":
    main()

