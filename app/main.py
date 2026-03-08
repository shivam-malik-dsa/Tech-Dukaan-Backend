from fastapi import FastAPI
from app.database import Base, engine
from app.routes.product_routes import router as product_router
from app.routes.ingest_routes import router as ingest_router
from app.routes.auth_routes import router as auth_router
from app.routes.cart_routes import router as cart_router
from app.routes.order_routes import router as order_router
from app.routes.seller_routes import router as seller_routes
from app.models import product, seller, image, tag, dimension, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(product_router)
app.include_router(ingest_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(seller_routes)
