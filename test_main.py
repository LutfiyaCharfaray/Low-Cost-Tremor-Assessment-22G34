from turtle import right
import unittest
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
import os, sys
import os.path as op
from functools import partial
from kivy.clock import Clock
from kivy.lang import Builder
from unittest.mock import patch

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)

import main, sp, cv2

class ButtonTestCase(GraphicUnitTest):
    # Test case obtained from Kivy documentation
    def test_render(self):
        from kivy.uix.button import Button

        button = Button()
        self.render(button)

        from kivy.base import EventLoop
        EventLoop.ensure_window()
        window = EventLoop.window

        touch = UnitTestTouch(
            *[s / 2.0 for s in window.size]
        )

        # bind something to test the touch with
        button.bind(
            on_release=lambda instance: setattr(
                instance, 'test_released', True
            )
        )

        # then let's touch the Window's center
        touch.touch_down()
        touch.touch_up()
        self.assertTrue(button.test_released)

class LabelTestCase(GraphicUnitTest): # generic label testing
    def test_lbl(self):
        from kivy.uix.label import Label

        label_ = Label(text = "Assessment Page", color=(1,1,1,1), font_size=30, pos_hint={'center_x':0.5, 'y': 0.8})
        text_ = "Assessment Page"
        self.assertEqual(text_, label_.text)

    def test_lbl2(self):
        from kivy.uix.label import Label

        label_ = Label(text = "Assessment Page", color=(1,1,1,1), font_size=30, pos_hint={'center_x':0.5, 'y': 0.8})
        text_ = "Results Page"
        self.assertNotEqual(text_, label_.text)

    def test_lblPosition(self):
        from kivy.uix.label import Label
        from kivy.graphics import Color

        label_ = Label(text = "Assessment Page", color=(1,1,1,1), font_size=30, pos_hint={'center_x':0.5, 'y': 0.8})
        pos = {'center_x':0.5, 'y': 0.8}
        self.assertEqual(pos, label_.pos_hint)

    def test_lblPosition2(self):
        from kivy.uix.label import Label
        from kivy.graphics import Color

        label_ = Label(text = "Assessment Page", color=(1,1,1,1), font_size=30, pos_hint={'center_x':0.5, 'y': 0.8})
        pos = {'center_x':0.8, 'y': 0.3}
        self.assertNotEqual(pos, label_.pos_hint)

class DrawLineTestCase(GraphicUnitTest):

    def test_line(self):
        # This test was also derived from the kivy documentation but it was altered to suit the application
        from kivy.uix.widget import Widget
        from kivy.graphics import Line, Color
        r = self.render

        # create a root widget
        wid = Widget()

        # put some graphics instruction on it
        with wid.canvas:
            Color(255, 0, 255, 1, mode='rgba')
            self.e = Line(points=(20,30,400,500,60), pos=(100, 100), width=3)

        # render, and capture it directly
        r(wid)

        # capture it in 2 frames:
        r(wid, 2)

        # capture it in 10 frames
        r(wid, 10)

