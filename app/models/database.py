from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Post(Base):
    """Database model for posts"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, index=True)
    topic = Column(String, index=True)
    likes = Column(Integer)
    shares = Column(Integer)
    comments = Column(Integer)
    version = Column(Integer)
    timestamp = Column(DateTime) 