from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.cart_services import add_to_cart_service
from app.utils.jwt import get_current_user
from fastapi import HTTPException
from app.models.cart import Cart

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user
    ).all()

    return cart_items


@router.post("/cart/add")
def add_to_cart(
    product_id: str,
    quantity: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return add_to_cart_service(db, user_id, product_id, quantity)


@router.put("/cart/update")
def update_quantity(
    product_id: str,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    item = db.query(Cart).filter(
        Cart.user_id == current_user,
        Cart.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(404, "Item not found")

    item.quantity = quantity

    db.commit()

    return {"message": "Quantity updated"}


@router.delete("/cart/remove/{product_id}")
def remove_item(
    product_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    item = db.query(Cart).filter(
        Cart.user_id == current_user,
        Cart.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(404, "Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}

