# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:01:56 2019

@author: Zhong
"""
import cv2
import matplotlib.pyplot as plt
import skimage
from skimage.filters import gaussian
from skimage.segmentation import active_contour
v = cv2.VideoCapture('video/0227_1.mov')
img = []
#是否为四边型
def judge(result):
    return True
while True:
    re = v.read()
    if not re[0]:
        break
    img.append(re[1])
for i in range(5):
    gray = cv2.cvtColor(img[i*40], cv2.COLOR_BGR2GRAY)
    plt.figure(figsize=(16,16))
    plt.subplot(1,2,1)
    plt.imshow(gray, cmap='gray')
    blur = skimage.filters.gaussian(gray, 1)
    _, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)        #转换为二值图像  
    cs, y = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    fc = []
    for c in cs:
        if judge(c) and c.shape[0]<2800:
            fc.append(c)
        
    nn = cv2.drawContours(img[i*40],fc,-1,(0,0,255),2)  
    plt.subplot(1,2,2)
    plt.imshow(nn[:,:,::-1])
