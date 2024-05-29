import pyrebase
import firebase_admin
from firebase_admin import credentials


config = {
    "apiKey": "AIzaSyDcvoBNg5EsmH4bH12ONXR31afXzCS0HRM",
    "authDomain": "i-scambo.firebaseapp.com",
    "databaseURL": "https://i-scambo-default-rtdb.firebaseio.com",
    "projectId": "i-scambo",
    "storageBucket": "i-scambo.appspot.com",
    "messagingSenderId": "630141162199",
    "appId": "1:630141162199:web:9af822f5b73355b3609692",
    "measurementId": "G-28F9C2DTQX"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


cred = credentials.Certificate("C:\\Users\\Micro\\Downloads\\i-scambo-firebase-adminsdk-a1y8v-1217139269.json")
firebase_admin.initialize_app(cred)

def fazer_cadastro(nome, cpf, email, senha):
    try:
        user = auth.create_user_with_email_and_password(email, senha)
        auth.send_email_verification(user['idToken'])
        print("Usuário cadastrado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False
def fazer_login(email, senha):
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        user_info = auth.get_account_info(user['idToken'])
        user_name = user_info['users'][0].get('displayName', 'Usuário')
        print("Login bem-sucedido!")
        return True, user_name
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return False, ""

