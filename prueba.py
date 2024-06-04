import requests

# Configuración de Firebase Realtime Database
AuthSecret = "ezT2u0M4G8nDKEcNIb3Hmtg3qzZhDcoWRXSsWzFj"
BasePath = "https://deteccionfacial-3746c-default-rtdb.firebaseio.com/"

# Endpoint para escribir datos en la base de datos
endpoint = BasePath + "reconocimientos.json"

# Datos a escribir en la base de datos
data = {
    "persona": "Juan",
    "fecha": "2024-06-04T12:00:00"  # Cambia esto por la hora deseada en formato ISO8601
}

# Realizar una solicitud POST para escribir los datos en la base de datos
response = requests.post(endpoint, json=data, params={"auth": AuthSecret})

# Verificar el estado de la solicitud
if response.status_code == 200:
    print("Datos escritos en la base de datos correctamente.")
else:
    print("Error al escribir datos en la base de datos:", response.text)
