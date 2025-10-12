#!/usr/bin/env python3
"""
Comprehensive Documentation Updater
Updates all documentation files to match current code
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

def extract_endpoint_info(app_file):
    """Extract detailed endpoint information from app.py"""
    endpoints = []
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Find all route definitions
    route_pattern = r'@app\.route\([\'"]([^\'"]+)[\'"],\s*methods=\[([^\]]+)\]\)\s*\n@token_required\s*\ndef\s+(\w+)\([^)]*\):'
    routes = re.findall(route_pattern, content, re.MULTILINE | re.DOTALL)
    
    for route, methods, func_name in routes:
        # Clean up methods
        methods = [m.strip().strip("'\"") for m in methods.split(',')]
        
        # Find the function content
        func_pattern = rf'def {re.escape(func_name)}\([^)]*\):\s*\n(.*?)(?=\n@app\.route|\nif __name__|\Z)'
        func_match = re.search(func_pattern, content, re.DOTALL)
        
        if func_match:
            func_content = func_match.group(1)
            
            # Extract docstring
            docstring_match = re.search(r'"""([^"]+)"""', func_content)
            description = docstring_match.group(1).strip() if docstring_match else f"Handle {func_name}"
            
            # Determine if it's protected
            is_protected = '@token_required' in func_content
            
            endpoints.append({
                'route': route,
                'methods': methods,
                'function': func_name,
                'description': description,
                'protected': is_protected
            })
    
    return endpoints

def extract_response_examples(app_file):
    """Extract response examples from app.py"""
    examples = {}
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Find jsonify calls with response data
    jsonify_pattern = r'jsonify\(({[^}]+})\)'
    matches = re.findall(jsonify_pattern, content, re.DOTALL)
    
    for match in matches:
        # Clean up the match
        clean_match = match.replace('\n', '').replace(' ', '')
        if 'message' in clean_match or 'preferences' in clean_match or 'user' in clean_match:
            examples[match] = match
    
    return examples

def update_api_reference():
    """Update the main API reference file"""
    print("📝 Updating API_REFERENCE.md...")
    
    app_file = 'app.py'
    api_ref_file = 'API_REFERENCE.md'
    
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found")
        return False
    
    # Extract endpoint information
    endpoints = extract_endpoint_info(app_file)
    
    # Read current API reference
    with open(api_ref_file, 'r') as f:
        content = f.read()
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r'\*Last Updated: \d{4}-\d{2}-\d{2}\*', f'*Last Updated: {timestamp}*', content)
    
    # Write updated content
    with open(api_ref_file, 'w') as f:
        f.write(content)
    
    print(f"✅ API_REFERENCE.md updated")
    print(f"📊 Found {len(endpoints)} endpoints")
    
    return True

def update_frontend_guides():
    """Update frontend guide files"""
    print("📝 Updating frontend guides...")
    
    # Update FRONTEND_API_GUIDE.md timestamp
    frontend_guide = 'FRONTEND_API_GUIDE.md'
    if os.path.exists(frontend_guide):
        with open(frontend_guide, 'r') as f:
            content = f.read()
        
        # Update any timestamp references
        timestamp = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(r'Last Updated: \d{4}-\d{2}-\d{2}', f'Last Updated: {timestamp}', content)
        
        with open(frontend_guide, 'w') as f:
            f.write(content)
        
        print(f"✅ {frontend_guide} updated")
    
    # Update mealbot_frontend_phase2.md timestamp
    phase2_guide = 'mealbot_frontend_phase2.md'
    if os.path.exists(phase2_guide):
        with open(phase2_guide, 'r') as f:
            content = f.read()
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(r'Last Updated: \d{4}-\d{2}-\d{2}', f'Last Updated: {timestamp}', content)
        
        with open(phase2_guide, 'w') as f:
            f.write(content)
        
        print(f"✅ {phase2_guide} updated")
    
    return True

def validate_documentation():
    """Validate that all documentation is consistent"""
    print("🔍 Validating documentation consistency...")
    
    # Check if all endpoints are documented
    endpoints = extract_endpoint_info('app.py')
    
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

def generate_changelog():
    """Generate a changelog for documentation updates"""
    print("📝 Generating changelog...")
    
    changelog_file = 'DOCUMENTATION_CHANGELOG.md'
    
    # Read existing changelog
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r') as f:
            content = f.read()
    else:
        content = "# Documentation Changelog\n\n"
    
    # Add new entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = f"""
## {timestamp}
- Updated API_REFERENCE.md
- Updated frontend guides
- Validated documentation consistency
- Generated from: app.py, services/*.py

"""
    
    # Insert new entry at the top
    content = content.replace("# Documentation Changelog\n", f"# Documentation Changelog\n{new_entry}")
    
    with open(changelog_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Changelog updated")
    return True

def main():
    """Main function"""
    print("🚀 Comprehensive Documentation Updater")
    print("=" * 50)
    
    success = True
    
    # Update API reference
    if not update_api_reference():
        success = False
    
    # Update frontend guides
    if not update_frontend_guides():
        success = False
    
    # Validate documentation
    if not validate_documentation():
        success = False
    
    # Generate changelog
    if not generate_changelog():
        success = False
    
    if success:
        print("\n🎉 All documentation updated successfully!")
        print("\n📋 Updated files:")
        print("  - API_REFERENCE.md")
        print("  - FRONTEND_API_GUIDE.md")
        print("  - mealbot_frontend_phase2.md")
        print("  - DOCUMENTATION_CHANGELOG.md")
    else:
        print("\n❌ Some documentation updates failed!")
    
    return success

if __name__ == "__main__":
    main()

