import sqlite3
def createtables():
  conn = sqlite3.connect("users.db")
  crsr = conn.cursor()

  crsr.execute("""CREATE TABLE IF NOT EXISTS users (
              uid CHAR(36) NOT NULL,
              email VARCHAR(255) PRIMARY KEY NOT NULL,
              username VARCHAR(255) NOT NULL,
              date_created CHAR(8),
              hashed_password VARCHAR(255) NOT NULL
  );""")
  # crsr.execute("INSERT INTO users VALUES ('f3d9804a-a019-4b02-8823-42a2bff141a7','Aly@gmail.com','Aly','supersecretpwd','20/20/20'),('e6f35720-cbca-4975-926f-548f1dfd77ff','Joel@gmail.com','Joel','varunisthe123+4','20/20/20')")
  crsr.execute("""CREATE TABLE IF NOT EXISTS credentials (
               credid CHAR(36) PRIMARY KEY NOT NULL,
               uid CHAR(36) NOT NULL,
               site VARCHAR(255) NOT NULL,
               username VARCHAR(255),
               email VARCHAR(255),
               password VARCHAR(255) NOT NULL,
               date_added CHAR(8),
               old BOOLEAN,
               FOREIGN KEY (uid) REFERENCES users (uid) 

  );""")
  conn.commit()
  conn.close()
createtables()