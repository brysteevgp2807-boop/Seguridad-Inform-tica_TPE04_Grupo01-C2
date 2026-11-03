
from flask import Flask, request, render_template
from database import crear_tabla, conectar

app = Flask(__name__)

crear_tabla()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]

    conexion = conectar()
    cursor = conexion.cursor()

    # Consulta vulnerable para laboratorio:
    consulta = (
        "SELECT * FROM usuarios WHERE usuario = '"
        + usuario
        + "' AND password = '"
        + password
        + "'"
    )

    try:
        cursor.execute(consulta)
        resultado = cursor.fetchone()
    except Exception:
        resultado = None
    finally:
        conexion.close()

    if resultado:
        return "Acceso concedido: " + resultado[1]

    return "Usuario o contraseña incorrectos"

if __name__ == "__main__":
    app.run(debug=True)
