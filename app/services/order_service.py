from fastapi import HTTPException
from app.models.product import Product
from app.models.order import Order


def create_order_service(db, user_id, product_id, quantity):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total = product.price * quantity

    order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    
    return {
        "message": "Order created",
        "order_id": str(order.id)
    }
