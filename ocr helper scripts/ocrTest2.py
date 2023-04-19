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
from pynput.keyboard import Key, Controller         # type: ignore

def touch(emulator, x, y, dx = 0, dy = 0, doubleClick = False):
    time.sleep(1)
    x = str(x + dx)
    y = str(y + dy)
    msg = 'input touchscreen tap ' + x + ' ' + y
    emulator.shell(msg)
    if doubleClick == True:
        emulator.shell(msg)
    time.sleep(1)

def swipe(emulator, device):
    global counter
    counter += 1
    print(counter)
    touch(emulator, 65, 715, 50, 50)
    x1 = str(random.randint(-150, 150) + 250)
    x2 = x1
    y1, y2 = '800', '520'
    swipe_time = '5'
    device.shell("input swipe " + str(x1) + " 572 " + str(x2) + " 174 2000")
    emulator.shell("input swipe " + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)

def recognizeText(emulator):
    emulator.shell("screencap -p /sdcard/screen.png")
    emulator.pull("/sdcard/screen.png", r"C:\Users\Administrator\Desktop\Automatization\screen.png")
    img = cv2.imread(r'C:\Users\Administrator\Desktop\Automatization\screen.png')
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    x,y,w,h = 600, 330, 30, 60  
    croppedImg1 = threshImg[y:y+h,x:x+w]
    x,y,w,h = 600, 720, 30, 60  
    croppedImg2 = threshImg[y:y+h,x:x+w]
    matchText1 = pytesseract.image_to_string(grayImg, lang='eng',config='--psm 6')
    print(matchText1)
    matchText2 = pytesseract.image_to_string(threshImg, lang='eng',config='--psm 6')
    print(matchText2)
    if re.search('Sign up with email instead', matchText1):
        print('phone')
    else:
        print('mobile')
    cv2.imshow('Original', img)
    cv2.imshow('Gray image', grayImg)
    cv2.imshow('Tresh image', threshImg)
    cv2.waitKey()

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
    x1 = str(random.randint(-150, 150) + 250)
    x2 = x1
    y1, y2 = '800', '520'
    emulator.shell("input swipe 250 800 250 520")
    global counter 
    counter = 0
    for i in range(30):
        swipe(emulator, emulator)
    recognizeText(emulator)
