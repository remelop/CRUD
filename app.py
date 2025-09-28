from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="desarrollo_web"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['POST'])
def add():
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)", (nombre, precio, cantidad))
    db.commit()
    flash('Producto agregado correctamente')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cursor.execute("UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
                   (nombre, precio, cantidad, id))
    db.commit()
    flash('Producto actualizado correctamente')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    db.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
