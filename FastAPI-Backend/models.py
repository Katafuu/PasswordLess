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
  uid: str
  site: str
  username: Optional[str] = "None"
  email: str
  password: str
  date_added: Optional[str] = Field(default_factory=get_date)


 # THIS IS WHERE I LEFT OFF 29th Feb 24. Does it matter what order json is in when creating Credential object?

class Token(BaseModel):
  access_token: str
  token_type: str

