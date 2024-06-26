from typing import Optional
import datetime
from pyaes256 import PyAES256
from sqlmodel import SQLModel, Field, create_engine

class encrypted_data(SQLModel):
   url:str
   salt:bytes
   iv:bytes

def get_date():
   return datetime.datetime.now().strftime("%x")

class UserBase(SQLModel):
  id: Optional[int] = Field(default=None, primary_key=True, index=True)
  email: str = Field(unique=True)
  username: str
  date_created: Optional[str] = Field(default_factory=get_date)

class UserInDB(UserBase, table=True):
   __tablename__ = 'users'
   hashed_password: str

class UserIn(UserBase):
   password: str

class UserOut(UserBase):
   pass


class CredentialBase(SQLModel):
  id: Optional[int] = Field(default=None, primary_key=True)
  site: Optional[str] = Field(default=None, index=True)
  username: Optional[str] = Field(default=None)
  email: Optional[str] = Field(default=None)
  password: str
  date_added: Optional[str] = Field(default_factory=get_date)

  

class CredentialInDB(CredentialBase, table = True):
  __tablename__ = 'credentials'
  owner_id: Optional[int] = Field(default=None, index=True, foreign_key="users.id")
  
class CredentialIn(CredentialBase):
  password: str

class CredentialOut(CredentialBase):
  password: str
  def model_post_init(self, __context) -> None:
      self.password = "***" 


class oldCredential(CredentialBase, table=True):
  __tablename__ = 'oldcredentials'
  credid: Optional[int] = Field(index=True, foreign_key="credentials.id")
  date_removed: Optional[str] = Field(default_factory=get_date)

class oldCredOut(CredentialOut):
  date_removed: Optional[str] = Field(default_factory=get_date)


