import pytest
import httpx
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import Post, Base, load_mock_data
import tempfile
import os
import shutil
import time
from fastapi.testclient import TestClient
from main import app

class TestStatsEndpoint:
    """Test class for the /stats endpoint"""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self):
        """Setup a fresh test database for each test"""
        # Create a temporary database file
        self.test_db_path = "test_posts.db"
        
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
        # Close all database connections first
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
    
    def test_stats_endpoint(self):
        """Test the /stats endpoint with mock data"""
        # Create test client with overridden database dependency
        def get_test_db():
            db = self.TestSessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        # Override the database dependency for testing
        from main import get_db
        app.dependency_overrides[get_db] = get_test_db
        
        with TestClient(app) as client:
            # Send request to /stats endpoint
            response = client.get("/stats")
            
            # Verify response status
            assert response.status_code == 200
            
            # Parse response data
            data = response.json()
            
            # Verify response structure
            assert "topics" in data
            assert isinstance(data["topics"], list)
            
            # Convert to dictionary for easier testing
            topics_dict = {topic["topic"]: topic for topic in data["topics"]}
            
            # Verify specific topics exist
            expected_topics = {"health", "finance", "news", "sports", "tech"}
            assert set(topics_dict.keys()) == expected_topics
            
            # Test specific values based on mock data analysis
            # These values are calculated from the mock data considering only latest versions
            # and excluding -1 values (missing data)
            
            # Health topic assertions
            health_stats = topics_dict["health"]
            assert health_stats["posts_count"] == 4  # 4 unique posts with latest versions
            assert health_stats["total_likes"] == 28  # Sum of positive likes from latest versions
            assert health_stats["total_shares"] == 22  # Sum of positive shares from latest versions
            assert health_stats["total_comments"] == 29  # Sum of positive comments from latest versions
            
            
            # Verify all stats are non-negative
            for topic_stats in data["topics"]:
                assert topic_stats["posts_count"] >= 0
                assert topic_stats["total_likes"] >= 0
                assert topic_stats["total_shares"] >= 0
                assert topic_stats["total_comments"] >= 0
        
        # Clean up dependency override
        app.dependency_overrides.clear()

def test_mock_data_loading():
    """Test that mock data can be loaded correctly"""
    # Create a temporary database
    test_db_path = "temp_test.db"
    test_db_url = f"sqlite:///./{test_db_path}"
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    
    try:
        # Create tables
        Base.metadata.create_all(bind=test_engine)
        
        # Create session
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        db = TestSessionLocal()
        
        # Clear existing data
        db.query(Post).delete()
        db.commit()
        
        # Load mock data
        df = pd.read_csv('mock_posts.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
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
        
        # Verify data was loaded
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
                # On Windows, sometimes the file is still in use
                pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 