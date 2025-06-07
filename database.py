import sqlite3
from contextlib import contextmanager
from datetime import datetime
import pytz


@contextmanager
def get_connection():
    connection = sqlite3.connect("zet.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bot (id INTEGER PRIMARY KEY, admin TEXT NOT NULL, props TEXT NOT NULL, qr TEXT)''')
    cursor.execute('INSERT OR IGNORE INTO Bot (id, admin, props) VALUES (?, ?, ?)', (1, 'zetadmin', "996100200300"))
    cursor.execute('''CREATE TABLE IF NOT EXISTS Props (id INTEGER PRIMARY KEY, props TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT, xid INTEGER, points INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payments (date TEXT, user_id INTEGER, username TEXT, xid INTEGER, sum INTEGER, method TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Withdraws (date TEXT, user_id INTEGER, username TEXT, xid INTEGER, sum INTEGER, code INTEGER, method TEXT, props TEXT)''')

    try:
        yield connection
        connection.commit() 
    finally:
        connection.close() 


def get_bot_data():
    with get_connection() as conn:
        cursor = conn.cursor()
               
        cursor.execute("SELECT admin, props FROM Bot LIMIT 1")
        row = cursor.fetchone()

        if row:
            cursor.execute("SELECT props FROM Props")
            new_props = [r[0] for r in cursor.fetchall()]

            return {
                "admin": row[0],
                "props": row[1],
                "new_props": new_props,
            }
        else:
            return {"admin": None, "props": None, "new_props": [], "qr": None}


def update_admin(new_admin):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Bot SET admin = ? WHERE id = ?", (new_admin, 1))

def get_props():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, props FROM Props")
        rows = cursor.fetchall()
        return rows

def update_props(new_props):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Bot set props = ? WHERE id = ?", (new_props, 1))

def update_new_props(props_id, new_props):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Props SET props = ? WHERE id = ?", (new_props, props_id))
        
def delete_new_props(props_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Props WHERE id = ?", (props_id,))
  
 
def add_props(news_props):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Props (props) VALUES (?)''', (news_props,))        
        

def get_user_data(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT xid FROM Users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if not result:
         return None
        else:
         return result[0]

def get_username(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if not result:
         return None
        else:
         return result[0]
        
def update_user(user_id: int, username: str, xid: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT xid FROM Users WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if not result:
            cursor.execute(
                "INSERT INTO Users (id, username, xid, points) VALUES (?, ?, ?, ?)",
                (user_id, username, xid, 0)
            )
        else:
            current_xid = result[0]
            if current_xid != xid:
                cursor.execute("UPDATE Users SET xid = ? WHERE id = ?",(xid, user_id))

def update_user_points(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(Users)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'points' not in columns:
            cursor.execute("ALTER TABLE Users ADD COLUMN points INTEGER")
            
        cursor.execute("SELECT points FROM Users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if row is not None:
            current_points = row[0] or 0
            cursor.execute("UPDATE Users SET points = ? WHERE id = ?", (current_points + 1, user_id))
        else:
            print(f"User with id {user_id} not found.")

def get_user_points(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM Users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0]

def check_qr_column():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(BOT)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'qr' not in columns:
            cursor.execute("ALTER TABLE BOT ADD COLUMN qr TEXT")
                
def update_qr(link: str):
    check_qr_column()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE BOT SET qr = ? WHERE id = ?",(link, 1))          
                
def update_payment_history(user_id, username, xid, amount, method):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        tz = pytz.timezone("Asia/Bishkek")
        time = datetime.now(tz)
        date = time.strftime("%d.%m.%Y-%H:%M")         
        cursor.execute("""INSERT INTO Payments (date, user_id, username, xid, sum, method) VALUES (?, ?, ?, ?, ?, ?)""", (date, user_id, username, xid, amount, method))

def delete_payment(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Payments WHERE user_id = ?", (user_id,))

def get_user_payments(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payments WHERE user_id = ?", (user_id,))
        payments = cursor.fetchall()
        return payments

def get_all_payments():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payments")
        payments = cursor.fetchall()  
        return payments         
        
        
def update_withdraw_history(user_id, username, xid, amount, code, method, props):
    with get_connection() as conn:
        cursor = conn.cursor()
        tz = pytz.timezone("Asia/Bishkek")
        time = datetime.now(tz)
        date = time.strftime("%d.%m.%Y-%H:%M")          
        cursor.execute("""INSERT INTO Withdraws (date, user_id, username, xid, sum, code, method, props) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (date, user_id, username, xid, amount, code, method, props))

def delete_withdraw(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Withdraws WHERE user_id = ?", (user_id,))

