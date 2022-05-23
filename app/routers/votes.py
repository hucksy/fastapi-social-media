from app.database import get_db
from app import models, schemas, oath2
from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Dict
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=["votes"])


@router.get("/{post_id}", response_model=Dict)
def get_votes(post_id: int, db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_votes = db.query(models.Votes).filter(models.Votes.post_id == post_id).all()
    vote_results = {"number_votes": len(queried_votes)+1,
                    "votes": queried_votes}
    return vote_results


@router.post("/")
def add_vote(vote: schemas.VotesIn,
             db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oath2.get_current_user)):
    queried_post = db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
    if queried_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="that post doesn't exist")
    # if it's a positive vote, check if it already exists before adding it
    if vote.vote:
        queried_vote = db.query(models.Votes).filter(models.Votes.user_id == current_user.user_id,
                                                     models.Votes.post_id == vote.post_id).first()
        if queried_vote is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you already like this post")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.user_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    # if it's a minus vote, delete if possible
    if not vote.vote:
        queried_vote = db.query(models.Votes).filter(models.Votes.user_id == current_user.user_id)
        queried_vote.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
