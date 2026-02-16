from sqlalchemy import Column, Integer, String, Text
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)  # Foreign Key (logical) to Product Service
    user_name = Column(String)
    rating = Column(Integer)
    comment = Column(Text)
