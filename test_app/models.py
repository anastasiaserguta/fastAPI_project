from datetime import datetime
from typing import List, Union
from pydantic import BaseModel



class User(BaseModel):
    age: int
    name: str

class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool

class UserAuth(BaseModel):
    username: str
    password: str

USER_DATA = [UserAuth(**{"username": "nastia1", "password": "1234"}), UserAuth(**{"username": "nastia2", "password": "12345"})]


class UserJwt(BaseModel):
    user_name: str
    password: str

USER_DATA_JWT = [UserJwt(**{"user_name": "nastia1", "password": "1234"}), UserJwt(**{"user_name": "nastia2", "password": "12345"})]
