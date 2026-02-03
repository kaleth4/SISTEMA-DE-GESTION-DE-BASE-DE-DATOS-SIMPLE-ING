import sqlite3
import shutil
import os
from datetime import datetime

DB_NAME = "database.db"
BACKUP_DIR = "backup"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            edad INTEGER
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON usuarios(email)")
    conn.commit()
    conn.close()

def add_user():
    nombre = input("Nombre: ")
    email = input("Email: ")
    edad = input("Edad: ")

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, edad) VALUES (?, ?, ?)",
            (nombre, email, edad)
        )
        conn.commit()
        print("✅ Usuario agregado correctamente")
    except sqlite3.IntegrityError:
        print("❌ Error: Email duplicado")
    finally:
        conn.close()

def query_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        print(user)

def backup_db():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{BACKUP_DIR}/database_backup_{timestamp}.db"
    shutil.copy(DB_NAME, backup_name)
    print(f"📦 Backup creado: {backup_name}")

def main():
    create_table()

    while True:
        command = input("\nComando (add user | query | backup | exit): ").lower()

        if command == "add user":
            add_user()
        elif command == "query":
            query_users()
        elif command == "backup":
            backup_db()
        elif command == "exit":
            break
        else:
            print("❌ Comando no reconocido")

if __name__ == "__main__":
    main()
