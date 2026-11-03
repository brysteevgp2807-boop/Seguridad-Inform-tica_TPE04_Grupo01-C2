
import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash

def conectar():
    return sqlite3.connect("usuarios.db")

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        SELECT id FROM usuarios WHERE usuario = ?
    """, ("admin",))

    admin = cursor.fetchone()

    if not admin:
        print("Configuración inicial del administrador")
        password = getpass("Ingrese una contraseña segura: ")

        if len(password) < 12:
            conexion.close()
            raise ValueError("La contraseña debe tener al menos 12 caracteres.")

        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (?, ?)
        """, ("admin", password_hash))

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tabla()
    print("Base de datos configurada correctamente.")
