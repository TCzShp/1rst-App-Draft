import threading

import wikipedia
from kivy.core.clipboard import Clipboard

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import requests
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem


Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

class UI(ScreenManager):
    pass

class MainApp(MDApp):
    def build (self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Pink"
        Builder.load_file('./KVStyle/Estilo.kv')
        self.url = 'https://sttestdraft-default-rtdb.firebaseio.com/.json' #firebase link to use here.
        self.key = 'RJfF8DpYoSKMWHCmcCseRHlsT0W81pigbEfHDtNc' #testpassword
        
        return UI()
    
    def login_data(self):
        userx = self.root.ids.user.text
        passwordx = self.root.ids.password.text
        state = False
        data = requests.get(self.url + '?auth=' + self.key)
        
        for key, value in data.json().items():
            user_reg = value ['User']
            password_reg = value ['Password']
            
            if userx == user_reg:
                if passwordx == password_reg:
                    state = True
                    self.root.ids.signal_login.text = ''
                    self.root.ids.user.text = ''
                    self.root.ids.password.text = ''
                else:
                    self.root.ids.signal_login.text = 'Contraseña Incorrecta'
                    self.root.ids.user.text = ''
                    self.root.ids.password.text = ''
            else:
                self.root.ids.signal_login.text = 'Usuario Incorrecto'
                self.root.ids.user.text = ''
                self.root.ids.password.text = ''
        return state
    
    def register_data(self):
        state = 'Datos Incorrectos'
        
        userx = self.root.ids.new_user.text
        password_one = self.root.ids.new_password.text
        password_two = self.root.ids.new_password_two.text
        
        data = requests.get(self.url + '?auth=' + self.key)
        
        if password_one != password_two:
            state = 'Las contraseñas no coinciden.'
        elif len(userx) <= 4:
            state = 'Nombre de Usuario muy corto'
        elif password_one == password_two and len(password_two) <= 5:
            state = 'Contraseña debe tener más de 5 caracteres'
        else:
            for key, value in data.json().items():
                user = value['User']
                if user == userx:
                    state = 'Este Usuario ya existe'
                    break
                else:
                    state = 'Registrado Correctamente'
                    data ={userx:{
                    'User' : userx,
                    'Password': password_one}
                    }
                    requests.patch(url = self.url, json = data)
                    self.root.ids.signal_register.text = 'Registrado Correctamente'
        
        self.root.ids.signal_register.text = state
        self.root.ids.new_user.text = ''
        self.root.ids.new_password.text = ''
        self.root.ids.new_password_two.text = ''
        return state
    
    def clear_signal(self):
        self.root.ids.signal_register.text = ''
        self.root.ids.signal_login.text = ''
        
    #Attempt at a repository part.
    url = ""
        
    def search(self, text):
        t1 = threading.Thread(target=self.get_wiki, args=(text,))
        t1.start()

    def get_wiki(self, text):
        self.root.ids.rc_spin.active = True
        self.root.ids.summary.text = ""
        self.root.ids.title.text = ""
        self.root.ids.error.text = ""

        wikipedia.set_lang("es")
        try:
            summary = wikipedia.page(text.strip())
            self.root.ids.title.text = summary.title
            self.root.ids.summary.text = f"\n{summary.summary}"
        except Exception as e:
            print(e)
            self.root.ids.summary.text = (
                "Disculpa, no se pudo encontrar " + self.root.ids.fld.text + " en la Wiki, prueba algo más específico"
            )
        self.root.ids.rc_spin.active = False
        
    #End of Attempt
        
if __name__=="__main__":
    MainApp().run()