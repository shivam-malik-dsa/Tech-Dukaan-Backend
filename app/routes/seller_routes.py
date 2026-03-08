from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.seller import Seller
from app.models.user import User
from app.dependencies.auth import get_current_user
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/seller/become-seller")
def become_seller(
    name: str,
    website: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role == "seller":
        raise HTTPException(400, "Already a seller")

    seller = Seller(
        user_id=current_user.id,
        name=name,
        website=website
    )

    db.add(seller)
    user = db.query(User).filter(User.id == current_user.id).first()
    user.role = "seller"
    db.commit()
    db.refresh(user)
    
    return {"message": "You are now a seller"}