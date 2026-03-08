from sqlalchemy import Column, Numeric, ForeignKey,String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class ProductDimension(Base):
    __tablename__ = "product_dimensions"

    product_id = Column(String, ForeignKey("products.id"), primary_key=True)
    length_cm = Column(Numeric(5, 2))
    width_cm = Column(Numeric(5, 2))
    height_cm = Column(Numeric(5, 2))
