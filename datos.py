from conexion import initialize_firebase_admin, db

from geopy.geocoders import Nominatim

def registra_persona_reconocida(data):
    initialize_firebase_admin()
    ref = db.reference('reconocimientos')
    new_persona_ref = ref.push()  # Genera una nueva referencia para almacenar la persona
    new_persona_ref.set({
        'persona': data['persona'],
        'fecha_hora': data['fecha_hora'],
        'latitud': data['latitud'],
        'longitud': data['longitud'],
        'direccion' : obtener_ubicacion_desde_coordenadas(data['latitud'], data['longitud'])
    })
    print("Persona agregada a la base de datos")

def obtener_personas_reconocidas():
    initialize_firebase_admin()
    ref = db.reference('reconocimientos')
    personas = ref.get()
    return personas

def obtener_ubicacion_desde_coordenadas(latitud, longitud):
    geolocalizador = Nominatim(user_agent="nombre_de_tu_app")
    ubicacion = geolocalizador.reverse((latitud, longitud))
    return ubicacion.address if ubicacion else None
