from fastapi import FastAPI, Depends, HTTPException, status, Request
import sqlite3
from datetime import timedelta, datetime, timezone
from models import UserInDB, UserIn, UserOut, CredentialIn, CredentialOut, CredentialInDB, oldCredential, encrypted_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from pyaes256 import PyAES256
import json
import db
import string

SECRET_KEY = "5b0cebd0127a1eb2b06333f7dd133e69686b36fab502ba8c0225a20e7c0b6330"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/getToken",scheme_name="JWT")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db():
  db.SQLModel.metadata.create_all(db.engine)


if __name__ == "main":
   create_db()



app = FastAPI()
origins = [
    "http://passwordless.duckdns.org",
    "http://www.passwordless.duckdns.org",
    "https://passwordless.duckdns.org",
    "https://www.passwordless.duckdns.org",
    'null'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
   return pwd_context.verify(plain_password, hashed_password)  # returns True or False by hashing the plain pass then comparing with the hashed pass

def hash_password(password):
   return pwd_context.hash(password)

def create_access_token(to_encode: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta #calculates when it should expire
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) #incase not provided
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str):
    user = db.get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        print("oh no, wrong pwd\n\n")
        return False
    return user


def map_list_to_dict(lstitem, attrs: list):
  kwargs = dict(zip(attrs,lstitem))
  return kwargs



async def process_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.get_user_by_id(uid)
    if user is None:
        raise credentials_exception
    return user

def AES_encrypt(data: str):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  ciphertext = PyAES256().encrypt(data,key)
  print(f"CIPHER:  {ciphertext}")
  return encrypted_data(**ciphertext)

def AES_decrypt(data: encrypted_data):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  plaintext = PyAES256().decrypt(url=data.url, salt=data.salt, iv=data.iv, password=key)
  return bytes.decode(plaintext)

#------------------------------------------------------- endpoint start, utility end
@app.post("/getToken")
async def checkUserDetails(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
  user = authenticate_user(form_data.username.lower(), form_data.password)

  if not user:
     raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
  expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  data = {"sub":str(user.id)}
  access_token = create_access_token(data, expiry)
  return {"access_token": access_token, "token_type":"bearer"}

@app.post("/users/addUser", status_code=201) #create new user account
async def add_user(user: UserIn):
  response = db.add_user(user)
  return response

@app.get("/users/self", response_model=UserOut)
async def read_me(current_user: Annotated[UserInDB, Depends(process_token)]):
   return current_user

@app.get("/creds/getCreds")
async def getActiveCreds(current_user: Annotated[UserIn, Depends(process_token)], response_model=CredentialOut):
  return db.get_creds(current_user)
  

@app.get("/creds/getOldCreds")
async def getOldCreds(credid: int, current_user: Annotated[UserIn, Depends(process_token)]):
  return db.get_old_creds_byid(credid, current_user.id)

@app.post("/creds/addCred")
async def addCred(cred: CredentialIn, current_user: Annotated[UserIn, Depends(process_token)]):
  pwd = AES_encrypt(cred.password)
  cred.password = pwd.model_dump_json()
  print(cred.password, type(cred.password))
  response = db.add_cred(cred, current_user.id)
  return response
  

@app.put("/creds/modifyCred")
async def modifyCred(request: Request, current_user: Annotated[UserIn,  Depends(process_token)]):
   body = await request.json()
   updCred = CredentialIn(**body)
   print(updCred)
   response = db.modify_cred(updCred)
   return response
@app.delete("/creds/delCred")
async def delCred(credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
   return db.delete_cred(credid, False)

@app.delete("/creds/delOldCred")
async def delOldCred(credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
   return db.delete_cred(credid, True)

@app.get("/creds/getDecryptPassword")
async def getDecryptPwd(tbl: str, credid: int, current_user: Annotated[UserIn, Depends(process_token)]):
  if tbl == "old":
     model = oldCredential
  else:
     model = CredentialInDB
  pwd = db.get_password(model, credid)
  print(pwd)
  pwd = json.loads(pwd)
  print(pwd)
  pwd = AES_decrypt(db.encrypted_data(**pwd))
  print(pwd)
  return {credid:pwd}