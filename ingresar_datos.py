import sqlite3

conexion = sqlite3.connect("tareas.db")
cursor = conexion.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tareas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done  BOOLEAN NOT NULL DEFAULT 0
    )
    """
    
)

tareas = [
    ("Aprender Boostrap", False),
    ("Desplegar aplicaion", False),
    ("Crear API REST", True),
    ("Leer documentacion SQLite", False),
    ("Repasar lo aprendido en el webinar", False)
]

cursor.executemany("INSERT INTO tareas (title, done) VALUES (?,?) ", tareas)
conexion.commit()
conexion.close()

print("SE ha realiazado correctamente")