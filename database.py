import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#####",
    database="Journal_Unfiltered"
)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users1(
        id_user INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries1(
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_user INT,
        date DATE,
        text LONGTEXT,
        mood VARCHAR(20),
        keywords VARCHAR(255),
        insight LONGTEXT,
        FOREIGN KEY (id_user) REFERENCES users1(id_user)
    )
    """)
    conn.commit()

# --- User Management ---
def create_user(name, email, password):
    # Hash password and store as string
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode('utf-8')
    cursor.execute(
        "INSERT INTO users1 (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_str)
    )
    conn.commit()

def login_user(email, password):
    cursor.execute("SELECT * FROM users1 WHERE email=%s", (email,))
    user = cursor.fetchone()
    # Encode stored string back to bytes for bcrypt check
    if user and bcrypt.checkpw(password.encode(), user[3].encode('utf-8')):
        return user
    return None

# --- Journal Management ---
def save_entry(id_user, entry_date, text, mood, keywords, insight):
    cursor.execute("""
    INSERT INTO entries1 (id_user, date, text, mood, keywords, insight)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_user, entry_date, text, mood, keywords, insight))
    conn.commit()

def get_entries(id_user):
    cursor.execute("SELECT * FROM entries1 WHERE id_user=%s ORDER BY id DESC", (id_user,))
    return cursor.fetchall()