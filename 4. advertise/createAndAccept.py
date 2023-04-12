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

#815, 190       gmx app
#916, 190       snapchat app

#adb devices id
# 0 - 5554
# 1 - 5556
# 2 - 5558
# 3 - 5560
# 4 - 5562
# 5 - 5564
# 6 - 5566
# 7 - 5568
# 8 - 5570
# 9 - 5572
# 10 - 5574
# 11 - 5576
# 12 - 5578

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.initialize()
        self.create_widgets()
        self.test()

    def initialize(self):
        self.numEmulators = 6
        self.index = 0
        self.indexSnapUsername = 0
        self.fullGmx = []
        self.gmxMails = []
        self.gmxPasswords = []
        self.snapNames = []
        self.snapPasswords = []
        self.snapUsernames = []
        self.usedSnapUsernames = []
        self.usernames = []
        self.fileName = ''

    def create_widgets(self):
        self.main_frame = tk.Frame(master=self.master)
        self.main_frame.pack(fill =tk.BOTH, side = tk.LEFT, expand = True)
        self.frame_buttons = tk.Frame(master=self.main_frame)
        self.button_start = tk.Button(master=self.frame_buttons, text= "START", font = ('Arial',10,'bold'), width= 15, pady= 5, background= "green", foreground= "white", command= self.start_process)
        self.button_quit = tk.Button(master=self.frame_buttons, text= "STOP", font = ('Arial',10,'bold'), width= 15, pady= 5, bg= "red", fg= "white", command= self.stop_process)
        self.button_quit.config(state='disabled', background = 'gray', foreground='gray')
        self.button_start.pack(side = tk.LEFT, padx = 10)
        self.button_quit.pack(side = tk.LEFT)
        self.frame_emulators = tk.Frame(master=self.main_frame)
        self.emulator_entry = []
        for i in range(6):
            self.e = tk.Entry(self.frame_emulators, width = 10, font=('Arial',10,'bold'))       
            self.e.grid(row=i, column=1)
            self.e.insert(tk.END, 'Emulator ' + str(i + 1))
            self.e.config(state='disabled')
            self.e = tk.Entry(self.frame_emulators, width = 52, font=('Arial',10,'bold'))
            self.emulator_entry.append(self.e)
            self.e.grid(row=i, column=2)
            self.e.insert(tk.END, 'Emulator doesn\'t exists')
            self.e.config(state='disabled')
        self.main_frame.rowconfigure(0, minsize = 10)
        self.main_frame.columnconfigure(0, minsize = 30)
        self.frame_buttons.grid(row=1, column= 1, sticky="ns", pady=30)
        self.frame_emulators.grid(row=2, column= 1, sticky="ns")

    def insert_text(self, emulator_entry, text):
        emulator_entry.config(state='normal')
        emulator_entry.delete(0,"end")
        emulator_entry.insert(0, text)
        emulator_entry.config(state='disabled')

    def move_and_click(self, x, y):
        pyautogui.moveTo(x, y, 0.5)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(0.5)

    def delete_first_6(self):
        self.move_and_click(1088, 399)      #display LD multiplayer app
        start = [
            [462, 290],
            [462, 342],
            [462, 393],
            [461, 442],
            [460, 495],
            [461, 545],
        ]
        for i in range(6):
            self.move_and_click(start[i][0], start[i][1])       #(i+1). checker
        self.move_and_click(586, 679)       #batch
        self.move_and_click(630, 649)       #remove selected
        self.move_and_click(706, 504)       #confirm

    def change_emulator_name(self, x, y):
        self.move_and_click(x, y)
        time.sleep(1)
        pyautogui.click(x, y)
        time.sleep(1)
        for i in range(20):
            pyautogui.hotkey('backspace')
            time.sleep(0.1)
        today = date.today()
        s = today.strftime("%d %m")
        d, m = s.split(" ")
        m = m.lstrip('0')
        text = d + '.' + m
        pyautogui.write(text, interval = 0.2)

    def create_and_adjust_first_emulator(self):
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(1008, 681)      #new/clone
        self.move_and_click(660, 397)       #new player
        time.sleep(5)
        self.change_emulator_name(626, 594)
        time.sleep(3)
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(951, 596)       #7. emulator open settings
        time.sleep(1)
        self.move_and_click(818, 150)       #mobile
        self.move_and_click(708, 286)       #540x960 (dpi 240)
        self.move_and_click(782, 416)       #RAM
        self.move_and_click(757, 580)       #2048M
        self.move_and_click(448, 497)       #other settings
        self.move_and_click(793, 500)       #ADB debugging
        self.move_and_click(774, 526)       #open local connection
        self.move_and_click(994, 718)       #save
        time.sleep(1)
        self.move_and_click(1088, 399)      #display LD multiplayer app
        time.sleep(1)
        self.move_and_click(861, 593)       #run first emulator
        time.sleep(30)
        #fix bug with emulator
        pyautogui.moveTo(x=552, y=39)
        time.sleep(0.2)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(x=551, y=33)
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')
        time.sleep(1)
        self.move_and_click(762, 573)      #click on emulator
        #uninstall app on 3rd place, because maybe it is there
        pyautogui.moveTo(x = 814, y = 192)
        time.sleep(0.5)
        pyautogui.mouseDown(button='left')
        time.sleep(2)
        pyautogui.moveTo(x = 659, y = 158)
        pyautogui.mouseUp(button='left')
        self.move_and_click(898, 504)
        time.sleep(1)
        self.move_and_click(762, 573)      #click on emulator
        time.sleep(1)
        #click install apk GMX
        keyboard.press(Key.ctrl)
        keyboard.press('3')
        keyboard.release('3')
        keyboard.release(Key.ctrl)
        time.sleep(2)
        self.move_and_click(770, 146)       #GMX aplikacija
        self.move_and_click(1146, 456)      #open
        time.sleep(20)
        self.move_and_click(762, 573)       #click on emulator
        #click install apk Snapchat
        keyboard.press(Key.ctrl)
        keyboard.press('3')
        keyboard.release('3')
        keyboard.release(Key.ctrl)
        time.sleep(2)
        self.move_and_click(775, 167)       #Snapchat aplikacija
        self.move_and_click(1146, 456)      #open
        time.sleep(20)
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(861, 593)      #turn off first emulator
        self.move_and_click(708, 486)       #confirm
        time.sleep(10)

    def batch_clone_5(self):
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(462, 596)       #check first emulator
        self.move_and_click(588, 680)       #batch
        self.move_and_click(642, 558)       #batch clone(5 players)
        time.sleep(20)
        self.move_and_click(462, 596)       #uncheck first emulator

    def rename_emulators(self):
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(1094, 630)      #scroll down
        rename = [
            [862, 370],
            [863, 421],
            [862, 470],
            [863, 521],
            [862, 575],
            [864, 626]
        ]
        for i in range(6):
            self.move_and_click(rename[i][0], rename[i][1])       #check first emulator
            time.sleep(1)
            pyautogui.click(rename[i][0], rename[i][1])
            time.sleep(1)
            if i > 0:
                pyautogui.hotkey('backspace')
                time.sleep(0.1)
                pyautogui.hotkey('backspace')
            pyautogui.write(" - " + self.usernames[i], interval = 0.5)

    def make_emulators(self):
        self.delete_first_6()
        self.create_and_adjust_first_emulator()
        self.batch_clone_5()

    def touch(self, emulator, x, y, dx = 0, dy = 0, double_click = False):
        time.sleep(1)
        x = str(x + dx)
        y = str(y + dy)
        emulator.shell('input touchscreen tap ' + x + ' ' + y)
        if double_click == True:
            emulator.shell('input touchscreen tap x y')
        time.sleep(1)

    def swipe(emulator):
        x1 = x2 = str(random.randint(-150, 150) + 250)
        y1, y2 = '800', '520'
        emulator.shell("input swipe " + x1 + " " + y1  + " " + x2  + " " + y2)

    def log_on_gmx(self, emulator):
        self.touch(emulator, 308, 157, random.randint(-5, 5), random.randint(-5, 5))        #enter gmx app
        time.sleep(10)
        text = 'input text ' + self.gmxMails[self.index]
        self.touch(emulator, 240, 345, random.randint(-100, 100), random.randint(-2, 2))        #enter gmx email
        time.sleep(2)
        emulator.shell(text)
        time.sleep(2)
        text = 'input text ' + self.gmxPasswords[self.index]
        self.touch(emulator, 240, 480, random.randint(-100, 100), random.randint(-2, 2))        #enter gmx password
        time.sleep(2)
        emulator.shell(text)
        time.sleep(2)
        self.touch(emulator, 246, 716, random.randint(-150, 150), random.randint(-5, 5))       #login
        time.sleep(10)
        for i in range(4):
            self.touch(emulator, 250, 855, random.randint(-150, 150), random.randint(-10, 10))
            time.sleep(1)
        time.sleep(10)
        emulator.shell('input keyevent 3')
        time.sleep(3)

    def log_on_snapchat(self, emulator):
        self.touch(emulator, 430, 163, random.randint(-10, 10), random.randint(-10, 10))        #enter snapchat app
        time.sleep(10)
        self.touch(emulator, 340, 865, random.randint(-30, 30), random.randint(-5, 5))      #sign up
        time.sleep(2)
        self.touch(emulator, 250, 865, random.randint(-100, 100), random.randint(-5, 5))        #continue
        time.sleep(2)
        self.touch(emulator, 280, 560, random.randint(-2, 2), random.randint(-1, 1))        #allow snapchat to access your contacts? Deny
        time.sleep(2)
        self.touch(emulator, 280, 560, random.randint(-2, 2), random.randint(-1, 1))        #allow snapchat to make and manage phone calls? Deny
        time.sleep(1)
        text = 'input text ' + self.snapNames[self.index]
        self.touch(emulator, 250, 373, random.randint(-70, 70), random.randint(-7, 7))      #first name    
        time.sleep(2)
        emulator.shell(text)
        time.sleep(2)
        self.touch(emulator, 250, 865, random.randint(-100, 100), random.randint(-5, 5))        #Sign up and accept
        time.sleep(2)
        #choose month of birthday
        temp1 = random.randint(1, 12)
        for i in range(temp1):
            self.touch(emulator, 118, 690, random.randint(-5, 5), random.randint(-2, 2))
        #choose day of birthday
        temp2 = random.randint(1, 30)
        for i in range(temp2):
            self.touch(emulator, 240, 690, random.randint(-5, 5), random.randint(-2, 2))
        #choose year of birthday
        temp3 = random.randint(5, 8)
        for i in range(temp3):
            self.touch(emulator, 360, 690, random.randint(-5, 5), random.randint(-2, 2))
        self.touch(emulator, 250, 558, random.randint(-100, 100), random.randint(-10, 10))      #Continue
        time.sleep(2)
        if self.ocr(emulator) == 'Change my username':
            self.touch(emulator, 250, 500, random.randint(-20, 20), random.randint(-1, 1))      #change my username
            self.touch(emulator, 250, 510, random.randint(-100, 100), random.randint(-3, 3), True)        #username
        else:
            self.touch(emulator, 250, 525, random.randint(-100, 100), random.randint(-3, 3))        #username
        time.sleep(1)
        #OCR: is already taken! // Username available
        self.remember_username()
        while True:
            text = 'input text ' + self.snapUsernames[self.indexSnapUsername]
            time.sleep(4)
            if self.ocr(emulator) == 'Username available':
                break
            self.remember_username()
        emulator.shell(text)
        time.sleep(3)
        self.touch(emulator, 250, 865, random.randint(-100, 100), random.randint(-5, 5))        #Continue
        time.sleep(2)
        self.touch(emulator, 250, 510, random.randint(-100, 100), random.randint(-5, 5))        #password
        text = 'input text ' + self.snapPasswords[self.index]
        emulator.shell(text)
        time.sleep(3)
        self.touch(emulator, 250, 865, random.randint(-100, 100), random.randint(-5, 5))        #Continue
        time.sleep(2)
        self.touch(emulator, 281, 573, random.randint(-2, 2), random.randint(-1, 1))        #allow snapchat to make and manage phone calls? Deny
        time.sleep(1)
        if self.ocr(emulator) == 'Sign up with email instead':
            self.touch(emulator, 240, 285, random.randint(-70, 70), random.randint(-2, 2))      #sign up with email instead
            time.sleep(1)
            self.touch(emulator, 280, 562, random.randint(-5, 5), random.randint(-1, 1))        #deny
            time.sleep(1)
            self.touch(emulator, 250, 480, random.randint(-100, 100), random.randint(-3, 3))    #email
        text = 'input text ' + self.gmxMails[self.index]
        emulator.shell(text)
        time.sleep(1)
        self.touch(emulator, 250, 865, random.randint(-100, 100), random.randint(-5, 5))        #Continue
        time.sleep(1)
        self.touch(emulator, 465, 85, random.randint(-1, 1), random.randint(-1, 1))     #skip
        time.sleep(1)
        self.touch(emulator, 245, 615, random.randint(-3, 3), random.randint(-1, 1))     #skip
        time.sleep(1)
        self.touch(emulator, 250, 565, random.randint(-100, 100), random.randint(-10, 10))      #turn on
        time.sleep(1)
        self.touch(emulator, 389, 594, random.randint(-2, 2), random.randint(-1, 1))        #allow snapchat to take pictures and record videos? allow
        time.sleep(1)
        self.touch(emulator, 389, 594, random.randint(-2, 2), random.randint(-1, 1))      #allow snapchat to access photos, media, and files on your device? allow
        time.sleep(1)
        self.touch(emulator, 285, 525, random.randint(-2, 2), random.randint(-1, 1))        #allow snapchat to record audio? deny
        time.sleep(1)
        self.touch(emulator, 20, 50, random.randint(-2, 2), random.randint(-1, 1))      #profile
        time.sleep(1)
        self.create_avatar(emulator)
        self.touch(emulator, 462, 60, random.randint(-2, 2), random.randint(-1, 1))     #settings
        time.sleep(1)
        time.sleep(1)
        self.touch(emulator, 250, 485, random.randint(-50, 50), random.randint(-5, 5))      #email  
        time.sleep(1)
        self.touch(emulator, 390, 462, random.randint(-2, 2), random.randint(-1, 1))        #uncheck
        time.sleep(1)
        self.touch(emulator, 250, 547, random.randint(-50, 50), random.randint(-1, 1))      #resend verification email
        time.sleep(1)
        self.touch(emulator, 250, 545, random.randint(-50, 50), random.randint(-5, 5))      #okay
        emulator.shell('input keyevent 66')
        self.touch(emulator, 308, 157, random.randint(-5, 5), random.randint(-5, 5))        #enter gmx app
        time.sleep(10)
        time.sleep(1)
        self.touch(emulator, 250, 190, random.randint(-50, 50), random.randint(-2, 2))      #team snapchat
        time.sleep(1)
        self.touch(emulator, 235, 780, random.randint(-10, 10), random.randint(-2, 2))      #confirm email
        time.sleep(5)
        emulator.shell('input keyevent 66')

    def create_avatar(self, emulator):
        self.touch(emulator, 250, 257, random.randint(-2, 2), random.randint(-1, 1))        #create my avatar
        self.touch(emulator, 365, 750, random.randint(-2, 2), random.randint(-1, 1))        #press man
        self.touch(emulator, 450, 50, random.randint(-2, 2), random.randint(-1, 1))     #skip
        self.touch(emulator, 180, 535, random.randint(-20, 20), random.randint(0, 305))     #skin tone
        self.touch(emulator, 85, 875, random.randint(-2, 2), random.randint(-1, 1))     #hair
        self.touch(emulator, 20, 525, random.randint(0, 445), random.randint(0, 315))       #hair color
        self.touch(emulator, 170, 875, random.randint(-2, 2), random.randint(-1, 1))     #hair
        if random.randint(0, 1) == 0:
            self.touch(emulator, 20, 665, random.randint(0, 440), random.randint(0, 115))       #choose hair
        else:
            self.swipe(emulator, 250, 800, 250, 520)
            self.touch(emulator, 20, 570, random.randint(0, 440), random.randint(0, 240))       #choose hair
        self.touch(emulator, 450, 65, random.randint(-2, 2), random.randint(-1, 1))     #save
        self.touch(emulator, 240, 475, random.randint(-100, 100), random.randint(-7, 7))     #ready to pick an outfit? yes
        #choose outfit
        self.touch(emulator, 65, 715, 50, 50)
        end = random.randint(1, 20)
        for i in range(end):
            self.swipe(emulator, 250, 800, 250, 520)
        self.touch(emulator, 20, 505, random.randint(0, 440), random.randint(0, 310))
        self.touch(emulator, 450, 65, random.randint(-2, 2), random.randint(-1, 1))     #save
    
    def ocr(self, emulator):
        emulator.shell("screencap -p /sdcard/screen.png")
        emulator.pull("/sdcard/screen.png", r"C:\Users\Administrator\Desktop\Automatization\screen.png")
        img = cv2.imread(r'C:\Users\Administrator\Desktop\Automatization\screen.png')
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        match_text1 = pytesseract.image_to_string(gray_img, lang='eng',config='--psm 6')
        match_text2 = pytesseract.image_to_string(thresh_img, lang='eng',config='--psm 6')
        self.check_ocr(self, match_text1, match_text2)

    def check_ocr(self, match_text1, match_text2):
        if bool(re.search("Username available", match_text1)) or bool(re.search("Username available", match_text2)):
            return "Username available"
        else:
            return ""

    def remember_username(self):
        while True:
            if self.snapUsernames[self.indexSnapUsername] in self.usedSnapUsernames:
                self.indexSnapUsername += 1
                self.indexSnapUsername %= len(self.snapUsernames)
            else:
                break
        if len(self.snapUsernames) > 0:
            self.snapUsername = self.snapUsernames[self.indexSnapUsername]
            self.indexSnapUsername += 1
            self.indexSnapUsername %= len(self.snapUsernames)


    def run_and_connect_emulator(self, start, i, client, emulators_names):
        self.move_and_click(start[i][0], start[i][1])       #run (i+1). emulator
        time.sleep(30)
        emulator = 0
        while True:
            try:
                os.system('cmd /c "adb devices"')
                emulator = client.device(emulators_names[i])
                break
            except:
                print('Try to connect to ' + emulators_names[i])
                time.sleep(1)
        print('Successufuly connected to ' + emulators_names[i] + "!")
        pyautogui.moveTo(x=552, y=39)
        time.sleep(0.2)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(x=551, y=33)
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')
        time.sleep(1)
        self.move_and_click(762, 573)      #click on emulator
        time.sleep(1)
        return emulator

    def abort(self):
        self.button_quit.config(state='disabled', background = 'gray', foreground='gray')
        self.button_start.config(state='disabled', background = 'gray', foreground='gray')

    def catch_adb_device(self):
        self.move_and_click(1088, 399)      #display LD multiplayer app
        time.sleep(1)
        self.move_and_click(1095, 223)      #scroll up
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save('./screenshot.png')
        time.sleep(2)
        img = cv2.imread('./screenshot.png', 0)
        thresh_img = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        x,y,w,h = 600, 720, 30, 60  
        cropped_img = thresh_img[y:y+h,x:x+w]
        match_text = pytesseract.image_to_string(cropped_img, lang='eng',config='--psm 6')
        print(match_text)
        if bool(re.search("1", match_text)):
            emulators_names = ["emulator-5556", "emulator-5558", "emulator-5560", "emulator-5562", "emulator-5564", "emulator-5566"]
            return emulators_names
        if bool(re.search("7", match_text)):
            emulators_names = ["emulator-5568", "emulator-5570", "emulator-5572", "emulator-5574", "emulator-5576", "emulator-5578"]
            return emulators_names
        return []

    def work(self):
        emulators_names = self.catch_adb_device()
        if emulators_names == []:
            self.insert_text(self.emulator_entry[0], 'Error: ocr can\'t recognize number')
            return
        print(emulators_names)
        client = AdbClient(host = "127.0.0.1", port = 5037)
        start = [
            [862, 370],
            [863, 420],
            [861, 473],
            [860, 522],
            [861, 574],
            [859, 627]
        ]
        time.sleep(1)
        self.move_and_click(1088, 399)      #display LD multiplayer app
        self.move_and_click(1094, 630)      #scroll down
        for i in range(0, 6):
            emulator = self.run_and_connect_emulator(start, i, client, emulators_names)
            j = 0
            for f in self.functions:
                f(emulator)
                if self.flag:
                    self.insert_text(self.emulator_entry[i], 'Error: ' + self.functionsName[j])
                    self.abort()
                    return
                j += 1
            self.move_and_click(1088, 399)      #display LD multiplayer app
            self.move_and_click(1094, 630)      #scroll down
            self.move_and_click(start[i][0], start[i][1])       #turn off emulator
            self.insert_text(self.emulator_entry[i], 'Emulator is complete with setup')
            self.nextFunction()
        self.finishFunction()
        self.rename_emulators()

    def makeOutputFile(self):
        today = date.today()
        s = today.strftime("%d %m")
        d, m = s.split(" ")
        m = m.lstrip('0')
        self.fileName = '../' + d + '.' + m + '.txt'
        with open(self.fileName, 'w') as Writer:
            pass

    def extractSnapNames(self):
        self.scNamesMainTxt = './Names for SC.txt'
        self.scNamesHelperTxt = './namesSC.txt'
        with open('./namesSC.txt', 'r') as Reader:
            lines = Reader.readlines()
        if len(lines) < self.numEmulators:
            with open('./Names for SC.txt', 'r') as Reader:
                lines2 = Reader.readlines()
            with open('./namesSC.txt', 'w') as Writer:
                Writer.writelines(lines2)
        with open('./namesSC.txt', 'r') as Reader:
            for i in range(0, self.numEmulators):
                line = Reader.readline().rstrip('\n')
                self.snapNames.append(line)
            lines2 = Reader.readlines()
        with open('./namesSC.txt', 'w') as Writer:
            Writer.writelines(lines2)

    def extractData(self):
        for i in range(0, len(self.fullGmx)):
            gmxMail, gmxPassword = self.fullGmx[i].split(':')
            self.gmxMails.append(gmxMail)
            self.gmxPasswords.append(gmxPassword.rstrip('\n'))
            self.snapPasswords.append('Password321')         

    def extractSnapUsernames(self):
        with open('./snapUsernames.txt', 'r') as Reader:
            lines = Reader.readlines()
        self.snapUsernames = []
        for i in range(0, len(lines)):
            self.snapUsernames.append(lines[i].rstrip('\n'))

    def checkEnoughData(self):
        self.initialize()
        with open('./gmx.txt', "r") as Reader:
            lines = Reader.readlines()
            if len(lines) < self.numEmulators:
                for i in range(6):
                    self.insert_text(self.emulator_entry[i], 'there are not enough gmx mails you have only ' + str(len(lines)) + ' mails')
                return False
        with open('./gmx.txt', "r") as Reader:
            for i in range(0, self.numEmulators):
                line = Reader.readline()
                self.fullGmx.append(line)
            lines2 = Reader.readlines()
        with open('./gmx.txt', "w") as Writer:
            Writer.writelines(lines2)
        with open('./mails.txt', "w") as Writer:
            self.fullGmx[self.numEmulators - 1] = self.fullGmx[self.numEmulators - 1].rstrip('\n')
            Writer.writelines(self.fullGmx) 
            self.fullGmx[self.numEmulators - 1] += '\n'
        self.makeOutputFile()
        self.extractSnapNames()
        self.extractData()
        self.extractSnapUsernames()
        if len(self.snapUsernames) < self.numEmulators:
            for i in range(6):
                self.insert_text(self.emulator_entry[i], 'there are not enough snap usernames you have only ' + str(len(self.snapUsernames)) + ' usernames')
            return False
        return True

    def nextFunction(self):
        if self.snapUsername != '':
            self.usedSnapUsernames.append(self.snapUsername)
        with open(self.fileName, 'a') as Writer:
            Writer.write(self.fullGmx[self.index])
            Writer.write(self.snapUsername + ':' + self.snapPasswords[self.index] + '\n' + '\n' + '\n')
        if self.index < self.numEmulators - 1:
            self.index += 1
        self.usernames.append(self.snapUsername)
        self.snapUsername = ''

    def finishFunction(self):
        self.nextFunction()
        with open(self.fileName, 'r') as Reader:
            lines = Reader.readlines()
        with open(self.fileName, 'w') as Writer:
            Writer.writelines(lines[:-2])
        with open('../' + self.fileName[3:-4] + ' messages.txt', 'w') as Writer2:
            with open('../Traffic Processor/orders/alba.txt', 'w') as Writer:
                for i in range(0, len(self.usernames)):
                    if i == len(self.usernames) - 1:
                        Writer.write(self.usernames[i])
                        Writer2.write('{Do you want to become rich? I have a great tip for you, you can add me on} snapchat: ' + self.usernames[i])
                    else:
                        Writer.write(self.usernames[i] + '\n')
                        Writer2.write('{Do you want to become rich? I have a great tip for you, you can add me on} snapchat: ' + self.usernames[i] + '\n')
        for username in self.usedSnapUsernames:
            if username != '':
                self.snapUsernames.remove(username)
        for i in range(0, len(self.snapUsernames) - 1):
            self.snapUsernames[i] = self.snapUsernames[i] + '\n' 
        with open('./snapUsernames.txt', 'w') as Writer:
            Writer.writelines(self.snapUsernames)

    def start_process(self):
        if self.checkEnoughData() == False:
            return
        subprocess.Popen('D:/LDPlayer/LDPlayer4.0/dnmultiplayer.exe')
        time.sleep(2)
        self.move_and_click(1418, 14)
        time.sleep(3)
        #self.make_emulators()
        self.button_quit.config(state='normal', background = 'red', foreground='white')
        self.button_start.config(state='disabled', background = 'gray', foreground='gray')
        self.flag = False
        self.functions = [
            self.log_on_gmx,
            self.log_on_snapchat,
        ]
        self.functionsName = [
            'log on gmx',
            'log on snapchat'
        ]
        self.work()
    
    def stop_process(self):
        self.flag = True
        self.button_quit.config(state='disabled', background = 'gray', foreground='gray')
        self.button_start.config(state='normal', background = 'green', foreground='white')
        for i in range(6):
            self.insert_text(self.emulator_entry[i], 'Emulator is turned off')

    def test(self):
        self.start_process()    

    # def start_process_accepting(self):
    #     self.make_emulators()
    #     self.button_quit.config(state='normal', background = 'red', foreground='white')
    #     self.button_start.config(state='disabled', background = 'gray', foreground='gray')
    #     self.emulators = [1, 2, 3, 4, 5, 6]
    #     self.flags = [False]*6
    #     threads = []
    #     self.functions = [
    #         self.run_emulator,
    #         self.log_on_gmx,
    #         self.log_on_snapchat,
    #         self.turn_off_emulator
    #     ]
    #     for i in range(6):
    #         t = threading.Thread(target = self.work, args = (self.emulators[i], self.flags[i]))
    #         threads.append(t)
    #         t.start()

    # def work_accepting(self, emulator, em_ind):
    #     i = 0
    #     while self.flags[em_ind]:
    #         self.functions[i](emulator, em_ind)
    #         i += 1

if __name__ == "__main__":
    try:
        pytesseract.pytesseract.tesseract_cmd = "C:/Users/Administrator/Downloads/tesseract-ocr/tesseract.exe"
        keyboard = Controller()     # Create the controller
        w = tk.Tk()
        w.geometry('650x300')
        w.resizable(0, 0)
        t = Application(w)
        w.mainloop()
    except KeyboardInterrupt:
        print('Program has successfully interrupted from keyboard.')
