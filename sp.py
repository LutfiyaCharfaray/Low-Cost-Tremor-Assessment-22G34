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

def get_pixels1(name_, sur_): 
    img = cv2.imread("dominant.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bw_img = ""
    ret, bw_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY) #converts to binary
    temp_black_px = np.sum(bw_img == 0) # determine number of black pixels in image 

    im2 = cv2.imread(f"{name_} {sur_} dominant hand.png") # f"{name_} {sur_} dominant hand.png"
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

    im2 = cv2.imread(f"{name_} {sur_} non-dominant hand.png") # f"{name_} {sur_} non-dominant hand.png"
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    bw_im2 = ""
    ret, bw_im2 = cv2.threshold(im2, 120, 255, cv2.THRESH_BINARY) #converts to binary
    black_px = np.sum(bw_im2 == 0)
     
    pink_px = black_px - temp_black_px 
    
    return pink_px