from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.repositories.post_repository import PostRepository
from app.services.stats_service import StatsService
from app.schemas.responses import StatsResponse

class StatsController:
    """Controller for handling statistics-related HTTP requests"""
    
    @staticmethod
    async def get_stats(db: Session = Depends(get_db)) -> StatsResponse:
        """
        Get statistics for each topic including:
        - Number of posts
        - Total likes, shares, and comments
        Only the latest version of each post is considered.
        """
        post_repository = PostRepository(db)
        stats_service = StatsService(post_repository)
        
        return stats_service.get_topic_statistics() 