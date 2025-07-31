from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./posts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, index=True)
    topic = Column(String, index=True)
    likes = Column(Integer)
    shares = Column(Integer)
    comments = Column(Integer)
    version = Column(Integer)
    timestamp = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class TopicStats(BaseModel):
    topic: str
    posts_count: int
    total_likes: int
    total_shares: int
    total_comments: int

class StatsResponse(BaseModel):
    topics: List[TopicStats]

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="VineSight Exercise",
    description="A FastAPI application for the VineSight exercise",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to VineSight Exercise API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics for each topic including:
    - Number of posts
    - Total likes, shares, and comments
    Only the latest version of each post is considered.
    """
    # Get the latest version of each post
    from sqlalchemy import text
    latest_posts_query = text("""
        SELECT p.* FROM posts p
        INNER JOIN (
            SELECT post_id, MAX(version) as max_version
            FROM posts
            GROUP BY post_id
        ) latest ON p.post_id = latest.post_id AND p.version = latest.max_version
    """)
    latest_posts = db.query(Post).from_statement(latest_posts_query).all()
    
    # Group by topic and calculate stats
    topic_stats = {}
    for post in latest_posts:
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

def load_mock_data():
    """Load mock data from CSV file into the database"""
    # Clear existing data
    db = SessionLocal()
    db.query(Post).delete()
    db.commit()
    
    # Read CSV file
    df = pd.read_csv('mock_posts.csv')
    
    # Convert timestamp strings to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Insert data into database
    for _, row in df.iterrows():
        post = Post(
            post_id=row['post_id'],
            topic=row['topic'],
            likes=row['likes'],
            shares=row['shares'],
            comments=row['comments'],
            version=row['version'],
            timestamp=row['timestamp']
        )
        db.add(post)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    import uvicorn
    # Load mock data on startup
    load_mock_data()
    uvicorn.run(app, host="0.0.0.0", port=8000) 