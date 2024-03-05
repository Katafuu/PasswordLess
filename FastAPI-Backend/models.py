from uuid import UUID,uuid4
from pydantic import BaseModel, Field
from typing import Optional
import datetime
from pyaes256 import PyAES256
import json

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

class encrypted_data(BaseModel):
   url:str
   salt:bytes
   iv:bytes

async def AES_encrypt(data: str):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  ciphertext = PyAES256().encrypt(data,key)
  return ciphertext

class CredentialBase(BaseModel):
  credid: Optional[UUID] = Field(default_factory=uuid4)
  site: Optional[str] = "null"
  username: Optional[str] = "null"
  email: Optional[str] = "null"
  password: encrypted_data
  date_added: Optional[str] = Field(default_factory=get_date)


class CredentialInDB(CredentialBase):
  uid: Optional[str] = None

class CredentialIn(CredentialBase):
  uid: Optional[str] = None
  password: str

class CredentialOut(CredentialBase):
  password: encrypted_data
  def model_post_init(self, __context) -> None:
      self.password = "***" 


class oldCredential(CredentialBase):
  oldcred_uid: Optional[str] = Field(default_factory=uuid4)
  date_removed: Optional[str] = Field(default_factory=get_date)

