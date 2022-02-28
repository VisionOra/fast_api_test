from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # The OATH thing, stores the login details in a dictionary with keys username and password
    # The details are expected in form-data and not the body!
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Create and Return the token
    # We can send whatever we want here, we have chosen to send the userid only
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}