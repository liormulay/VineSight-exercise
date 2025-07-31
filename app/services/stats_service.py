from app.repositories.post_repository import PostRepository
from app.schemas.responses import TopicStats, StatsResponse
from typing import Dict, Any

class StatsService:
    """Service for calculating post statistics"""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    def get_topic_statistics(self) -> StatsResponse:
        """Calculate statistics for each topic"""
        latest_posts = self.post_repository.get_latest_posts()
        
        # Group by topic and calculate stats
        topic_stats = self._calculate_topic_stats(latest_posts)
        
        # Convert to response format
        topics = [
            TopicStats(
                topic=topic,
                posts_count=stats['posts_count'],
                total_likes=stats['total_likes'],
                total_shares=stats['total_shares'],
                total_comments=stats['total_comments']
            )
            for topic, stats in topic_stats.items()
        ]
        
        return StatsResponse(topics=topics)
    
    def _calculate_topic_stats(self, posts) -> Dict[str, Dict[str, Any]]:
        """Calculate statistics for each topic"""
        topic_stats = {}
        
        for post in posts:
            if post.topic not in topic_stats:
                topic_stats[post.topic] = {
                    'posts_count': 0,
                    'total_likes': 0,
                    'total_shares': 0,
                    'total_comments': 0
                }
            
            topic_stats[post.topic]['posts_count'] += 1
            
            # Only add positive values (skip -1 which indicates missing data)
            if post.likes > 0:
                topic_stats[post.topic]['total_likes'] += post.likes
            if post.shares > 0:
                topic_stats[post.topic]['total_shares'] += post.shares
            if post.comments > 0:
                topic_stats[post.topic]['total_comments'] += post.comments
        
        return topic_stats 