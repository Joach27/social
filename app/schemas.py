from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List 

# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


## ===================================== ##
# Post schema
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    # Supprimez content: str car déjà dans PostBase
    # Supprimez created_at car géré automatiquement
    pass  # Vous pouvez juste laisser vide

class PostUpdate(BaseModel):  # Pas PostBase car tous les champs sont optionnels
    title: Optional[str] = None
    content: Optional[str] = None
    # updated_at sera géré automatiquement par la base

class PostResponse(PostBase):
    id: int
    user_id: int  # Important à inclure
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: UserResponse

    class Config:
        from_attributes = True


## ===================================== ##
# Comment schema
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    # post_id et user_id viendront du contexte (URL ou user courant)
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True


## ===================================== ##
# Token schemas (pour l'authentification)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None