from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Float, nullable=False)  # The authoritative price
    description = Column(Text, nullable=True)
    category_id = Column(Integer, nullable=True)
