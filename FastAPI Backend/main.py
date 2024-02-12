from fastapi import FastAPI
import sqlite3
import datetime

conn = sqlite3.connect("users.db")
crsr = conn.cursor()

crsr.execute("""CREATE TABLE IF NOT EXISTS users (
             username VARCHAR(255) NOT NULL,
             password VARCHAR(30) NOT NULL,
             date_created DATE
             
);""")
crsr.execute("INSERT INTO users VALUES ('Aly','supersecretpassword'),('Joel',verysecretvarn)")
conn.commit()


app = FastAPI()

@app.get("/")
async def read_root():
  return {"Hello": "JOJO"}

@app.post("/api/users")    #
async def add_user(record: Record):
  crsr = conn.cursor()
  crsr.execute(f"INSERT INTO users VALUES (?,?,{datetime.date})", record)
  conn.commit()
  return {"msg": "Record successfully added"}

@app.get("/api/users/{username}")  #get info by username
async def find_user(username):
  crsr = conn.cursor()
  crsr.execute(f"SELECT * FROM users WHERE username={username}")
  return crsr.fetchall()
