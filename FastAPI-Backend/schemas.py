from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database import Base
from crud_utils import *

class User(Base):
   __tablename__ = "users"

   uid = Column(String, unique=True, primary_key=True)
   email = Column(String)
   username = Column(String)
   date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   hashed_password = Column(String)

   creds = relationship("Credential", back_populates="credentials")

class Credential(Base):
   __tablename__ = "credentials"

   credid = Column(String, primary_key=True)
   uid = Column(String, ForeignKey("users.uid"))
   site = Column(String)
   username = Column(String)
   email = Column(String)
   password = Column(String)
   date_added = Column(DATE)

   user = relationship("User", back_populates="creds")
   
class oldCredential(Base):
   __tablename__ = "old_credentials"

   oldcred_id = Column(String, )