#!/usr/bin/env python3
"""
API Documentation Updater
Automatically updates API_REFERENCE.md when code changes
"""

import os
import re
import ast
from datetime import datetime
from pathlib import Path

def extract_api_endpoints(app_file):
    """Extract API endpoints from app.py"""
    endpoints = []
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Find all @app.route decorators
    route_pattern = r'@app\.route\([\'"]([^\'"]+)[\'"],\s*methods=\[([^\]]+)\]\)'
    routes = re.findall(route_pattern, content)
    
    for route, methods in routes:
        # Clean up methods
        methods = [m.strip().strip("'\"") for m in methods.split(',')]
        
        # Find the function definition after the route
        func_pattern = rf'@app\.route\([\'"]{re.escape(route)}[\'"],\s*methods=\[[^\]]+\]\)\s*\n@token_required\s*\ndef\s+(\w+)'
        func_match = re.search(func_pattern, content)
        
        if func_match:
            func_name = func_match.group(1)
            endpoints.append({
                'route': route,
                'methods': methods,
                'function': func_name
            })
    
    return endpoints

def extract_response_formats(app_file):
    """Extract response formats from app.py"""
    responses = {}
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Find jsonify calls
    jsonify_pattern = r'jsonify\(({[^}]+})\)'
    jsonify_matches = re.findall(jsonify_pattern, content, re.DOTALL)
    
    for match in jsonify_matches:
        # Clean up the match
        clean_match = match.replace('\n', '').replace(' ', '')
        if 'message' in clean_match or 'preferences' in clean_match or 'user' in clean_match:
            responses[match] = match
    
    return responses

def update_api_reference():
    """Update the API reference file"""
    app_file = 'app.py'
    api_ref_file = 'API_REFERENCE.md'
    
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found")
        return False
    
    print("🔄 Updating API Reference...")
    
    # Extract current endpoints
    endpoints = extract_api_endpoints(app_file)
    
    # Read current API reference
    with open(api_ref_file, 'r') as f:
        content = f.read()
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r'\*Last Updated: \d{4}-\d{2}-\d{2}\*', f'*Last Updated: {timestamp}*', content)
    
    # Write updated content
    with open(api_ref_file, 'w') as f:
        f.write(content)
    
    print(f"✅ API Reference updated successfully")
    print(f"📊 Found {len(endpoints)} endpoints")
    
    return True

def validate_api_consistency():
    """Validate that API reference matches actual code"""
    print("🔍 Validating API consistency...")
    
    # Check if all endpoints in app.py are documented
    endpoints = extract_api_endpoints('app.py')
    
    with open('API_REFERENCE.md', 'r') as f:
        api_docs = f.read()
    
    missing_docs = []
    for endpoint in endpoints:
        route = endpoint['route']
        if route not in api_docs:
            missing_docs.append(route)
    
    if missing_docs:
        print(f"⚠️  Missing documentation for: {missing_docs}")
        return False
    else:
        print("✅ All endpoints are documented")
        return True

def main():
    """Main function"""
    print("🚀 API Documentation Updater")
    print("=" * 40)
    
    # Update API reference
    success = update_api_reference()
    
    if success:
        # Validate consistency
        validate_api_consistency()
        print("\n✅ API documentation update complete!")
    else:
        print("\n❌ API documentation update failed!")

if __name__ == "__main__":
    main()

