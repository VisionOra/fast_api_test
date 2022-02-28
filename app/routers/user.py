from .. import models,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags= ['User APIs']
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateRespose)
# Using an ORM
# Pydantic model validates the request, the email and password will be stored in the
# user variable
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password in user.password
    hashed_password = utils.pwdhasher(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserCreateRespose)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")

    return user


@router.put("/{id}", response_model=schemas.UserCreateRespose)
def update_user(id: int, updated_user: schemas.UserCreateRespose,
 db: Session = Depends(get_db)):

    post_query= db.query(models.User).filter(models.User.id == id)
    post = post_query.first()

    post_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()


    return post_query.first()


    