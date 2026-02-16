import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base, SessionLocal
import models
import schemas
from seed import seed_data

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review Service", version="1.0.0")


@app.on_event("startup")
def startup_event():
    """
    Runs when the application starts. 
    Initializes the DB session and seeds data if empty.
    """
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


# Configuration
PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL", "http://product-service:30002/api/v2/products")

# --- Helper Functions ---


def verify_product_exists(product_id: int) -> bool:
    """
    Communicates with the Product Service to ensure the product exists
    before allowing a review to be posted.
    """
    try:
        url = f"{PRODUCT_SERVICE_URL}/{product_id}"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        # Fallback: If product service is down, we might want to fail safe
        # or log an error. For this demo, we assume failure.
        print(f"❌ Error contacting Product Service at {url}")
        return False

# --- Routes ---


@app.get("/health")
def health_check():
    return {"status": "up", "service": "review-service"}


@app.get("/api/v2/reviews/products/{product_id}", response_model=List[schemas.ReviewResponse])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch all reviews for a specific product ID.
    """
    reviews = db.query(models.Review).filter(
        models.Review.product_id == product_id).all()

    # Map SQLAlchemy objects to Pydantic models manually to handle snake_case -> camelCase
    return [
        schemas.ReviewResponse(
            id=r.id,
            productId=r.product_id,
            userName=r.user_name,
            rating=r.rating,
            comment=r.comment
        ) for r in reviews
    ]


@app.post("/api/v2/reviews/products/{product_id}", response_model=schemas.ReviewResponse)
def add_review(product_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """
    Add a new review. Verifies product existence first.
    """
    # 1. Verify Product Exists (Inter-service communication)
    if not verify_product_exists(product_id):
        raise HTTPException(
            status_code=404, detail="Product not found or Product Service unavailable")

    # 2. Save Review
    new_review = models.Review(
        product_id=product_id,
        user_name=review.userName,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # 3. Return Response
    return schemas.ReviewResponse(
        id=new_review.id,
        productId=new_review.product_id,
        userName=new_review.user_name,
        rating=new_review.rating,
        comment=new_review.comment
    )
