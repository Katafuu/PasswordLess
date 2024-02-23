from fastapi import FastAPI, Depends, HTTPException, status
import sqlite3
from datetime import timedelta, datetime, timezone
from models import UserBase, UserInDB, UserIn, UserOut, Credential, Token
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = "5b0cebd0127a1eb2b06333f7dd133e69686b36fab502ba8c0225a20e7c0b6330"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def createtables():  
  conn = sqlite3.connect("users.db")
  crsr = conn.cursor()

  crsr.execute("""CREATE TABLE IF NOT EXISTS users (
              uid CHAR(36) NOT NULL,
              email VARCHAR(255) PRIMARY KEY NOT NULL,
              username VARCHAR(255) NOT NULL,
              password VARCHAR(30) NOT NULL,
              date_created CHAR(8)
  );""")
  # crsr.execute("INSERT INTO users VALUES ('f3d9804a-a019-4b02-8823-42a2bff141a7','Aly@gmail.com','Aly','supersecretpwd','20/20/20'),('e6f35720-cbca-4975-926f-548f1dfd77ff','Joel@gmail.com','Joel','varunisthe123+4','20/20/20')")
  crsr.execute("""CREATE TABLE IF NOT EXISTS credentials (
               credid CHAR(36) PRIMARY KEY NOT NULL,
               uid CHAR(36) NOT NULL,
               site VARCHAR(255) NOT NULL,
               username VARCHAR(255),
               password VARCHAR(255) NOT NULL,
               date_added CHAR(8),
               FOREIGN KEY (uid) REFERENCES users (uid) 

  );""")
  conn.commit()
  conn.close()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()
origins = [
    "http://passwordless.duckdns.org",
    "http://www.passwordless.duckdns.org",
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
  fields = UserInDB.__fields__
  kwargs = dict(zip(fields,data))
  return UserInDB(**kwargs)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # returns True or False by hashing the plain pass then comparing with the hashed pass

def hash_password(password):
   return pwd_context.hash(password)

def get_user_by_email(email):
  with sqlite3.connect("users.db") as conn:
    try:
      user = conn.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchone()
      user = convert_list_to_userindbmodel(user)
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
    print(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def process_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/addUser", status_code=201) #create new user account
async def add_user(user: UserIn):
  user.password = hash_password(user.password)
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO users VALUES('{user.uid}','{user.email}','{user.username}','{user.password}','{user.date_created}')")
    conn.commit()
    return {"message":f"user{user.uid}successfully added", "name":{user.username}}

@app.post("/token")
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
  return {"access_token":access_token, "token_type":"bearer"}
    
@app.get("/users/config", response_model=UserOut)
async def read_me(current_user: Annotated[UserOut, Depends(process_token)]):
   return current_user


@app.get("/")
async def read_root():
  return {"message": "Server is operational"}


@app.get("/users/userbyID")  #get info by UID
async def find_user(ID: str):
  with sqlite3.connect("users.db") as conn:
    result = conn.execute(f"SELECT * FROM users WHERE uid = '{ID}'").fetchall()
    if result:
      result = dict(ID=result[0][0], username=result[0][1],password=result[0][2], date = result[0][3])
    else:
      result = {"errormsg":"user not found"}
  return result

@app.get("/users/getAll")
async def getall():
  with sqlite3.connect('users.db') as conn:
    return conn.execute(f"SELECT * FROM users").fetchall()   

@app.post("/addCred")
async def addCred(cred: Annotated[Credential, Depends(process_token)]):
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO credentials VALUES('{cred.credid}','{cred.uid}','{cred.site}','{cred.email}','{cred.username}',{cred.password},{cred.date_added})")
    conn.commit()
  return {"response": "success", "username": cred.username, "site": cred.site}

@app.get("/getCredsbyUID")
async def getCreds(uid: Annotated[str, Depends(process_token)]):
  with sqlite3.connect("users.db") as conn:
    creds = conn.execute(f"SELECT * FROM credentials WHERE uid = '{uid}'").fetchall()
    conn.commit()
  return creds

@app.get("/cleardb")
async def cleardb():
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"DELETE FROM users")
    conn.commit()
  return("successfully cleared db")


