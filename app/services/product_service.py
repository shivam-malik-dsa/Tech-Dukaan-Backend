from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.seller import Seller
from app.models.image import ProductImage
from app.models.tag import ProductTag
from app.models.dimension import ProductDimension
from sqlalchemy import or_, asc, desc
import uuid

def get_all_products(
    db: Session,
    page: int = 1,
    limit: int = 10,
    min_price=None,
    max_price=None,
    brand=None,
    search=None,
    sort_by=None,
    order="asc",
):

    # Base Query with joinedload (N+1 solved)
    query = db.query(Product).options(
        joinedload(Product.seller),
        joinedload(Product.images),
        joinedload(Product.tags),
        joinedload(Product.dimension),
    )

    # ✅ Filtering
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    # ✅ Search
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
            )
        )

     # ✅ Sorting
    allowed_sorts = {
    "price": Product.price,
    "rating": Product.rating,
    "created_at": Product.created_at,
    }

    # Sorting only if sort_by provided
    if sort_by and sort_by in allowed_sorts:
        column = allowed_sorts[sort_by]

        if order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    # ✅ Total Count BEFORE pagination
    total = query.count()

    # ✅ Pagination
    products = query.offset((page - 1) * limit).limit(limit).all()

    result = []

    for product in products:
        result.append(
            {
                "id": str(product.id),
                "name": product.name,
                "price": float(product.price),
                "stock": product.stock,
                "seller": product.seller.name if product.seller else None,
                "images": [img.image_url for img in product.images],
                "tags": [tag.tag for tag in product.tags],
                "dimensions": (
                    {
                        "length": (
                            float(product.dimension.length_cm)
                            if product.dimension
                            else None
                        ),
                        "width": (
                            float(product.dimension.width_cm)
                            if product.dimension
                            else None
                        ),
                        "height": (
                            float(product.dimension.height_cm)
                            if product.dimension
                            else None
                        ),
                    }
                    if product.dimension
                    else None
                ),
            }
        )

    return {"total": total, "page": page, "limit": limit, "data": result}


def get_product_by_id(db: Session, product_id):

    product = (
        db.query(Product)
        .options(
            joinedload(Product.seller),
            joinedload(Product.images),
            joinedload(Product.tags),
            joinedload(Product.dimension),
        )
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "stock": product.stock,
        "rating": float(product.rating) if product.rating else None,
        "seller": product.seller.name if product.seller else None,
        "images": [img.image_url for img in product.images],
        "tags": [tag.tag for tag in product.tags],
        "dimensions": (
            {
                "length": (
                    float(product.dimension.length_cm) if product.dimension else None
                ),
                "width": (
                    float(product.dimension.width_cm) if product.dimension else None
                ),
                "height": (
                    float(product.dimension.height_cm) if product.dimension else None
                ),
            }
            if product.dimension
            else None
        ),
    }


def create_product_service(db, sku, name, price, stock, user_id):

    seller = db.query(Seller).filter(Seller.user_id == user_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    product = Product(
        sku=sku,
        name=name,
        price=price,
        stock=stock,
        seller_id=seller.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product_service(db, product_id, price, stock, user_id):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    seller = db.query(Seller).filter(Seller.user_id == user_id).first()

    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    product.price = price
    product.stock = stock

    db.commit()

    return {"message": "Product updated"}


def delete_product_service(db, product_id, user_id):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    seller = db.query(Seller).filter(Seller.user_id == user_id).first()

    if product.seller_id != seller.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}
