import kivy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager  import ScreenManager,Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty,ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color
from kivy.uix.progressbar import ProgressBar
import os,sys
from script.get_parameters_reforms_tests_variables_folder_paths import *
from script.interpeters.variables_file_interpeter import *
from script.interpeters.parameters_interpeter import *
from script.interpeters.reforms_file_interpeter import *
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button


# Screen
class InitScreen(Screen):

    def __init__(self,**kwargs):
        super(InitScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        #Builder.load_file("screens\init_screen_folder\init_screen_body.kv")
        self.ids.home_file_chooser.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def selected_file(self,*args): #in args ci sta il filepath di openfisca scelto
        PATH_OPENFISCA = args[1][0]
        #self.manager.get_screen('home').ids.btn_visual_system.text = PATH_OPENFISCA
        dict = get_all_paths(PATH_OPENFISCA)
        if dict:
            if self.manager.current == 'init':
                 self.manager.current = 'home'
                 self.manager.get_screen('visualize_system'). ricevi_inizializza_path(PATH_OPENFISCA)
        else:
            print "Path errato"
            self.ids.lbl_txt_2.text = "[u][b]The selected directory doesn't \n contain an openfisca regular system[/b][/u]"


class HomeScreen(Screen):

    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def go_to_visualize(self):
        if self.manager.current == 'home':
             self.manager.current = 'visualize_system'

    def go_to_reforms(self):
        pass

    def go_to_simulation(self):
        if self.manager.current == 'home':
             self.manager.current = 'make_simulation'



class VisualizeSystemScreen(Screen):
    dict_path = ''

    def __init__(self,**kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,path):
        self.dict_path = get_all_paths(path)
        os.chdir(os.getcwd())

    def show_variables(self):
        self.ids.visualize_file_chooser_variables.path = self.dict_path['variables']
        self.ids.current_path_variables.text = self.ids.visualize_file_chooser_variables.path


    def show_parameters(self):
        self.ids.visualize_file_chooser_parameters.path = self.dict_path['parameters']
        self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path


    def show_reforms(self):
        self.ids.visualize_file_chooser_reforms.path = self.dict_path['reforms']
        self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path


    def file_allowed(self,directory,filename):
        filename, file_extension = os.path.splitext(filename)
        return ((file_extension in ['.py','.yaml'] and not(os.path.basename(filename) == '__init__')) or (os.path.isdir(os.path.join(directory, filename))))


    def selected_file(self,*args):
        try:
                # clear document viewer
            self.ids.document_variables_viewer.source = ""
            self.ids.document_parameters_viewer.source = ""
            self.ids.document_reforms_viewer.source = ""
            path_file_scelto = args[1][0]
            # the file could be a parameter or a variable
            parameter_interpeter = ParameterInterpeter(path_file_scelto)
            dict_param = parameter_interpeter.understand_type()
            variable_interpeter = Variable_File_Interpeter(path_file_scelto)
            reform_interpeter = Reform_File_Interpeter(path_file_scelto)
            if (parameter_interpeter.return_type() == ParameterType.normal) and dict_param:
                path_prm = parameter_interpeter.generate_RST_normal_parameter_view(dict_param)
                self.ids.document_variables_viewer.source = path_prm
                self.ids.document_parameters_viewer.source = path_prm
                self.ids.document_reforms_viewer.source = path_prm
            elif (parameter_interpeter.return_type() == ParameterType.scale) and dict:
                path_prm = parameter_interpeter.generate_RST_scale_parameter_view(dict_param)
                self.ids.document_variables_viewer.source = path_prm
                self.ids.document_parameters_viewer.source = path_prm
                self.ids.document_reforms_viewer.source = path_prm
            elif (variable_interpeter.file_is_a_variable() and not(reform_interpeter.file_is_a_reform())):
                variable_interpeter.start_interpetration()
                path_rst = variable_interpeter.generate_RSTs_variables()
                self.ids.document_variables_viewer.source = path_rst
                self.ids.document_parameters_viewer.source = path_rst
                self.ids.document_reforms_viewer.source = path_rst
            elif (reform_interpeter.file_is_a_reform()):
                reform_interpeter.start_interpetration_reforms()
                path_rst = reform_interpeter.generate_RST_reforms()
                self.ids.document_variables_viewer.source = path_rst
                self.ids.document_parameters_viewer.source = path_rst
                self.ids.document_reforms_viewer.source = path_rst
            else: # file for which the interpretation is not defined yet
                self.ids.document_variables_viewer.source = path_file_scelto
                self.ids.document_parameters_viewer.source = path_file_scelto
                self.ids.document_reforms_viewer.source = path_file_scelto
            self.ids.current_path_variables.text = self.ids.visualize_file_chooser_variables.path
            self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path
            self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path
        except Exception as e:
            print "Some error ", e

    def go_to_home(self):
        if self.manager.current == 'visualize_system':
             self.manager.current = 'home'


class MakeSimulation(Screen):
    def __init__(self,**kwargs):
        super(MakeSimulation, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self,dt):
        valori = ['','Pluto','Paperino','Aldo','Rodo']
        self.ids.menu_a_tendina_variabili.values = valori
        self.ids.menu_a_tendina_variabili.text = valori[0]
        self.ids.information.text = """
[b]Instructions[/b]:
    - Select a variable
    - Insert into the text input form its value
    - Click on "Add Variable"

[b]Rules[/b]:
    - You can't insert a blank variable
    - You can't insert a blank variable value
            """

    def go_to_home(self):
        if self.manager.current == 'make_simulation':
            #Reset when you go to home
            self.ids.variable_added.clear_widgets()
            self.ids.menu_a_tendina_variabili.text = ''
            self.ids.input_value_variable.text = ''
            #Go to home
            self.manager.current = 'home'


    def add_value_and_reset_form(self):
        if self.ids.menu_a_tendina_variabili.text != '' and self.ids.input_value_variable.text != '':
            self.ids.variable_added.add_widget(Button(text=self.ids.menu_a_tendina_variabili.text+": "+self.ids.input_value_variable.text))
            #last_object = self.ids.variable_added.children[len(self.ids.variable_added.children)-1]
            #self.manager.get_screen('make_simulation').destroy_widget(last_object)
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.input_value_variable.text = ''


class MyScreenManager(ScreenManager):
    pass



# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('app.kv')
        self.icon = 'openfisca.ico'
        self.title = 'Openfisca Managing Tool'
        return MyScreenManager()

# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
