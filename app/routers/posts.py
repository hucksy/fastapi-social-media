from ..database import get_db
from .. import models, schemas, oath2
from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

router = APIRouter(prefix="/posts", tags=["posts]"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit=10, skip=0, search="",
              current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_posts = db.query(models.Post, func.count().label("vote_count")).join(
        models.Votes, models.Post.post_id == models.Votes.post_id, isouter=True).group_by(models.Post.post_id).all()
    return queried_posts


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_post = db.query(models.Post, func.count().label("vote_count")).join(
        models.Votes, models.Post.post_id == models.Votes.post_id, isouter=True).filter(models.Post.post_id == post_id).group_by(models.Post.post_id).first()

    if queried_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post found with post_id = {post_id}")

    # last_orders = db.session.query(
    #     Order.customer_id, db.func.max(Order.order_date).label('last_order_date')
    # ).group_by(Order.customer_id).subquery()
    # query = Order.query.join(
    #     last_orders, Order.customer_id == last_orders.c.customer_id
    # ).order_by(last_orders.c.last_order_date.desc(), Order.order_date.desc())

    return queried_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def make_post(post: schemas.PostCreate, db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    new_post = models.Post(**post.dict(), author_id=current_user.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_post = db.query(models.Post).filter(models.Post.post_id == post_id
                                                , models.Post.author_id == current_user.user_id)
    if queried_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post found for post_id = {post_id}, under this user")

    queried_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_post = db.query(models.Post).filter(models.Post.post_id == post_id,
                                                models.Post.author_id == current_user.user_id)
    if queried_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post found for post_id = {post_id}, under current user {current_user.user_id}")

    queried_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return queried_post.first()
