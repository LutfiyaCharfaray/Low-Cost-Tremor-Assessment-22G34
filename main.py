# import classes, functions and modules
import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window

import sqlite3

class LoginWindow(Screen):
    pass

class MenuWindow(Screen):
    pass

class RegWindow(Screen):
    ptname = ObjectProperty(None)
    ptsname = ObjectProperty(None)
    ptage = ObjectProperty(None)
    ptnum = ObjectProperty(None)

    def submit(self):
        if self.ptname.text != "" and self.ptsname.text != "" and self.ptage.text != "" and self.ptnum.text != "":

            age_length = 3
            num_length = 10

            if len(self.ptage.text) <= age_length and len(self.ptnum.text) == num_length:
                # connect to database and populate rows
                conn = sqlite3.connect('patientinfo.db')
                c = conn.cursor()
                                     
                c.execute("""INSERT INTO details(Name, Surname, Age, ContactNo) VALUES (:pname, :psname, :page, :pnum)""",
                {
                    'pname': self.ids.ptname.text,
                    'psname': self.ids.ptsname.text,
                    'page': self.ids.ptage.text,
                    'pnum': self.ids.ptnum.text
                })

                # clear text input fields
                self.ptname.text = ""
                self.ptsname.text = ""
                self.ptage.text = ""
                self.ptnum.text = ""
                
                # To check if database is being populated; can comment out later
                c.execute("SELECT * FROM details") 

                data = c.fetchall()

                for i in data:
                    print(i)

                conn.commit()
                conn.close()

            else:
                notif = Popup(title = 'Invalid Form', content = Label(text='Invalid Age or Contact Number.'), 
                              size_hint=(None, None), size=(300,300))
                notif.open()

        else:
            notif = Popup(title = 'Invalid Form', content = Label(text='Text fields cannot be empty.'), size_hint=(None, None), size=(300,300))
            notif.open()

class StartScreen(Screen):
    pass

class LineTemplate(Widget):
    pass

class PracScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("tremor.kv") # to specify kv file

class TremorAssessmentApp(App): # to build app
    def build(self): 
        conn = sqlite3.connect('patientinfo.db')
        c = conn.cursor()
        # create table in database to store patient details
        c.execute("""CREATE TABLE if not exists details( 
                         pt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                         Name TEXT NOT NULL,
                         Surname TEXT NOT NULL,
                         Age INTEGER NOT NULL,
                         ContactNo CHAR(10) NOT NULL
        ) """)

        conn.commit() # to commit changes to database
        conn.close() # close the connection to the database

        return kv

if __name__ == "__main__": # to run app
    TremorAssessmentApp().run()