class ssimTestCase(unittest.TestCase):
    # The similarity index compares the similarity between two images. Not similar: -1 and similar: 1
    # This is used to get the tremor index, which is tremor index = 1 - similarity index
    def test_template(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("spiraltemp.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/spiraltemp_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim

        expected = 1
        self.assertEqual(ssim, expected)
    
    # the comparison of the template to itself should not be anything other than 1
    def test_template2(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("spiraltemp.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/spiraltemp_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim

        expected = 0.9
        self.assertNotEqual(ssim, expected)

    def test_template3(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("spiraltemp.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/spiraltemp_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim

        expected = -1
        self.assertNotEqual(ssim, expected)

    # test similarity of the normal simulated case to the spiral template
    def test_normal(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("normal case.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/normal case_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim
        ssim = float(round(ssim, 2))

        expected = 0.9 # typical expectation for normal simulated case
        self.assertEqual(ssim, expected)

    def test_normal2(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("normal case.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/normal case_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim
        ssim = float(round(ssim, 2))

        expected = 1
        self.assertNotEqual(ssim, expected)

    def test_normal3(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("normal case.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/normal case_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim
        ssim = float(round(ssim, 2))

        expected = -1
        self.assertNotEqual(ssim, expected)

    def test_normal4(self):
        original = cv2.imread("spiraltemp.png")  
        compare = cv2.imread("normal case.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/normal case_resized_image.png", resized)

        ssim = sp.get_sim(original, resized) #perform ssim
        ssim = float(round(ssim, 2))

        expected = 0.5
        self.assertNotEqual(ssim, expected)
    
    # dominant hand tremor simulation tests
    def test_abnormalDH(self): 
        original = cv2.imread("test images/dominant hand_template.png")  
        compare = cv2.imread("test images/tremor case_dh.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/tremor casedh_resized_image.png", resized)

        ssim = sp.get_sim(original, resized)
        ssim = float(round(ssim, 2))

        expected = 1
        self.assertNotEqual(ssim, expected) #to show that it definitely is not similar to the template

    def test_abnormalDH2(self):
        original = cv2.imread("test images/dominant hand_template.png")  
        compare = cv2.imread("test images/tremor case_dh.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/tremor casedh_resized_image.png", resized)

        ssim = sp.get_sim(original, resized)
        ssim = float(round(ssim, 2))

        expected = 0.9
        self.assertNotEqual(ssim, expected) #to show that it does not produce the same results as the normal simulated case

    #non dominant hand tremor simulation tests
    def test_abnormalNDH(self): 
        original = cv2.imread("test images/non-dom hand_temp.png")  
        compare = cv2.imread("test images/tremor case_ndh.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/tremor casendh_resized_image.png", resized)

        ssim = sp.get_sim(original, resized)
        ssim = float(round(ssim, 2))

        expected = 1
        self.assertNotEqual(ssim, expected)

    def test_abnormalNDH(self): #non dominant hand tremor simulation test
        original = cv2.imread("test images/non-dom hand_temp.png")  
        compare = cv2.imread("test images/tremor case_ndh.png")

        resized = cv2.resize(compare, (original.shape[1], original.shape[0]))
        cv2.imwrite("test images/tremor casendh_resized_image.png", resized)

        ssim = sp.get_sim(original, resized)
        ssim = float(round(ssim, 2))

        expected = 0.9
        self.assertNotEqual(ssim, expected)  

class whichHandTestCase(unittest.TestCase):   
    #testing the logic of the code used to obtain and display the dominant and non-dominant hand
    def test_right(self): #should return left if input is right
        def get_hand(hand_side):
            if hand_side == "Left":
                other_hand ="Right"
            elif hand_side == "Right":
                other_hand ="Left"
            return other_hand

        hand = "Right"
        other = get_hand(hand)
        self.assertNotEqual(hand, other)

    def test_left(self): #should return right if input is left
        def get_hand(hand_side):
            if hand_side == "Left":
                other_hand ="Right"
            elif hand_side == "Right":
                other_hand ="Left"
            return other_hand

        hand = "Left"
        other = get_hand(hand)
        self.assertNotEqual(hand, other)

class percentageTestCase(unittest.TestCase):
    # test the percentage of the time taken for a drawing and compare it to a "normal" case
    def test_slowtime(self): #test slower than normal
        def comparetonorm(time_result):
            normal_time_d = 14 #14 sec
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 16
        percentage = comparetonorm(time_in_sec)
        result = "slower than normal"
        self.assertEqual(result, percentage)

    def test_notslowtime(self):
        def comparetonorm(time_result):
            normal_time_d = 14 #14 sec
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 10
        percentage = comparetonorm(time_in_sec)
        result = "slower than normal"
        self.assertNotEqual(result, percentage)

    def test_fasttime(self):
        def comparetonorm(time_result):
            normal_time_d = 14 #14 sec
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 12
        percentage = comparetonorm(time_in_sec)
        result = "faster than normal"
        self.assertEqual(result, percentage)

    def test_notfasttime(self):
        def comparetonorm(time_result):
            normal_time_d = 14 #14 sec
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 20
        percentage = comparetonorm(time_in_sec)
        result = "faster than normal"
        self.assertNotEqual(result, percentage)

    def test_changenormtime(self): #test slower than normal
        def comparetonorm(time_result):
            normal_time_d = 20 
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 22
        percentage = comparetonorm(time_in_sec)
        result = "slower than normal"
        self.assertEqual(result, percentage)

    def test_changenormtimef(self): #test faster than normal
        def comparetonorm(time_result):
            normal_time_d = 20 
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc1=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc2=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return res

        time_in_sec = 18
        percentage = comparetonorm(time_in_sec)
        result = "faster than normal"
        self.assertEqual(result, percentage)

    def test_percentage(self): #test slower than normal
        def comparetonorm(time_result):
            normal_time_d = 15
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return perc

        time_in_sec = 18
        percentage = comparetonorm(time_in_sec)
        result = 20
        self.assertEqual(result, percentage)

    def test_percentagef(self): #test faster than normal
        def comparetonorm(time_result):
            normal_time_d = 15
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return perc

        time_in_sec = 10
        percentage = comparetonorm(time_in_sec)
        result = 34
        self.assertEqual(result, percentage)

    def test_notpercentage(self): #test slower than normal
        def comparetonorm(time_result):
            normal_time_d = 15
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return perc

        time_in_sec = 18
        percentage = comparetonorm(time_in_sec)
        result = 50
        self.assertNotEqual(result, percentage)

    def test_notpercentagef(self): #test faster than normal
        def comparetonorm(time_result):
            normal_time_d = 15
            diff = time_result-normal_time_d
            
            if diff<=0: #Faster than normal
                perc=100-int((time_result/normal_time_d)*100)
                res = "faster than normal"
            
            else:      #slower than normal
                perc=int((diff/normal_time_d)*100)
                res = "slower than normal" 
            return perc

        time_in_sec = 10
        percentage = comparetonorm(time_in_sec)
        result = 78
        self.assertNotEqual(result, percentage)

class formTestCase(unittest.TestCase):
    def test_emptyform(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        empty = submit("","","","")
        self.assertEqual(ans,empty)

    def test_emptyname(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                   # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        emptyname = submit("","Parker","23","0369852147")
        self.assertEqual(ans,emptyname)

    def test_emptysurname(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        emptysur = submit("Peter","","63","0741596325")
        self.assertEqual(ans,emptysur)

    def test_emptyage(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        emptyage = submit("Peter","Parker","","0741596325")
        self.assertEqual(ans,emptyage)

    def test_emptynum(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        emptynum = submit("Peter","Parker","24","")
        self.assertEqual(ans,emptynum)

    def test_twoemptyfields(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        emptyfields = submit("","","24","7854123698")
        self.assertEqual(ans,emptyfields)

    def test_invalidage(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        age_ = submit("Peter","Parker","2436","0369852147")
        self.assertEqual(ans,age_)

    def test_invalidnum(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        invalnum = submit("Peter","Parker","24","0369852")
        self.assertEqual(ans,invalnum)

    def test_invalidnum2(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Invalid"
        invalnum = submit("Peter","Parker","24","03698521569787")
        self.assertEqual(ans,invalnum)

    def test_validform(self):
        def submit(name,surname,age,num):
            if name != "" and surname != "" and age != "" and num != "":
                age_length = 3
                num_length = 10

                if len(age) <= age_length and len(num) == num_length:
                    # populate the database here
                    notif = "Valid"
                else:
                    notif = "Invalid"
            else:
                notif = "Invalid"
            return notif

        ans = "Valid"
        invalnum = submit("Peter","Parker","24","0369852156")
        self.assertEqual(ans,invalnum)

if __name__ == '__main__':
    unittest.main()