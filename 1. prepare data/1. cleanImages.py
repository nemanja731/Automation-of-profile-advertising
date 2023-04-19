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

    #setup GUI
    def createWidgets(self):
        self.folderPath = tk.StringVar()
        self.setupCheckVars()
        self.frameMain= tk.Frame(master=self.master)
        self.labelFolder = tk.Label(master=self.frameMain, text= "Select Folder to Clean")
        self.entryFolder = tk.Entry(master=self.frameMain, width=100, text=self.folderPath)
        self.buttonBrowser = tk.Button(master=self.frameMain, text = "Browse", width= 10, pady= 5, borderwidth=3, command = self.browseFolder)
        self.setupCheckButtons()
        self.metadata = tk.IntVar()
        self.radioButton1 = tk.Radiobutton(master=self.frameMain, text= "Change Metadata", variable=self.metadata, value=1)
        self.radioButton2 = tk.Radiobutton(master=self.frameMain, text= "Remove Metadata", variable=self.metadata, value=2)
        self.frameMultipleTimes= tk.Frame(master=self.frameMain, width= 250)
        self.labelMultipleTimes = tk.Label(master=self.frameMultipleTimes, text= "Whole process again")
        self.entryMultipleTimes = tk.Entry(master=self.frameMultipleTimes, width=20)
        self.buttonSelectAll = tk.Button(master=self.frameMain, text = "Select All", width= 10, pady= 5, borderwidth=3, command = self.selectAll)
        self.buttonStart = tk.Button(master=self.frameMain, text= "START",width= 50,borderwidth=3, background= "green", foreground= "white", command= self.startProcess)
        self.labelProgess = tk.Label(master=self.frameMain, text="")
        self.packEverything()

    def setupCheckButtons(self):
        self.checkButton1 = tk.Checkbutton(master=self.frameMain, text= "Delete Landscape Photos", variable = self.CheckVar1, onvalue = 1, offvalue = 0)
        self.checkButton2 = tk.Checkbutton(master=self.frameMain, text= "Face Detection (Remove if multiple)", variable = self.CheckVar2, onvalue = 1, offvalue = 0)
        self.checkButton3 = tk.Checkbutton(master=self.frameMain, text= "White Borders detection (Remove Picture)", variable = self.CheckVar3, onvalue = 1, offvalue = 0)
        self.checkButton4 = tk.Checkbutton(master=self.frameMain, text= "No Face (Remove Picture)", variable = self.CheckVar4, onvalue = 1, offvalue = 0)
        self.checkButton5 = tk.Checkbutton(master=self.frameMain, text= "High Quality (Remove if too HQ)", variable = self.CheckVar5, onvalue = 1, offvalue = 0)
        self.checkButton6 = tk.Checkbutton(master=self.frameMain, text= "Pixel Detection (Remove if lower)", variable = self.CheckVar6, onvalue = 1, offvalue = 0)
        self.checkButton7 = tk.Checkbutton(master=self.frameMain, text= "Face Over 50%", variable = self.CheckVar7, onvalue = 1, offvalue = 0)
        self.checkButton8 = tk.Checkbutton(master=self.frameMain, text= "Compress Images", variable = self.CheckVar8, onvalue = 1, offvalue = 0)
        self.checkButton9 = tk.Checkbutton(master=self.frameMain, text= "Unique Pixels" , variable = self.CheckVar9, onvalue = 1, offvalue = 0)
        self.checkButton10 = tk.Checkbutton(master=self.frameMain, text= "Colour Change", variable = self.CheckVar10, onvalue = 1, offvalue = 0)
        self.checkButton11 = tk.Checkbutton(master=self.frameMain, text= "Shuffle Images", variable = self.CheckVar11, onvalue = 1, offvalue = 0)
        self.checkButtons = [self.checkButton1, self.checkButton2, self.checkButton3, self.checkButton4, self.checkButton5, self.checkButton6, self.checkButton7, self.checkButton8, self.checkButton9, self.checkButton10, self.checkButton11]

    def setupCheckVars(self):
        self.CheckVar1 = tk.IntVar()
        self.CheckVar2 = tk.IntVar()
        self.CheckVar3 = tk.IntVar()
        self.CheckVar4 = tk.IntVar()
        self.CheckVar5 = tk.IntVar()
        self.CheckVar6 = tk.IntVar()
        self.CheckVar7 = tk.IntVar()
        self.CheckVar8 = tk.IntVar()
        self.CheckVar9 = tk.IntVar()
        self.CheckVar10 = tk.IntVar()
        self.CheckVar11 = tk.IntVar()
        self.checkVars = [self.CheckVar1, self.CheckVar2, self.CheckVar3, self.CheckVar4, self.CheckVar5, self.CheckVar6, self.CheckVar7, self.CheckVar8, self.CheckVar9, self.CheckVar10, self.CheckVar11]

    #configuring variables and adding them to Frame that we pack to root window
    def packEverything(self):
        self.frameMain.columnconfigure(0, weight= 3)
        self.frameMain.columnconfigure(1, weight = 1)
        self.labelFolder.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryFolder.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.buttonBrowser.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.checkButton1.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.checkButton2.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.checkButton3.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.checkButton4.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.checkButton5.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.checkButton6.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)
        self.checkButton7.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)
        self.checkButton8.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)
        self.checkButton9.grid(column=0, row=11, sticky=tk.W, padx=5, pady=5)
        self.checkButton10.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        self.checkButton11.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
        self.radioButton1.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
        self.radioButton2.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)
        self.labelMultipleTimes.pack(side=tk.LEFT, fill= tk.Y)
        self.entryMultipleTimes.pack(side=tk.LEFT, fill= tk.Y)
        self.frameMultipleTimes.grid(column=1, row=8, sticky=tk.NSEW, padx=5, pady=5)
        self.buttonSelectAll.grid(column=1, row=9, sticky=tk.W, padx=5, pady=5)
        self.buttonStart.grid(column=1, row=10, sticky=tk.EW, padx=5, pady=5)
        self.labelProgess.grid(column=1, row=11, sticky=tk.W, padx=5, pady=5)
        self.frameMain.pack(side= tk.TOP, fill= tk.BOTH)

    #function that is called when start button is pressed
    def startProcess(self):
        self.labelProgess["text"] = "Processing..."
        folder = self.entryFolder.get()
        vars = 11*[0]
        for i in range(len(self.checkVars)):
            vars[i] = self.checkVars[i].get()
        metadata = self.metadata.get()
        multipleTimes = self.entryMultipleTimes.get()
        if multipleTimes == "":
            multipleTimes = 1
        itr = 0
        self.process(vars, folder, metadata, multipleTimes, itr)
        if vars[10] == 1:
            self.shuffleImages()
        self.labelProgess["text"] = "Done!"

    def process(self, vars, folder, metadata, multipleTimes, itr):
        for i in range(int(multipleTimes)):
            itr = itr + 1
            self.createNewFolders(folder, itr)
            for root, dirs, files in os.walk(folder, topdown = False):
                self.processEveryFolder(vars, metadata, itr, root, files)

    def processEveryFolder(self, vars, metadata, itr, root, files):
        for file in files:
            fileName = os.path.join(root, file)
            fileext = os.path.splitext(fileName)[1]
            if fileext == ".jpeg" or fileext == ".png" or fileext == ".jpg":
                self.processImage(vars, metadata, itr, root, file)

    #for each image, everything that has been checked should be done
    def processImage(self, vars, metadata, itr, file):
        d = os.path.dirname(fileName)
        de = os.path.split(d)[1]
        destinationDir = f"./cleaned_images/{itr}cleaned_" + de
        destination = os.path.join(destinationDir, file)
        img = cv2.imread(fileName)
        if self.checkFunction1(img, fileName, vars):
            return
        if self.checkFunction2(img, fileName, vars):
            return
        if self.checkFunction3(img, fileName, vars):
            return
        if self.checkFunction4(img, fileName, vars):
            return
        if self.checkFunction5(img, fileName, vars):
            return
        if self.checkFunction6(img, fileName, vars):
            return
        if self.checkFunction7(img, fileName, vars):
            return
        shutil.copyfile(fileName,destination)
        fileName = destination
        self.function8(img, fileName, vars)
        self.function9(img, fileName, vars)
        self.function10(img, vars)
        self.function11(metadata, fileName, vars)

    #delete Landscape Photos
    def checkFunction1(self, img, fileName, vars):
        if vars[0] == 1:
            h, w, _ = img.shape
            if w >= h:
                os.remove(fileName)
                return True
        return False

    #face detection (remove if multiple faces)
    def checkFunction2(self, img, fileName, vars):
        if vars[1] == 1:
            cascPath = "./haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(cascPath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) > 1:
                os.remove(fileName)
                return True
        return False
    
    #white borders detection (remove image)
    def checkFunction3(self, img, fileName, vars):
        if vars[2] == 1:
            if img[3,3][0] == 255 and img[3,3][1] == 255 and img[3,3][2] == 255: 
                os.remove(fileName)
                return True
        return False

    #no face (remove image)
    def checkFunction4(self, img, fileName, vars):
        if vars[3] == 1:
            cascPath = "./haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(cascPath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                os.remove(fileName)
                return True
        return False
    
    #high quality (remove if quality is too high - HQ)
    def checkFunction5(self, img, fileName, vars):
        if vars[4] == 1:
            h, w, _ = img.shape
            if h > 1920 or w > 1080:
                os.remove(fileName)
                return True
        return False

    #pixel detection (remove if lower)
    def checkFunction6(self, img, fileName, vars):
        if vars[5] == 1:
            h, w, _ = img.shape
            if h < 654 or w < 420:
                os.remove(fileName)
                return True
        return False

    #face over 50%
    def checkFunction7(self, img, fileName, vars):
        if vars[10] == 1:
            cascPath = "./haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(cascPath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                if w > img.shape[1]*0.45 or h > img.shape[0]*0.45:
                    os.remove(fileName)
                    return True
        return False

    #compess images to desire format
    def function8(self, img, fileName, vars):
        if vars[6] == 1:
            image = img
            height, width, _ = image.shape
            targetHeight = 1360
            scale = height/targetHeight
            image = cv2.resize(img, (int(width/scale), int(height/scale)), interpolation = cv2.INTER_LANCZOS4)
            cv2.imwrite(fileName,image, (cv2.IMWRITE_JPEG_QUALITY, 100))

    #unique pixels
    def function9(self, img, fileName, vars):
        if vars[8] == 1:
            h = random.randint(1,10)
            w = random.randint(1,10)
            c = random.randint(1,2)
            height1, width1, _ = img.shape
            if c == 1:
                crop_img = img[1:height1-h, 1:width1-w]
            elif c == 2:
                crop_img = img[h:height1, w:width1]
            cv2.imwrite(fileName, crop_img)

    #change colour
    def function10(self, img, vars):
        if vars[9] == 1:
            r1 = random.randint(1,img.shape[0])
            r2 = random.randint(1,img.shape[1])
            r,g,b = img[r1,r2]
            img[r1,r2] = [r, g-1, b]

    #change or remove metadata
    def function11(self, metadata, fileName, vars):
        #change
        if metadata == 1:
            #didn't implement
            pass
        #remove
        elif metadata == 2:
            image = Image.open(fileName)
            data = list(image.getdata())
            imageWithoutExif = Image.new(image.mode, image.size)
            imageWithoutExif.putdata(data)
            imageWithoutExif.save(fileName)

    def shuffleImages(self):
        for root, dirs, files in os.walk(".\cleaned_images", topdown = True):
            for name in dirs:
                self.shuffle(root, name)

    def shuffle(self, root, name):
        d = os.path.join(root, name)
        fileCount = sum(len(files) for _, _, files in os.walk(d))
        l = list(range(fileCount))
        random.shuffle(l)
        j=0
        for fileName in os.listdir(d):
            print(d)
            if fileName.endswith(".jpeg") or fileName.endswith(".png") or fileName.endswith(".jpg"):
                os.rename(os.path.join(d,fileName),os.path.join(d,f"{l[j]}_{fileName}"))
                j = j + 1

    #create folders where image will be placed
    def createNewFolders(self, folder, itr):
        for root, dirs, files in os.walk(folder, topdown = True):
            for name in dirs:
                newName = f"{itr}cleaned_" + name   
                rdir = "./cleaned_images"
                try:
                    if not("cleaned_" in name):
                        os.mkdir(os.path.join(rdir, newName))
                except:
                    pass
                print(os.path.join(root, name))
            if len(dirs) == 0:
                name = os.path.split(root)[1]
                newName = f"{itr}cleaned_" + name 
                rdir = "./cleaned_images"
                os.mkdir(os.path.join(rdir, newName))

    #function for the button 'Select all'
    def selectAll(self):
        vars = 11*[0]
        for i in range(len(self.checkVars)):
            vars[i] = self.checkVars[i].get()
        if sum(vars) == 11:
            for b in self.checkButtons:
                b.deselect()
            else:
                b.select()

    def browseFolder(self):
        fileName = filedialog.askdirectory()
        self.folderPath.set(fileName)
        print(fileName)

if __name__ == "__main__":
    #create a root window
    window = tk.Tk()
    window.geometry("800x520")
    window.minsize(800, 520)
    window.maxsize(800, 520)
    window.title("Image Preprocessing")
    app = Application(master=window)
    app.mainloop()