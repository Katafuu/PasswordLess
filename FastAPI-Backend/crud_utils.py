from sqlmodel import Session
from models import *
from schemas import *
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserIn):
  hashedPwd = pwd_context.hash(user.password)
  newUser = UserInDB(email=user.email, username=user.username, hashed_password=hashedPwd)
  db.add(newUser)
  db.commit()
  db.refresh(newUser)
  return True
def get_user_by_uid(db: Session, uid: str):
  return db.query(UserOut).filter(UserOut.uid == uid).first()

def get_user_by_email(db: Session, email: str):
  return db.query(UserOut).filter(UserOut.email == email).first()

def get_all_creds(db: Session, uid: str):
  db.query()

def add_cred(db:Session, cred: CredentialIn, user: UserInDB):
  db.add(**cred.model_dumps(), uid=user.uid)
  db.commit()
  db.refresh()
  return True