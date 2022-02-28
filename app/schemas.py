from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic.types import conint



# Response Schema sent back after User is created
class UserCreateRespose(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True
# Request Schema when user wants to Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 1st level of Inheritance
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# 2nd level of Inheritance
# Request Schema when new post is requested
class PostCreate(PostBase):
    pass


# Request Schema when post is sent as a Respose
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateRespose

    class Config:
        orm_mode=True

class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode=True


# Request Schema to create new users
# EmailStr validates the email, special pydntic libarary function
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Schema from server when users are verified
class Token(BaseModel):
    access_token: str
    token_type: str

# Response from server
class TokenData(BaseModel):
    id: Optional[str]


# Request from user to vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)