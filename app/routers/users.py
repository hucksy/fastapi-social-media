from app.database import get_db
from app import models, schemas, utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    queried_user = db.query(models.Users).filter(models.Users.user_id == int(user_id)).first()
    if queried_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user found for {user_id}")

    return queried_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def make_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.get_hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
