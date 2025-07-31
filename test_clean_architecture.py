#!/usr/bin/env python3
"""
Test script for the clean architecture implementation
Tests each layer independently
"""
import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Post, Base
from app.repositories.post_repository import PostRepository
from app.services.stats_service import StatsService
from app.services.data_loader_service import DataLoaderService
import tempfile
import os
import time

class TestCleanArchitecture:
    """Test class for clean architecture components"""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self):
        """Setup a fresh test database for each test"""
        # Create a temporary database file
        self.test_db_path = "test_clean_arch.db"
        
        # Create engine for test database
        self.test_db_url = f"sqlite:///./{self.test_db_path}"
        self.test_engine = create_engine(self.test_db_url, connect_args={"check_same_thread": False})
        
        # Create tables
        Base.metadata.create_all(bind=self.test_engine)
        
        # Create session factory
        self.TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.test_engine)
        
        # Load mock data into test database
        self._load_mock_data_to_test_db()
        
        yield
        
        # Cleanup: remove test database file
        if hasattr(self, 'TestSessionLocal'):
            db = self.TestSessionLocal()
            db.close()
        
        # Wait a bit and try to remove the file
        time.sleep(0.1)
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except PermissionError:
                # On Windows, sometimes the file is still in use
                pass
    
    def _load_mock_data_to_test_db(self):
        """Load mock data from CSV into the test database"""
        # Clear existing data
        db = self.TestSessionLocal()
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
    
    def test_repository_layer(self):
        """Test the repository layer"""
        db = self.TestSessionLocal()
        repository = PostRepository(db)
        
        # Test getting latest posts
        latest_posts = repository.get_latest_posts()
        assert len(latest_posts) > 0
        
        # Verify we get the latest version of each post
        post_ids = set()
        for post in latest_posts:
            post_ids.add(post.post_id)
        
        # Should have 18 unique post IDs (from mock data)
        assert len(post_ids) == 18
        
        db.close()
    
    def test_service_layer(self):
        """Test the service layer"""
        db = self.TestSessionLocal()
        repository = PostRepository(db)
        service = StatsService(repository)
        
        # Test getting topic statistics
        stats_response = service.get_topic_statistics()
        
        # Verify response structure
        assert hasattr(stats_response, 'topics')
        assert isinstance(stats_response.topics, list)
        
        # Verify specific topics exist
        topics_dict = {topic.topic: topic for topic in stats_response.topics}
        expected_topics = {"health", "finance", "news", "sports", "tech"}
        assert set(topics_dict.keys()) == expected_topics
        
        # Test specific values for health topic
        health_stats = topics_dict["health"]
        assert health_stats.posts_count == 4  # 4 latest health posts
        assert health_stats.total_likes == 28  # Sum of positive likes from latest versions
        assert health_stats.total_shares == 22  # Sum of positive shares from latest versions
        assert health_stats.total_comments == 29  # Sum of positive comments from latest versions
        
        db.close()
    
    def test_data_loader_service(self):
        """Test the data loader service"""
        # Create a separate test database for this test
        test_db_path = "temp_loader_test.db"
        test_db_url = f"sqlite:///./{test_db_path}"
        test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
        
        try:
            # Create tables
            Base.metadata.create_all(bind=test_engine)
            
            # Create session
            TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
            
            # Override the SessionLocal in the data loader service
            original_SessionLocal = DataLoaderService.__init__.__defaults__
            
            # Create a custom data loader that uses our test database
            class TestDataLoaderService(DataLoaderService):
                def __init__(self):
                    self.db = TestSessionLocal()
                    self.post_repository = PostRepository(self.db)
            
            # Test loading data
            data_loader = TestDataLoaderService()
            data_loader.load_mock_data()
            
            # Verify data was loaded
            db = TestSessionLocal()
            total_posts = db.query(Post).count()
            assert total_posts == 50  # Total number of rows in mock_posts.csv
            
            # Verify unique post_ids
            unique_post_ids = db.query(Post.post_id).distinct().count()
            assert unique_post_ids == 18  # 18 unique post_ids in the data
            
            # Verify topics
            unique_topics = db.query(Post.topic).distinct().all()
            expected_topics = {"health", "finance", "news", "sports", "tech"}
            actual_topics = {topic[0] for topic in unique_topics}
            assert actual_topics == expected_topics
            
            db.close()
            
        finally:
            # Cleanup
            time.sleep(0.1)
            if os.path.exists(test_db_path):
                try:
                    os.remove(test_db_path)
                except PermissionError:
                    pass

def test_end_to_end_integration():
    """Test the complete flow from repository to service"""
    # Create a temporary database
    test_db_path = "temp_integration_test.db"
    test_db_url = f"sqlite:///./{test_db_path}"
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    
    try:
        # Create tables
        Base.metadata.create_all(bind=test_engine)
        
        # Create session
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        db = TestSessionLocal()
        
        # Load mock data using the same approach as other tests
        df = pd.read_csv('mock_posts.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Clear existing data first
        db.query(Post).delete()
        db.commit()
        
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
        
        # Test the complete flow
        repository = PostRepository(db)
        service = StatsService(repository)
        
        # Get statistics
        stats_response = service.get_topic_statistics()
        
        # Verify the response
        assert len(stats_response.topics) == 5  # 5 topics in mock data
        
        # Verify health topic specifically
        health_topic = next(topic for topic in stats_response.topics if topic.topic == "health")
        assert health_topic.posts_count == 4  # 4 latest health posts
        assert health_topic.total_likes == 28  # Sum of positive likes from latest versions
        assert health_topic.total_shares == 22  # Sum of positive shares from latest versions
        assert health_topic.total_comments == 29  # Sum of positive comments from latest versions
        
        db.close()
        
    finally:
        # Cleanup
        time.sleep(0.1)
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
            except PermissionError:
                pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 