from uuid import UUID,uuid4
from pydantic import BaseModel
from typing import Optional
import datetime

class User(BaseModel):
  uid: Optional[UUID] = uuid4()
  email: str
  username: str
  password: str
  date_created: str | None = datetime.datetime.now().strftime("%x")