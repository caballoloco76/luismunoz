from flask import Flask, render_template, request, redirect
from datetime import datetime
import psycopg2
import os

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL (Render la inyecta como variable de entorno)
DB_URL = os.environ.get('DATABASE_URL')

def guardar_reserva(nombre, telefono, email, vehiculo_interes, vehiculo_permuta):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservas (nombre, telefono, email, vehiculo_interes, vehiculo_permuta, fecha_envio)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, telefono, email, vehiculo_interes, vehiculo_permuta, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        vehiculo_interes = request.form.get("vehiculo")
        vehiculo_permuta = request.form.get("permuta")
        guardar_reserva(nombre, telefono, email, vehiculo_interes, vehiculo_permuta)
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
