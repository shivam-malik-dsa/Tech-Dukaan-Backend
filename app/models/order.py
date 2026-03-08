from sqlalchemy import Column, Integer, String, Float
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    product_id = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)