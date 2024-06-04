
import cv2
import numpy as np
from keras.models import load_model
import datetime
import requests
import os
from conexion import initialize_firestore

def gen_frames():  # Generador de fotogramas para la transmisión de video
    # Función de inicialización de Firebase

    initialize_firestore()

    # Cargar el modelo entrenado
    model = load_model('modeloCNN.h5')

    dataPath = os.path.join(os.getcwd(),"faces") 
    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start_time = datetime.datetime.now()
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
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

                    # Separar la fecha y la hora
                    fecha_hora_actual = datetime.datetime.now()
                    # Almacenar el nombre de la persona y la hora en Firestore cada 5 segundos
                    if fecha_hora_actual - start_time >= datetime.timedelta(seconds=5):
                        data = {
                            "persona": persona,
                            "fecha_hora": fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")  # Guardar fecha y hora combinadas
                        }
                        write_to_firestore(data)
                        start_time = fecha_hora_actual
                else:
                    cv2.putText(frame, 'No Buscado', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Transmite el fotograma como imagen JPEG

    cap.release()

def write_to_firestore(data):
    # Configuración de la base de datos de Firebase Realtime
    BasePath = "https://deteccionfacial-3746c-default-rtdb.firebaseio.com/"
    AuthSecret = "ezT2u0M4G8nDKEcNIb3Hmtg3qzZhDcoWRXSsWzFj"

    endpoint = BasePath + "reconocimientos.json?auth=" + AuthSecret
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        print("Datos escritos en la base de datos correctamente.")
    else:
        print("Error al escribir datos en la base de datos:", response.text)


