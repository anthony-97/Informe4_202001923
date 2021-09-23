from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from usuario import Usuario
from publicacion import Publicacion
import sqlite3

miconexion=sqlite3.connect("Profesores")
micursor=miconexion.cursor()
#micursor.execute("CREATE TABLE PROFESORES (NOMBRE VARCHAR(400))")
micursor.execute("INSERT INTO PROFESORES VALUES('Carlos Alberto Molina Jerez')")
micursor.execute("INSERT INTO PROFESORES VALUES('Luis Alberto Lopez Marquez')")
micursor.execute("INSERT INTO PROFESORES VALUES('Gerson Melciades Estrada Cabrera')")
micursor.execute("INSERT INTO PROFESORES VALUES('Alicia Estefany Garcia Aguilar')")
micursor.execute("INSERT INTO PROFESORES VALUES('Juan Federico Martinez Pelaez')")
micursor.execute("INSERT INTO PROFESORES VALUES('Mariana Andrea del Cid')")
micursor.execute("INSERT INTO PROFESORES VALUES('Mario Alfredo Valle Martinez')")
micursor.execute("INSERT INTO PROFESORES VALUES('Luz Maria Rogel Nimajuan')")
micursor.execute("INSERT INTO PROFESORES VALUES('Antonio Javier Galvez Perez')")

micursor.execute("SELECT * FROM PROFESORES")
varios=micursor.fetchall()
miconexion.commit()
miconexion.close()

app = Flask(__name__)
CORS(app)

administrador = {
    "nombres":"Anthony Alexander",
    "apellidos":"Aquino Santiago",
    "carnet":"202001923",
    "contrasena":"admin"
}

usuarios = []
publicaciones = []


@app.route('/', methods=['GET'])
def principal():
    return "API Informe 4 Prácticas Iniciales"

@app.route('/registro_usuario', methods=['POST'])
def registro_usuario():
    cuerpo = request.get_json()
    carnet = cuerpo['carnet'] 
    nombres = cuerpo['nombres']
    apellidos = cuerpo['apellidos']
    contrasena = cuerpo['contrasena']
    correo = cuerpo['correo']
    nuevo_usuario = Usuario(carnet,nombres,apellidos,contrasena,correo)
    global usuarios
    usuarios.append(nuevo_usuario)
    return jsonify({'agregado':1,'mensaje':'Registro exitoso'})

@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    json_usuarios = []
    global usuarios
    for usuario in usuarios:
        json_usuarios.append(usuario.get_json())
    return jsonify(json_usuarios)


@app.route('/editar_usuario', methods=['POST'])
def editar_usuario():
    cuerpo = request.get_json()
    carnet = cuerpo['carnet'] 
    contrasena = cuerpo['contrasena']
    contador=0
    global usuarios
    for u in usuarios:
        if u.carnet == carnet:
            break
        contador+=1
    usuarios[contador].recuperar(carnet,contrasena)
    return jsonify(usuarios[contador].get_json())

def verificar_contrasena(carnet, contrasena):
    if carnet == administrador['carnet'] and contrasena == administrador['contrasena']:
        return 1
    global usuarios
    for usuario in usuarios:
        if usuario.carnet == carnet and usuario.contrasena == contrasena:
            return 2
    return 0

@app.route('/login', methods=['GET'])
def login():
    carnet = request.args.get("carnet")
    contrasena = request.args.get("contrasena")
    if not existe_usuario(carnet):
        return jsonify({'estado': -1,'mensaje':'No existe este usuario'})
    sesion = verificar_contrasena(carnet,contrasena)
    if sesion == 1 or 2 or 0:
        return jsonify({'estado': 1, 'sesion': sesion, 'mensaje':'Login exitoso','indice': get_indice_usuario(carnet), 'nombres': get_nombre(carnet)})
    return jsonify({'estado': 0, 'sesion': sesion,'mensaje':'La contrasena es incorrecta'})

def get_indice_usuario(carnet):
    for i in range(len(usuarios)):
        if usuarios[i].carnet == carnet:
            return i
    return -1

def get_nombre(carnet):
    for i in range(len(usuarios)):
        if usuarios[i].carnet == carnet:
            return usuarios[i].nombres
    return -1

def existe_usuario(carnet):
    if carnet == administrador['carnet']:
        return True
    global usuarios
    for usuario in usuarios:
        if usuario.carnet == carnet:
            return True
    return False

@app.route('/restablecer_usuario', methods=['GET'])
def restablecer_usuario():
    carnet = request.args.get("carnet")
    correo = request.args.get("correo")
    for usuario in usuarios:
        if usuario.carnet == carnet and usuario.correo == correo:
            return jsonify({'encontrado':1,'usuario': usuario.nombres,'mensaje':'Usuario encontrado'})
            break
        else:
            return jsonify({'encontrado':0, 'mensaje':'Usuario no encontrado'})

@app.route('/obtener_publicaciones', methods=['GET'])
def obtener_publicaciones():
    json_citas = []
    global citas
    for publicacion in publicaciones:
        json_citas.append(publicacion.get_json())
    return jsonify(json_citas)

@app.route('/crear_publicacion', methods=['POST'])
def crear_publicacion():
    cuerpo = request.get_json()
    autor = cuerpo['autor']
    fecha = cuerpo['fecha']
    hora = cuerpo['hora']
    curso = cuerpo['curso'] 
    profesor = cuerpo['profesor']
    mensaje = cuerpo['mensaje']
    nueva_publicacion = Publicacion(autor,fecha,hora,curso,profesor,mensaje)
    global citas
    publicaciones.append(nueva_publicacion)
    return jsonify({'agregado':1,'mensaje':'Publicada exitosamente'})

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)