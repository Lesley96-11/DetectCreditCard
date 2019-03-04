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
# load the image and resize
image = cv2.imread("D:\\NetVirtaChanllengeProject\\test5.jpg")
image = imutils.resize(image, height = 500)
image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)

#substract background
def fill_color_demo(image):
    copyIma = image.copy()
    h, w = image.shape[:2]
    print(h, w)
    mask = np.zeros([h+2, w+2], np.uint8)
    cv.floodFill(copyIma, mask, (20, 20), (0, 0, 0), (50, 50, 50), (50, 50, 50), cv.FLOODFILL_FIXED_RANGE)  
    return copyIma
image_blurred = cv2.medianBlur(image, 5)#pyrMeanShiftFiltering(image, 25, 10)pyrMeanShiftFiltering(image, 25, 10)#GaussianBlur(image, (9, 9),0)#cv2.medianBlur(image, 5)
image_water = fill_color_demo(image_blurred)
cv2.imshow("filter", image_blurred)
cv2.imshow("fill_color", image_water)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image_water, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)
def stretch(img):
    max_ = float(img.max())
    min_ = float(img.min())
 
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (255 / (max_ - min_)) * img[i, j] - (255 * min_) / (max_ - min_)
    return img
stretchedimg = stretch(gray)
cv2.imshow('stretchedimg', stretchedimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
## edge detection
edges = cv2.Canny(stretchedimg, 50, 150, apertureSize=3)
#
## dilate
closed = cv2.dilate(edges, None, iterations = 4)
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", closed)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
