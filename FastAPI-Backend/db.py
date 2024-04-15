from sqlmodel import SQLModel, create_engine, Session, select, or_, col # col used to say that an expression is a db column rather than a standard python model
from models import *
from passlib.context import CryptContext



DATABASE_URL = "sqlite:///dbtest.db"
engine = create_engine(DATABASE_URL) #echo makes it print whenever it executes for learning
# engine will be imported elsewhere for CRUD

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db():
  SQLModel.metadata.create_all(engine)

def create_mock_data():
   with Session(engine) as db:
    user = UserInDB(email="user@gmail.com", username="katafu", hashed_password="blacblach.hashed#,")
    credential = CredentialInDB(site="site.com", username="katafucred1", email="cred@gmail.com", password="secret")
    db.add(user)
    db.commit()
    db.refresh(user)
    credential.owner_id = user.id
    db.add(credential)
    db.commit()
    db.refresh(credential)

  
    old_cred = oldCredential(owner_id=user.id, credid=credential.id, site="siteold.com", username="katafucred0", email="credold@gmail.com", password="secretold")

  
    db.add(old_cred)

    db.commit()



def main():
  create_db()
  # create_mock_data()

def get_user_by_email(email: str):
  with Session(engine) as db:
    select_statemenet = select(UserInDB).where(UserInDB.email == email)
    user = db.exec(select_statemenet).first()
    return user

def get_user_by_id(id: int):
  with Session(engine) as db:
    user = db.get(UserInDB, id)
    return user

def get_creds(current_user: UserIn):
  with Session(engine) as db:
    result = db.exec(select(CredentialInDB).where(CredentialInDB.owner_id == current_user.id)).all()
    creds = []
    for cred in result:
      cred.password = "******"
      cred = CredentialOut(**cred.model_dump())
      creds.append(cred)
    return creds
  
def get_old_creds_byid(id: int, uid: int):
  with Session(engine) as db:
    result = db.exec(select(oldCredential).where(oldCredential.credid == CredentialInDB.id).where(CredentialInDB.owner_id == id)).all()
    for x in result:
      print("X:---")
      print(x, type(x))
    creds = []
    for cred in result:
      cred.password = "******"
      cred = oldCredOut(**cred.model_dump())
      creds.append(cred)
    return creds

def add_user(user: UserInDB):
  with Session(engine) as db:
    hashedPwd = pwd_context.hash(user.password)
    newUser = UserInDB(email=user.email, username=user.username, hashed_password=hashedPwd)
    db.add(newUser)
    db.commit()
    return {"success":"user added"}

def add_cred(newCred: CredentialIn, id: int):
  with Session(engine) as db:
    newCred = CredentialInDB(**newCred.model_dump(), owner_id=id)
    try:
      db.add(newCred)
      db.commit()
    except Exception as e:
      return {"error": "user already exists", "response":e}
    return {"success": "new credential added"}

def modify_cred(updCred: CredentialIn):
  with Session(engine) as db:
    cred = db.exec(select(CredentialInDB).where(CredentialInDB.id == updCred.id)).one()
    if cred.username == updCred.username and cred.email == updCred.email and cred.password == updCred.password and cred.site == updCred.site:
      return {"error": "duplication-error, no changes made"}
    
    
    oldCred = cred.model_dump()
    del oldCred['id'] # ensuring id is empty so that it generates a new unique id in the db
    oldCred = oldCredential(**oldCred, credid=cred.id, date_removed=get_date()) #saving old credential
    oldCred.password = str(AES_encrypt(oldCred.password))
    db.add(oldCred)

    cred.site = updCred.site
    cred.username = updCred.username
    cred.email = updCred.email
    cred.password = updCred.password
    db.add(cred)
    db.commit()

    db.refresh(oldCred)
    db.refresh(cred)
    return {'success': 'data-updated', 'old':oldCred, 'new':cred}


def delete_cred(credid: int, old:bool):
  if old:
    model = oldCredential
  else:
    model = CredentialInDB
  with Session(engine) as db:
    toDelete = db.exec(select(model).where(model.id == credid)).one()
    db.delete(toDelete)
    db.commit()
    

    stillExists = db.exec(select(model).where(model.id == credid)).first() #first returns None instead of error
    if stillExists is None:
      return {"success": "deleted credential", "site": toDelete.site, "email": toDelete.email}
    return {"error": "credential not deleted"}

def get_password(model, credid: int):
  with Session(engine) as db:
    return db.exec(select(model.password).where(model.id == credid)).one()
  
def get_site_cred(siteurl: str):
  with Session(engine) as db:
    return db.exec(select(CredentialInDB).where(CredentialInDB.site == siteurl)).all()

if __name__ == "__main__": # run this file to create DB using engine. using if statement to prevent it from running when engine is imported
  main()


