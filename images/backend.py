import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:\Users\Micro\Downloads\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://i-scambo-default-rtdb.firebaseio.com/'
})

from firebase_admin import db

# Referência para o nó 'users'
ref = db.reference('users')

def fazer_cadastro(nome, email, senha):
    try:
        # Crie o usuário no Firebase Authentication
        user = auth.create_user(
            email=email,
            password=senha,
            display_name=nome
        )
        
        # Adicione os dados do usuário ao banco de dados Firebase
        ref = db.reference('users')
        ref.push({
            'username': nome,
            'email': email
        })
        
        print("Usuário cadastrado com sucesso!")
        # Aqui você pode redirecionar o usuário para a próxima tela após o cadastro bem-sucedido
        root.manager.current = "login"  # Substitua "proxima_tela" pelo nome da próxima tela
    except auth.AuthError as e:
        # Se ocorrer um erro ao criar o usuário, imprima o erro
        print(f"Erro ao cadastrar usuário: {e.message}")