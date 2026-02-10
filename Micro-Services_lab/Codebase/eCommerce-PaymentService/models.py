import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)  # Link to Monolith Order ID
    amount = Column(Float)
    status = Column(String, default="SUCCESS")
    transaction_id = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now)
