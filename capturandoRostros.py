import cv2
import os
from conexion import initialize_firebase_admin, storage

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        print('Carpeta creada:', folder_path)
        os.makedirs(folder_path)

def capture_faces(document, frame, count):
    dataPath = os.path.join(os.getcwd(), "faces")
    personPath = os.path.join(dataPath, document)
    create_folder(personPath)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    faces = faceClassif.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    initialize_firebase_admin()
    bucket = storage.bucket()

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(personPath, 'rostro_{}.jpg'.format(count)), rostro)

        # Subir la imagen a Firebase Storage
        blob = bucket.blob('faces/{}/rostro_{}.jpg'.format(document, count))
        blob.upload_from_filename(filename=os.path.join(personPath, 'rostro_{}.jpg'.format(count)))
        count += 1

    return frame, count

def gen_frames_capture(document, nrofotos):  
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame, count = capture_faces(document, frame, count)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if count >= int(nrofotos):
                break

    cap.release()
    cv2.destroyAllWindows()
