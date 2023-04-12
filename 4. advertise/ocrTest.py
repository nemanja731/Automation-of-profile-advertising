import cv2
import os
import pyautogui
import pytesseract
import pyperclip
import random
import re
import subprocess
import threading
import time
import tkinter as tk
from datetime import date
from ppadb.client import Client as AdbClient
from pynput.keyboard import Key, Controller

def touch(emulator, x, y, dx = 0, dy = 0, double_click = False):
    time.sleep(1)
    x = str(x + dx)
    y = str(y + dy)
    msg = 'input touchscreen tap ' + x + ' ' + y
    emulator.shell(msg)
    if double_click == True:
        emulator.shell(msg)
    time.sleep(1)

def swipe(emulator):
    global counter
    counter += 1
    print(counter)
    #touch(emulator, 65, 715, 50, 50)
    x1 = str(random.randint(-150, 150) + 250)
    x2 = x1
    y1, y2 = '800', '520'
    swipe_time = '5'
    #device.shell("input swipe " + str(x1) + " 572 " + str(x2) + " 174 2000")
    emulator.shell("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)

def recognize_text(emulator):
    emulator.shell("screencap -p /sdcard/screen.png")
    emulator.pull("/sdcard/screen.png", r"C:\Users\Administrator\Desktop\Automatization\screen.png")
    img = cv2.imread(r'C:\Users\Administrator\Desktop\Automatization\screen.png')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #x,y,w,h = 600, 330, 30, 60  
    #cropped_img1 = thresh_img[y:y+h,x:x+w]
    #x,y,w,h = 600, 720, 30, 60  
    #cropped_img2 = thresh_img[y:y+h,x:x+w]
    match_text1 = pytesseract.image_to_string(gray_img, lang='eng',config='--psm 6')
    print(match_text1)
    match_text2 = pytesseract.image_to_string(thresh_img, lang='eng',config='--psm 6')
    print(match_text2)
    if re.search('Sign up with email instead', match_text1):
        print('phone')
    else:
        print('mobile')
    # cv2.imshow('Original', img)
    # cv2.imshow('Gray image', gray_img)
    # cv2.imshow('Tresh image', thresh_img)
    # cv2.waitKey()

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = "C:/Users/Administrator/Downloads/tesseract-ocr/tesseract.exe"
    client = AdbClient(host = "127.0.0.1", port = 5037)
    while True:
        try:
            os.system('cmd /c "adb devices"')
            emulator = client.device("emulator-5568")
            break
        except:
            print('Try to connect to emulator-5568')
            time.sleep(1)
    print('Successufuly connected to emulator-5568!')
    #x1 = str(random.randint(-150, 150) + 250)
    #x2 = x1
    #y1, y2 = '800', '520'
    #emulator.shell("input swipe 250 800 250 520")
    global counter 
    counter = 0
    for i in range(30):
        swipe(emulator)
    #recognize_text(emulator)
