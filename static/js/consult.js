function consult_pet() {
    let id_mascota = document.getElementById("mascota").value
    let id_propietario = document.getElementById("propietario").value
    let obj_pet = {
        "mascota": id_mascota,
        "propietario": id_propietario
    }
    fetch("/consult_pet", {
        "method": "post",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(obj_pet)
    })
    .then(resp => resp.json())
    .then(data => {
        alert(data.status)
    })
    .catch(err => {
        alert("Error " + err)
    })
}