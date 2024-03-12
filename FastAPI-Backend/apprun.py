import uvicorn, os

currentdir = os.path.dirname(os.path.realpath(__file__))
keydir = currentdir+"/localkey.pem"
certdir = currentdir+"/localcert.pem"

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", ssl_certfile=certdir, ssl_keyfile=keydir, reload=True)
# uvicorn main:app --host 0.0.0.0 --ssl-keyfile D:/Projects/Passwordless/Website/FastAPI-Backend/localkey.pem --ssl-certfile D:/Projects/Passwordless/Website/FastAPI-Backend/localcert.pemcert.pem 