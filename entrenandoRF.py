import cv2
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

dataPath = 'G:/IA/OmesTutorials2020-master/6 RECONOCIMIENTO FACIAL/Rostros' 
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []

for label, nameDir in enumerate(peopleList):
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo las imágenes')

    for fileName in os.listdir(personPath):
        print('Rostros: ', nameDir + '/' + fileName)
        labels.append(label)
        img = cv2.imread(os.path.join(personPath, fileName), cv2.IMREAD_GRAYSCALE)
        facesData.append(cv2.resize(img, (100, 100)))  # Redimensionamos a un tamaño uniforme

facesData = np.array(facesData)
labels = np.array(labels)

# Normalización de los datos
facesData = facesData / 255.0

# Definir la arquitectura del modelo CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(len(peopleList), activation='softmax'))

# Compilar el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenamiento del modelo
model.fit(facesData.reshape(-1, 100, 100, 1), labels, epochs=10, batch_size=32)

# Guardar el modelo entrenado
model.save('modeloCNN.h5')
print("Modelo almacenado...")
