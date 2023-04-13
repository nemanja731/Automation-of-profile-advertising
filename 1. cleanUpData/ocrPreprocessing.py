import cv2
import numpy as np
import os
import re
import pytesseract
from pytesseract import Output

def loading(img_dir_path):
    data = sorted([os.path.join(img_dir_path, file) for file in os.listdir(img_dir_path) if file.endswith('.png')])
    img = [cv2.imread(d) for d in data]
    return img

def resizing(img):
    height = 220
    width = 220
    dim = (width, height)
    res_img = []
    for i in range(len(img)):
        res_img.append(cv2.resize(img[i], dim, interpolation = cv2.INTER_LINEAR))
    return res_img
    #print("Resized", res_img[0].shape)

def blurring(img):
    blur_img = []
    for i in range(len(img)):
        blur = cv2.GaussianBlur(img[i], (5, 5), 0)
        #blur = cv2.blur(img[i], (5, 5), 0)
        blur_img.append(blur)
    return blur_img

def rgb_to_gray(img):
    gray_img = []
    for i in range(len(img)):
        gray = cv2.cvtColor(img[i], cv2.COLOR_BGR2GRAY)
        gray_img.append(gray)
    return gray_img

def thresholding(gray_img):
    _, thresh_img = cv2.threshold(gray_img[0], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh_img

def get_fg_bg(thresh_img):
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    return sure_fg, sure_bg

# Preprocessing
def processing(img_dir_path):
    img = loading(img_dir_path)
    res_img = resizing(img)
    blur_img = blurring(img)
    gray_img = rgb_to_gray(img)
    thresh_img = thresholding(gray_img)
    fg_img, bg_img = get_fg_bg(thresh_img)
    cv2.imshow("Original Image", img[0])
    cv2.waitKey(0)
    cv2.imshow("Resized Image", res_img[0])
    cv2.waitKey(0)
    cv2.imshow("Blurred Image", blur_img[0])
    cv2.waitKey(0)
    cv2.imshow("Gray Image", gray_img[0])
    cv2.waitKey(0)
    cv2.imshow("Treshold Image", thresh_img)
    cv2.waitKey(0)
    cv2.imshow("Background Image", bg_img)
    cv2.waitKey(0)
    cv2.imshow("Foreground Image", fg_img)
    cv2.waitKey(0)

def get_words_from_boxes(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img1 = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('img', img1)
    cv2.waitKey(0)

def get_characters_from_boxes(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img2 = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 0, 0), 1)
    cv2.imshow('img', img2)
    cv2.waitKey(0)

def find_pattern(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if re.match(date_pattern, d['text'][i]):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(0)

if __name__ == "__main__":
    #pro = processing(img_dir_path = "./")
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = cv2.imread('./1.png')
    print(pytesseract.image_to_string(img))
    cv2.imshow('Slika', img)
    cv2.waitKey(0)
    #find_pattern(img)
    #get_words_from_boxes(img)
    #get_characters_from_boxes(img)