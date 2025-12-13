import sqlite3
import hashlib

db_name = "credentials.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS Credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT
            )''')

conn.commit()

def add_user(login, password, full_name=None):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""INSERT INTO Credentials (login, password, full_name) VALUES (?, ?, ?)
            """, (login, password_hash, full_name))
    conn.commit()

def update_password(login, new_password):
    new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute("""UPDATE Credentials SET password = ? WHERE login = ?""", (new_password_hash, login))
    conn.commit()

def authentication_check(login, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    row = cursor.execute("""SELECT password FROM Credentials WHERE login = ?""", (login,)).fetchone()

    if row is None:
        print("Authorization failed!")
        return
    stored_hash = row[0]

    if stored_hash == password_hash:
        print("Authorization successful!")
    else:
        print("Authorization failed!")

if __name__ == "__main__":
    add_user("admin", "admin")
    add_user("qwerty", "1234")
    update_password("qwerty", "H4rD_PasSw0rd")
    inp_password = input("Введіть пароль для admin:")
    authentication_check("admin", inp_password)
    
    conn.close()



