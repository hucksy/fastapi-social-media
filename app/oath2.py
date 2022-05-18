from . import database, models, schemas
from .config import env_settings
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

SECRET_KEY = env_settings.secret_key
ALGORITHM = env_settings.algorithm
EXPIRE_TIME_MIN = env_settings.expire_time_min

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    encode_data = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME_MIN)
    encode_data.update({"exp": expire_time})
    encode_data = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

    return encode_data


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        legit_user_id = schemas.TokenData(user_id=user_id).user_id
    except JWTError:
        raise credentials_exception
    else:
        return legit_user_id


def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                          detail="invalid credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    user_id = verify_token(token, credentials_exception)
    current_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    return current_user


