from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from backend import fazer_cadastro, fazer_login  # Importe a função fazer_login do backend
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from tkinter import Tk, filedialog

Window.size = (310, 580)

LabelBase.register(name='MPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Medium.ttf")
LabelBase.register(name='BPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Semibold.ttf")

class InicioScreen(Screen):
    pass

class LoginScreen(Screen):
    def fazer_login(self):
        email = self.ids.email_input.text
        senha = self.ids.senha_input.text
        if fazer_login(email, senha):
            print("Login bem-sucedido!")
            self.manager.current = "principal"
        else:
            print("Credenciais inválidas. Verifique seu email e senha.")

class CadastroScreen(Screen):
    def fazer_cadastro(self):
        nome = self.ids.nome_input.text
        cpf = self.ids.cpf_input.text
        email = self.ids.email_input.text
        senha = self.ids.senha_input.text

        if fazer_cadastro(nome, cpf, email, senha):
            self.manager.current = "login"

class PrincipalScreen(Screen):
    def add_anuncio(self, titulo, informacoes, imagem, portfolio):
        card = MDCard(orientation='vertical', size_hint=(0.9, None), height=300, pos_hint={'center_x': 0.5})
        
        card.add_widget(imagem)
        card.add_widget(MDLabel(text=titulo, theme_text_color="Primary", size_hint_y=None, height=40, halign='center'))
        card.add_widget(MDLabel(text=informacoes, theme_text_color="Secondary", size_hint_y=None, height=40, halign='center'))
        
        def on_ler_mais(instance):
            self.manager.current = 'anuncio_detalhes'
            anuncio_detalhes = self.manager.get_screen('anuncio_detalhes')
            anuncio_detalhes.ids.detalhes_label.text = f"Título: {titulo}\nInformações: {informacoes}\nPortfólio: {portfolio}"
        
        ler_mais_button = MDRaisedButton(text='Ler mais', pos_hint={'center_x': 0.5})
        ler_mais_button.bind(on_release=on_ler_mais)
        
        card.add_widget(ler_mais_button)
        self.ids.anuncios_layout.add_widget(card)

class AnuncioScreen(Screen):
    def anunciar(self):
        titulo = self.ids.titulo_input.text
        informacoes = self.ids.informacoes_input.text
        portfolio = self.ids.portfolio_input.text

        root = Tk()
        root.withdraw()  
        arquivo = filedialog.askopenfilename()

        if arquivo:
            self.manager.get_screen('principal').add_anuncio(titulo, informacoes, ImagemArquivo(arquivo), portfolio)
            self.manager.current = 'principal'
        else:
            print("Nenhum arquivo selecionado.")

class ImagemArquivo(BoxLayout):
    def __init__(self, arquivo, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 200
        self.ids.imagem.source = arquivo

class ConfiguracaoScreen(Screen):
    pass

class FavoritosScreen(Screen):
    pass

class NotificacoesScreen(Screen):
    pass

class MensagensScreen(Screen):
    pass

class AnuncioDetalhesScreen(Screen):
    pass

class eScambo(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        Builder.load_file('telas.kv')
        sm = ScreenManager()
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(PrincipalScreen(name='principal'))
        sm.add_widget(AnuncioScreen(name='anuncio'))
        sm.add_widget(ConfiguracaoScreen(name='configuracao'))
        sm.add_widget(FavoritosScreen(name='favoritos'))
        sm.add_widget(NotificacoesScreen(name='notificacoes'))
        sm.add_widget(MensagensScreen(name='mensagens'))
        sm.add_widget(AnuncioDetalhesScreen(name='anuncio_detalhes'))
        return sm

if __name__ == '__main__':
    eScambo().run()
