from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_404_NOT_FOUND
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags= ['Vote APIs']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

                post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
                if not post:
                    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

                vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.
                    user_id == current_user.id)

                found_vote = vote_query.first()
                # User has sent a positive vote
                if (vote.dir == 1):
                    # User has voted before, so cant do it again!
                    if found_vote:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                         detail=f"user {current_user.id} has already voted on the post {vote.post_id}")
                    # User NOT has voted before, so the vote is aded     
                    new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
                    db.add(new_vote)
                    db.commit()
                    return{"message": "Thanks for your Vote"}
                # User has sent a 0 vote
                else:
                    # User NOT has voted before, so he cannot delete his vote
                    if not found_vote:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
                    
                     # User has voted before, so he can remove his vote
                    vote_query.delete(synchronize_session=False)
                    db.commit()

                    return{"message": "Vote Deleted"} 
