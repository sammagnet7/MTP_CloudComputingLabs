from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
