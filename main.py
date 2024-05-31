from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.utils import platform
import webbrowser
from backend import fazer_cadastro, fazer_login, criar_anuncio, search_anuncios, db, firestore
from kivymd.uix.button import MDRaisedButton

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
    has_content = BooleanProperty(False)

    def on_enter(self, *args):
        super(PrincipalScreen, self).on_enter(*args)
        self.exibir_ultimo_anuncio()

    def update_anuncio(self, titulo, informacoes):
        self.ids.titulo_label.text = titulo
        self.ids.informacoes_label.text = informacoes
        self.has_content = True

    def exibir_ultimo_anuncio(self):
        query = db.collection('anuncios').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()

        if query:
            ultimo_anuncio = query[0].to_dict()
            self.update_anuncio(ultimo_anuncio.get('titulo', ''), ultimo_anuncio.get('informacoes', ''))
        else:
            self.ids.titulo_label.text = 'Nenhum anúncio encontrado'
            self.ids.informacoes_label.text = ''
            self.has_content = False

class SearchScreen(Screen):
    def search(self):
        query = self.ids.search_field.text  
        results = search_anuncios(query) 
        result_text = "\n".join(results)  
        self.ids.result_label.text = result_text

        self.ids.result_label.clear_widgets()

        for result in results:
            button = MDRaisedButton(text=result, size_hint=(None, None), size=(400, 50))
            button.bind(on_release=lambda btn: self.show_anuncio_details(btn.text))
            self.ids.result_label.add_widget(button)

    def get_detalhes_anuncio(self, anuncio):

        detalhes_anuncio = {
            'titulo': anuncio,
            'informacoes': 'Informações detalhadas sobre ' + anuncio,
            'experiencias': 'Experiências relevantes para ' + anuncio,
            'formacao': 'Formação acadêmica relevante para ' + anuncio,
            'anexo': 'Anexos relevantes para ' + anuncio,
            'portfolio': 'Portfólio relevante para ' + anuncio
        }
        return detalhes_anuncio

    def show_anuncio_details(self, anuncio):
        detalhes_anuncio = self.get_detalhes_anuncio(anuncio)  
        self.manager.get_screen('anuncio_detalhes').update_detalhes(**detalhes_anuncio)
        self.manager.current = 'anuncio_detalhes'


class AnuncioScreen(Screen):
    titulo_input = ObjectProperty(None)
    informacoes_input = ObjectProperty(None)
    experiencias_input = ObjectProperty(None)
    formacao_input = ObjectProperty(None)
    anexo_input = ObjectProperty(None)
    portfolio_input = ObjectProperty(None)


        
    def anunciar(self):
    
        titulo = self.ids.titulo_input.text
        informacoes = self.ids.informacoes_input.text
        experiencias = self.ids.experiencias_input.text
        formacao = self.ids.formacao_input.text
        anexo = self.ids.anexo_input.text
        portfolio = self.ids.portfolio_input.text


        novo_anuncio = {
            'titulo': titulo,
            'informacoes': informacoes,
            'experiencias': experiencias,
            'formacao': formacao,
            'anexo': anexo,
            'portfolio': portfolio
        }

        db.collection('anuncios').add(novo_anuncio)


        self.ids.titulo_input.text = ''
        self.ids.informacoes_input.text = ''
        self.ids.experiencias_input.text = ''
        self.ids.formacao_input.text = ''
        self.ids.anexo_input.text = ''
        self.ids.portfolio_input.text = ''

        self.manager.current = 'principal'
        
    def abrir_explorador_arquivos(self):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_selection=self.selecionar_arquivo_callback)
        self.popup = Popup(title="Selecione um arquivo", content=file_chooser, size_hint=(None, None), size=(600, 400))
        self.popup.open()

    def selecionar_arquivo_callback(self, instance, selection):
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
        sm.add_widget(SearchScreen(name='search'))
        return sm

    def change_screen(self, screen_name):
        self.root.current = screen_name
    
    def open_whatsapp(self):
        if platform == "android":
            link = "https://wa.me/81994183346"
        else:
            link = "https://web.whatsapp.com/send?phone=81994183346"
        webbrowser.open(link)

if __name__ == '__main__':
    eScambo().run()
