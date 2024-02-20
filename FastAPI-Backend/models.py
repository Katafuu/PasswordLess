from uuid import UUID,uuid4
from pydantic import BaseModel, Field
from typing import Optional
import datetime

class User(BaseModel):
  uid: Optional[UUID] = Field(default_factory=uuid4)
  email: str
  username: str
  password: str
  date_created: Optional[str] = Field(default_factory=datetime.datetime.now().strftime("%x"))

class Credential(BaseModel):
  credid: Optional[UUID] = uuid4()
  uid: str
  site: str
  email: str
  username: Optional[str] = "none"
  password: str
  date_added: Optional[str] = datetime.datetime.now().strftime("%x")