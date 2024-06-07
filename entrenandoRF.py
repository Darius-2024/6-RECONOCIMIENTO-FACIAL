import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from conexion import initialize_firebase_admin, storage

# Inicializar Firebase Admin y obtener una referencia al bucket de almacenamiento
def initialize_firebase():
    initialize_firebase_admin()
    return storage.bucket()

# Descargar imágenes desde Firebase Storage
def download_images_from_firebase(bucket, folder_name):
    images = []
    labels = []
    blobs = bucket.list_blobs(prefix=folder_name)
    for blob in blobs:
        blob_bytes = blob.download_as_bytes()
        image = cv2.imdecode(np.frombuffer(blob_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (100, 100))
        images.append(image)
        label = folder_name.split('/')[1]
        labels.append(label)
    return np.array(images), np.array(labels)

# Preprocesamiento de las imágenes
def preprocess_images(images, scale=1.0):
    images = images * scale
    return images

# Definir arquitectura del modelo CNN
def create_cnn_model(input_shape, num_classes):
    # Definición del modelo secuencial
    model = Sequential()
    # Capa convolucional con 32 filtros de 3x3 y activación 'relu'
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    # Capa de Max Pooling con ventana de 2x2
    model.add(MaxPooling2D((2, 2)))
    # Segunda capa convolucional con 64 filtros de 3x3 y activación 'relu'
    model.add(Conv2D(64, (3, 3), activation='relu'))
    # Segunda capa de Max Pooling con ventana de 2x2
    model.add(MaxPooling2D((2, 2)))
    # Capa de aplanado para convertir las características en un vector unidimensional
    model.add(Flatten())
    # Capa densa con 64 neuronas y activación 'relu'
    model.add(Dense(64, activation='relu'))
    # Capa de salida con número de neuronas igual al número de clases y activación 'softmax'
    model.add(Dense(num_classes, activation='softmax'))
    return model

# Entrenar el modelo
def train_model(model, images, labels, epochs=10, batch_size=32):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', #que es adecuada para problemas de clasificación con múltiples clases cuando las etiquetas son enteros.
                  metrics=['accuracy']) #clasificacion
    label_dict = {label: i for i, label in enumerate(np.unique(labels))}
    labels_int = np.array([label_dict[label] for label in labels])
    model.fit(images.reshape(-1, 100, 100, 1), labels_int, epochs=epochs, batch_size=batch_size)
    return model

# Guardar modelo en Firebase Storage
def save_model_to_firebase(model, bucket, filename):
    model.save(filename)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print("Modelo almacenado en Firebase Storage...")

# Ejecutar todo el proceso
def run_entrenamiento():
    bucket = initialize_firebase()
    images = []
    labels = []
    for person_folder in bucket.list_blobs(prefix='faces/'):
        person_images, person_labels = download_images_from_firebase(bucket, person_folder.name)
        images.extend(person_images)
        labels.extend(person_labels)

    images = preprocess_images(np.array(images))

    model = create_cnn_model((100, 100, 1), len(np.unique(labels, scale=1/255.0)))
    trained_model = train_model(model, images, labels)
    save_model_to_firebase(trained_model, bucket, 'models/modeloCNN.h5')

    cv2.destroyAllWindows()
