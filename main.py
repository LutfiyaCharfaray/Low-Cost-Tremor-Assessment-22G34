# import classes, functions and modules
import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

import sqlite3
import sp, cv2, os, shutil

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
    def checkbox_click1(self,instance, value,side):
     self.sidee=""
     if value==True:
         self.sidee="Left"
     print(self.sidee)
     
    def checkbox_click2(self,instance, value,side):
     self.sidee=""
     if value==True:
         self.sidee="Right"
     print(self.sidee)    


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
        
        x_co = touch.x #get coordinates
        y_co = touch.y
        print("Touch Start:", "X = ", x_co, "Y = ",  y_co)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
            x_co = touch.x 
            y_co = touch.y
            print("X  = ", x_co, "Y = ", y_co)
        
    def on_touch_up(self, touch):
        x_co = touch.x 
        y_co = touch.y
        print("Touch End: ", "X = ", x_co, "Y = ", y_co)

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
        self.ids.export1.export_to_png(f"{namee} {sur} practice round.png")

class SpiralWidget(Widget):
    pass
class DSpiralScreen(Screen):
    def capture(self, *args):
        namee = self.manager.get_screen("search").ids.word_input.text
        sur = self.manager.get_screen("search").ids.surname_input.text
        self.ids.export2.export_to_png(f"{namee} {sur} dominant hand.png")
        
    #Timer code:    
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.count = 0
       self.finalCount=0
       
    def update_label(self,*args):
       self.count = self.count +1
       
    def stop(self):
       Clock.unschedule(self.update_label)
       self.finalCount=self.count
       print(self.finalCount)  #To check the time
       self.count=0  #Resets the time
       
    def start(self):
       Clock.schedule_interval(self.update_label,1)

class VRScreen1(Screen): #Visual Rating Screen 1
    pass

class NdSpiralScreen(Screen):
    def capture(self, *args):
        namee = self.manager.get_screen("search").ids.word_input.text
        sur = self.manager.get_screen("search").ids.surname_input.text
        self.ids.export3.export_to_png(f"{namee} {sur} non-dominant hand.png") 
        
    #Timer code    
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.count = 0
       self.finalCount=0
       
    def update_label(self,*args):
       self.count = self.count +1
         
    def stop(self):
       Clock.unschedule(self.update_label)
       self.finalCount=self.count
       print(self.finalCount)  #Just to check the time
       self.count=0  #Reset counter
       
    def start(self): #Start counter
       Clock.schedule_interval(self.update_label,1)  

class VRScreen2(Screen):
    pass

class ResultScreen1(Screen):
    vrs1 = NumericProperty()
    vrs2 = NumericProperty()
    
    def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text

        results1 = self.ids.export4.export_to_png(f"{name_} {sur_} results part1.png")
        
    def simIndex(self): 
        original = cv2.imread("normal case.png") #load images "normal case.png" = 0.9 "spiraltemp.png"

        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        compare_dh = cv2.imread(f"{name_} {sur_} dominant hand.png")
        compare_nh = cv2.imread(f"{name_} {sur_} non-dominant hand.png")

        # resize image by specifying width and height
        resized_dh = cv2.resize(compare_dh, (original.shape[1], original.shape[0]))
        resized_nh = cv2.resize(compare_nh, (original.shape[1], original.shape[0]))
    
        #print(f"Resized Dimensions : {resized.shape}")
        cv2.imwrite(f"{name_} {sur_} dh_resized_image.png", resized_dh)
        cv2.imwrite(f"{name_} {sur_} nh_resized_image.png", resized_nh)

        ssim_dh = sp.get_sim(original, resized_dh) #perform ssim
        ssim_nh = sp.get_sim(original, resized_nh) 
        
        ti_dh = 1 - ssim_dh # tremor index
        ti_nh = 1 - ssim_nh
        ti_dh = float(round(ti_dh, 2)) #round off to 2 decimal places
        ti_nh = float(round(ti_nh, 2))

        #send to kv to create label
        self.ids.sim_label.text = str(ti_dh)
        self.ids.sim_label2.text = str(ti_nh)
        return ti_dh, ti_nh
    
class ResultScreen2(Screen):
    
 def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        results1 = self.ids.export5.export_to_png(f"{name_} {sur_} results part2.png")
        
 #Function to show which hand was used to make drawings (Left/Right)  
 def on_enter(self,*args):
       ok= self.manager.get_screen("tick").sidee
       print(ok)
       self.ids.side_label.text=ok
       self.non=""
    
    #if statement that sets the hand side to left/right
       if ok=="Left":
        self.non="Right"
        self.ids.non_side_label.text=self.non
       else:
        self.non="Left"
        self.ids.non_side_label.text=self.non
       
        
 #Displays the time taken to draw dominant and non-dominant drawings       
 def time_result(self):
    #Obtain time values from doiminant hand spiral drawing 
    screen_manager=App.get_running_app().root
    window_one = screen_manager.get_screen("dom_spiral")
    time3= window_one.finalCount
    self.ids.time_results1.text=f'{str(time3) + "s" }'
    
    #Obtain time values from non-doiminant hand spiral drawing 
    screen_manager=App.get_running_app().root
    window_one = screen_manager.get_screen("nondom_spiral")
    time4= window_one.finalCount
    self.ids.time_results2.text=f'{str(time4) + "s" }'
    
 #Calculations to describe what % time the drawing was drawn faster/slower
 #than the normal drawing   
 def time_percentage(self):
    #Obtain time values from doiminant hand spiral drawing 
    screen_manager=App.get_running_app().root
    window_one = screen_manager.get_screen("dom_spiral")
    time3= window_one.finalCount
    normal_time_d=14
    diff=time3-14
    
    if diff<=0: #Faster than normal
        perc1=100-int((time3/normal_time_d)*100)
        self.ids.time_percentage_results.text=f'{str(perc1) + "% faster than normal"}'
    
    else:      #slower than normal
        perc2=int((diff/normal_time_d)*100)
        self.ids.time_percentage_results.text=f'{str(perc2) + "% slower than normal" }'
        
    #Obtain time values from non-doiminant hand spiral drawing 
    screen_manager=App.get_running_app().root
    window_one = screen_manager.get_screen("nondom_spiral")
    time4= window_one.finalCount
    normal_time_nd=16
    diff2=time4-16
         
    if diff2<=0: #Faster than normal
        perc3=100-int((time4/normal_time_nd)*100)
        self.ids.time_percentage_results2.text=f'{str(perc3) + "% faster than normal"}'
    
    else:       #slower than normal
        perc4=int((diff2/normal_time_nd)*100)
        self.ids.time_percentage_results.text=f'{str(perc4) + "% slower than normal" }'
     
    
class ResultScreen3(Screen):
 pass


class SaveScreen(Screen):
    def change_dir(self):
        # save images in directory
        if not os.path.exists("Patient Results/Patient_drawings_results"):
            os.makedirs("Patient Results/Patient_drawings_results")

        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text

        images = [f"{name_} {sur_} practice round.png", f"{name_} {sur_} dominant hand.png", f"{name_} {sur_} non-dominant hand.png",
                f"{name_} {sur_} dh_resized_image.png", f"{name_} {sur_} nh_resized_image.png", f"{name_} {sur_} results part1.png", f"{name_} {sur_} results part2.png"]

        # iterate on all files to move them to destination folder
        for i in images:
            shutil.move(i, 'Patient Results/Patient_drawings_results')

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