This setup tested using Python 3.5
Non-standard libraries needed: sqlite3, bottle

The server is capable of adding new users to a database. If a user enters info that is already in the database, they are
not added twice. 

To test, run server.py from the top-level directory, then navigate to 127.0.0.1:8080 in a web browser.