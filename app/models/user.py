from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(500), unique=True, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, default="user")   

    created_at = Column(TIMESTAMP, server_default=func.now())