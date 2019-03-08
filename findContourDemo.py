# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:01:56 2019

@author: Zhong
"""
import numpy as np
import argparse
import cv2
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# floodfill to seperate background
def fill_color_demo(image):
    copyIma = image.copy()
    h, w = image.shape[:2]
    print(h, w)
    mask = np.zeros([h+2, w+2], np.uint8)
    cv2.floodFill(copyIma, mask, (30, 30), (0, 0, 0), (50, 50, 50),  (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)  
    return copyIma
#first do floodFill in RGB image then edge detected image
#it is effective to image with line background
def twofloodFill_1(image):
      image_blurred = cv2.medianBlur(image, 5)#pyrMeanShiftFiltering(image, 25, 10)pyrMeanShiftFiltering(image, 25, 10)#GaussianBlur(image, (9, 9),0)#cv2.medianBlur(image, 5)
      #seperate background in RGB picture
      image_water = fill_color_demo(image_blurred)
      #edge detection
      edges1 = cv2.Canny(image_water, 50, 150, apertureSize=3)
      image_water1 = fill_color_demo(edges1)
      edges = cv2.Canny(image_water1, 50, 150, apertureSize=3)
      #dilate
      closed = cv2.dilate(edges, None, iterations = 2)
      print("STEP 1: Edge Detection")
      cv2.imshow("Image", edges)
      cv2.imshow("Edged", closed)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      cnts = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      cnts = imutils.grab_contours(cnts)
      cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
      screenCnt = []
      area = 0
      for c in cnts:
      # approximate the contour
      	peri = cv2.arcLength(c, True)
      	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
      	# if our approximated contour has four points, then we
      	# can assume that we have found our screen
      	if len(approx) == 4:
                screenCnt = approx
                area = cv2.contourArea(c)
                break
      return screenCnt, area
#first do edge detection and then do floodfill
#it is effective to image with pure background
def twofloodFill_2(image):
      image_blurred = cv2.GaussianBlur(image, (9, 9),0)#pyrMeanShiftFiltering(image, 25, 10)pyrMeanShiftFiltering(image, 25, 10)#GaussianBlur(image, (9, 9),0)#cv2.medianBlur(image, 5)
      edges1 = cv2.Canny(image_blurred, 50, 150, apertureSize=3)
      image_water1 = fill_color_demo(edges1)
      ## 边缘检测
      edges = cv2.Canny(image_water1, 50, 150, apertureSize=3)
      ## 膨胀处理
      closed = cv2.dilate(edges, None, iterations = 2)
      print("STEP 1: Edge Detection")
      cv2.imshow("Image", edges)
      cv2.imshow("Edged", closed)
      cv2.waitKey(0)
      cnts = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      cnts = imutils.grab_contours(cnts)
      cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
      screenCnt = []
      area = 0
      for c in cnts:
      # approximate the contour
      	peri = cv2.arcLength(c, True)
      	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
      	# if our approximated contour has four points, then we
      	# can assume that we have found our screen
      	if len(approx) == 4:
                area = cv2.contourArea(c)
                screenCnt = approx
                break 
      return screenCnt, area	
def drawContour(screenCnt, image):
      print("STEP 2: Find contours of card")
      cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
      cv2.imshow("Outline1", image)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
#load image and resize
image = cv2.imread("D:\\NetVirtaChanllengeProject\\test-image\\test28.jpg")
image = imutils.resize(image, height = 500)
image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)
image1 = image.copy()
#use two methods to deal with the image and get the corrdinates and area of contour
screenCnt1, area1 = twofloodFill_1(image)
screenCnt2, area2 = twofloodFill_2(image1)
print("screen1:", screenCnt1)
print("screen2:", screenCnt2)
# compare the two contour and find a best one
if len(screenCnt1) == 4 or len(screenCnt2) == 4:
      if area1 > area2:
            drawContour(screenCnt1, image.copy())
      else:
            drawContour(screenCnt2, image.copy())
