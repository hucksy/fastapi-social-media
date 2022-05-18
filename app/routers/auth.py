from ..database import get_db
from app import models, oath2, schemas, utils
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=["auth"])


@router.post("/", response_model=schemas.AccessToken)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    queried_user = db.query(models.Users).filter(models.Users.email == user.username).first()

    if queried_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify(user.password, queried_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = {
        "access_token": oath2.create_access_token(data={"user_id": queried_user.user_id}),
        "token_type": "Bearer"
    }

    return access_token
