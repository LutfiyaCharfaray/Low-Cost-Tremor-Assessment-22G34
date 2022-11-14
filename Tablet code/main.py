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
from kivy.clock import Clock
import sqlite3, cv2
from kivy.app import App 
import numpy as np

from os.path import dirname, join
dcim = join(dirname(App().user_data_dir), 'DCIM')

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
                
                conn = sqlite3.connect('patientinfo.db')
                c = conn.cursor()
                                     
                c.execute("""INSERT INTO details(Name, Surname, Age, ContactNo) VALUES (:pname, :psname, :page, :pnum)""",
                {
                    'pname': self.ids.ptname.text,
                    'psname': self.ids.ptsname.text,
                    'page': self.ids.ptage.text,
                    'pnum': self.ids.ptnum.text
                })

                self.ptname.text = ""
                self.ptsname.text = ""
                self.ptage.text = ""
                self.ptnum.text = ""

                conn.commit()
                conn.close()

            else:
                notif = Popup(title = 'Invalid Form', content = Label(text='Invalid Age or Contact Number.'),size_hint=(None, None), size=(600,600))
                notif.open()

        else:
            notif = Popup(title = 'Invalid Form', content = Label(text='Text fields cannot be empty.'), size_hint=(None, None), size=(600,600))
            notif.open()
                         
class SearchWindow(Screen): 
   word_input = ObjectProperty(None)
   surname_input=ObjectProperty(None)  
   
   def show_id(self):
       
      conn = sqlite3.connect('patientinfo.db')
      c = conn.cursor()
          
      c.execute("SELECT * from details WHERE Name = (:first) AND Surname = (:second)",
                 {
                 'first': self.ids.word_input.text,
                 'second':self.ids.surname_input.text
                 })
      
      records = c.fetchall()
      self.id =''
      self.name_=''
      self.surname_=''
      self.output=''
      self.contact_=''
      self.Age_=''
       
      for i in records:
       
           id=i[0]
           name_=i[1]
           surname_=i[2]
           Age_=i[3]
           contact_=i[4]
           output=f'{"Name: " + name_ }\n{"Surname: " + surname_}\n{"Age: " + str(Age_)}\n{"Contact number: " + str(contact_)}\n{"ID: " + str(id)}'
           
           self.ids.id_label.text= output
       
      conn.commit() 
      conn.close()   
      return id 

class StartScreen(Screen):
    pass

class LineWidget(Widget):
    pass

class DrawLine(Widget):  

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            Color(255, 0, 255, 1, mode='rgba')
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

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
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text 
        self.ids.export1.export_to_png(f"/sdcard/DCIM/{name_} {sur_} practice round.png")

class TickBox(Screen):
    def checkbox_click1(self,instance, value,side):
        self.sidee=""
        if value==True:
            self.sidee="Left"
     
    def checkbox_click2(self,instance, value,side):
        self.sidee=""
        if value==True:
            self.sidee="Right" 

class SpiralWidget(Widget):
    pass

class DSpiralScreen(Screen):
    def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        self.ids.export2.export_to_png(f"/sdcard/DCIM/{name_} {sur_} dominant hand.png")
            
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.count = 0
       self.finalCount=0
       
    def update_label(self,*args):
       self.count = self.count +1
       
    def stop(self):
       Clock.unschedule(self.update_label)
       self.finalCount=self.count
       self.count=0  #Resets the time
       
    def start(self):
       Clock.schedule_interval(self.update_label,1)

class VRScreen1(Screen): #Visual Rating Screen 1
    pass

class NdSpiralScreen(Screen):
    def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        self.ids.export3.export_to_png(f"/sdcard/DCIM/{name_} {sur_} non-dominant hand.png")
          
    def __init__(self, **kwargs): #Timer code
       super().__init__(**kwargs)
       self.count = 0
       self.finalCount=0
       
    def update_label(self,*args):
       self.count = self.count +1
         
    def stop(self):
       Clock.unschedule(self.update_label)
       self.finalCount=self.count
       self.count=0  #Reset counter
       
    def start(self): #Start counter
       Clock.schedule_interval(self.update_label,1)  

class VRScreen2(Screen):
    pass

def get_pixels1(name_, sur_): 
    img = cv2.imread("dominant.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bw_img = ""
    ret, bw_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY) #converts to binary
    temp_black_px = np.sum(bw_img == 0) # determine number of black pixels in image 

    im2 = cv2.imread(f"/sdcard/DCIM/{name_} {sur_} dominant hand.png") # f"{name_} {sur_} dominant hand.png"
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    bw_im2 = ""
    ret, bw_im2 = cv2.threshold(im2, 120, 255, cv2.THRESH_BINARY) #converts to binary
    black_px = np.sum(bw_im2 == 0)
    
    pink_px = black_px - temp_black_px 
    
    return pink_px

