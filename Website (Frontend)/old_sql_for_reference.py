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
      print(cred["password"], type(cred["password"]))
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