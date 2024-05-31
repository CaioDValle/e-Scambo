import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração do Firebase
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

# Inicialização do Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\Micro\\Downloads\\i-scambo-firebase-adminsdk-a1y8v-1217139269.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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

def criar_anuncio(titulo, informacoes):
    try:
        # Adiciona um novo documento à coleção 'anuncios' com os dados do anúncio
        db.collection('anuncios').add({
            'titulo': titulo,
            'informacoes': informacoes
        })
        print("Anúncio criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar anúncio: {e}")

def search_anuncios(query):
    try:
        # Realiza uma consulta para recuperar os anúncios que correspondem à consulta
        results = []
        query_ref = db.collection('anuncios').where('titulo', '>=', query).where('titulo', '<=', query + '\uf8ff').limit(10).get()
        for doc in query_ref:
            results.append(doc.to_dict()['titulo'])
        return results
    except Exception as e:
        print(f"Erro ao pesquisar anúncios: {e}")
        return []
