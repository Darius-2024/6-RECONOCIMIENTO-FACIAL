from geopy.geocoders import Nominatim

def obtener_ubicacion():
    # Crear un objeto geolocalizador
    geolocalizador = Nominatim(user_agent="mi_app")

    # Obtener la ubicación actual
    ubicacion = geolocalizador.geocode("Mi ubicación actual")

    # Verificar si se obtuvo la ubicación
    if ubicacion is not None:
        # Imprimir la ubicación
        print(ubicacion.address)
        print((ubicacion.latitude, ubicacion.longitude))
    else:
        print("No se pudo obtener la ubicación.")

obtener_ubicacion()
