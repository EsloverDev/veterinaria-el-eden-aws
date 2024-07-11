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
    mascota = request.form["mascota"]
    propietario = request.form["propietario"]
    tipo_mascota = request.form["tipo_mascota"]
    raza = request.form["raza"]
    sexo = request.form["sexo"]
    edad = request.form["edad"]
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
    obj_mascota = request.get_json()
    mascota = obj_mascota["mascota"]
    propietario = obj_mascota["propietario"]
    result_data = consult_pet(mascota, propietario)
    if result_data != False and len(result_data) != 0:
        s3_resource = connection_s3()
# confirmar_mascota es una variable que almacena lo que retorna la función consult_file() que en este caso es la parte final de la ruta donde está guardada la foto de la mascota = images/nombreFoto.jpg
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