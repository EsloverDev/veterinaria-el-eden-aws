from flask import render_template, request
from database.db import *
from controller.admin_s3 import *

def func_home_page():
    return render_template("index.html")

def func_register_page():
    return render_template("register.html")
    
def func_consult_page():
    return render_template("consult.html")
    
def func_register_user():
# aquí se hace una petición para que desde el front end se capturen los datos que se están ingresando en el formulario y se guarden en variables; al request.form[] se le debe pasar el nombre del input que está en el documento register.html tal cual como está en el atributo name=""
    mascota = request.form["mascota"]
    propietario = request.form["propietario"]
    tipo_mascota = request.form["tipo_mascota"]
    raza = request.form["raza"]
    sexo = request.form["sexo"]
    edad = request.form["edad"]
# Aquí se hace una petición para capturar el archivo de la foto que el usuario está subiendo en el front end
    foto = request.files["foto"]
    confirm_pet = add_pet(mascota, propietario, tipo_mascota, raza, sexo, edad)
    if confirm_pet:
        s3_resource = connection_s3()
        ruta_foto_local = save_file(foto)
        confirmar_foto = upload_file(s3_resource, foto, ruta_foto_local, mascota)
        if confirmar_foto:
            return "The pet and the photo were saved successfully"
        else:
            return "The pet was saved without photo"
    else:
        return "Error: The user was not created"

def func_consult_pet():
# Aquí se hace la petición de los datos que vienen del formulario del front end en un formato json, gracias al método fetch que viene del consult.js, que solicitó la ruta /consult_pet, y esta a su vez ejecutó esta función
    obj_mascota = request.get_json()
# Aquí estoy capturando el valor del nombre de la mascota y el propietario que vienen en el objeto json que se almacenó en obj_mascota
    mascota = obj_mascota["mascota"]
    propietario = obj_mascota["propietario"]
# Aquí llamo a la función consult_pet() que se encuentra en el archivo db.py, y le envío como argumentos los datos que capturé del json y el registro que retorna la función consult_pet(), se almacena en la variable result_data en forma de un array
    result_data = consult_pet(mascota, propietario)
# Aquí valido que se haya encontrado el registro en la base de datos y que no esté vacio
    if result_data != False and len(result_data) != 0:
# Aquí llamo al método connection_s3() que se encuentra en el archivo admin_s3.py, y que me retorna la conexión con s3, para poder traer la foto de la mascota en caso de que exista, porque también puede ocurrir que se haya creado el registro de una mascota sin foto; la conexión con s3 se almacena en la variable s3_resource
        s3_resource = connection_s3()
# confirmar_mascota es una variable que almacena lo que retorna la función consult_file() que en este caso es la parte final de la ruta donde está guardada la foto de la mascota = images/nombreFoto.jpg; la función consult_file() se encuentra en el archivo admin_s3.py
        confirmar_mascota = consult_file(s3_resource, mascota)
# Aquí valido que la mascota tenga una foto
        if confirmar_mascota != None:
# Aquí construyo la url completa de la ubicación de la foto
            url_foto_mascota = "https://fotos-de-mascotas.s3.amazonaws.com/" + confirmar_mascota
        else:
            url_foto_mascota = ""
        response = {
                'status': "ok",
                'mascota': result_data[0][1],
                'propietario': result_data[0][2],
                'tipo_mascota': result_data[0][3],
                'raza': result_data[0][4],
                'sexo': result_data[0][5],
                'edad': result_data[0][6],
                'foto': url_foto_mascota
            }
    else:
        response = {
            'status': "error"
        }
    return response