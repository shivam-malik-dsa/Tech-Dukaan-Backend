from sqlalchemy import (
    Column, String, Integer, Numeric, Boolean,
    ForeignKey, TIMESTAMP, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import uuid


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String(500), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(String)
    category = Column(String(500))
    brand = Column(String(500))
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="INR")
    discount_percent = Column(Integer, default=0)
    stock = Column(Integer, nullable=False)
    rating = Column(Numeric(2, 1))
    is_active = Column(Boolean, default=True)
    seller_id = Column(String, ForeignKey("sellers.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    seller = relationship("Seller")
    images = relationship("ProductImage")
    tags = relationship("ProductTag")
    dimension = relationship("ProductDimension", uselist=False)
