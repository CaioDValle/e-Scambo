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
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import ObjectProperty, BooleanProperty , StringProperty

Window.size = (310, 580)

LabelBase.register(name='MPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Medium.ttf")
LabelBase.register(name='BPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Semibold.ttf")

class InicioScreen(Screen):
    pass
class LoginScreen(Screen):
    def fazer_login(self):
        email = self.ids.email_input.text
        senha = self.ids.senha_input.text
        sucesso, nome_usuario = fazer_login(email, senha)
        if sucesso:
            print("Login bem-sucedido!")
            self.manager.current = "principal"
            app = MDApp.get_running_app()
            app.user_name = nome_usuario
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
    has_content = BooleanProperty(False)  # Propriedade para controlar se há conteúdo postado ou não

    def update_anuncio(self, titulo, informacoes):
        self.ids.titulo_label.text = titulo
        self.ids.informacoes_label.text = informacoes
        self.has_content = True  # Atualiza a propriedade para indicar que há conteúdo postado


class AnuncioScreen(Screen):
    titulo_input = ObjectProperty(None)
    informacoes_input = ObjectProperty(None)
    experiencias_input = ObjectProperty(None)
    formacao_input = ObjectProperty(None)
    anexo_input = ObjectProperty(None)
    portfolio_input = ObjectProperty(None)

    def anunciar(self):
        titulo = self.titulo_input.text
        informacoes = self.informacoes_input.text
        experiencias = self.experiencias_input.text
        formacao = self.formacao_input.text
        anexo = self.anexo_input.text
        portfolio = self.portfolio_input.text

        principal_screen = self.manager.get_screen('principal')
        detalhes_screen = self.manager.get_screen('anuncio_detalhes')

        principal_screen.update_anuncio(titulo, informacoes)
        detalhes_screen.update_detalhes(titulo, informacoes, experiencias, formacao, anexo, portfolio)

        self.manager.current = 'principal'
        
    def abrir_explorador_arquivos(self):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_selection=self.selecionar_arquivo_callback)  # Adiciona o evento de seleção
        self.popup = Popup(title="Selecione um arquivo", content=file_chooser, size_hint=(None, None), size=(600, 400))
        self.popup.open()

    def selecionar_arquivo_callback(self, instance, selection):  # Recebe a seleção do arquivo
        if selection:
            self.anexo_input.text = selection[0]
            self.popup.dismiss()

            detalhes_screen = self.manager.get_screen('anuncio_detalhes')
            detalhes_screen.ids.detalhes_anexo.text = self.anexo_input.text
class ConfiguracaoScreen(Screen):
    pass

class FavoritosScreen(Screen):
    pass

class NotificacoesScreen(Screen):
    pass

class MensagensScreen(Screen):
    pass

class AnuncioDetalhesScreen(Screen):
    def update_detalhes(self, titulo, informacoes, experiencias, formacao, anexo, portfolio):
        self.ids.detalhes_titulo.text = titulo
        self.ids.detalhes_informacoes.text = informacoes
        self.ids.detalhes_experiencias.text = experiencias
        self.ids.detalhes_formacao.text = formacao
        self.ids.detalhes_anexo.text = anexo
        self.ids.detalhes_portfolio.text = portfolio


class eScambo(MDApp):
    user_name = StringProperty("Nome de Usuario")
    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = 'Dark' 
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