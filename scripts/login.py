import sys
import sqlite3
import datetime

class Session:
  def __init__(self, username, password):
     self.__LoggedIn = False
     self.username = username
  def accMenu(self):
    menuSelection = input("Welcome to the login portal, please select an option:\n1) Login\n2) Create Account\n")
    while menuSelection not in ["1","2"]:
        menuSelection = input("Welcome to the login portal, please select an option:\n1) Login\n2) Create Account\n")
    if menuSelection == "1":
        self.__login()
    elif menuSelection == "2":
        self.__signup()
    else:
        print("unrecognized input, please select either '1' or '2'")

  def checkNameExists(self,name):
    connection = sqlite3.connect("accounts.db")
    crsr = connection.cursor()
    crsr.execute(f"SELECT name FROM user WHERE username = {name}")
    lst = crsr.fetchall()
    if lst:
        return True
    else:
        return False
    connection.close()
  def addUser(name,pwd):
    datetime.date

  def __signup(self):
      self.username, password = input("Select a username (0 to return):\n"), input("Select a password:\n")
      if self.username == '0':
          self.accMenu()
      else:
        if self.checkNameExists(self.username):
          print("Username already taken, please select another")
          self.login()
        else:
          try:
            self.addUser(self.username,password)
          except:
            print("Error, could not enter account")
  def __login(self):
      self.username, password = input("Enter username:\n"), input("Enter password:\n")
      if self.checkNameExists(self.username):
         self.__LoggedIn = True
      print('byebye')

unam = sys.argv[1]
pwd = sys.argv[2]
session = Session(unam,pwd)
