import sqlite3

# this class streamlines interfacing with a sqlite database file
class DatabaseHelper(object):

    # connects to input database file
    def __init__(self, database_file):
        self.db = sqlite3.connect(database_file)
        self.cursor = self.db.cursor()

    # creates a new table with fields email, first name, and last name
    # adds some default users
    def create_users_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                first TEXT NOT NULL,
                last TEXT NOT NULl,
                email TEXT NOT NULL UNIQUE PRIMARY KEY
            )
            """
        )
        self.cursor.execute(
            """
            INSERT INTO users (email, first, last)
            VALUES
                ("test@test.com", "John", "McTest"),
                ("sif@anorlondo.com", "Knight", "Artorias"),
                ("crystals@dragonschool.edu", "Big Hat", "Logan")
            """
        )
        self.db.commit()

    # returns a tuple containing the result of running command on db with arguments
    def query(self, command, *args):
        return self.cursor.execute(command, args).fetchall()

    # inserts args into database using command
    def insert(self, command, *args):
        self.cursor.execute(command, args)
        self.db.commit()