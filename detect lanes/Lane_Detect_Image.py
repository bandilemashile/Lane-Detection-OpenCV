# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:40:37 2020

@author: Bandile Mashile
"""


import cv2
import numpy as np



def make_coordinates(image,line_parameters):
    slope,intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])
   
def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
           left_fit.append((slope,intercept))
        else:
           right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit,axis = 0)
    right_fit_average = np.average(right_fit,axis = 0)
    left_line = make_coordinates(image,left_fit_average)
    right_line = make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])
       

def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
           x1,y1,x2,y2 = line.reshape(4)
           cv2.line(line_image,(x1,y1), (x2,y2), (255,0,0) ,10)
    return line_image

def canny(image):
   gray = cv2.cvtColor(road_copy,cv2.COLOR_RGB2GRAY)
   blur = cv2.GaussianBlur(gray, (5,5),0)
   canny = cv2.Canny(blur, 50, 150)
   return  canny

def region_of_intrest(image):
    height = image.shape[0]  
    polygons = np.array([[(200, height), (1100, height), (550 , 250)]])
    mask =np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

image = cv2.imread('road.png')
road_copy = np.copy(image)

canny_image = canny(road_copy)
cropped_image = region_of_intrest(canny_image)
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40,maxLineGap =5)
averaged_lines = average_slope_intercept(road_copy,lines)
line_image = display_lines(road_copy, averaged_lines)
combo__image = cv2.addWeighted(road_copy, 0.8, line_image, 1, 1)
cv2.imshow('result',combo__image )
cv2.waitKey(0)
cv2.destroyAllWindows()