from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.order import Order
from app.database import SessionLocal
from app.services.order_service import create_order_service
from app.utils.jwt import get_current_user
from fastapi import HTTPException

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    orders = db.query(Order).filter(
        Order.user_id == current_user
    ).all()

    return orders


@router.post("/order")
def create_order(
    product_id: str,
    quantity: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return create_order_service(db, user_id, product_id, quantity)


@router.get("/orders/{order_id}")
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user
    ).first()

    if not order:
        raise HTTPException(404, "Order not found")

    return order



@router.delete("/orders/{order_id}")
def delete_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user
    ).first()

    if not order:
        raise HTTPException(404, "Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted"}