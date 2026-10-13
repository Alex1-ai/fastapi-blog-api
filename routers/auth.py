from fastapi import APIRouter, Depends, status, HTTPException, Response

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from model.database import get_db
from model.schemas import UserLogin, Token
from sqlalchemy.orm import Session
from model import model
from utils import verify
from oauth2 import create_access_token

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db) ):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials 1")

    if not verify(user_credentials.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials 2")

    # Create a token and return it
    access_token = create_access_token(data={"user_id": user.id})
    return {"message": "Login successful",
            "access_token": access_token, "token_type": "bearer"}
