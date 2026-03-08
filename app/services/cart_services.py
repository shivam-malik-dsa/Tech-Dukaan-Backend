from app.models.cart import Cart

def add_to_cart_service(db, user_id, product_id, quantity):

    item = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(item)
    db.commit()

    return {"message": "Added to cart"}

