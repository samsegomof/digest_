from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    pass


class UserReadSchema(BaseModel):
    username: str
    id: int

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    source: str


class SubscriptionCreate(SubscriptionBase):
    user_id: int


class SubscriptionSchema(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    content: str
    popularity: int = 0


class PostCreate(PostBase):
    subscription_id: int


class PostSchema(PostBase):
    id: int
    subscription_id: int

    class Config:
        orm_mode = True


class DigestBase(BaseModel):
    user_id: int


class DigestSchema(DigestBase):
    id: int
    posts: List[str]

    class Config:
        orm_mode = True
