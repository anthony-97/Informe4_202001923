from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from usuario import Usuario
from publicacion import Publicacion
from random import randint


app = Flask(__name__)
CORS(app)

administrador = {
    "nombres":"Anthony Alexander",
    "apellidos":"Aquino Santiago",
    "carnet":"2020",
    "contrasena":"admin"
}
usuarios = []
publicaciones = []
u1= Usuario("2021","Melany", "Salazar","anthony", "mely123@gmail.com", randint(10,200))
u2= Usuario("202001923","Anthony Alexander", "Aquino Santiago","mel", "anthony97@gmail.com", randint(10,200))
u3= Usuario("2008","Luis", "Morales","polares", "ls@gmail.com", randint(30,200))
usuarios.append(u1)
usuarios.append(u2)
usuarios.append(u3)

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
    nuevo_usuario = Usuario(carnet,nombres,apellidos,contrasena,correo,randint(10,200))
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
    for usuario in usuarios:
        if usuario.carnet == carnet:
            usuario.contrasena = contrasena

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
        return jsonify({'estado': 1, 'sesion': sesion, 'carnet': carnet, 'mensaje':'Login exitoso','indice': get_indice_usuario(carnet), 'nombres': get_nombre(carnet)})
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
    contador=0
    for usuario in usuarios:
        contador+=1
        if str(usuario.carnet) == str(carnet) and str(usuario.correo) == str(correo):
            print("Si")
            return jsonify({'encontrado':1,'usuario': usuario.nombres,'mensaje':'Usuario encontrado'})
        else:
            if contador==len(usuarios):
                return jsonify({'encontrado':0, 'mensaje':'Usuario no encontrado'})
            else:
                continue

@app.route('/obtener_publicaciones', methods=['GET'])
def obtener_publicaciones():
    json_pubs = []
    global publicaciones
    for publicacion in publicaciones:
        json_pubs.append(publicacion.get_json())
    return jsonify(json_pubs)

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
    global publicaciones
    publicaciones.append(nueva_publicacion)
    return jsonify({'agregado':1,'mensaje':'Publicada exitosamente'})

@app.route('/buscar', methods=['GET'])
def buscar():
    carnet = request.args.get("carnet")
    if not existe_usuario(carnet):
        return jsonify({'estado': -1,'mensaje':'No existe este usuario'})
    else:
        encontrado=buscarC(carnet)
        return jsonify({'estado': 1, 'carnet':encontrado[0], 'nombres': encontrado[1], 'apellidos':encontrado[2],'correo':encontrado[3], 'creditos':encontrado[4]})

def buscarC(carnet):
    global usuarios
    print(carnet)
    for usuario in usuarios:
        if usuario.carnet==carnet:
            print("Se encontro")
            json_usuarios=[]
            json_usuarios.append(usuario.carnet)
            json_usuarios.append(usuario.nombres)
            json_usuarios.append(usuario.apellidos)
            json_usuarios.append(usuario.correo)
            json_usuarios.append(str(usuario.creditos))
            print(json_usuarios)
    return json_usuarios


if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)