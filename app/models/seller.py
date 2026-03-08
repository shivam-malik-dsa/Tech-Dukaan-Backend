from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id")) 

    name = Column(String(500), nullable=False)
    email = Column(String(500))
    website = Column(String)

    created_at = Column(TIMESTAMP, server_default=func.now())
    