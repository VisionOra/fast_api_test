from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils import verify
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config  import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes

# data is the access token payload, of type dict
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # A jwt token contsins 3 parts: A payload, Secret Key and Algorithem used
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# We need to decode the token sent by frontend

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail=f"Could Not Validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    # This can be done, also we fetch the User ID from the database and verify
    # return verify_access_token(token, credentials_exception)
    token =  verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user