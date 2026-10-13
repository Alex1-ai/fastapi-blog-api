from fastapi import FastAPI, HTTPException, status,Response, Depends, APIRouter
from fastapi.params import Body
from model.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from model import model
from model.database import get_db
from utils import hash_password
from model import model


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# @user_router.post("/users", status_code=status.HTTP_201_CREATED,  response_model=UserResponse)
@user_router.post("/", status_code=status.HTTP_201_CREATED,  response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    payload = payload.model_dump()
    user_check =  db.query(model.User).filter(model.User.email == payload["email"]).first()
    if user_check:
        print(user_check.email, user_check.id)
    else:
        print("Not found", user_check)
    if user_check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email: {payload['email']} already exists")
    payload["password"] = hash_password(payload["password"])


    new_user = model.User(**payload)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# @user_router.get("/users/{id}", response_model=UserResponse, )
@user_router.get("/{id}", response_model=UserResponse, )
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")


    return user


