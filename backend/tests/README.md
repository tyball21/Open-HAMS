# Open HAMS Backend Tests

This directory contains diagnostic and validation tests for the Open HAMS backend system.

## Purpose

These tests were originally created to debug a persistent 422 "Unprocessable Entity" error when creating animals through the API. The issue was traced to incorrect use of `Animal.model_validate()` on `AnimalIn` data, which was missing required fields like `id`, `created_at`, and `updated_at`.

## Test Files

### `test_database_schema.py`
- **Purpose**: Validates that the database schema matches expectations
- **Use Cases**: 
  - Debugging database migration issues
  - Verifying schema after database changes
  - Ensuring required reference data exists (like zoos)
- **Run**: `python tests/test_database_schema.py`

### `test_animal_model.py`
- **Purpose**: Tests animal model creation and database operations
- **Use Cases**:
  - Verifying the AnimalIn → Animal conversion works correctly
  - Testing full database lifecycle (create, save, delete)
  - Catching model validation issues before they cause API errors
- **Run**: `python tests/test_animal_model.py`

## Key Lessons Learned

1. **Model Validation Issue**: Never use `Animal.model_validate(animal_in_data)` - use `Animal(**animal_in_data.model_dump())` instead
2. **Optional Fields**: Frontend should only send optional fields when they have meaningful values
3. **Database Type Matters**: The system uses PostgreSQL, not SQLite (important for debugging queries)

## Running Tests

### Individual Tests
```bash
# From the backend directory
python tests/test_database_schema.py
python tests/test_animal_model.py
```

### All Tests
```bash
# Run both diagnostic tests
python -c "
from tests.test_database_schema import print_database_info
from tests.test_animal_model import run_animal_model_tests
print_database_info()
print()
run_animal_model_tests()
"
```

## Integration with Development

These tests are particularly useful:
- **Before major database migrations**: Run schema validation
- **After model changes**: Verify animal creation still works
- **When debugging API 422 errors**: Check if the issue is at the model level
- **For new contributors**: Understand how the animal models should work

## Future Enhancements

Consider expanding these tests to:
- Test other models (Event, User, etc.)
- Add proper pytest integration
- Create automated CI/CD checks
- Add performance benchmarks for database operations 