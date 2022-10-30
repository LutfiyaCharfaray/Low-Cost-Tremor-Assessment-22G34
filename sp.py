# signal/image processing functions
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def get_sim(original, resized):

    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    compare = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #resized

    ssim_ = ssim(original, compare) 
    #print("THIS IS THE SSIM: ", ssim_)
    return ssim_ 

def Histo(name, surname, image_name1, image_name2): 
   img1 = cv2.imread("normal case.png",0) #grayscale mode ,0
   hist1 = cv2.calcHist([img1],[0],None,[256],[0,256])

   img2 = cv2.imread(image_name1,0) #grayscale mode ,0
   hist2 = cv2.calcHist([img2],[0],None,[256],[0,256])

   img3 = cv2.imread(image_name2,0) #grayscale mode ,0
   hist3 = cv2.calcHist([img3],[0],None,[256],[0,256])

   plt.figure()
   plt.xlabel("Pixel Values")
   plt.ylabel("No. of pixels")
   plt.plot(hist1, color='blue', label='Normal')
   plt.plot(hist2, color='green', label='Patient Dominant Hand Drawing')
   plt.plot(hist3, color='red', label='Patient Non-dominant Hand Drawing')
   plt.legend()
   fig = plt.savefig(f"{name}, {surname} graph.png") #store according to pt names
   
   plt.clf()
   plt.close()

   return fig, f"{name}, {surname} graph.png"