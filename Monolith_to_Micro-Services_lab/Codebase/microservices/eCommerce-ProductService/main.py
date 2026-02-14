from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import database

app = FastAPI(title="Product Catalog Service", version="1.0")
router = APIRouter(prefix="/api/v2")

# Create tables on startup (for demo purposes)
models.Base.metadata.create_all(bind=database.engine)

# Seed data (Optional: Run this only once in real life)


def seed_data(db: Session):
    if db.query(models.Product).count() == 0:
        products = [
            models.Product(id=1, name="Smartphone", price=699.00,
                           description="Flagship phone", category_id=101),
            models.Product(id=2, name="Laptop", price=1200.00,
                           description="Gaming Laptop", category_id=102),
            models.Product(id=5, name="Mechanical Keyboard", price=120.00,
                           description="Clicky keys", category_id=103),
            models.Product(id=8, name="Ergonomic Mouse", price=40.00,
                           description="Wrist friendly", category_id=103),
        ]
        db.add_all(products)
        db.commit()


@router.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    seed_data(db)
    db.close()

# --- ROUTES ---


@router.get("/products", response_model=List[schemas.ProductResponse])
def get_all_products(db: Session = Depends(database.get_db)):
    """
    Fetch all products. 
    Strangler Fig: This replaces the Monolith's GET /products
    """
    return db.query(models.Product).all()


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    """
    Fetch specific product details.
    Strangler Fig: Checkout service calls this to get the AUTHORITATIVE price.
    """
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


app.include_router(router)
