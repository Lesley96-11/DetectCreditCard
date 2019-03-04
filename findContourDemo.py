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

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image1 = cv2.GaussianBlur(image, (7 , 7), 0)
## edge detection
edges = cv2.Canny(image1, 50, 150, apertureSize=3)
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
