from uuid import UUID,uuid4
from pydantic import BaseModel, Field
from typing import Optional
import datetime

def get_date():
   return datetime.datetime.now().strftime("%x")

class User(BaseModel):
  uid: Optional[UUID] = Field(default_factory=uuid4)
  email: str
  username: str
  password: str
  date_created: Optional[str] = Field(default_factory=get_date)

class Credential(BaseModel):
  credid: Optional[UUID] = Field(default_factory=uuid4)
  uid: str
  site: str
  email: str
  username: Optional[str] = "None"
  password: str
  date_added: Optional[str] = Field(default_factory=get_date)

class Stored_User(User):
    hashed_password: str

class Token(BaseModel):
  access_token: str
  token_type: str   