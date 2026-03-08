import json
from app.database import SessionLocal
from app.models.seller import Seller
from app.models.product import Product
from app.models.image import ProductImage
from app.models.tag import ProductTag
from app.models.dimension import ProductDimension


def ingest_products(file_path: str):

    db = SessionLocal()

    try:
        with open(file_path, "r") as f:
            products = json.load(f)

        products_to_insert = []
        images_to_insert = []
        tags_to_insert = []
        dimensions_to_insert = []

        for item in products:

            #  SELLER CHECK
            seller_data = item["seller"]

            seller = db.query(Seller).filter(
                Seller.id == seller_data["seller_id"]
            ).first()

            if not seller:
                seller = Seller(
                    id=seller_data["seller_id"],
                    name=seller_data["name"],
                    email=seller_data["email"],
                    website=seller_data["website"]
                )
                db.add(seller)
                db.flush()

            # IDEMPOTENCY CHECK
            existing_product = db.query(Product).filter(
                Product.id == item["id"]
            ).first()

            if existing_product:
                continue

            product = Product(
                id=item["id"],
                sku=item["sku"],
                name=item["name"],
                description=item["description"],
                category=item["category"],
                brand=item["brand"],
                price=item["price"],
                currency=item["currency"],
                discount_percent=item["discount_percent"],
                stock=item["stock"],
                rating=item["rating"],
                is_active=item["is_active"],
                seller_id=seller.id
            )

            products_to_insert.append(product)

            # IMAGES
            for url in item["image_urls"]:
                images_to_insert.append(
                    ProductImage(
                        product_id=item["id"],
                        image_url=url
                    )
                )

            # TAGS
            for tag in item["tags"]:
                tags_to_insert.append(
                    ProductTag(
                        product_id=item["id"],
                        tag=tag
                    )
                )

            # DIMENSIONS
            dim = item["dimensions_cm"]

            dimensions_to_insert.append(
                ProductDimension(
                    product_id=item["id"],
                    length_cm=dim["length"],
                    width_cm=dim["width"],
                    height_cm=dim["height"]
                )
            )

        #  BULK INSERT (FAST)
        db.bulk_save_objects(products_to_insert)
        db.bulk_save_objects(images_to_insert)
        db.bulk_save_objects(tags_to_insert)
        db.bulk_save_objects(dimensions_to_insert)

        db.commit()

        print("Ingestion completed successfully")

    except Exception as e:
        db.rollback()
        print("Ingestion failed:", str(e))
        raise e

    finally:
        db.close()
