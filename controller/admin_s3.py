import boto3
from credentials.keys import *

def connection_s3():
    try:
        session_aws = boto3.session.Session(ACCESS_KEY, SECRET_KEY)
        s3_resource = session_aws.resource('s3')
        print("Connected to s3")
        return s3_resource
    except Exception as err:
        print("Error: ", err)
        return None
        
def save_file(foto):
    try:
        ruta_foto_local = "/tmp/foto.JPG"
        foto.save(ruta_foto_local)
        print("photo saved")
        return ruta_foto_local
    except Exception as err:
        print("Error: ", err)
        return None
        
def upload_file(s3_resource, ruta_foto_local):
    try:
        bucket_name = "fotos-de-mascotas"
        ruta_foto_destino = "images/" + "foto.JPG"
        bucket_connection = s3_resource.meta.client.upload_file(ruta_foto_local, bucket_name, ruta_foto_destino)
        print("File uploaded")
        return True
    except Exception as err:
        print("Error: ", err)
        return False