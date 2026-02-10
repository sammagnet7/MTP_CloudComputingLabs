import os
import uuid
import httpx
import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

import models
import schemas
import database

# ==========================================
# ⚙️ CONFIG & SEEDING
# ==========================================
ORDER_SERVICE_URL = os.getenv(
    "ORDER_SERVICE_URL", "http://localhost:30003/orders/api/users/{userId}"
)


def seed_data(db: Session):
    """Pre-load the microservice with the Monolith's historical data"""
    if db.query(models.Payment).count() == 0:
        print("🌱 Seeding initial payment data...")
        # Match data from your SQL script
        p1 = models.Payment(
            id=1,
            order_id=1,
            amount=1240.00,
            status="SUCCESS",
            transaction_id="TXN_BUDDHA_001",
        )
        p2 = models.Payment(
            id=2,
            order_id=2,
            amount=50.00,
            status="SUCCESS",
            transaction_id="TXN_BUDDHA_002",
        )
        db.add_all([p1, p2])
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed data
    models.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    seed_data(db)
    db.close()
    yield


app = FastAPI(title="Payment Microservice", lifespan=lifespan)
router = APIRouter(prefix="/api/v2")
# ==========================================
# 🚀 API ENDPOINTS
# ==========================================

# 1. POST /payments/ (Process new payment)


@router.post("/payments/", response_model=schemas.PaymentResponse)
def process_payment(
    payment: schemas.PaymentCreate, db: Session = Depends(database.get_db)
):
    print(f"💳 Processing payment for Order {payment.orderId}")

    db_payment = models.Payment(
        order_id=payment.orderId,
        amount=payment.amount,
        status="SUCCESS",
        transaction_id=str(uuid.uuid4()),
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


# 2. GET /payments/order/{id} (Single Order lookup)


@router.get("/payments/order/{order_id}", response_model=schemas.PaymentResponse)
def get_payment_by_order(order_id: int, db: Session = Depends(database.get_db)):
    payment = (
        db.query(models.Payment).filter(models.Payment.order_id == order_id).first()
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# 3. GET /payments/users/{id} (User History - STRANGLER PATTERN)


@router.get("/payments/users/{user_id}", response_model=List[schemas.PaymentResponse])
async def get_user_payments(user_id: int, db: Session = Depends(database.get_db)):

    # Step A: Ask OrderService for this user's orders
    url = ORDER_SERVICE_URL.format(userId=user_id)
    print(f"🔍 Fetching orders from OrderService: {url}")

    order_ids = []
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                orders = resp.json()
                order_ids = [order["id"] for order in orders]
            else:
                print(f"⚠️ OrderService returned {resp.status_code}")
                return []  # Or raise error
        except Exception as e:
            print(f"❌ Connection to OrderService failed: {e}")
            raise HTTPException(status_code=503, detail="OrderService Unavailable")

    if not order_ids:
        return []

    # Step B: Find payments for those orders in our local DB
    payments = (
        db.query(models.Payment).filter(models.Payment.order_id.in_(order_ids)).all()
    )
    return payments


app.include_router(router)
