from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window

Window.size = (310, 580)


class PrincipalScreen(Screen):
    pass


class eScambo(MDApp):
    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        Builder.load_file('telas.kv')
        sm = ScreenManager()
        sm.add_widget(PrincipalScreen(name='principal'))
       
        return sm

if __name__ == '__main__':
    eScambo().run()