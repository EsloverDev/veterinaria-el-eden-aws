function consult_pet() {
    let id_mascota = document.getElementById("mascota").value
    let id_propietario = document.getElementById("propietario").value
    let obj_pet = {
        "mascota": id_mascota,
        "propietario": id_propietario
    }
// A través del método fetch se genera una conexión con la ruta /consult_pet del archivo route.py el cuál tiene como parámetros la ruta y la solicitud; la solicitud contiene un method, un headers y un body y esa solicitud se envía al server cin la ruta /consult_pet
    fetch("/consult_pet", {
        "method": "post",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(obj_pet)
    })
// .then es una promesa que espera a que respuesta llegue y la convierte en un formato json
    .then(resp => resp.json())
// cuando la información ya esté lista en formato json entonces se imprime a través de un alert el status de esos datos
    .then(data => {
        if (data.status == "ok") {
            document.getElementById("txt-data").value = "Nombre de la mascota: " + data.mascota + "\n" + "Dueño: " + data.propietario + "\n" + "Tipo de mascota: " + data.tipo_mascota + "\n" + "Raza: " + data.raza + "\n" + "Sexo: " + data.sexo + "\n" + "Edad: " + data.edad + "\n" +"Foto: " + data.foto
        }
        else {
            alert("No se encontró la mascota")
            document.getElementById("txt-data").value = ""
        }
    })
    .catch(err => {
        alert("Error " + err)
    })
}