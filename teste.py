from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView

Window.size = (310, 580)

LabelBase.register(name='MPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Medium.ttf")
LabelBase.register(name='BPoppins', fn_regular="C:\\Users\\Micro\\Downloads\\Poppins\\Poppins-Semibold.ttf")

class ChatWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.chat_history = Label(text="Bem-vindo ao chat!\n")
        self.add_widget(self.chat_history)

        self.message_input = TextInput(hint_text="Digite sua mensagem aqui", multiline=False)
        self.message_input.bind(on_text_validate=self.send_message)
        self.add_widget(self.message_input)

    def send_message(self, instance):
        message = self.message_input.text
        if message.strip() != '':
            self.chat_history.text += "Você: {}\n".format(message)
            self.message_input.text = ""


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

            # Atualiza o texto do anexo na tela de detalhes do anúncio
            detalhes_screen = self.manager.get_screen('anuncio_detalhes')
            detalhes_screen.ids.detalhes_anexo.text = self.anexo_input.text

class AnuncioDetalhesScreen(Screen):
    def update_detalhes(self, titulo, informacoes, experiencias, formacao, anexo, portfolio):
        self.ids.detalhes_titulo.text = titulo
        self.ids.detalhes_informacoes.text = informacoes
        self.ids.detalhes_experiencias.text = experiencias
        self.ids.detalhes_formacao.text = formacao
        self.ids.detalhes_anexo.text = anexo
        self.ids.detalhes_portfolio.text = portfolio


class eScambo(MDApp):
    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        Builder.load_file('telas.kv')
        sm = ScreenManager()
        principal_screen = PrincipalScreen(name='principal')
        sm.add_widget(principal_screen)
        sm.add_widget(AnuncioScreen(name='anuncio'))
        sm.add_widget(AnuncioDetalhesScreen(name='anuncio_detalhes'))
   
        return sm

if __name__ == '__main__':
    eScambo().run()
