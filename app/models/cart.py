from sqlalchemy import Column, Integer, ForeignKey,String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Cart(Base):
    __tablename__ = "cart"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    