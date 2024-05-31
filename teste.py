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

class PrincipalScreen(Screen):
    has_content = BooleanProperty(False)  # Propriedade para controlar se há conteúdo postado ou não

    def update_anuncio(self, titulo, informacoes):
        self.ids.titulo_label.text = titulo
        self.ids.informacoes_label.text = informacoes
        self.has_content = True  # Atualiza a propriedade para indicar que há conteúdo postado

class SearchScreen(Screen):
    def search(self):
        query = self.root.get_screen('search').ids.search_field.text
        self.root.get_screen('search').ids.result_label.text = f"Procurando por: {query}"

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
    def change_screen(self, screen_name):
        self.root.current = screen_name

if __name__ == '__main__':
    eScambo().run()
