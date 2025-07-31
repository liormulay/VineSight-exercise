from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import health_routes, stats_routes
from app.services.data_loader_service import DataLoaderService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("Starting application...")
    data_loader = DataLoaderService()
    print("Loading mock data...")
    data_loader.load_mock_data()
    print("Application startup complete!")
    yield
    # Shutdown (if needed)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="VineSight Exercise",
        description="A FastAPI application for the VineSight exercise",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_routes.router, tags=["health"])
    app.include_router(stats_routes.router, tags=["stats"])
    
    return app

app = create_app() 