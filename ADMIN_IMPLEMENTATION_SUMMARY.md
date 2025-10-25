# Administrator Role Implementation - CRUD Tests + Questions

## Overview
Complete implementation of the Administrator role for the Sirius Career Platform, following DDD architecture with separate domains. This implementation provides full CRUD operations for tests and questions management.

## File Structure Created

```
api/app/domains/
├── __init__.py
└── admin/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   ├── test.py          # Test SQLAlchemy model
    │   └── question.py      # Question SQLAlchemy model
    ├── schemas/
    │   ├── __init__.py
    │   ├── test.py          # Test Pydantic schemas
    │   └── question.py      # Question Pydantic schemas
    ├── repositories/
    │   ├── __init__.py
    │   ├── test_repository.py      # Test data access layer
    │   └── question_repository.py  # Question data access layer
    ├── services/
    │   ├── __init__.py
    │   └── test_service.py         # Test business logic
    └── routers/
        ├── __init__.py
        └── admin_tests.py          # FastAPI endpoints

api/alembic/versions/
└── 001_create_tests_and_questions_tables.py  # Database migration
```

## Key Components

### 1. Database Models

**Test Model (`test.py`):**
- Fields: `id`, `slug` (unique), `name`, `description`, `is_active`, `created_at`, `updated_at`
- Relationships: one-to-many with Question
- Indexes: slug, is_active for performance

**Question Model (`question.py`):**
- Fields: `id`, `test_id` (FK), `text`, `order`, `type`, `config` (JSON), `created_at`, `updated_at`
- Relationships: many-to-one with Test
- Indexes: test_id, composite (test_id, order)

### 2. Pydantic Schemas

**Request Schemas:**
- `TestCreate`: slug, name, description, is_active, questions[]
- `TestUpdate`: name?, description?, is_active?, questions?[]
- `QuestionCreate`: text, order, type, config
- `QuestionUpdate`: text?, order?, type?, config?

**Response Schemas:**
- `TestListResponse`: id, slug, name, is_active, timestamps
- `TestDetailResponse`: full test data with nested questions
- `QuestionResponse`: complete question data

**Validation Features:**
- Slug format validation (alphanumeric + hyphens/underscores)
- Question order validation (unique and sequential)
- Question type validation (likert_scale, binary_choice, multiple_choice, text_input)
- Config validation based on question type

### 3. Repository Layer

**TestRepository:**
- `get_all()`, `get_by_slug()`, `get_by_id()`
- `create()`, `update()`, `delete()`
- `exists_by_slug()`, `has_completed_results()`
- `get_active_tests()`, `get_inactive_tests()`

**QuestionRepository:**
- `get_by_test_id()`, `get_by_id()`
- `create()`, `create_bulk()`, `update()`, `delete()`
- `delete_by_test_id()`, `exists_by_test_and_order()`

### 4. Service Layer

**TestService:**
- Business logic for test operations
- Transaction management
- Validation of business rules
- Error handling with custom exceptions

**Key Business Rules:**
- Slug uniqueness validation
- Question order validation (sequential, no gaps)
- Integrity protection (cannot delete tests with results)
- Config validation per question type

### 5. API Endpoints

**Admin Tests Router (`/admin/tests`):**
```
GET    /admin/tests              # List all tests
POST   /admin/tests              # Create test + questions
GET    /admin/tests/{slug}       # Get test details
PUT    /admin/tests/{slug}       # Update test
DELETE /admin/tests/{slug}       # Delete test
GET    /admin/tests/active/      # List active tests
GET    /admin/tests/inactive/    # List inactive tests
```

**Authentication:**
- Mock authentication via `X-User-ID` header
- All endpoints require admin authentication

### 6. Error Handling

**Custom Exceptions:**
- `TestNotFoundException` (404)
- `TestSlugAlreadyExistsException` (409)
- `TestHasResultsException` (409)
- `InvalidQuestionConfigException` (422)
- `InvalidQuestionOrderException` (422)

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 204: Deleted
- 404: Not Found
- 409: Conflict (slug exists, has results)
- 422: Validation Error

### 7. Database Migration

**Migration File:** `001_create_tests_and_questions_tables.py`
- Creates `tests` table with proper indexes
- Creates `questions` table with foreign key constraints
- Includes proper indexes for performance
- Supports rollback

## Question Types Supported

### 1. Likert Scale
```json
{
  "type": "likert_scale",
  "config": {
    "scale": "openness",
    "min_value": 1,
    "max_value": 5,
    "reverse": false
  }
}
```

### 2. Binary Choice
```json
{
  "type": "binary_choice",
  "config": {
    "option_a": "Extraverted",
    "option_b": "Introverted"
  }
}
```

### 3. Multiple Choice
```json
{
  "type": "multiple_choice",
  "config": {
    "options": ["Option 1", "Option 2", "Option 3"]
  }
}
```

### 4. Text Input
```json
{
  "type": "text_input",
  "config": {}
}
```

## Usage Examples

### Create a Test
```bash
curl -X POST "http://localhost:8000/admin/tests" \
  -H "X-User-ID: admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "big-five",
    "name": "Big Five Personality Test",
    "description": "Test for measuring personality traits",
    "is_active": true,
    "questions": [
      {
        "text": "I am outgoing and social",
        "order": 0,
        "type": "likert_scale",
        "config": {
          "scale": "extraversion",
          "min_value": 1,
          "max_value": 5
        }
      }
    ]
  }'
```

### Get Test Details
```bash
curl -X GET "http://localhost:8000/admin/tests/big-five" \
  -H "X-User-ID: admin123"
```

### Update Test
```bash
curl -X PUT "http://localhost:8000/admin/tests/big-five" \
  -H "X-User-ID: admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Big Five Test",
    "is_active": false
  }'
```

## Integration Notes

1. **Main App Integration:** Admin router is included in `main.py`
2. **Database:** Uses existing SQLAlchemy setup with proper session management
3. **CORS:** Inherits CORS settings from main app
4. **Error Handling:** Integrates with existing exception handling
5. **Validation:** Uses Pydantic v2 for request/response validation

## Future Extensions

1. **TestResult Integration:** When TestResult model is created, update `has_completed_results()` method
2. **Question CRUD:** Add individual question management endpoints if needed
3. **Bulk Operations:** Add bulk import/export functionality
4. **Audit Logging:** Add audit trail for test modifications
5. **Permissions:** Extend authentication to support role-based permissions

## Testing Recommendations

1. **Unit Tests:** Test service layer business logic
2. **Integration Tests:** Test repository layer with database
3. **API Tests:** Test all endpoints with various scenarios
4. **Validation Tests:** Test all validation rules
5. **Error Tests:** Test all error conditions and status codes

This implementation provides a solid foundation for the Administrator role with full CRUD functionality for tests and questions, following DDD principles and FastAPI best practices.

