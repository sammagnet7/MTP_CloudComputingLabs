from pydantic import BaseModel

# Schema for creating a review (Client input)
class ReviewCreate(BaseModel):
    userName: str
    rating: int
    comment: str

# Schema for reading a review (API Output)
class ReviewResponse(BaseModel):
    id: int
    productId: int
    userName: str
    rating: int
    comment: str

    class Config:
        # Allows Pydantic to read data from SQLAlchemy models
        from_attributes = True
