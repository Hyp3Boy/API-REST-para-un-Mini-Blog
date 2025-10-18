from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    user_id: int 

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int 

class UserInDB(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class Comment(CommentBase):
    id: int
    created_at: datetime
    author: UserInDB

    model_config = ConfigDict(from_attributes=True)

class Post(PostBase):
    id: int
    created_at: datetime
    author: UserInDB 
    comments: List[Comment] = []

    model_config = ConfigDict(from_attributes=True)
    
class User(UserBase):
    id: int
    posts: List[Post] = []
    comments: List[Comment] = []

    model_config = ConfigDict(from_attributes=True)