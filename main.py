# import classes, functions and modules
import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

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
      print(Age_)
       
      conn.commit() # to commit changes to database
      conn.close() # to close connection to database   
      return id   
  
class AssStart(Screen): 
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