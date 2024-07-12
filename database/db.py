import pymysql

db_host = 'instance-cym.cbmy2g8ysf8d.us-east-1.rds.amazonaws.com'
db_user = 'Eslover'
db_password = '05226.Eslover'
db_database = 'mi_veterinaria'
db_table = 'paciente'

def conectionSQL():
    try:
        connection_sql = pymysql.connect(
            host = db_host,
            user = db_user,
            password = db_password,
            database = db_database
        )
        print("Successfull connection to the database")
        return connection_sql
    except Exception as err:
        print("Error connecting to the database")
        print(err)
        return None

def add_pet(mascota, propietario, tipo_mascota, raza, sexo, edad):
    instruction_sql = "INSERT INTO " + db_table + "(nombre_mascota, nombre_propietario, tipo_mascota, raza, sexo, edad) VALUES ('"+ mascota +"', '" + propietario + "', '" + tipo_mascota + "', '" + raza + "', '" + sexo + "', " + edad +");"
    insertar = conectionSQL()
    try:
        if insertar != None:
            cursor = insertar.cursor()
            cursor.execute(instruction_sql)
            insertar.commit()
            print("Pet added")
            return True
        else:
            print("Error connecting to the database")
            return False
    except Exception as err:
        print("Error creating a pet")
        print(err)
        return False

# Esta función consulta en la base de datos la existencia de una mascota y tiene como parámetro el nombre de la mascota y el nombre del propietario
def consult_pet(mascota, propietario):
# Creo una sentencia con los argumentos que se recibieron para encontrar la mascota que se está consultando
    instruction_sql = "SELECT * FROM paciente WHERE nombre_mascota = '" + mascota + "' AND nombre_propietario = '" + propietario + "';"
# Se llama el método conectionSQL() que retorna la conexión con la base de datos, y esto se guarda en la variable conexion
    conexion = conectionSQL()
    try:
        cursor = conexion.cursor()
        cursor.execute(instruction_sql)
        result_data = cursor.fetchall()
# aquí se retorna el registro en caso de ser encontrado en la base de datos        
        return result_data
    except Exception as err:
        print("Error: ", err)
        return False