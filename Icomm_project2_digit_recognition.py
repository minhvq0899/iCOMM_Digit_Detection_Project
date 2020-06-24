# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:48:09 2020

@author: minhv
"""

import cv2 
import pytesseract 
import argparse

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe' 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required = True, 
                help="path to input image")
ap.add_argument("-o", "--output", type=str, required = True, 
                help="path to output image")
args = vars(ap.parse_args())

class digit_detection_processor():
    def __init__(self, image):
        self.image = image
    def process(self):
        # input
        img = self.image
        H,W,l = img.shape
        img = cv2.resize(img, (W*10, H*10)) 
        H,W,l = img.shape
        cv2.imshow('Raw Input', img)
        cv2.waitKey(0) 
        
        # result
        result = pytesseract.image_to_string(img)
        
        # edit
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255-gray
        ret,thresh = cv2.threshold(gray,100,0,cv2.THRESH_TOZERO)
        thresh = 255-thresh
        cv2.imshow('After Threshed', thresh)
        cv2.waitKey(0) 
        
        # get boxes
        boxes = pytesseract.image_to_boxes(img)
        font = cv2.FONT_HERSHEY_TRIPLEX
        
        for b in boxes.splitlines():
            b = b.split(' ')
            x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img,(x,H-y),(w,H-h),(0,0,255),1)
            cv2.putText(img,b[0],(x,H-y),font,0.75,(50,50,255),1)
        
        # print(boxes)
        
        cv2.imshow('Output', img)
        cv2.waitKey(0) 
        
        print(result)
        
        return img
            

if __name__ == "__main__":
    image = cv2.imread(args["image"]) 
    processor = digit_detection_processor(image)
    image = processor.process()
    cv2.imwrite(args["output"], image)
        
    
    