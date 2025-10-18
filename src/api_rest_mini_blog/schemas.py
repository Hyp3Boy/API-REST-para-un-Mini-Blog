from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Esquemas para Users
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    posts: List[Post] = []
    comments: List[Comment] = []

    class Config:
        from_attributes = True

# Esquemas para Comments
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    user_id: int

class Comment(CommentBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

# Esquemas para Posts
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    comments: List[Comment] = []

    class Config:
        from_attributes = True