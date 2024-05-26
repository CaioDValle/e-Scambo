from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
Window.size = (310, 580)

LabelBase.register(name='MPoppins', fn_regular=r"C:\Users\Micro\Downloads\Poppins\Poppins-Medium.ttf")
LabelBase.register(name='BPoppins', fn_regular=r"C:\Users\Micro\Downloads\Poppins\Poppins-Semibold.ttf")

class InicioScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class CadastroScreen(Screen):
    pass

class PrincipalScreen(Screen):
    pass

class AnuncioScreen(Screen):
    pass

class eScambo(MDApp):

    def build(self):
        Builder.load_file('telas.kv')
        sm = ScreenManager()
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(PrincipalScreen(name='principal'))
        sm.add_widget(AnuncioScreen(name='anuncio'))
        return sm


if __name__ == '__main__':
    eScambo().run()