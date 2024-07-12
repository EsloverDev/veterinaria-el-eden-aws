//Desde el consult.html, cuando se hace click en el botón de consultar se invoca esta función
function consult_pet() {
// Aquí capturo los datos del nombre de la mascota y del propietario que son ingresados por el usuario en el formulario de consultar
    let id_mascota = document.getElementById("mascota").value
    let id_propietario = document.getElementById("propietario").value
// Para poder enviar los datos en un formato json debo convertirlos en un objeto que contiene la información que se capturó anteriormente
    let obj_pet = {
        "mascota": id_mascota,
        "propietario": id_propietario
    }
// A través del método fetch se solicita el recurso /consult_pet del archivo route.py el cuál tiene como parámetros la ruta y la solicitud; la solicitud contiene un method, un headers y un body y esa solicitud se envía al server cin la ruta /consult_pet
    fetch("/consult_pet", {
//Aquí se indica el método, si es get, post, put o delete
        "method": "post",
//Aquí se le indica el tipo de contenido, en este caso un json para que el servidor lo interprete como un json
        "headers": {"Content-Type": "application/json"},
//El body contiene los datos que vienen en el objeto obj_pet que declaré anteriormente
        "body": JSON.stringify(obj_pet)
    })
// Aquí se lee la respuesta de la solicitud a la ruta /consult_pet y se procesa; .then es una promesa que espera a que la respuesta llegue y la convierte en un formato json
    .then(resp => resp.json())
// cuando la información ya esté lista en formato json entonces se procesa su status
    .then(data => {
// En caso de que el status de la respuesta que se envía desde la función func_consult_pet() que se encuentra en el archivo controller.py sea igual a "ok", entonces se ejecuta el siguiente código:
        if (data.status == "ok") {
// primero obtengo el id del textarea que se encuentra en el archivo consult.html a través de su atributo name="", y ahí es donde voy a imprimir los datos de la mascota para que sean visibles para el usuario en el front end 
            document.getElementById("txt-data").value = "Nombre de la mascota: " + data.mascota + "\n" + "Dueño: " + data.propietario + "\n" + "Tipo de mascota: " + data.tipo_mascota + "\n" + "Raza: " + data.raza + "\n" + "Sexo: " + data.sexo + "\n" + "Edad: " + data.edad
// Aquí através del id de la etiqueta img que está incrustada en el consutl.html id="", se le asigna la url de la foto como argumento al atributo src="" para que se muestre la imagen en el front end
            document.getElementById("img-pet").src = data.foto
        }
// En caso de que el status de la respuesta sea diferente a "ok" entonces se ejecuta el siguiente bloque de código
        else {
// Se imprime una alerta para indicarle al usuario que la mascota no está registrada
            alert("No se encontró la mascota")
// Se deja en blanco el text area y la imagen
            document.getElementById("txt-data").value = ""
            document.getElementById("img-pet").src = ""
        }
    })
    .catch(err => {
        alert("Error " + err)
    })
}