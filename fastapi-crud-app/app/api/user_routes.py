from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.models.user_model import User
from app.db.database import get_db
from app.utils.hash import hash_password
from app.core.security import create_access_token

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()