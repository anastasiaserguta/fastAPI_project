from datetime import datetime
from typing import List, Union
from pydantic import BaseModel



class User(BaseModel):
    age: int
    name: str

class Feedback(BaseModel):
    name: str
    message: str


