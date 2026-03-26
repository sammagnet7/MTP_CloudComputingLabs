from sqlalchemy import Column, Integer, String, Text
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    # TODO: Define the columns for the table.
    # Requirements:
    # 1. 'id' (Integer, Primary Key, Index)
    # 2. 'product_id' (Integer, Index) - Acts as a logical Foreign Key to Product Service
    # 3. 'user_name' (String)
    # 4. 'rating' (Integer)
    # 5. 'comment' (Text)
    
    # HINT: Look at seed.py to see what fields are expected!
    
    # id = Column(...)
    pass
