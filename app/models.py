from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    public = Column(Boolean, server_default="True")
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    author_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    author = relationship("Users")


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
