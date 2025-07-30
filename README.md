# VineSight Exercise

A FastAPI application for the VineSight exercise.

## Features

- FastAPI framework
- CORS middleware enabled
- Health check endpoint
- Auto-generated API documentation

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

## Project Structure

```
VineSight-exercise/
├── main.py              # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── README.md           # Project documentation
``` 