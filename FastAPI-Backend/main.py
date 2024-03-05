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

SECRET_KEY = "5b0cebd0127a1eb2b06333f7dd133e69686b36fab502ba8c0225a20e7c0b6330"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
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
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def map_list_to_dict(lstitem, attrs: list):
  kwargs = dict(zip(attrs,lstitem))
  return kwargs

def get_user_by_uid(uid: str):
  with sqlite3.connect("users.db") as conn:
    try:
      cursor = conn.cursor()
      user = cursor.execute(f"SELECT * FROM users WHERE uid = '{uid}'").fetchone()
      attributes = [x[0] for x in cursor.description]
      user = map_list_to_dict(user, attributes)
      user = UserInDB(**user)
      return user
    except:
      return None



def get_user_by_email(email: str):
  with sqlite3.connect("users.db") as conn:
    try:
      cursor = conn.cursor()
      user = cursor.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchone()
      attributes = [x[0] for x in cursor.description]
      user = map_list_to_dict(user, attributes)
      user = UserInDB(**user)
      return user
    except Exception as e:
      print(e)
      return None

def get_creds(current_user: UserIn):
  with sqlite3.connect('users.db') as conn:
    cursor = conn.cursor()
    cred_data = cursor.execute(f"SELECT * FROM credentials WHERE uid='{current_user.uid}';").fetchall()
    columns = [x[0] for x in cursor.description]
    creds = []
    for cred in cred_data:
      cred = map_list_to_dict(cred, columns)
      cred["password"] = json.loads(cred["password"])
      creds.append(cred)
  return creds

def get_old_creds_bycredid(credid: str):
   with sqlite3.connect('users.db') as conn:
    cursor = conn.cursor()
    cred_data = cursor.execute(f"SELECT * FROM old_credentials WHERE credid='{credid}';").fetchall()
    columns = [x[0] for x in cursor.description]
    creds = []
    for cred in cred_data:
      cred = map_list_to_dict(cred, columns)
      cred["password"] = json.loads(cred["password"])
      creds.append(cred)
   return creds

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

def AES_encrypt(data: str):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  ciphertext = PyAES256().encrypt(data,key)
  print(f"CIPHER:  {ciphertext}")
  return encrypted_data(**ciphertext)

def AES_decrypt(data: encrypted_data):
  key = "ff4f015ead69df0f0729154409375600bfe0ddf7942c0e2e0fe818509e66fb2e"
  plaintext = PyAES256().decrypt(url=data.url, salt=data.salt, iv=data.iv, password=key)
  plaintext = bytes.decode(plaintext)
  return {"plaintext": plaintext}

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
  data = {"sub":str(user.uid)}
  access_token = create_access_token(data, expiry)
  return {"access_token": access_token, "token_type":"bearer"}

@app.post("/users/addUser", status_code=201) #create new user account
async def add_user(user: UserIn):
  user.password = hash_password(user.password)
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO users VALUES('{user.uid}','{user.email.lower()}','{user.username}','{user.date_created}','{user.password}')")
    conn.commit()
    return {"message":f"user with id: {user.uid} - successfully added", "name":{user.username}}

@app.get("/users/self", response_model=UserOut)
async def read_me(current_user: Annotated[UserInDB, Depends(process_token)]):
   return current_user

@app.get("/creds/getCreds")
async def getActiveCreds(current_user: Annotated[UserIn, Depends(process_token)]):
  return get_creds(current_user)

@app.get("/creds/getOldCreds")
async def getOldCreds(credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
  return get_old_creds_bycredid(credid)

@app.post("/creds/addCred")
async def addCred(cred: CredentialIn, current_user: Annotated[UserIn, Depends(process_token)]):
  cred = cred.model_dump()
  cred["password"] = AES_encrypt(cred["password"])
  cred = CredentialInDB(**cred)
  with sqlite3.connect("users.db") as conn:
    exists = conn.execute(f"SELECT * FROM credentials WHERE (uid='{current_user.uid}' AND site='{cred.site}') AND (email='{cred.email}' OR username='{cred.username}')").fetchone()
    if exists:
       return {"message": "error, already exists"}
    else:
      conn.execute(f"INSERT INTO credentials VALUES('{cred.credid}','{current_user.uid}','{cred.site}','{cred.username}','{cred.email}','{cred.password.model_dump_json()}','{cred.date_added}');")
      conn.commit()
  return {"response": "success", "username": cred.username, "site": cred.site}

@app.put("/creds/modifyCred")
async def modifyCred(request: Request, current_user: Annotated[UserIn,  Depends(process_token)]):
   body = await request.json()
   updCred = CredentialIn(**body)
   with sqlite3.connect('users.db') as conn:
      cursor = conn.cursor()
      oldCred = cursor.execute(f"SELECT * FROM credentials WHERE credid='{updCred.credid}'").fetchone()
      columns = [x[0] for x in cursor.description]
      oldCred = oldCredential(**map_list_to_dict(oldCred, columns))
      identical = oldCred.site == updCred.site and oldCred.email == updCred.email and oldCred.username == updCred.username and updCred.password == AES_decrypt(oldCred.password)
      if identical:
         return {"message": "no changes made"}
      else:
        updCred = updCred.model_dump()
        updCred["password"] = AES_encrypt(updCred["password"])
        updCred = CredentialInDB(**updCred)
        conn.execute(f"UPDATE credentials SET site='{updCred.site}', username='{updCred.username}', email='{updCred.email}', password='{updCred.password.model_dump_json()}', date_added='{updCred.date_added}' WHERE credid='{updCred.credid}';")
        conn.execute(f"INSERT INTO old_credentials VALUES('{oldCred.oldcred_uid}','{oldCred.credid}','{oldCred.site}','{oldCred.username}','{oldCred.email}','{oldCred.password}','{oldCred.date_added}','{updCred.date_added}');")
        conn.commit()
   return {'message': 'success'}

@app.delete("/creds/delCred")
async def delCred(credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
   with sqlite3.connect('users.db') as conn:
      cursor = conn.cursor()
      cred_data = cursor.execute(f"SELECT * FROM credentials WHERE credid='{credid}';").fetchone()
      columns = [x[0] for x in cursor.description]
      oldCred = oldCredential(**map_list_to_dict(cred_data, columns))
      conn.execute(f"DELETE FROM credentials WHERE credid = '{credid}';")
      conn.execute(f"INSERT INTO old_credentials VALUES('{oldCred.oldcred_uid}','{oldCred.credid}','{oldCred.site}','{oldCred.username}','{oldCred.email}','{oldCred.password}','{oldCred.date_added}','{datetime.now().strftime('%x')}');")
      conn.commit()
   return {'message': 'success', 'cred_removed': credid}

@app.delete("/creds/delOldCred")
async def delOldCred(credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
   with sqlite3.connect('users.db') as conn:
      conn.execute(f"DELETE FROM old_credentials WHERE oldcred_uid = '{credid}';")
      conn.commit()
   return {'message': 'success', 'cred_removed': credid}

@app.post("/creds/getDecryptPassword")
async def getDecryptPwd(db: str, credid: str, current_user: Annotated[UserIn, Depends(process_token)]):
  with sqlite3.connect('users.db') as conn:
    cursor = conn.cursor()
    cred_data = cursor.execute(f"SELECT password FROM {db} WHERE credid='{credid}';").fetchone()
    columns = [x[0] for x in cursor.description]
    cred_data = map_list_to_dict(cred_data, columns)
  return {credid: cred_data}
