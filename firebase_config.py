import pyrebase

def initialize_firebase():
    config = {
        "apiKey": "AIzaSyCl2yNqMddN8aogK3VvE86vbA9-rg0MSH8",
        "authDomain": "chat-55ed3.firebaseapp.com",
        "projectId": "chat-55ed3",
        "storageBucket": "chat-55ed3.appspot.com",
        "messagingSenderId": "840464832280",
        "appId": "1:840464832280:web:fab0ca26b3b9359abcf06d",
        "measurementId": "G-DBJX5LP5VH",
        "databaseURL": "https://chat-55ed3-default-rtdb.firebaseio.com/"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    return auth, db