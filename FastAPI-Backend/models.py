from uuid import UUID,uuid4
from pydantic import BaseModel, Field
from typing import Optional
import datetime

def get_date():
   return datetime.datetime.now().strftime("%x")

class UserBase(BaseModel):
  uid: Optional[UUID] = Field(default_factory=uuid4)
  email: str
  username: str
  date_created: Optional[str] = Field(default_factory=get_date)

class UserInDB(UserBase):
   hashed_password: str

class UserIn(UserBase):
   password: str

class UserOut(UserBase):
   pass




class Credential(BaseModel):
  credid: Optional[UUID] = Field(default_factory=uuid4)
  uid: Optional[str] = None
  site: Optional[str] = "null"
  username: Optional[str] = "null"
  email: Optional[str] = "null"
  password: str
  date_added: Optional[str] = Field(default_factory=get_date)
  old: Optional[int] = 0


class decrypt_data(BaseModel):
   url:str
   salt:bytes
   iv:bytes

class Token(BaseModel):
  access_token: str
  token_type: str

