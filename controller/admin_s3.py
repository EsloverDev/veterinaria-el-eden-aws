import boto3
from credentials.keys import *

bucket_name = "fotos-de-mascotas"

# Esta funcion me ayuda a conectarme con S3 a través de SDK boto3
def connection_s3():
    try:
# En esta línea creo una sesión en la cuál debo pasar como argumento el ACCESS_KEY y el SECRET_KEY que fueron unas credenciales que se crearon a través del servicio de IAM
        session_aws = boto3.session.Session(ACCESS_KEY, SECRET_KEY)
# Aquí le indico que puntualmente me quiero conectar con el servicio de s3
        s3_resource = session_aws.resource('s3')
# Aquí retorno la conexión exitosa con s3
        return s3_resource
    except Exception as err:
        print("Error: ", err)
        return None
        
# Esta función me ayuda a almacenar la foto "localmente" y temporalmente en la instancia EC2
def save_file(foto):
    try:
        ruta_foto_local = "/tmp/foto"
        foto.save(ruta_foto_local)
        print("photo saved")
        return ruta_foto_local
    except Exception as err:
        print("Error: ", err)
        return None

# Esta función me ayuda a subir la foto al bucket
def upload_file(s3_resource, foto, ruta_foto_local, mascota):
    try:
        nombre_foto = foto.filename
        extension_foto = nombre_foto.split(".")[len(nombre_foto.split("."))-1]
        ruta_foto_destino = "images/" + mascota + "." + extension_foto
        bucket_connection = s3_resource.meta.client.upload_file(ruta_foto_local, bucket_name, ruta_foto_destino)
        print("File uploaded")
        return True
    except Exception as err:
        print("Error: ", err)
        return False
        
# Esta función me ayuda a consultar una foto específica que está guardada en el bucket, tiene como parámetros la conexión a s3 y el nombre de la mascota
def consult_file(s3_resource, mascota):
# La conexión s3 tiene un método que se llama Bucket que me ayuda a conectarme con un bucket en particular; a éste método se le pasa el nombre del bucket como argumento
    bucket_repo = s3_resource.Bucket(bucket_name)
# Obtengo todos los elementos que están en el bucket a través del método objects.all(); trae los elementos en un array y los guardo en la variable bucket_objects
    bucket_objects = bucket_repo.objects.all()
# Como solo necesito el nombre de un objeto en particular entonces recorro el array para encontrarlo
    for obj in bucket_objects:
# bucket_objects tiene todos los atributos de los objetos del bucket, pero yo solo necesito el nombre, entonces con obj.key obtengo la key del objeto en la forma images/nombreFoto.jpg
        lista_fotos_s3 = obj.key
# Como solo necesito nombreFoto entonces debo dividir la ruta para extraerlo y ahora me queda objetos_sin_ruta = ["images", "nombreFoto.jpg"]
        objetos_sin_ruta = lista_fotos_s3.split("/")
# Ahora tomo el último elemento de objetos_sin_ruta, que sería nombreFoto.jpg y por medio de split(".")[0] obtengo nombreFoto sin la extensión; ahora nombre_foto es un array con todos los nombres de las fotos que hay en el bucket
        nombre_foto = objetos_sin_ruta[len(objetos_sin_ruta)-1].split(".")[0]
# Ahora valido si el argumento que se pasó en mascota existe en la lista nombre_foto
        if nombre_foto == mascota:
# Aquí se retorna la ruta en forma = images/nombreFoto.jpg cuando el nombre de la foto coincida con el nombre de la mascota
            return lista_fotos_s3
    return None