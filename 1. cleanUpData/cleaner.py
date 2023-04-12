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
        self.create_widgets()

    def create_widgets(self):
        #Defining variables
        self.folder_path = tk.StringVar()
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
        self.frm_main= tk.Frame(master=self.master)
        self.lbl_folder = tk.Label(master=self.frm_main, text= "Select Folder to Clean")
        self.ent_folder = tk.Entry(master=self.frm_main, width=100, text=self.folder_path)
        self.btn_browse = tk.Button(master=self.frm_main, text = "Browse", width= 10, pady= 5, borderwidth=3, command = self.browse_folder)
        self.chkbtn_1 = tk.Checkbutton(master=self.frm_main, text= "Delete Landscape Photos", variable = self.CheckVar1, onvalue = 1, offvalue = 0)
        self.chkbtn_2 = tk.Checkbutton(master=self.frm_main, text= "Colour Change", variable = self.CheckVar10, onvalue = 1, offvalue = 0)
        self.chkbtn_3 = tk.Checkbutton(master=self.frm_main, text= "White Borders detection (Remove Picture)", variable = self.CheckVar3, onvalue = 1, offvalue = 0)
        self.chkbtn_4 = tk.Checkbutton(master=self.frm_main, text= "Blank Image (Remove Picture)", variable = self.CheckVar4, onvalue = 1, offvalue = 0)
        self.chkbtn_5 = tk.Checkbutton(master=self.frm_main, text= "High Quality (Remove if too HQ)", variable = self.CheckVar5, onvalue = 1, offvalue = 0)
        self.chkbtn_6 = tk.Checkbutton(master=self.frm_main, text= "Pixel Detection (Remove if lower)", variable = self.CheckVar6, onvalue = 1, offvalue = 0)
        self.chkbtn_7 = tk.Checkbutton(master=self.frm_main, text= "Compress Images", variable = self.CheckVar7, onvalue = 1, offvalue = 0)
        self.chkbtn_8 = tk.Checkbutton(master=self.frm_main, text= "Shuffle Images", variable = self.CheckVar8, onvalue = 1, offvalue = 0)
        self.chkbtn_9 = tk.Checkbutton(master=self.frm_main, text= "Unique Pixels" , variable = self.CheckVar9, onvalue = 1, offvalue = 0)
        self.v = tk.IntVar()
        self.radiobtn_1 = tk.Radiobutton(master=self.frm_main, text= "New Metadata", variable=self.v, value=1)
        self.radiobtn_2 = tk.Radiobutton(master=self.frm_main, text= "Remove Metadata", variable=self.v, value=2)
        self.frm_multipletimes= tk.Frame(master=self.frm_main, width= 250)
        self.lbl_multipletimes = tk.Label(master=self.frm_multipletimes, text= "Multiple times")
        self.ent_multipletimes = tk.Entry(master=self.frm_multipletimes, width=20)
        self.btn_select_all = tk.Button(master=self.frm_main, text = "Select All", width= 10, pady= 5, borderwidth=3, command = self.select_all)
        self.btn_start = tk.Button(master=self.frm_main, text= "START",width= 50,borderwidth=3, background= "green", foreground= "white", command= self.start_process)
        self.lbl_progress = tk.Label(master=self.frm_main, text="")
        #Configuring variables and adding them to Frame that we pack to root window
        self.frm_main.columnconfigure(0, weight= 3)
        self.frm_main.columnconfigure(1, weight = 1)
        self.lbl_folder.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.ent_folder.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.btn_browse.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_1.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_2.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_3.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_4.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_11.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_5.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_6.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_7.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_8.grid(column=0, row=11, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_9.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        self.chkbtn_10.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
        self.radiobtn_1.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
        self.radiobtn_2.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)
        self.lbl_multipletimes.pack(side=tk.LEFT, fill= tk.Y)
        self.ent_multipletimes.pack(side=tk.LEFT, fill= tk.Y)
        self.frm_multipletimes.grid(column=1, row=8, sticky=tk.NSEW, padx=5, pady=5)
        self.btn_select_all.grid(column=1, row=9, sticky=tk.W, padx=5, pady=5)
        self.btn_start.grid(column=1, row=10, sticky=tk.EW, padx=5, pady=5)
        self.lbl_progress.grid(column=1, row=11, sticky=tk.W, padx=5, pady=5)
        self.frm_main.pack(side= tk.TOP, fill= tk.BOTH)

    def start_process(self):
        self.lbl_progress["text"] = "Processing..."
        folder = self.ent_folder.get()
        var1 = self.CheckVar1.get()
        var2 = self.CheckVar2.get()
        var3 = self.CheckVar3.get()
        var4 = self.CheckVar4.get()
        var5 = self.CheckVar5.get()
        var6 = self.CheckVar6.get()
        var7 = self.CheckVar7.get()
        var8 = self.CheckVar8.get()
        var9 = self.CheckVar9.get()
        var10 = self.CheckVar10.get()
        var11 = self.CheckVar11.get()
        varR = self.v.get()
        multipletimes = self.ent_multipletimes.get()
        if multipletimes == "":
            multipletimes = 1
        #print(folder, var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, varR, multipletimes)
        
        itr = 0
        for i in range(int(multipletimes)):
            itr = itr + 1
            for root, dirs, files in os.walk(folder, topdown = True):
                for name in dirs:
                    new_name = f"{itr}cleaned_" + name   
                    rdir = "./cleaned_images"
                    try:
                        if not("cleaned_" in name):
                            os.mkdir(os.path.join(rdir, new_name))
                    except:
                        pass
                    print(os.path.join(root, name))
                if len(dirs) == 0:
                    name = os.path.split(root)[1]
                    new_name = f"{itr}cleaned_" + name 
                    rdir = "./cleaned_images"
                    os.mkdir(os.path.join(rdir, new_name))
            for root, dirs, files in os.walk(folder, topdown = False):
                for file in files:
                    filename = os.path.join(root,file)
                    fileext = os.path.splitext(filename)[1]
                    if fileext == ".jpeg" or fileext == ".png" or fileext == ".jpg":
                        d = os.path.dirname(filename)
                        de = os.path.split(d)[1]
                        dst_dir = f"./cleaned_images/{itr}cleaned_" + de
                        dst = os.path.join(dst_dir, file)
                        img = cv2.imread(filename)
                        if var1 == 1:
                            h, w, _ = img.shape
                            if w >= h:
                                #os.remove(filename)
                                continue
                        if var2 == 1:
                            cascPath = "./haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascPath)
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                            if len(faces) > 1:
                                #os.remove(filename)
                                continue
                        if var3 == 1:
                            if img[3,3][0] == 255 and img[3,3][1] == 255 and img[3,3][2] == 255: 
                                #os.remove(filename)
                                continue
                        if var4 == 1:
                            cascPath = "./haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascPath)
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                            if len(faces) == 0:
                                #os.remove(filename)
                                continue
                        if var11 == 1:
                            cascPath = "./haarcascade_frontalface_default.xml"
                            faceCascade = cv2.CascadeClassifier(cascPath)
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                            for (x, y, w, h) in faces:
                                if w > img.shape[1]*0.45 or h > img.shape[0]*0.45:
                                    #os.remove(filename)
                                    continue
                        if var5 == 1:
                            h, w, _ = img.shape
                            if h > 1920 or w > 1080:
                                #os.remove(filename)
                                continue
                        if var6 == 1:
                            h, w, _ = img.shape
                            if h < 654 or w < 420:
                                #os.remove(filename)
                                continue
                        shutil.copyfile(filename,dst)
                        filename = dst
                        if var7 == 1:
                            _image = img
                            height, width, _ = _image.shape
                            target_height = 1360
                            scale = height/target_height
                            _image = cv2.resize(img, (int(width/scale), int(height/scale)), interpolation = cv2.INTER_LANCZOS4)
                            cv2.imwrite(filename,_image, (cv2.IMWRITE_JPEG_QUALITY, 100))
                        if var9 == 1:
                            h = random.randint(1,10)
                            w = random.randint(1,10)
                            c = random.randint(1,2)
                            height1, width1, _ = img.shape
                            if c == 1:
                                crop_img = img[1:height1-h, 1:width1-w]
                            elif c == 2:
                                crop_img = img[h:height1, w:width1]
                            cv2.imwrite(filename, crop_img)
                        if var10 == 1:
                            r1 = random.randint(1,img.shape[0])
                            r2 = random.randint(1,img.shape[1])
                            r,g,b = img[r1,r2]
                            img[r1,r2] = [r, g-1, b]
                        if varR == 1:
                            pass
                        elif varR == 2:
                            image = Image.open(filename)
                            data = list(image.getdata())
                            image_without_exif = Image.new(image.mode, image.size)
                            image_without_exif.putdata(data)
                            image_without_exif.save(filename)
        if var8 == 1:
            for root, dirs, files in os.walk(".\cleaned_images", topdown = True):
                for name in dirs:
                    d = os.path.join(root, name)
                    file_count = sum(len(files) for _, _, files in os.walk(d))
                    l = list(range(file_count))
                    random.shuffle(l)
                    j=0
                    for filename in os.listdir(d):
                        print(d)
                        if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
                            os.rename(os.path.join(d,filename),os.path.join(d,f"{l[j]}_{filename}"))
                            j =j + 1
        self.lbl_progress["text"] = "Done!"

    def select_all(self):
        var1 = self.CheckVar1.get()
        var2 = self.CheckVar2.get()
        var3 = self.CheckVar3.get()
        var4 = self.CheckVar4.get()
        var5 = self.CheckVar5.get()
        var6 = self.CheckVar6.get()
        var7 = self.CheckVar7.get()
        var8 = self.CheckVar8.get()
        var9 = self.CheckVar9.get()
        var10 = self.CheckVar10.get()
        var11 = self.CheckVar11.get()
        if var1 == 1 and var2 == 1 and var3 == 1 and var4 == 1 and var5 == 1 and var6 == 1 and var7 == 1 and var8 == 1 and var9 == 1 and var10 == 1 and var11 == 1:
            self.chkbtn_1.deselect()
            self.chkbtn_2.deselect()
            self.chkbtn_3.deselect()
            self.chkbtn_4.deselect()
            self.chkbtn_5.deselect()
            self.chkbtn_6.deselect()
            self.chkbtn_7.deselect()
            self.chkbtn_8.deselect()
            self.chkbtn_9.deselect()
            self.chkbtn_10.deselect()
            self.chkbtn_11.deselect()
        else:
            self.chkbtn_1.select()
            self.chkbtn_2.select()
            self.chkbtn_3.select()
            self.chkbtn_4.select()
            self.chkbtn_5.select()
            self.chkbtn_6.select()
            self.chkbtn_7.select()
            self.chkbtn_8.select()
            self.chkbtn_9.select()
            self.chkbtn_10.select()
            self.chkbtn_11.select()

    def browse_folder(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)
        print(filename)

# Create a root window. 
window = tk.Tk()
window.geometry("800x520")
window.minsize(800, 520)
window.maxsize(800, 520)
window.title("Image Preprocessing")
app = Application(master=window)
app.mainloop()
