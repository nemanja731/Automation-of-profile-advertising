import cv2
import numpy as np
import os
import re
import pytesseract
from pytesseract import Output

def loading(imgDirPath):
    data = sorted([os.path.join(imgDirPath, file) for file in os.listdir(imgDirPath) if file.endswith('.png')])
    img = [cv2.imread(d) for d in data]
    return img

def resizing(img):
    height = 220
    width = 220
    dim = (width, height)
    resizedImg = []
    for i in range(len(img)):
        resizedImg.append(cv2.resize(img[i], dim, interpolation = cv2.INTER_LINEAR))
    return resizedImg
    #print("Resized", resizedImg[0].shape)

def blurring(img):
    blurImg = []
    for i in range(len(img)):
        blur = cv2.GaussianBlur(img[i], (5, 5), 0)
        #blur = cv2.blur(img[i], (5, 5), 0)
        blurImg.append(blur)
    return blurImg

def rgbToGray(img):
    grayImg = []
    for i in range(len(img)):
        gray = cv2.cvtColor(img[i], cv2.COLOR_BGR2GRAY)
        grayImg.append(gray)
    return grayImg

def thresholding(grayImg):
    _, threshImg = cv2.threshold(grayImg[0], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return threshImg

def getFgBg(threshImg):
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sureBg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    distTransform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sureFg = cv2.threshold(distTransform, 0.7 * distTransform.max(), 255, 0)
    # Finding unknown region
    sureFg = np.uint8(sureFg)
    return sureFg, sureBg

# Preprocessing
def processing(imgDirPath):
    img = loading(imgDirPath)
    resizedImg = resizing(img)
    blurImg = blurring(img)
    grayImg = rgbToGray(img)
    threshImg = thresholding(grayImg)
    fgImg, bgImg = getFgBg(threshImg)
    cv2.imshow("Original Image", img[0])
    cv2.waitKey(0)
    cv2.imshow("Resized Image", resizedImg[0])
    cv2.waitKey(0)
    cv2.imshow("Blurred Image", blurImg[0])
    cv2.waitKey(0)
    cv2.imshow("Gray Image", grayImg[0])
    cv2.waitKey(0)
    cv2.imshow("Treshold Image", threshImg)
    cv2.waitKey(0)
    cv2.imshow("Background Image", bgImg)
    cv2.waitKey(0)
    cv2.imshow("Foreground Image", fgImg)
    cv2.waitKey(0)

def getWordsFromBoxes(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    nBoxes = len(d['level'])
    for i in range(nBoxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img1 = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('img', img1)
    cv2.waitKey(0)

def getCharactersFromBoxes(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img2 = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 0, 0), 1)
    cv2.imshow('img', img2)
    cv2.waitKey(0)

def findPattern(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    datePattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
    nBoxes = len(d['text'])
    for i in range(nBoxes):
        if re.match(datePattern, d['text'][i]):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(0)

if __name__ == "__main__":
    pro = processing(imgDirPath = "./")
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = cv2.imread('./1.png')
    print(pytesseract.image_to_string(img))
    cv2.imshow('Slika', img)
    cv2.waitKey(0)
    findPattern(img)
    getWordsFromBoxes(img)
    getCharactersFromBoxes(img)