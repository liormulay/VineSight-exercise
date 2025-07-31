# Automated Integration Test

This directory contains an automated integration test that validates the `/stats` endpoint functionality with a fresh database and mock data.

## Test Overview

The test performs the following steps:

1. **Bootstraps a fresh database** - Creates a temporary SQLite database for testing
2. **Loads mock data** - Imports data from `mock_posts.csv` into the database
3. **Sends a request** - Makes a GET request to the `/stats` endpoint
4. **Verifies the response** - Validates the response structure and specific values

## Files

- `tests/test_integration.py` - The main integration test
- `run_tests.py` - Simple test runner script
- `pytest.ini` - Pytest configuration
- `mock_posts.csv` - Mock data used by the test

## Running the Test

### Option 1: Using the test runner script
```bash
python run_tests.py
```

### Option 2: Using pytest directly
```bash
# Run the specific test
python -m pytest tests/test_integration.py::TestIntegration::test_stats_endpoint_with_mock_data -v

# Run all tests
python -m pytest tests/ -v
```

### Option 3: Using pytest with more output
```bash
python -m pytest tests/test_integration.py::TestIntegration::test_stats_endpoint_with_mock_data -v -s
```

## Test Details

### What the test validates:

1. **Response Structure**
   - Returns HTTP 200 status
   - Contains a `topics` array
   - Each topic has `topic`, `posts_count`, `total_likes`, `total_shares`, `total_comments` fields

2. **Data Integrity**
   - All expected topics are present (health, finance, news, sports, tech)
   - All numeric values are non-negative
   - Post counts are positive and reasonable

3. **Specific Values** (based on mock data)
   - **Health**: 4 posts, 28 likes, 22 shares, 29 comments
   - Other topics are validated for structure but not specific values

### Test Features:

- **Isolated Database**: Uses a temporary database file that's cleaned up after the test
- **Fresh Data**: Clears existing data and loads fresh mock data for each test run
- **Error Handling**: Gracefully handles file cleanup on Windows
- **Detailed Output**: Shows actual response values for debugging

## Mock Data

The test uses `mock_posts.csv` which contains 50 records with the following structure:
- `post_id`: Unique post identifier
- `topic`: Category (health, finance, news, sports, tech)
- `likes`, `shares`, `comments`: Engagement metrics (some values are -1 indicating missing data)
- `version`: Post version number
- `timestamp`: When the post was created

## Dependencies

The test requires the following packages (already in `requirements.txt`):
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for testing
- `fastapi` - Web framework
- `sqlalchemy` - Database ORM
- `pandas` - CSV data processing

## Troubleshooting

### Common Issues:

1. **Permission Error**: The test creates temporary files. If you see permission errors, the test will continue and clean up on the next run.

2. **Database Lock**: If the database is locked, the test will retry or skip cleanup.

3. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Debugging:

To see detailed output including the actual response values:
```bash
python -m pytest tests/test_integration.py::TestIntegration::test_stats_endpoint_with_mock_data -v -s
```

## Expected Output

When the test passes, you should see output similar to:
```
Loading data from /tmp/temp.csv...
Clearing existing data...
Reading CSV file...
Found 50 records to process
Inserting data into database...
Successfully loaded 50 records into database

Actual response values:
news: 8 posts, likes: 204, shares: 88, comments: 24
finance: 7 posts, likes: 294, shares: 96, comments: 9
health: 4 posts, likes: 28, shares: 22, comments: 29
sports: 5 posts, likes: 55, shares: 77, comments: 39
tech: 6 posts, likes: 114, shares: 81, comments: 26
PASSED
``` 