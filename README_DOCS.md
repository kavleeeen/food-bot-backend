# 📚 Documentation Management

## Overview
This project includes comprehensive API documentation that is automatically maintained and updated.

## 📋 Documentation Files

### 1. **API_REFERENCE.md** - Complete API Documentation
- **Purpose**: Comprehensive API reference with all endpoints, request/response formats, and examples
- **Content**: All API endpoints, data models, error handling, cURL examples
- **Updated**: Automatically when code changes

### 2. **FRONTEND_API_GUIDE.md** - Frontend Integration Guide
- **Purpose**: Guide for frontend developers to integrate with the API
- **Content**: Basic API endpoints, authentication flow, implementation guidelines
- **Updated**: Automatically when code changes

### 3. **mealbot_frontend_phase2.md** - Phase 2 Frontend Guide
- **Purpose**: Enhanced frontend guide for Phase 2 features
- **Content**: AI agent system, preference management, conversational features
- **Updated**: Automatically when code changes

### 4. **FRONTEND_PHASE2_GUIDE.md** - Comprehensive Frontend Guide
- **Purpose**: Complete frontend implementation guide for Phase 2
- **Content**: UI/UX design, component architecture, state management, testing
- **Updated**: Manually when needed

### 5. **TOOL_TEST_REPORT.md** - Testing Documentation
- **Purpose**: Comprehensive test results and validation
- **Content**: Test results, performance metrics, production readiness
- **Updated**: When tests are run

## 🔄 Automatic Updates

### Git Hooks
- **Pre-commit Hook**: Automatically updates documentation before each commit
- **Location**: `.git/hooks/pre-commit`
- **Function**: Runs `update_api_docs.py` and adds updated files to commit

### Manual Updates
```bash
# Update all documentation
python update_docs.py

# Update only API reference
python update_api_docs.py
```

## 📝 Documentation Standards

### API Documentation Format
```markdown
### X. Endpoint Name
**Endpoint:** `METHOD /path`

**Description:** Brief description

**Request Body:**
```json
{
  "field": "type"
}
```

**Success Response (200):**
```json
{
  "field": "value"
}
```

**Error Responses:**
- `400` - Description
- `500` - Description

**Example cURL:**
```bash
curl -X METHOD http://localhost:5003/path
```
```

### Response Format Standards
- **Success Responses**: Always include relevant data and timestamp
- **Error Responses**: Always include error message
- **Consistent Structure**: All responses follow the same pattern
- **Type Information**: Clear data types for all fields

## 🚀 Keeping Documentation Updated

### Automatic Updates
1. **Git Hooks**: Documentation updates automatically on commit
2. **CI/CD**: Can be integrated into continuous integration
3. **Monitoring**: Scripts validate consistency

### Manual Updates
1. **Run Update Script**: `python update_docs.py`
2. **Validate Changes**: Check that all endpoints are documented
3. **Review Changes**: Ensure accuracy and completeness

### When to Update
- **New Endpoints**: Add new API endpoints
- **Response Changes**: Modify response formats
- **Error Handling**: Update error responses
- **Authentication**: Change auth requirements
- **Data Models**: Update data structures

## 🔍 Validation

### Consistency Checks
- All endpoints in code are documented
- Response formats match actual code
- Error codes are accurate
- Examples are working

### Quality Checks
- Clear descriptions
- Complete examples
- Proper formatting
- Up-to-date timestamps

## 📊 Documentation Status

| File | Status | Last Updated | Auto-Updated |
|------|--------|--------------|--------------|
| API_REFERENCE.md | ✅ Current | 2025-10-11 | ✅ Yes |
| FRONTEND_API_GUIDE.md | ✅ Current | 2025-10-11 | ✅ Yes |
| mealbot_frontend_phase2.md | ✅ Current | 2025-10-11 | ✅ Yes |
| FRONTEND_PHASE2_GUIDE.md | ✅ Current | 2025-10-11 | ❌ Manual |
| TOOL_TEST_REPORT.md | ✅ Current | 2025-10-11 | ❌ Manual |

## 🛠️ Tools

### Update Scripts
- **`update_docs.py`**: Comprehensive documentation updater
- **`update_api_docs.py`**: API reference specific updater
- **Git Hooks**: Automatic pre-commit updates

### Validation
- **Consistency Checks**: Ensures all endpoints are documented
- **Format Validation**: Validates markdown formatting
- **Example Testing**: Validates cURL examples

## 📞 Support

### Documentation Issues
- Check `DOCUMENTATION_CHANGELOG.md` for recent changes
- Run `python update_docs.py` to refresh all documentation
- Validate with `python update_docs.py` for consistency checks

### Adding New Documentation
1. Update the relevant markdown file
2. Run `python update_docs.py` to validate
3. Commit changes (automatic updates will run)

---

**Note**: This documentation system ensures that API documentation is always up-to-date and accurate. The automatic update system prevents documentation drift and maintains consistency across all files.

