import firebase_admin
from firebase_admin import credentials, storage, initialize_app, firestore, db

def initialize_firebase_admin():
   if not firebase_admin._apps:
        cred = credentials.Certificate("credentials/deteccionfacial-3746c-firebase-adminsdk-byuv3-cffbb6349a.json")
        initialize_app(cred, {
            'apiKey': "AIzaSyBX1Aj4jR3z9IGeLru_6LqgwlkMyEede6c",
            'authDomain': "deteccionfacial-3746c.firebaseapp.com",
            'databaseURL': "https://deteccionfacial-3746c-default-rtdb.firebaseio.com",
            'projectId': "deteccionfacial-3746c",
            'storageBucket': "deteccionfacial-3746c.appspot.com",
            'messagingSenderId': "126524860785",
            'appId': "1:126524860785:web:bd6b0caa349e085df46ed0",
            'measurementId': "G-VS6GXHVDKS"
        }) 
