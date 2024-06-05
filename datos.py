from conexion import initialize_firebase_admin, db

def registra_persona_reconocida(data):
    initialize_firebase_admin()
    ref = db.reference('reconocimientos')
    new_persona_ref = ref.push()  # Genera una nueva referencia para almacenar la persona
    new_persona_ref.set({
        'persona': data['persona'],
        'fecha_hora': data['fecha_hora']
    })
    print("Persona agregada a la base de datos")
