from fastapi import FastAPI
import sqlite3
# import datetime | for future use once everything is working
from uuid import UUID,uuid4
from models import User
from fastapi.middleware.cors import CORSMiddleware

def createtables():  
  conn = sqlite3.connect("users.db")
  crsr = conn.cursor()

  crsr.execute("""CREATE TABLE IF NOT EXISTS users (
              uid CHAR(36),
              email VARCHAR(255),
              username VARCHAR(255) NOT NULL,
              password VARCHAR(30) NOT NULL,
              date_created CHAR(8)
  );""")
  # crsr.execute("INSERT INTO users VALUES ('f3d9804a-a019-4b02-8823-42a2bff141a7','Aly@gmail.com','Aly','supersecretpwd','20/20/20'),('e6f35720-cbca-4975-926f-548f1dfd77ff','Joel@gmail.com','Joel','varunisthe123+4','20/20/20')")
  crsr.execute("""CREATE TABLE IF NOT EXISTS creds (
               uid CHAR(36),
               site VARCHAR(255),
               username VARCHAR(255),
               password VARCHAR(255)
               date_added CHAR(8)
  )
""")
  conn.commit()
  conn.close()
app = FastAPI()
origins = [
    "http://passwordless.duckdns.org",
    "http://192.168.0.135:8000/"
    "file:///D:/Projects/PasswordLess/Website/loginsignup.html",
    'null'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
  return {"message": "Server is operational"}


@app.get("/users/userbyID")  #get info by UID
async def find_user(ID: str):
  with sqlite3.connect("users.db") as conn:
    result = conn.execute(f"SELECT * FROM users WHERE uid = {ID}").fetchall()
    if result:
      result = dict(ID=result[0][0], username=result[0][1],password=result[0][2], date = result[0][3])
    else:
      result = {"errormsg":"user not found"}
  return result

@app.get("/users/getAll")
async def getall():
  with sqlite3.connect('users.db') as conn:
    return conn.execute(f"SELECT * FROM users").fetchall()


@app.post("/users/addUser") #create new user account
async def add_user(user: User):
  with sqlite3.connect("users.db") as conn:
    conn.execute(f"INSERT INTO users VALUES('{user.uid}','{user.email}','{user.username}','{user.password}','{user.date_created}')")
    conn.commit()
  return {"message":f"user{user.uid}successfully added", "name":{user.username}}

@app.get("/users/loginUser")
async def checkUserDetails(username:str,password:str):
  with sqlite3.connect("users.db") as conn:
    personExists = conn.execute(f"SELECT * FROM users WHERE email = {username} AND password = {password}").fetchall()
    if personExists:
      return {"response":True}
    else:
      return {"response":"user details incorrect or does not exist"}