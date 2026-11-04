from pathlib import Path
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "laboratorio.db"
app = Flask(__name__)
app.config["SECRET_KEY"] = "CAMBIAR-ESTA-CLAVE-EN-PRODUCCION"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
def get_db():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; return conn
def init_db():
    with get_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL UNIQUE, clave TEXT NOT NULL, rol TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, categoria TEXT NOT NULL, precio REAL NOT NULL)")
        if conn.execute("SELECT COUNT(*) n FROM usuarios").fetchone()["n"] == 0:
            conn.executemany("INSERT INTO usuarios(usuario,clave,rol) VALUES(?,?,?)", [("admin","Admin123!","administrador"),("carlos","Clase123!","usuario"),("luly","Prueba123!","usuario")])
        if conn.execute("SELECT COUNT(*) n FROM productos").fetchone()["n"] == 0:
            conn.executemany("INSERT INTO productos(nombre,categoria,precio) VALUES(?,?,?)", [("Laptop","Computacion",650),("Teclado","Accesorios",22.5),("Mouse","Accesorios",12),("Monitor","Computacion",180)])
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "usuario" not in session: abort(403)
        return view(*args, **kwargs)
    return wrapped
@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"]="nosniff"; response.headers["X-Frame-Options"]="DENY"; response.headers["Referrer-Policy"]="strict-origin-when-cross-origin"; return response
@app.route("/")
def index(): return render_template("index.html")
@app.route("/login-vulnerable", methods=["GET","POST"])
def login_vulnerable():
    resultado=None; consulta_mostrada=None
    if request.method=="POST":
        usuario=request.form.get("usuario",""); clave=request.form.get("clave","")
        consulta="SELECT id, usuario, rol FROM usuarios WHERE usuario = '%s' AND clave = '%s'" % (usuario,clave)
        consulta_mostrada=consulta
        try:
            with get_db() as conn: fila=conn.execute(consulta).fetchone()
            resultado=("ACCESO CONCEDIDO (demostración vulnerable) — usuario devuelto: "+fila["usuario"]) if fila else "Acceso denegado"
        except sqlite3.Error as exc: resultado=f"Error SQL de demostración: {exc}"
    return render_template("login.html",modo="vulnerable",resultado=resultado,consulta=consulta_mostrada)
@app.route("/login-seguro", methods=["GET","POST"])
def login_seguro():
    resultado=None
    if request.method=="POST":
        usuario=request.form.get("usuario","").strip(); clave=request.form.get("clave","")
        if not usuario or not clave: resultado="Debe completar ambos campos."
        else:
            sql="SELECT id, usuario, rol FROM usuarios WHERE usuario = ? AND clave = ?"
            with get_db() as conn: fila=conn.execute(sql,(usuario,clave)).fetchone()
            if fila:
                session["usuario"]=fila["usuario"]; session["rol"]=fila["rol"]; resultado=f"Acceso concedido. Bienvenido, {fila['usuario']}."
            else: resultado="Acceso denegado: credenciales incorrectas."
    return render_template("login.html",modo="seguro",resultado=resultado,consulta=None)
@app.route("/salir")
def salir(): session.clear(); flash("Sesión cerrada."); return redirect(url_for("index"))
@app.route("/buscar-vulnerable",methods=["GET","POST"])
def buscar_vulnerable():
    productos=[]; consulta=None; error=None; termino=""
    if request.method=="POST":
        termino=request.form.get("termino",""); consulta="SELECT * FROM productos WHERE nombre LIKE '%%%s%%'" % termino
        try:
            with get_db() as conn: productos=conn.execute(consulta).fetchall()
        except sqlite3.Error as exc: error=str(exc)
    return render_template("buscar.html",modo="vulnerable",productos=productos,consulta=consulta,error=error,termino=termino)
@app.route("/buscar-seguro",methods=["GET","POST"])
def buscar_seguro():
    productos=[]; termino=""
    if request.method=="POST":
        termino=request.form.get("termino","").strip()
        with get_db() as conn: productos=conn.execute("SELECT * FROM productos WHERE nombre LIKE ?",(f"%{termino}%",)).fetchall()
    return render_template("buscar.html",modo="seguro",productos=productos,consulta=None,error=None,termino=termino)
@app.route("/panel")
@login_required
def panel(): return render_template("panel.html",usuario=session["usuario"],rol=session.get("rol"))
@app.route("/prueba-xss",methods=["GET","POST"])
def prueba_xss():
    entrada=request.form.get("texto","") if request.method=="POST" else ""
    return render_template("xss.html",entrada=entrada)
@app.errorhandler(403)
def forbidden(_error): return render_template("error.html",codigo=403,mensaje="Acceso prohibido. Inicia sesión con una cuenta válida."),403
@app.errorhandler(404)
def not_found(_error): return render_template("error.html",codigo=404,mensaje="La página solicitada no existe."),404
if __name__=="__main__":
    init_db(); app.run(host="127.0.0.1",port=5000,debug=False)
