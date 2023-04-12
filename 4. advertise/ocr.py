import tkinter as tk
import pytesseract
import cv2
import re


if __name__ == '__main__':
    path = './screen.jpg'
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _,imgthreshInv = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    matchText1 = pytesseract.image_to_string(img, lang = "eng")
    matchText2 = pytesseract.image_to_string(gray, lang = "eng")
    matchText3 = pytesseract.image_to_string(blurred, lang = "eng")
    matchText4 = pytesseract.image_to_string(imgthreshInv, lang = "eng")
    if re.search('Close', matchText1):    
        print('Ima')
    # cv2.imshow('Original image', img)
    # cv2.imshow('Gray image', gray)
    # cv2.imshow('Blurred image', blurred)
    # cv2.imshow('Treshold image', imgthreshInv)
    # cv2.waitKey(0)
    print(matchText1)
    print(matchText2)
    print(matchText3)
    print(matchText4)
