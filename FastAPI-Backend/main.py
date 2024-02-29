from fastapi import FastAPI, Depends, HTTPException, status
import sqlite3
from datetime import timedelta, datetime, timezone
from models import UserInDB, UserIn, UserOut, Credential, Token, decrypt_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from pyaes256 import PyAES256
from fastapi.responses import HTMLResponse

SECRET_KEY = "5b0cebd0127a1eb2b06333f7dd133e69686b36fab502ba8c0225a20e7c0b6330"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/getToken",scheme_name="JWT")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

def convert_list_to_userindbmodel(data: list):
  fields = UserInDB.model_fields
  kwargs = dict(zip(fields,data))
  return UserInDB(**kwargs)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # returns True or False by hashing the plain pass then comparing with the hashed pass

def hash_password(password):
   return pwd_context.hash(password)

def get_user_by_uid(uid):
  with sqlite3.connect("users.db") as conn:
    try:
      user = conn.execute(f"SELECT * FROM users WHERE uid = '{uid}'").fetchone()
      user = convert_list_to_userindbmodel(user)
      return user
    except:
      return None

def get_user_by_email(email):
  with sqlite3.connect("users.db") as conn:
    try:
      user = conn.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchone()
      user = convert_list_to_userindbmodel(user)
      print(user)
      return user
    except:
      return None

def create_access_token(to_encode: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta #calculates when it should expire
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) #incase not provided
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def convert_credslist_to_json(lst):
   result = []
   fields = Credential.model_fields
   for cred in lst:
    kwargs = dict(zip(fields,cred))
    result.append(kwargs)
   return result

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
    user = get_user_by_uid(uid)
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/addUser", status_code=201) #create new user account
async def add_user(user: UserIn):
  user.password = hash_password(user.password)
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO users VALUES('{user.uid}','{user.email}','{user.username}','{user.date_created}','{user.password}')")
    conn.commit()
    return {"message":f"user{user.uid}successfully added", "name":{user.username}}

@app.post("/getToken")
async def checkUserDetails(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
  user = authenticate_user(form_data.username, form_data.password)
  if not user:
     raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
  expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  data = {"sub":str(user.uid)}
  access_token = create_access_token(data, expiry)
  return {"access_token": access_token, "token_type":"bearer"}

@app.get("/users/config", response_model=UserOut)
async def read_me(current_user: Annotated[UserInDB, Depends(process_token)]):
   return current_user


@app.get("/")
async def read_root():
  return {"message": "Server is operational"}


@app.get("/users/getAll")
async def getall():
  with sqlite3.connect('users.db') as conn:
    return conn.execute(f"SELECT * FROM users").fetchall()

@app.post("/creds/addCred")
async def addCred(cred: Annotated[Credential, Depends(process_token)]):
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO credentials VALUES('{cred.credid}','{cred.uid}','{cred.site}','{cred.email}','{cred.username}',{cred.password},{cred.date_added})")
    conn.commit()
  return {"response": "success", "username": cred.username, "site": cred.site}

@app.get("/creds/getCreds")
async def getCreds(current_user: Annotated[UserIn, Depends(process_token)]):
  with sqlite3.connect("users.db") as conn:
    creds = conn.execute(f"SELECT * FROM credentials WHERE uid = '{current_user.uid}'").fetchall()
  return convert_credslist_to_json(creds)

@app.delete("/creds/delCred")
async def delCred():
   pass # to work on soon

@app.get("/cleardb")
async def cleardb():
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"DELETE FROM users")
    conn.commit()
  return("successfully cleared db")

@app.post("/encrypt")
async def AES_encrypt(data: str):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  ciphertext = PyAES256().encrypt(data,key)
  return ciphertext

@app.post("/decrypt")
def AES_decrypt(data: decrypt_data):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  plaintext = PyAES256().decrypt(url=data.url, salt=data.salt, iv=data.iv, password=key)
  plaintext = bytes.decode(plaintext)
  return {"plaintext": plaintext}

