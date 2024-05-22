import firebase_admin
from firebase_admin import credentials

# Caminho para o arquivo JSON de suas credenciais do Firebase
cred = credentials.Certificate("C:\\Users\\aluno.sesipaulista\\Downloads\\i-scambo-firebase-adminsdk-a1y8v-86130ef2cc.json")

# Inicializar o aplicativo Firebase Admin com as credenciais e a URL do banco de dados
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://i-scambo-default-rtdb.firebaseio.com/'
})

from firebase_admin import db

# Referência para o nó 'users'
ref = db.reference('users')

# Adicionar um novo usuário
ref.push({
    'username': 'john_doe',
    'email': 'john@example.com'
})