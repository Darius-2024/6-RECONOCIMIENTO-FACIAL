import cv2
import os
import numpy as np
from keras.models import load_model
import conexion

# Obtener una referencia al bucket de almacenamiento
bucket = conexion.initialize_firestore()

# Descargar el modelo desde Firebase Storage
blob = bucket.blob('modeloCNN.h5')
blob.download_to_filename('modeloCNN.h5')

# Cargar el modelo entrenado
model = load_model('modeloCNN.h5')

dataPath = 'G:/IA/OmesTutorials2020-master/6 RECONOCIMIENTO FACIAL/faces' 
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture('videos/Edson.mp4')

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret == False: 
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (100, 100))  # Redimensionar a la misma dimensión que usamos en el entrenamiento
        rostro = np.expand_dims(rostro, axis=0)
        rostro = np.expand_dims(rostro, axis=3)
        resultado = model.predict(rostro)

        # Obtener el nombre de la persona
        persona = peopleList[np.argmax(resultado)]

        if resultado[0][np.argmax(resultado)] > resultado[0][1 - np.argmax(resultado)]:
            cv2.putText(frame, 'Buscado: ' + persona, (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.putText(frame, 'No Buscado', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
