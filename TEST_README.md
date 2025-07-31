# Automated Tests for VineSight Exercise

This directory contains automated tests for the VineSight Exercise FastAPI application.

## Test Overview

The test suite includes:

1. **TestStatsEndpoint.test_stats_endpoint**: Tests the `/stats` endpoint
   - Bootstraps a fresh test database
   - Loads mock data from `mock_posts.csv`
   - Sends a request to `/stats`
   - Verifies the response structure and specific values

2. **test_mock_data_loading**: Tests mock data loading functionality
   - Verifies that mock data can be loaded correctly
   - Checks data integrity (total rows, unique post IDs, topics)

## Running the Tests

### Prerequisites
Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
# Run all tests
python -m pytest test_main.py -v

# Run with verbose output
python -m pytest test_main.py -v -s

# Run a specific test
python -m pytest test_main.py::TestStatsEndpoint::test_stats_endpoint -v
```

## Test Details

### Database Setup
- Each test creates a fresh SQLite database
- Mock data is loaded from `mock_posts.csv`
- Database connections are properly cleaned up after each test

### Expected Values
The tests verify specific values based on the mock data:
- **Health**: 4 posts, 28 likes, 22 shares, 29 comments
- **Finance**: 7 posts, 294 likes, 96 shares, 9 comments  
- **News**: 8 posts, 204 likes, 88 shares, 24 comments
- **Sports**: 5 posts, 55 likes, 77 shares, 39 comments
- **Tech**: 6 posts, 114 likes, 81 shares, 26 comments

### Key Features Tested
- ✅ Fresh database bootstrap for each test
- ✅ Mock data loading from CSV
- ✅ HTTP request to `/stats` endpoint
- ✅ Response structure validation
- ✅ Specific value assertions
- ✅ Proper cleanup of test resources

## Test Data
The tests use the provided `mock_posts.csv` file which contains:
- 50 total rows
- 18 unique post IDs
- 5 topics: health, finance, news, sports, tech
- Multiple versions of posts (only latest versions are considered in stats)
- Missing data represented as -1 (excluded from calculations) 