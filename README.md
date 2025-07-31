# VineSight Exercise - Clean Architecture

A FastAPI application refactored to follow MVC-inspired Clean Architecture principles.

## Architecture Overview

The application follows Clean Architecture principles with clear separation of concerns:

```
app/
├── models/          # Database models (SQLAlchemy)
├── schemas/         # Pydantic schemas for API responses
├── database/        # Database connection and session management
├── repositories/    # Data access layer (Repository pattern)
├── services/        # Business logic layer
├── controllers/     # Request handling layer
├── routes/          # API route definitions
└── main.py         # Application entry point
```

## Layers

### 1. Models Layer (`app/models/`)
- **Purpose**: Database models using SQLAlchemy
- **Responsibility**: Define database schema and relationships
- **Files**: `database.py` - Contains the `Post` model

### 2. Schemas Layer (`app/schemas/`)
- **Purpose**: Pydantic models for API request/response validation
- **Responsibility**: Define data contracts for API communication
- **Files**: `responses.py` - Contains `TopicStats` and `StatsResponse` schemas

### 3. Database Layer (`app/database/`)
- **Purpose**: Database connection and session management
- **Responsibility**: Configure database engine and provide session dependency
- **Files**: `connection.py` - Database setup and session management

### 4. Repository Layer (`app/repositories/`)
- **Purpose**: Data access abstraction (Repository pattern)
- **Responsibility**: Encapsulate data access logic and provide clean interface
- **Files**: `post_repository.py` - Contains `PostRepository` for post data operations

### 5. Service Layer (`app/services/`)
- **Purpose**: Business logic implementation
- **Responsibility**: Handle complex business rules and orchestrate data operations
- **Files**: 
  - `stats_service.py` - Statistics calculation logic
  - `data_loader_service.py` - Mock data loading functionality

### 6. Controller Layer (`app/controllers/`)
- **Purpose**: Request handling and coordination
- **Responsibility**: Coordinate between routes and services, handle HTTP concerns
- **Files**: `stats_controller.py` - Contains `StatsController` for stats endpoints

### 7. Routes Layer (`app/routes/`)
- **Purpose**: API endpoint definitions
- **Responsibility**: Define HTTP routes and map them to controllers
- **Files**: 
  - `stats_routes.py` - Statistics-related endpoints
  - `health_routes.py` - Health check endpoints

## Key Benefits

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility
2. **Testability**: Business logic is isolated and easily testable
3. **Maintainability**: Changes in one layer don't affect others
4. **Scalability**: Easy to add new features without modifying existing code
5. **Dependency Inversion**: High-level modules don't depend on low-level modules

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /stats` - Get topic statistics

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The application will start on `http://localhost:8000` and automatically load mock data from `mock_posts.csv`.

## Testing

Run tests with:
```bash
pytest
```

## Architecture Principles Applied

1. **Dependency Inversion**: Services depend on repository interfaces, not concrete implementations
2. **Single Responsibility**: Each class has one reason to change
3. **Open/Closed**: Open for extension, closed for modification
4. **Interface Segregation**: Clients depend only on the interfaces they use
5. **Dependency Injection**: Dependencies are injected rather than created internally 