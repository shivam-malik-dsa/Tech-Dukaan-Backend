from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.product_service import (get_all_products, get_product_by_id, create_product_service, update_product_service, delete_product_service)
from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products")
def fetch_products(
    page: int = 1,
    limit: int = 10,
    min_price: float = None,
    max_price: float = None,
    brand: str = None,
    search: str = None,
    sort_by: str = None,
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return get_all_products(
        db, page, limit,
        min_price, max_price,
        brand, search, sort_by,
        order
    )


@router.get("/products/{product_id}")
def fetch_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    return get_product_by_id(db, product_id)


@router.post("/products")
def create_product(
    sku: str,
    name: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ⭐ ROLE CHECK
    if current_user.role != "seller":
        raise HTTPException(
            status_code=403,
            detail="Only sellers can create products"
        )

    return create_product_service(
        db,
        sku,
        name,
        price,
        stock,
        current_user.id
    )


@router.put("/products/{product_id}")
def update_product(
    product_id: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    return update_product_service(db, product_id, price, stock, current_user.id)


@router.delete("/products/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    return delete_product_service(db, product_id, current_user.id)

