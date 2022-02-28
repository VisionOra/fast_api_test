from .. import models,schemas,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db

from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags= ['Posts APIs']
)


# Get all Posts
@router.get("/", response_model=List[schemas.PostVote])
#@router.get("/")
# Using an ORM
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                limit: int=10, skip: int=0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Using a Database Directly
# def get_posts():
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return{"data": posts}

# Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# Using an ORM
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):

    # Automatically unpack the dictionary, it uses the pydantic model
    new_post = models.Post(owner_id= current_user.id,**post.dict())

    # Below is an ineffecient way of unpacking
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# Using a Database Directly
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * 
#                 """, (post.title, post.content, post.published))

#     new_post = cursor.fetchone()

#     conn.commit()            
    
#     return {"data": new_post}

# Get a specified post
@router.get("/{id}", response_model=schemas.PostVote)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post
# def get_posts(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()

#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     return{ "post detail": post}

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail=f"post with id: {id} does not belong to you!") 

    post_query.delete(synchronize_session=False)
    db.commit()
    # The pop method needs the index of the element in the list
    # my_posts.pop(index)
    # Raising a 204 is done because FastAPI dosent allow a message to 
    #sent when we have the 204 status code in the decorator function!

    return Response(status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id: int):

#     cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found") 
#     # The pop method needs the index of the element in the list
#     # my_posts.pop(index)
#     # Raising a 204 is done because FastAPI dosent allow a message to 
#     #sent when we have the 204 status code in the decorator function!
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):

    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post== None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail=f"post with id: {id} does not belong to you!") 

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()


    return post_query.first()
# def update_posts(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
#      RETURNING * 
#                 """, (post.title, post.content, post.published, str(id),))
    
#     updated_post = cursor.fetchone()
#     conn.commit()


#     if updated_post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found") 

#     # Take the data from the Post class and covert it to a dictionary
#     # post_dict = post.dict()
#     # We add the id so that the id is in the dictionary, id is not part of the Post
#     # base model class, its added while posting. So it needs to be 
#     # post_dict['id'] = id
#     # for post with the said index, replace it with the updated post
#     # my_posts[index] = post_dict

#     return {"data": updated_post}