import firebase_admin
from firebase_admin import credentials, storage, initialize_app, firestore


def initialize_firestore():
    cred = credentials.Certificate("credentials/deteccionfacial-3746c-firebase-adminsdk-byuv3-cffbb6349a.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'deteccionfacial-3746c.appspot.com'}) 
    return storage.bucket()