from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Determinar la URL de la base de datos
database_url = os.getenv("DATABASE_URL")
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videojuegos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    piezas = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Crear tablas SIEMPRE al iniciar la app, dentro del contexto de Flask
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    juegos = Videojuego.query.all()
    return render_template('index.html', juegos=juegos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo_juego = Videojuego(
        titulo=request.form['titulo'],
        plataforma=request.form['plataforma'],
        piezas=request.form['piezas'],
        precio=request.form['precio']
    )
    db.session.add(nuevo_juego)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    juego = Videojuego.query.get_or_404(id)
    db.session.delete(juego)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    juego = Videojuego.query.get_or_404(id)
    juego.titulo = request.form['titulo']
    juego.plataforma = request.form['plataforma']
    juego.piezas = request.form['piezas']
    juego.precio = request.form['precio']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

