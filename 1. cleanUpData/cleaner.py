import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import random
import shutil
import time
import math
import sys

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()

    def packing(self):
        #Configuring variables and adding them to Frame that we pack to root window
        self.frameMain.columnconfigure(0, weight= 3)
        self.frameMain.columnconfigure(1, weight = 1)
        self.labelFolder.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryFolder.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.buttonBrowse.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.checkButton1.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.checkButton2.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.checkButton3.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.checkButton4.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.checkButton5.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.checkButton6.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)
        self.checkButton7.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)
        self.checkButton8.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)
        self.checkButton9.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        self.radioButton1.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
        self.radioButton2.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)
        self.labelMultipleTimes.pack(side=tk.LEFT, fill= tk.Y)
        self.entryMultipletimes.pack(side=tk.LEFT, fill= tk.Y)
        self.frameMultipleTimes.grid(column=1, row=8, sticky=tk.NSEW, padx=5, pady=5)
        self.buttonselectAll.grid(column=1, row=9, sticky=tk.W, padx=5, pady=5)
        self.buttonstart.grid(column=1, row=10, sticky=tk.EW, padx=5, pady=5)
        self.labelProgress.grid(column=1, row=11, sticky=tk.W, padx=5, pady=5)
        self.frameMain.pack(side= tk.TOP, fill= tk.BOTH)

    def createWidgets(self):
        #Defining variables
        self.folderPath = tk.StringVar()
        self.checkVars = [self.CheckVar1, self.CheckVar2, self.CheckVar3, self.CheckVar4, self.CheckVar5, self.CheckVar6, self.CheckVar7, self.CheckVar8, self.CheckVar9]
        self.checkButtons = [self.checkButton1, self.checkButton2, self.checkButton3, self.checkButton4, self.checkButton5, self.checkButton6, self.checkButton7, self.checkButton8, self.checkButton9]
        for checkVar in self.checkVars:
            checkVar = tk.IntVar()
        self.frameMain= tk.Frame(master=self.master)
        self.labelFolder = tk.Label(master=self.frameMain, text= "Select Folder to Clean")
        self.entryFolder = tk.Entry(master=self.frameMain, width=100, text=self.folderPath)
        self.buttonBrowse = tk.Button(master=self.frameMain, text = "Browse", width= 10, pady= 5, borderwidth=3, command = self.browseFolder)
        self.checkButton1 = tk.CheckButton(master=self.frameMain, text= "Delete Landscape Photos", variable = self.CheckVar1, onvalue = 1, offvalue = 0)
        self.checkButton2 = tk.CheckButton(master=self.frameMain, text= "Colour Change", variable = self.CheckVar2, onvalue = 1, offvalue = 0)
        self.checkButton3 = tk.CheckButton(master=self.frameMain, text= "White Borders detection (Remove Picture)", variable = self.CheckVar3, onvalue = 1, offvalue = 0)
        self.checkButton4 = tk.CheckButton(master=self.frameMain, text= "Blank Image (Remove Picture)", variable = self.CheckVar4, onvalue = 1, offvalue = 0)
        self.checkButton5 = tk.CheckButton(master=self.frameMain, text= "High Quality (Remove if too HQ)", variable = self.CheckVar5, onvalue = 1, offvalue = 0)
        self.checkButton6 = tk.CheckButton(master=self.frameMain, text= "Pixel Detection (Remove if lower)", variable = self.CheckVar6, onvalue = 1, offvalue = 0)
        self.checkButton7 = tk.CheckButton(master=self.frameMain, text= "Compress Images", variable = self.CheckVar7, onvalue = 1, offvalue = 0)
        self.checkButton8 = tk.CheckButton(master=self.frameMain, text= "Unique Pixels", variable = self.CheckVar8, onvalue = 1, offvalue = 0)
        self.checkButton9 = tk.CheckButton(master=self.frameMain, text= "Shuffle Images" , variable = self.CheckVar9, onvalue = 1, offvalue = 0)
        self.v = tk.IntVar()
        self.radioButton1 = tk.radioButton(master=self.frameMain, text= "New Metadata", variable=self.v, value=1)
        self.radioButton2 = tk.radioButton(master=self.frameMain, text= "Remove Metadata", variable=self.v, value=2)
        self.frameMultipleTimes= tk.Frame(master=self.frameMain, width= 250)
        self.labelMultipleTimes = tk.Label(master=self.frameMultipleTimes, text= "Multiple times")
        self.entryMultipletimes = tk.Entry(master=self.frameMultipleTimes, width=20)
        self.buttonselectAll = tk.Button(master=self.frameMain, text = "Select All", width= 10, pady= 5, borderwidth=3, command = self.selectAll)
        self.buttonstart = tk.Button(master=self.frameMain, text= "START",width= 50,borderwidth=3, background= "green", foreground= "white", command= self.startProcess)
        self.labelProgress = tk.Label(master=self.frameMain, text="")
        self.packing()

    def makeFolders(self, folder, itr):
        itr = itr + 1
        for root, dirs, files in os.walk(folder, topdown = True):
            for name in dirs:
                newName = f"{itr}cleaned_" + name   
                rdir = "./cleanedimages"
                try:
                    if not("cleaned_" in name):
                        os.mkdir(os.path.join(rdir, newName))
                except:
                    pass
                print(os.path.join(root, name))
            if len(dirs) == 0:
                name = os.path.split(root)[1]
                newName = f"{itr}cleaned_" + name 
                rdir = "./cleanedimages"
                os.mkdir(os.path.join(rdir, newName))

    def finish(self, root, name):
        d = os.path.join(root, name)
        fileCount = sum(len(files) for _, _, files in os.walk(d))
        l = list(range(fileCount))
        random.shuffle(l)
        j=0
        for filename in os.listdir(d):
            print(d)
            if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
                os.rename(os.path.join(d,filename),os.path.join(d,f"{l[j]}_{filename}"))
                j =j + 1

    def startProcess(self):
        self.labelProgress["text"] = "Processing..."
        folder = self.entryFolder.get()
        vars = []
        for checkVar in self.checkVars:
            vars.append(checkVar.get())
        varR = self.v.get()
        Multipletimes = self.entryMultipletimes.get()
        if Multipletimes == "":
            Multipletimes = 1
        itr = 1
        for i in range(int(Multipletimes)):
            self.makeFolders(folder, itr)
            for root, dirs, files in os.walk(folder, topdown = False):
                self.checkFunction(files, root, vars, varR, itr)
        if vars[8] == 1:
            for root, dirs, files in os.walk(".\cleanedimages", topdown = True):
                for name in dirs:
                    self.finish(root, name)
        self.labelProgress["text"] = "Done!"

    def firstFunction(self, img):
        r1 = random.randint(1,img.shape[0])
        r2 = random.randint(1,img.shape[1])
        r,g,b = img[r1,r2]
        img[r1,r2] = [r, g-1, b]

    def secondFunction(self, img, filename):
        cascPath = "./haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) > 1:
            os.remove(filename)
            return
        
    def thirdFunction(self, img, filename):
        h = random.randint(1,10)
        w = random.randint(1,10)
        c = random.randint(1,2)
        height1, width1, _ = img.shape
        if c == 1:
            cropImg = img[1:height1-h, 1:width1-w]
        elif c == 2:
            cropImg = img[h:height1, w:width1]
        cv2.imwrite(filename, cropImg)
        
    def fourthFunction(self, img, filename):
        cascPath = "./haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            os.remove(filename)
            return

    def fifthFunction(self, img, filename):
        cascPath = "./haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            if w > img.shape[1]*0.45 or h > img.shape[0]*0.45:
                os.remove(filename)
                continue

    def sixthFunction(self, img, filename):
        h, w, _ = img.shape
        if h > 1920 or w > 1080:
            os.remove(filename)
            return
        
    def seventhFunction(self, img, filename, dst):
        h, w, _ = img.shape
        if h < 654 or w < 420:
            os.remove(filename)
            return
        shutil.copyfile(filename,dst)
        filename = dst

    def eighthFunction(self, img, filename):
        image = img
        height, width, _ = image.shape
        targetHeight = 1360
        scale = height/targetHeight
        image = cv2.resize(img, (int(width/scale), int(height/scale)), interpolation = cv2.INTER_LANCZOS4)
        cv2.imwrite(filename,image, (cv2.IMWRITE_JPEG_QUALITY, 100))

    def switchingVar(self, vars, varR, img, filename, dst):
        index = -1
        for i in range(len(vars)):
            if vars[i] == 1:
                index = i
                break
        #there is no switch in Python
        if index == 1:
            self.firstFunction(img)
        if index == 2:
            self.secondFunction(img, filename)
        if index == 3:
            self.thirdFunction(img, filename)
        if index == 4:
            self.fourthFunction(img, filename)
        if index == 5:
            self.fifthFunction(img, filename)
        if index == 6:
            self.sixthFunction(img, filename)
        if index == 7:
            self.seventhFunction(img, filename, dst)
        if index == 8:
            self.eighthFunction(img, filename)
        if varR == 1:
            pass
        elif varR == 2:
            image = Image.open(filename)
            data = list(image.getdata())
            imageWithoutExif = Image.new(image.mode, image.size)
            imageWithoutExif.putdata(data)
            imageWithoutExif.save(filename)

    def checkFunction(self, files, root, vars, varR, itr):
        for file in files:
            filename = os.path.join(root,file)
            fileext = os.path.splitext(filename)[1]
            if fileext == ".jpeg" or fileext == ".png" or fileext == ".jpg":
                d = os.path.dirname(filename)
                de = os.path.split(d)[1]
                destinationDir = f"./cleanedimages/{itr}cleaned_" + de
                dst = os.path.join(destinationDir, file)
                img = cv2.imread(filename)
                self.switchingVar(vars, varR, img, filename, dst)

    def selectAll(self):
        vars = []
        flag = False
        for var in self.checkVars:
            if var.get() != 1:
                flag = True
                break
        for checkButton in self.checkButtons:
            if flag == False:
                checkButton.deselect()
            else:
                checkButton.select()

    def browseFolder(self):
        filename = filedialog.askdirectory()
        self.folderPath.set(filename)
        print(filename)
    
if __name__ == "__main__":
    # Create a root window. 
    window = tk.Tk()
    window.geometry("800x520")
    window.minsize(800, 520)
    window.maxsize(800, 520)
    window.title("Image Preprocessing")
    app = Application(master=window)
    app.mainloop()
