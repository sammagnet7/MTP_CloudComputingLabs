import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, SessionLocal
import models
import schemas
from seed import seed_data 

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review Service", version="1.0.0")

# Service Discovery: URL of the Product Service
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:30002/api/v2/products")

# --------------------------------------------------------------------------
# TODO 1: LIFECYCLE EVENT
#
# When the service starts ("startup"), we need to initialize the database.
# 1. Create a new DB session using SessionLocal()
# 2. Call seed_data(db) to load initial data.
# 3. Close the session.
# --------------------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 Review Service Starting up...")
    # --- YOUR CODE HERE ---
    pass 


# --------------------------------------------------------------------------
# TODO 2: INTER-SERVICE COMMUNICATION
#
# We must validate that a product exists before we allow a review.
# Since the Product DB is in a different service, we cannot use a SQL JOIN.
# We must make a Synchronous HTTP Request.
#
# 1. Use requests.get() to call {PRODUCT_SERVICE_URL}/{product_id}
# 2. If status_code == 200, return True.
# 3. If 404 or connection error, return False.
# --------------------------------------------------------------------------
def verify_product_exists(product_id: int) -> bool:
    # --- YOUR CODE HERE ---
    return True # <--- ❌ REMOVE THIS PLACEHOLDER


# --- API Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "up", "service": "review-service"}

@app.get("/api/v2/reviews/products/{product_id}", response_model=List[schemas.ReviewResponse])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    # Provided for you: Fetch reviews from DB
    return db.query(models.Review).filter(models.Review.product_id == product_id).all()

@app.post("/api/v2/reviews/products/{product_id}", response_model=schemas.ReviewResponse)
def add_review(product_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    
    # ----------------------------------------------------------------------
    # TODO 3: POST LOGIC
    #
    # 1. Call verify_product_exists(product_id).
    #    - If False: raise HTTPException(status_code=404, detail="Product not found")
    #
    # 2. Create a models.Review object using the data from 'review' schema.
    #    - Note: 'review' has userName, rating, comment. You need to add product_id.
    #
    # 3. Add to db, commit, and refresh.
    # ----------------------------------------------------------------------
    
    # --- YOUR CODE HERE ---
    
    # Placeholder return (remove when implemented)
    raise HTTPException(status_code=501, detail="Not Implemented")
