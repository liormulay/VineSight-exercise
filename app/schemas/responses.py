from pydantic import BaseModel
from typing import List

class TopicStats(BaseModel):
    """Schema for topic statistics"""
    topic: str
    posts_count: int
    total_likes: int
    total_shares: int
    total_comments: int

class StatsResponse(BaseModel):
    """Schema for statistics response"""
    topics: List[TopicStats] 