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

if __name__ == '__main__':
    unittest.main()