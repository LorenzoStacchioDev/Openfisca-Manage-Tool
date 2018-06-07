import kivy
kivy.require("1.10.0")
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager  import ScreenManager,Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty,ObjectProperty
# Screen

PATH_OPENFISCA = ""

class InitScreen(Screen):

    def __init__(self,**kwargs):
        super(InitScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        #Builder.load_file("screens\init_screen_folder\init_screen_body.kv")
        self.ids.home_file_chooser.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def selected_file(self,*args): #in args ci sta il filepath di openfisca scelto
        try:
            PATH_OPENFISCA = args[1][0]
            print "Inside try",PATH_OPENFISCA
            self.manager.get_screen('home').ids.btn_boh.text = PATH_OPENFISCA
            if self.manager.current == 'init':
                 self.manager.current = 'home'
        except: pass


class HomeScreen(Screen):
    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        #print self.ids.btn_boh.text
        #print self.manager
        


class MyScreenManager(ScreenManager):
    pass

# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('app.kv')
        return MyScreenManager()

# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
