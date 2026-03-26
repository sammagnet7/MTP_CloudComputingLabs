from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PaymentBase(BaseModel):
    orderId: int
    amount: float


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(BaseModel):
    id: int
    order_id: int = Field(..., serialization_alias="orderId")
    amount: float
    status: str
    transaction_id: str = Field(..., serialization_alias="transactionId")
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
