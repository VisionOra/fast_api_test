# Utility Functions

# Function to hash the password 
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def pwdhasher(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)