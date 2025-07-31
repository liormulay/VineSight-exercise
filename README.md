# VineSight Exercise

A FastAPI application for the VineSight exercise that provides analytics on post data.

## Features

- FastAPI framework with SQLAlchemy ORM
- SQLite database for data storage
- `/stats` endpoint for topic analytics
- CORS middleware enabled
- Health check endpoint
- Auto-generated API documentation
- Comprehensive automated tests

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /stats` - Get statistics for each topic

### `/stats` Endpoint

Returns analytics for each topic including:
- Number of posts per topic
- Total likes, shares, and comments per topic
- Only considers the latest version of each post
- Handles missing data (represented as -1 in the CSV)

**Response Format:**
```json
{
  "topics": [
    {
      "topic": "health",
      "posts_count": 5,
      "total_likes": 159,
      "total_shares": 106,
      "total_comments": 68
    },
    ...
  ]
}
```

## Running Tests

The project includes comprehensive automated tests that verify the application functionality.

### Prerequisites
Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
# Run all tests with verbose output
python -m pytest test_main.py -v

# Run with additional output (shows print statements)
python -m pytest test_main.py -v -s

# Run using pytest directly
pytest test_main.py -v
```

### Run Specific Tests
```bash
# Run only the stats endpoint test
python -m pytest test_main.py::TestStatsEndpoint::test_stats_endpoint -v

# Run only the mock data loading test
python -m pytest test_main.py::test_mock_data_loading -v
```

### What the Tests Verify

The test suite includes:

1. **TestStatsEndpoint.test_stats_endpoint**: 
   - Bootstraps a fresh test database
   - Loads mock data from `mock_posts.csv`
   - Sends HTTP request to `/stats` endpoint
   - Verifies response structure and specific values
   - Tests health topic

2. **test_mock_data_loading**:
   - Verifies mock data can be loaded correctly
   - Checks data integrity (50 total rows, 18 unique post IDs)
   - Validates all 5 topics are present

### Expected Test Results

The tests verify specific values based on the mock data:
- **Health**: 4 posts, 28 likes, 22 shares, 29 comments


### Test Features
- ✅ Fresh database bootstrap for each test
- ✅ Mock data loading from CSV
- ✅ HTTP request to `/stats` endpoint
- ✅ Response structure validation
- ✅ Specific value assertions
- ✅ Proper cleanup of test resources
- ✅ Windows-compatible file handling

## Project Structure

```
VineSight-exercise/
├── main.py              # FastAPI application with database models
├── test_main.py         # Automated tests
├── mock_posts.csv       # Mock data for testing
├── requirements.txt      # Python dependencies
└── README.md           # Project documentation
```

## Database Schema

The application uses SQLite with the following schema:

**Posts Table:**
- `id` (Primary Key)
- `post_id` (Integer, indexed)
- `topic` (String, indexed)
- `likes` (Integer)
- `shares` (Integer)
- `comments` (Integer)
- `version` (Integer)
- `timestamp` (DateTime)

## Data Processing

- Only the latest version of each post is considered for analytics
- Missing data (represented as -1) is excluded from totals
- All topics are included in the response, even if they have no valid data 