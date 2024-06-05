from conexion import initialize_firebase_admin, storage


def upload_image_to_storage(image_path):
    initialize_firebase_admin()
    bucket = storage.bucket()
    image_blob = bucket.blob(image_path)
    image_blob.upload_from_filename(image_path)
    # Obtenemos la URL de descarga de la imagen
    image_url = image_blob.public_url
    print("Imagen subida a Firebase Storage con éxito. URL de descarga:", image_url)

image_path = "faces/rostro_1.jpg"  # Ruta de la imagen en tu sistema
upload_image_to_storage(image_path)