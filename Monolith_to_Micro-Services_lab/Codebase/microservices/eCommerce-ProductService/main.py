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
            models.Product(id=1, name="Smartphone",
                           description="Latest model with 5G and AI camera", price=699.00, category_id=1),
            models.Product(
                id=2, name="Laptop", description="High performance developer machine", price=1200.00, category_id=1),
            models.Product(id=3, name="Microservices Book",
                           description="Learn how to break monoliths safely", price=45.00, category_id=2),
            models.Product(id=4, name="Wireless Headphones",
                           description="Noise cancelling over-ear headphones", price=250.00, category_id=1),
            models.Product(id=5, name="Mechanical Keyboard",
                           description="RGB Backlit with Cherry MX Red switches", price=120.00, category_id=3),
            models.Product(id=6, name="4K Monitor",
                           description="27-inch Ultra HD display for coding", price=350.00, category_id=1),
            models.Product(id=7, name="Clean Code Book",
                           description="A Handbook of Agile Software Craftsmanship", price=50.00, category_id=2),
            models.Product(id=8, name="Ergonomic Mouse",
                           description="Vertical mouse to prevent wrist strain", price=40.00, category_id=3),
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
