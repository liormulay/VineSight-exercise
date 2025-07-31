from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.stats_controller import StatsController
from app.schemas.responses import StatsResponse

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics for each topic"""
    return await StatsController.get_stats(db) 