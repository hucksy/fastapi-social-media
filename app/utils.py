from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(password: str):
    return pwd_context.hash(password)


def verify(text_password, hashed_password):
    return pwd_context.verify(text_password, hashed_password)
