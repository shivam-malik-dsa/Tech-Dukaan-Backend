from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class ProductTag(Base):
    __tablename__ = "product_tags"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    tag = Column(String(50), nullable=False)
