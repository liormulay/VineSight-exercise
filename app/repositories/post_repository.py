from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.database import Post
from typing import List

class PostRepository:
    """Repository for post data access operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_latest_posts(self) -> List[Post]:
        """Get the latest version of each post"""
        latest_posts_query = text("""
            SELECT p.* FROM posts p
            INNER JOIN (
                SELECT post_id, MAX(version) as max_version
                FROM posts
                GROUP BY post_id
            ) latest ON p.post_id = latest.post_id AND p.version = latest.max_version
        """)
        return self.db.query(Post).from_statement(latest_posts_query).all()
    
    def clear_all_posts(self):
        """Clear all posts from the database"""
        self.db.query(Post).delete()
        self.db.commit()
    
    def add_post(self, post: Post):
        """Add a new post to the database"""
        self.db.add(post)
        self.db.commit() 