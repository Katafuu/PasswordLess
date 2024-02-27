import uvicorn

keydir = "D:/Projects/Passwordless/Website/FastAPI-Backend/localkey.pem"
certdir = "D:/Projects/Passwordless/Website/FastAPI-Backend/localcert.pem"
if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", ssl_certfile=certdir, ssl_keyfile=keydir)
# uvicorn main:app --host 0.0.0.0 --ssl-keyfile D:/Projects/Passwordless/Website/FastAPI-Backend/localkey.pem --ssl-certfile D:/Projects/Passwordless/Website/FastAPI-Backend/localcert.pemcert.pem 