def get_pixels2(name_, sur_): 
    img = cv2.imread("nondominant.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bw_img = ""
    ret, bw_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY) 
    temp_black_px = np.sum(bw_img == 0)

    im2 = cv2.imread(f"/sdcard/DCIM/{name_} {sur_} non-dominant hand.png") # f"{name_} {sur_} non-dominant hand.png"
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    bw_im2 = ""
    ret, bw_im2 = cv2.threshold(im2, 120, 255, cv2.THRESH_BINARY) #converts to binary
    black_px = np.sum(bw_im2 == 0)
     
    pink_px = black_px - temp_black_px 
    
    return pink_px

class ResultScreen1(Screen):
    vrs1 = NumericProperty()
    vrs2 = NumericProperty()
    
    def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        self.ids.export4.export_to_png(f"/sdcard/DCIM/{name_} {sur_} results part1.png")

    def quantify(self):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text

        px_d = abs(get_pixels1(name_, sur_))
        dt_d = App.get_running_app().root.get_screen("dom_spiral").finalCount
        speed_d = round((px_d/(dt_d*1000)), 2)

        px_n = abs(get_pixels2(name_, sur_))
        dt_n = App.get_running_app().root.get_screen("nondom_spiral").finalCount
        speed_n = round((px_n/(dt_n*1000)), 2)

        self.ids.speed_d.text = "DH Drawing Speed: {} pixels/sec".format(str(speed_d))
        self.ids.speed_n.text = "NH Drawing Speed: {} pixels/sec".format(str(speed_n))

        norm_v = 6 #px/ms
        norm_v2 = 6
        dom_error = round(((speed_d - norm_v)/norm_v)*100 , 1) # relative error
        nondom_error = round(((speed_n - norm_v2)/norm_v2)*100 , 1)

        if dom_error >= 0 and nondom_error >= 0: # (positive)
            self.ids.perc_dom.text = "{}%. faster than normal".format(str(dom_error))
            self.ids.perc_non.text = "{}%. faster than normal".format(str(nondom_error))
            
            notif = Popup(title = 'Tremor Alert', content = Label(text='Possible Tremor!'), size_hint=(None, None), size=(600,600))
            notif.open()

        else: # negative
            self.ids.perc_dom.text = "{}%. slower than normal".format(str(dom_error))
            self.ids.perc_non.text = "{}%. slower than normal".format(str(nondom_error))

        if speed_d <= 3.5 or speed_d >= 6:
            if speed_n <= 3.5 or speed_n >= 6:
                notif = Popup(title = 'Tremor Alert', content = Label(text='Possible Tremor!'), size_hint=(None, None), size=(600,600))
                notif.open()
        
        return speed_d, speed_n

class ResultScreen2(Screen):
    def capture(self, *args):
        name_ = App.get_running_app().root.get_screen("search").ids['word_input'].text
        sur_ = App.get_running_app().root.get_screen("search").ids['surname_input'].text
        self.ids.export5.export_to_png(f"/sdcard/DCIM/{name_} {sur_} results part2.png")

    def on_enter(self,*args):
       time_result=self.manager.get_screen("dom_spiral").finalCount
       self.ids.dom_time_label.text=f'{str(time_result)}'
       
       time_result2=self.manager.get_screen("nondom_spiral").finalCount
       self.ids.non_dom_time_label.text=f'{str(time_result2)}'
       
       normal_time_d = 14
       diff = time_result-14
    
       if diff<=0: #Faster than normal
        perc1=100-int((time_result/normal_time_d)*100)
        self.ids.dom_perc_label.text=f'{str(perc1) + "% Quicker"}'
    
       else:      #slower than normal
        perc2=int((diff/normal_time_d)*100)
        self.ids.dom_perc_label.text=f'{str(perc2) + "% Slower" }'
        
       normal_time_nd = 16
       diff2 = time_result2-16
         
       if diff2<=0: #Faster than normal
        perc3=100-int((time_result2/normal_time_nd)*100)
        self.ids.non_dom_perc_label.text=f'{str(perc3) + "% Quicker"}'
    
       else:       #slower than normal
        perc4=int((diff2/normal_time_nd)*100)
        self.ids.non_dom_perc_label.text=f'{str(perc4) + "% Slower" }'
        
       avg=(time_result+time_result2)/2
       self.ids.dom_avg_label.text=f'{str(avg)}'
       self.ids.non_dom_avg_label.text=f'{str(avg)}'
      
       hand_side= self.manager.get_screen("tick").sidee
       self.ids.dom_side.text=hand_side
       self.non=""
   
       if hand_side=="Left":
        self.non="Right"
        self.ids.non_dom_side.text=self.non
       else:
        self.non="Left"
        self.ids.non_dom_side.text=self.non

        Notif(diff,diff2)        

def Notif(diff1, diff2): #sends an alert if tremor is detected
    atypical_time = 4 # 4 seconds longer than average "normal" time 

    if diff1 > atypical_time and diff2 > atypical_time:
        notif = Popup(title='Tremor Alert', content = Label(text='Possible Tremor!'), size_hint=(None, None), size=(600,600))
        notif.open()
        return True
       
class SaveScreen(Screen):
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