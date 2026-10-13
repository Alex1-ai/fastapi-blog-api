
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
from typing import Annotated



class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email of the user", example="example@example.com")
    password: str = Field(..., description="Password of the user", example="password123")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@example.com",
                    "password": "password123"
                }
            ]
        }
    }


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email of the user",example="xxx@xxxxx.com")
    password: str = Field(..., description="Password of the user", example="xxxxx12312")


class Token(BaseModel):
    message: str
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str = Field(..., description="Title of the post", example="My First Post")
    content: str = Field(..., description="Body content of the post", example="Hello world!")
    published: Optional[bool] = Field(True, description="Whether the post is published")
    rating: Optional[float] = Field(0.0, description="Rating of the post", ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My First Post",
                    "content": "Hello world!",
                    "published": True
                }
            ]
        }
    }



class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass



class PostResponse(PostBase):
    id: int
    rating: Optional[float]
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int


    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]

