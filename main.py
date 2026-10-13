from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status,Response, Depends
from fastapi.params import Body
from model.schemas import PostCreate, PostResponse, UserCreate, UserResponse
from utils import hash_password

from psycopg2.extras import RealDictCursor
import time
from typing import Optional, List
from sqlalchemy.orm import Session
from model.database import engine, SessionLocal
from model import model
from routers.post import post_router
from routers.user import user_router
from routers.auth import auth_router
from routers.vote import vote_router
from model.config import settings


# this create the tables using sqlalchemy
# model.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
"*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentails=True,
    allow_methods=["*"],
    allow_headers=["*"]
)









app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)



@app.get("/")
def root():

    return {"message": "Welcome to my api"}
