from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    created_time: datetime.datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    email: EmailStr
    user_id: int
    created_time: datetime.datetime

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int]


class PostBase(BaseModel):
    title: str
    content: str
    public: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    post_id: int
    title: str
    content: str
    public: bool
    author_id: int
    created_time: datetime.datetime
    author: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    vote_count: int


class Votes(BaseModel):
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class VotesIn(BaseModel):
    post_id: int
    vote: bool

    class Config:
        orm_mode = True
