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