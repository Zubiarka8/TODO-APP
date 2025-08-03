from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3


    
app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def obtener_conexion():
    conexion = sqlite3.connect("tareas.db")
    conexion.row_factory = sqlite3.Row
    return conexion


# Función para inicializar la base de datos (crear la tabla si no existe)
def inicializar_db():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conexion.commit()
    conexion.close()

@app.route("/api/tareas", methods=["GET"])
def api_obtener_tareas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas").fetchall()
    conexion.close()
    return jsonify([dict(tarea) for tarea in tareas])

@app.route("/api/pendientes", methods=["GET"])
def api_obtener_pendientes():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas WHERE done = 0").fetchall()
    conexion.close()
    return jsonify([dict(tarea) for tarea in tareas])

@app.route("/api/completadas", methods=["GET"])
def api_obtener_completadas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas WHERE done = 1").fetchall()
    conexion.close()
    return jsonify([dict(tarea) for tarea in tareas])

# Rutas para renderizar plantillas HTML
@app.route("/", methods=["GET"])
def index():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas").fetchall()
    conexion.close()
    return render_template("index.html", tareas=tareas, title="Todas las Tareas")

@app.route("/pendientes", methods=["GET"])
def pendientes():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas WHERE done = 0").fetchall()
    conexion.close()
    return render_template("index.html", tareas=tareas, title="Tareas Pendientes")

@app.route("/realizadas", methods=["GET"])
def realizadas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tareas WHERE done = 1").fetchall()
    conexion.close()
    return render_template("index.html", tareas=tareas, title="Tareas Realizadas")

# Ruta para agregar una nueva tarea
@app.route("/add", methods=["POST"])
def add_tarea():
    titulo = request.form.get("title")
    if titulo:
        conexion = obtener_conexion()
        conexion.execute("INSERT INTO tareas (title, done) VALUES (?, ?)", (titulo, 0))
        conexion.commit()
        conexion.close()
    return redirect( request.referrer or url_for('index'))

# Ruta para marcar una tarea como completada
@app.route("/hecha/<int:id>")
def marcar_hecha(id):
    conexion = obtener_conexion()
    conexion.execute("UPDATE tareas SET done = 1 WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    return redirect(request.referrer or url_for('index'))

# Ruta para eliminar una tarea 
@app.route("/eliminar/<int:id>")
def eliminar_tarea(id):
    conexion = obtener_conexion()
    conexion.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    # Redirige a la página principal
    return redirect(request.referrer or url_for('index'))

# app.run(debug=True, port=5002)