import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)
DB_PATH = "laboratorio.db"


def init_db():
    """Inicializa la base de datos de prueba con usuarios y productos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            rol TEXT
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            precio REAL
        )
    """)

    # Cargar datos de prueba si están vacías
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            [('admin', 'admin123', 'Administrador'), ('user1', 'clave2026', 'Usuario')]
        )

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)",
            [('Laptop', 'Computación', 850.00), ('Teclado', 'Accesorios', 25.00), ('Mouse', 'Accesorios', 15.00)]
        )

    conn.commit()
    conn.close()


# Plantilla HTML incrustada para visualización directa
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Laboratorio SQL Injection - UNEMI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background-color: #f4f6f9; }
        .box { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h2 { color: #003366; }
        input[type="text"] { width: 300px; padding: 8px; margin-right: 10px; }
        button { padding: 8px 15px; background-color: #003366; color: white; border: none; border-radius: 4px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Laboratorio de Ciberseguridad: SQL Injection</h1>

    <div class="box">
        <h2>1. Iniciar Sesión (Ruta Vulnerable)</h2>
        <form action="/login_vulnerable" method="POST">
            <input type="text" name="username" placeholder="Usuario (Prueba: ' OR '1'='1)" required>
            <input type="text" name="password" placeholder="Contraseña">
            <button type="submit">Ingresar</button>
        </form>
    </div>

    <div class="box">
        <h2>2. Iniciar Sesión (Ruta Segura - Consulta Parametrizada)</h2>
        <form action="/login_seguro" method="POST">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="text" name="password" placeholder="Contraseña" required>
            <button type="submit">Ingresar de Forma Segura</button>
        </form>
    </div>

    {% if mensaje %}
    <div class="box">
        <h3>Resultado:</h3>
        <p><strong>{{ mensaje }}</strong></p>
        {% if datos %}
            <table>
                <tr>
                    {% for col in columnas %}
                    <th>{{ col }}</th>
                    {% endfor %}
                </tr>
                {% for fila in datos %}
                <tr>
                    {% for val in fila %}
                    <td>{{ val }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


# RUTA VULNERABLE (Concatenación de texto)
@app.route('/login_vulnerable', methods=['POST'])
def login_vulnerable():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # VULNERABILIDAD: Concatenación directa en la consulta SQL
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"

    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        conn.close()

        if resultado:
            return render_template_string(HTML_TEMPLATE, mensaje="¡Ataque exitoso / Autenticado!", datos=resultado,
                                          columnas=['ID', 'Usuario', 'Password', 'Rol'])
        else:
            return render_template_string(HTML_TEMPLATE, mensaje="Credenciales incorrectas.")
    except sqlite3.Error as e:
        return render_template_string(HTML_TEMPLATE, mensaje=f"Error SQL: {e}")


# RUTA SEGURA (Consultas Parametrizadas)
@app.route('/login_seguro', methods=['POST'])
def login_seguro():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    resultado = cursor.fetchall()
    conn.close()

    if resultado:
        return render_template_string(HTML_TEMPLATE, mensaje="Autenticación segura exitosa.", datos=resultado,
                                      columnas=['ID', 'Usuario', 'Password', 'Rol'])
    else:
        return render_template_string(HTML_TEMPLATE, mensaje="Acceso denegado: Entrada neutralizada correctamente.")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)