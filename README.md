Running this program does take some effort and time to setup all the server software and have the files located in the correct places. I HIGHLY reccomend simply accessing https://passwordless.duckdns.org and testing the program there whilst looking at the code on this github page for refernce to see how it works. Alternatively, here are the step-by-step instructions to run this software on your own public domain (because this cannot work when running locally or from files as cookies must be stored).


Step-By-Step guide to put PasswordLess into production on your hardware:
1. ensure you have git installed: refer to https://git-scm.com/downloads
2. download Apache2 server binary: https://www.apachelounge.com/download/VS17/binaries/httpd-2.4.58-240131-win64-VS17.zip
3. Extract Apache2 Folder from zip into C: drive, directory should be 'C:Apache2'
4. in command prompt, write 'cd c:\Apache24\bin', then 'httpd.exe' (this starts apache2)
5. open a command prompt in C:Apache24\htdocs, delete the existing index.html file and run 'git clone https://github.com/Katafuu/PasswordLess_Website C:\Apache24\htdocs'
6. copy the FastAPI-Backend folder from the htdocs folder into a different directory of your choosing, I will be using C:Desktop for this tutorial.
7. open a command prompt into C:Desktop/FastAPI-Backend/ and run './venv/Scripts/python.exe apprun.py'. Green text should appear saying that the server is running
8. now copy the 





