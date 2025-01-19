import sqlite3 #1
con = sqlite3.connect('database.db',  check_same_thread=False)
cur = con.cursor()

class Database:
    def __init__(self):
        db_file ='database.db'

        conn = sqlite3.connect('database.db')
        self.connection = con
        self.cursor = self.connection.cursor()









    def user_exists(self, username):
            with self.connection:
                result = self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,)).fetchall()

                return bool(len(result))
    def select_hash(self, username):
        with self.connection:

            return self.cursor.execute("SELECT * FROM session WHERE username = ?",(username,)).fetchone()
    def get_tie(self):

        with self.connection:
            return self.cursor.execute('SELECT * FROM tie').fetchall()

















    def load_tie(self, name):
        with self.connection:
            return self.cursor.execute("SELECT * FROM tie WHERE name = ?",(name,)).fetchone()

    def load_shop(self, username):
        with self.connection:
            return self.cursor.execute("SELECT shop FROM users WHERE username = ?",(username,)).fetchone()

    def get_username(self, hash):
        with self.connection:
            return self.cursor.execute("SELECT username FROM session WHERE hash = ?",(hash,)).fetchone()[0]
    def load_tie_id(self, id):
        with self.connection:






            return self.cursor.execute("SELECT * FROM tie WHERE id = ?", (id,)).fetchone()
    def load_all(self, username):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE username = ?",(username, )).fetchone()

    def update_shop(self, username, card):
        with self.connection:

            self.cursor.execute("UPDATE users SET shop = ? WHERE username = ?", (card, username,))


    def select_mail(self, mail):

        with self.connection:

            return self.cursor.execute("SELECT username FROM users WHERE mail = ?", (mail,)).fetchone()
    def select_mail1(self, mail):
        with self.connection:

            return self.cursor.execute("SELECT mail FROM code WHERE mail = ?", (mail,)).fetchone()
    def registry_code(self, username, code, mail, password, data):

        with self.connection:
            self.cursor.execute("INSERT INTO code (username, code, mail, password, data) VALUES (?, ?, ?, ?, ?)",

                                   (username, code, mail, password, data))
    def select_password_code(self, username, code, mail):
        with self.connection:

            return self.cursor.execute("SELECT password FROM code WHERE username = ? AND code = ? AND mail = ?", (username, code, mail)).fetchone()
    def registry_user(self, username, password, mail):
        with self.connection:

            self.cursor.execute("DELETE FROM code WHERE username = ?", (username,))
            self. cursor.execute("INSERT INTO users (username, password, mail) VALUES (?, ?, ?)",(username, password, mail))


    def registry_hash(self, hash, exp,username):


            with self.connection:
                self.cursor.execute("INSERT INTO session (hash, exp, username) VALUES (?, ?, ?)",(hash,exp,username,))


    def password(self, username, password):
        with self.connection:




            return self.cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password,)).fetchone()



    def get_sessions(self, username):

        with self.connection:
            return self.cursor.execute("SELECT * FROM sessions WHERE username = ?",(username,)).fetchone()

    def check_comment(self, msg):
        with self.connection:
            return self.cursor.execute("SELECT * FROM sessions WHERE message = ?",(msg,)).fetchone()

    def registry_buy(self, msg, username):
        with self.connection:

            self.cursor.execute("INSERT OR IGNORE INTO sessions (message, username) VALUES (?,?)",(msg, username))
    def get_hash(self, hash):

        with self.connection:
            return self.cursor.execute("SELECT * FROM session WHERE hash = ?",(hash,)).fetchone()














    def load_hash(self, username):
        with self.connection:
            return self.cursor.execute("SELECT hash FROM session WHERE username = ?",(username,)).fetchone()