import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

import conexion

# Obtener una referencia al bucket de almacenamiento
bucket = conexion.initialize_firestore()

# Definir función para descargar imágenes desde Firebase Storage
def descargar_imagenes_desde_firebase(folder_name):
    images = []
    labels = []
    blobs = bucket.list_blobs(prefix=folder_name)
    for blob in blobs:
        # Descargar la imagen desde Firebase Storage
        blob_bytes = blob.download_as_bytes()
        image = cv2.imdecode(np.frombuffer(blob_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
        # Redimensionar la imagen a un tamaño uniforme
        image = cv2.resize(image, (100, 100))
        images.append(image)
        # Obtener la etiqueta del nombre de la carpeta
        label = folder_name.split('/')[1]
        labels.append(label)
    return images, labels

# Obtener las imágenes y etiquetas de Firebase Storage
images = []
labels = []
for person_folder in bucket.list_blobs(prefix='images/'):
    person_images, person_labels = descargar_imagenes_desde_firebase(person_folder.name)
    images.extend(person_images)
    labels.extend(person_labels)

# Convertir las listas a arrays numpy
images = np.array(images)
labels = np.array(labels)

# Normalización de los datos
images = images / 255.0

# Definir la arquitectura del modelo CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(len(np.unique(labels)), activation='softmax'))

# Compilar el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Convertir las etiquetas de strings a números enteros
label_dict = {label: i for i, label in enumerate(np.unique(labels))}
labels_int = np.array([label_dict[label] for label in labels])

# Entrenamiento del modelo
model.fit(images.reshape(-1, 100, 100, 1), labels_int, epochs=10, batch_size=32)

# Guardar el modelo entrenado en un archivo local
model.save('modeloCNN.h5')

# Subir el archivo del modelo a Firebase Storage
blob = bucket.blob('modeloCNN.h5')
blob.upload_from_filename(filename='modeloCNN.h5')
print("Modelo almacenado en Firebase Storage...")
