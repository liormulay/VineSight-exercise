import pandas as pd
from app.repositories.post_repository import PostRepository
from app.models.database import Post
from app.database.connection import SessionLocal

class DataLoaderService:
    """Service for loading mock data into the database"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.post_repository = PostRepository(self.db)
    
    def load_mock_data(self, csv_file_path: str = 'mock_posts.csv'):
        """Load mock data from CSV file into the database"""
        print(f"Loading data from {csv_file_path}...")
        
        # Clear existing data
        print("Clearing existing data...")
        self.post_repository.clear_all_posts()
        
        # Read CSV file
        print("Reading CSV file...")
        df = pd.read_csv(csv_file_path)
        print(f"Found {len(df)} records to process")
        
        # Convert timestamp strings to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Insert data into database using bulk insert for better performance
        print("Inserting data into database...")
        posts = []
        for i, (_, row) in enumerate(df.iterrows()):
            if i % 1000 == 0:  # Log progress every 1000 records
                print(f"Processed {i}/{len(df)} records...")
            
            post = Post(
                post_id=row['post_id'],
                topic=row['topic'],
                likes=row['likes'],
                shares=row['shares'],
                comments=row['comments'],
                version=row['version'],
                timestamp=row['timestamp']
            )
            posts.append(post)
        
        # Bulk insert all posts at once
        self.db.add_all(posts)
        self.db.commit()
        
        print(f"Successfully loaded {len(df)} records into database")
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'db'):
            self.db.close() 