from fastapi import FastAPI
import sqlite3
# import datetime  for future use once everything is working
from uuid import UUID,uuid4
from models import User

def createtable():  
  conn = sqlite3.connect("users.db")
  crsr = conn.cursor()

  crsr.execute("""CREATE TABLE IF NOT EXISTS users (
              uid CHAR(36),
              email VARCHAR(255),
              username VARCHAR(255) NOT NULL,
              password VARCHAR(30) NOT NULL,
              date_created CHAR(8)
  );""")
  crsr.execute("INSERT INTO users VALUES ('f3d9804a-a019-4b02-8823-42a2bff141a7','Aly@gmail.com','Aly','supersecretpwd','20/20/20'),('e6f35720-cbca-4975-926f-548f1dfd77ff','Joel@gmail.com','Joel','varunisthe123+4','20/20/20')")
  conn.commit()
  conn.close()
app = FastAPI()

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
    conn.execute(f"INSERT INTO users VALUES({user.uid},{user.email},{user.username},{user.password}")
    conn.commit()
  return {"message":f"user{user.uid}successfully added", "name":{user.username}}

@app.post("/users/loginUser")
async def checkUserDetails(user: User):
  with sqlite3.connect("users.db") as conn:
    personExists = conn.execute(f"SELECT * FROM users WHERE email = {user.email} AND password = {user.password}").fetchall()
    if personExists:
      return {"response":"user details correct"}
    else:
      return {"response":"user details incorrect or does not exist"}