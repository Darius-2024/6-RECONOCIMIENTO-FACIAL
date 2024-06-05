from conexion import initialize_firebase_admin, db

def agregar_persona(nombre, fecha):
    initialize_firebase_admin()
    ref = db.reference('reconocimientos')
    new_persona_ref = ref.push()  # Genera una nueva referencia para almacenar la persona
    new_persona_ref.set({
        'nombre': nombre,
        'fecha': fecha
    })
    print("Persona agregada a la base de datos")

# Ejemplo de uso
nombre = "Juan Perez"
fecha = "05/06/2024"
agregar_persona(nombre, fecha)
