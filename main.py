# import classes, functions and modules
import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import sqlite3

# Screen Classes
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
                
                # To check if database is being populated
                # c.execute("SELECT * FROM details") 

                # data = c.fetchall()

                # for i in data:
                #     print(i)

                conn.commit()
                conn.close()

            else:
                notif = Popup(title = 'Invalid Form', content = Label(text='Invalid Age or Contact Number.'), 
                              size_hint=(None, None), size=(300,300))
                notif.open()

        else:
            notif = Popup(title = 'Invalid Form', content = Label(text='Text fields cannot be empty.'), size_hint=(None, None), size=(300,300))
            notif.open()
            
            
#Class to allow doctor to enter existing patient name and surname, where the database is queried and the patients 
#ID is displayed             
class SearchWindow(Screen): 
   word_input = ObjectProperty(None)
   surname_input=ObjectProperty(None)  
   
   def show_id(self):
       
      conn = sqlite3.connect('patientinfo.db')
      c = conn.cursor()
      
      #Query database to select specific patient with entered name and surname     
      c.execute("SELECT * from details WHERE Name = (:first) AND Surname = (:second)",
                 {
                 'first': self.ids.word_input.text,
                 'second':self.ids.surname_input.text
                 })
      
      #Create empty strings
      records = c.fetchall()
      self.id =''
      self.name_=''
      self.surname_=''
      self.output=''
      self.contact_=''
      self.Age_=''
      
      #Display patient details on page 
      for i in records:
       
           id=i[0]
           name_=i[1]
           surname_=i[2]
           Age_=i[3]
           contact_=i[4]
           output=f'{"Name: " + name_ }\n{"Surname: " + surname_}\n{"Age: " + str(Age_)}\n{"Contact number: " + str(contact_)}\n{"ID: " + str(id)}'
           
           self.ids.id_label.text= output
           
      #Clear input boxes from text
      #self.ids.word_input.text=''
      #self.ids.surname_input.text=''
      #print(Age_)
       
      conn.commit() # to commit changes to database
      conn.close() # to close connection to database   
      return id 

class StartScreen(Screen):
    pass

class TickBox(Screen):
    def checkbox_click(self,instance, value):
        pass

class TickBox2(Screen):
    def checkbox2_click(self,instamce,value):
       pass


# Widget Classes
class LineWidget(Widget):
    pass

class DrawLine(Widget):  

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            Color(255, 0, 255, 1, mode='rgba')
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=3)
        
        # start timer here
        print(touch)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
            print(touch)
        
    def on_touch_up(self, touch):
        # end timer here
        print("Touch Released!", touch)

    def reset_canvas(self):
        keep = self.children[:]
        self.clear_widgets()
        self.canvas.clear()

        for widget in keep:
            self.add_widget(widget)

class TextPopup(Popup):
    pass

class PracScreen(Screen):
    
    def capture(self, *largs): 
        namee = self.manager.get_screen("search").ids.word_input.text
        sur = self.manager.get_screen("search").ids.surname_input.text
        prac_img = self.ids.export1.export_to_png(f"{namee} {sur} practice round.png")
        # use prac_img variable to store image in file/database

class SpiralWidget(Widget):
    pass
class DSpiralScreen(Screen):
    def capture(self, *args):
        namee = self.manager.get_screen("search").ids.word_input.text
        sur = self.manager.get_screen("search").ids.surname_input.text
        dh_img = self.ids.export2.export_to_png(f"{namee} {sur} dominant hand.png")
        # use dh_img variable to store image in file/database

class NdSpiralScreen(Screen):
    def capture(self, *args):
        namee = self.manager.get_screen("search").ids.word_input.text
        sur = self.manager.get_screen("search").ids.surname_input.text
        ndh_img = self.ids.export3.export_to_png(f"{namee} {sur} non-dominant hand.png")
        # use ndh_img variable to store image in file/database    

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