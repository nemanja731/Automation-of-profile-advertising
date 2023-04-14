import os
import openpyxl
import PIL
import random
import shutil
import sys
import time
from abc import ABC, abstractmethod
from tkinter.constants import EXTENDED
from tkinter import ttk
from tkinter import *
import tkinter.font as TkFont
import tkinter as tk
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Application is the main class that represents the GUI. It contains tabs, and each tab is created as a separate class
class Application(tk.Tk):

    def __init__(self,*args,**kwargs):
       tk.Tk.__init__(self,*args,**kwargs)
       self.minsize(650, 620)
       self.geometry("650x620+400+120")
       self.title("Tkinter GUI")
       self.iconbitmap('./briefcase_business_elder_1732.ico')
       self.createTabs()

    #creation of tabs
    def createTabs(self):
       self.notebook = ttk.Notebook()
       self.tab1 = Tab1(self.notebook)
       self.tab2 = Tab2(self.notebook)
       self.tab3 = Tab3(self.notebook) 
       self.notebook.add(self.tab1,text="Generator")
       self.notebook.add(self.tab2,text="Trades")
       self.notebook.add(self.tab3,text="Profit")
       self.notebook.grid(row=0, column=0, sticky='nsew')

#an abstract class inherited by all tabs
class Tab(ABC, tk.Frame):

    def __init__(self,name,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
        
    #abstract method, inherited classes override it
    @abstractmethod
    def createWidgets(self):
        #left frame
        self.leftFrame = tk.Frame(self)
        self.leftFrame.pack(side= tk.LEFT, fill= tk.X, padx = 20, pady = 0)
        #middle frame
        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 0)

#class Tab1, which is called Generate, represents the first and main tab in the program
class Tab1(Tab):

    def __init__(self,name,*args,**kwargs):
        super().__init__(self,name,*args,**kwargs)
        self.createWidgets()
        self.initialize()
    #GUI creation

    def createWidgets(self):
        #call to function createWidgets, base class Tab
        super().createWidgets()
        self.setupClearSection()
        #shared frame (username, numTokens, numImagesPerToken)
        self.utiFrame = tk.Frame(self.leftFrame)
        self.utiFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.setupUsernameSection()
        self.setupNumTokensSection()
        self.setupNumImagesPerFolderSection()
        self.setupPromotionSection()
        self.setupBackupSection()
        self.setupPrefixSection()
        self.setupFilesSection()
        self.setupImageAsSection()
        self.setupRedoSection()
        self.setupProcessLogSection()

    def setupClearSection(self):
        #clearGUIReverse frames
        self.clearGUIReverseFrame = tk.Frame(self.leftFrame)
        self.clearGUIReverseFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 20)
        #clearGUI and reverse buttons
        self.clearGUIButton = tk.Button(master=self.clearGUIReverseFrame, text= "Clear GUI",width= 10, pady= 0, background= "gray", foreground= "white", command= self.clearGUI, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.clearGUIButton.grid(row= 0, column= 0, padx =  5, pady = 7)
        self.reverseButton = tk.Button(master=self.clearGUIReverseFrame, text= "Reverse",width= 10, pady= 0, background= "gray", foreground= "white", command= self.reverse, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.reverseButton.grid(row= 0, column= 1, padx = 5, pady = 5)

    def setupUsernameSection(self):
        #username frames
        self.usernameFrame = tk.Frame(master=self.utiFrame)
        self.usernameFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        self.usernameFrameL = tk.Frame(master=self.usernameFrame)
        self.usernameFrameL.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 0)
        self.usernameFrameE = tk.Frame(master=self.usernameFrame)
        self.usernameFrameE.pack(side= tk.LEFT, fill= tk.X, padx = 18, pady = 0)
        #username label and entry
        self.usernameLabel = tk.Label(master=self.usernameFrameL, text= "Username:")
        self.usernameLabel.grid(row= 0, column= 0)
        self.usernameEntry = tk.Entry(master=self.usernameFrameE, width=15, bd = 3)
        self.usernameEntry.grid(row= 0, column= 1)

    def setupNumTokensSection(self):
        #numTokens frames
        self.numTokensFrame = tk.Frame(master=self.utiFrame)
        self.numTokensFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        self.numTokensFrameL = tk.Frame(master=self.numTokensFrame)
        self.numTokensFrameL.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 0)
        self.numTokensFrameE = tk.Frame(master=self.numTokensFrame)
        self.numTokensFrameE.pack(side= tk.LEFT, fill= tk.X, padx = 52, pady = 0)
        #numTokens label and entry
        self.numTokensLabel = tk.Label(master=self.numTokensFrameL, text= "Num of tokens:")
        self.numTokensLabel.grid(row= 0, column= 0)
        self.numTokensEntry = tk.Entry(master=self.numTokensFrameE, width=5, bd = 3)
        self.numTokensEntry.grid(row= 0, column= 1)

    def setupNumImagesPerFolderSection(self):
        #numImagesPerFolder frames
        self.numImagesPerTokenFrame = tk.Frame(master=self.utiFrame)
        self.numImagesPerTokenFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        self.numImagesPerTokenFrameL = tk.Frame(master=self.numImagesPerTokenFrame)
        self.numImagesPerTokenFrameL.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 0)
        self.numImagesPerTokenFrameE = tk.Frame(master=self.numImagesPerTokenFrame)
        self.numImagesPerTokenFrameE.pack(side= tk.LEFT, fill= tk.X, padx = 10, pady = 0)
        #numImagesPerFolder label and entry
        self.numImagesPerTokenLabel = tk.Label(master=self.numImagesPerTokenFrameL, text= "Num images per token:")
        self.numImagesPerTokenLabel.grid(row= 0, column= 0)
        self.numImagesPerTokenEntry = tk.Entry(master=self.numImagesPerTokenFrameE, width=5, bd = 3)
        self.numImagesPerTokenEntry.grid(row= 0, column= 1)

    def setupPromotionSection(self):
        #promotion frames
        self.promotionFrame = tk.Frame(master=self.leftFrame)
        self.promotionFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.promotionFrameL = tk.Frame(master=self.promotionFrame)
        self.promotionFrameL.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        self.promotionFrameR1 = tk.Frame(master=self.promotionFrame)
        self.promotionFrameR1.pack(side= tk.TOP, fill= tk.X, padx = 10, pady = 1)
        self.promotionFrameR2 = tk.Frame(master=self.promotionFrame)
        self.promotionFrameR2.pack(side= tk.TOP, fill= tk.X, padx = 10, pady = 1)
        #promotion label
        self.promotionLabel = tk.Label(master=self.promotionFrameL, text= "Choose promotion:")
        self.promotionLabel.grid(row= 0, column= 0)
        #promotion radioButtons (bio, watermark, watermarkBio, no promo)
        self.varPromotion = IntVar() 
        self.bioPromotionRButton = Radiobutton(master=self.promotionFrameR1, text="Bio", variable=self.varPromotion, value=1)
        self.bioPromotionRButton.grid(row= 0, column= 0, ipadx = 20)
        self.watermarkBioPromotionRButton = Radiobutton(master=self.promotionFrameR1, text="Watermark + Bio", variable=self.varPromotion, value=2)
        self.watermarkBioPromotionRButton.grid(row= 0, column= 1, ipadx = 41)
        self.watermarkPromotionRButton = Radiobutton(master=self.promotionFrameR2, text="Watermark", variable=self.varPromotion, value=3)
        self.watermarkPromotionRButton.grid(row= 0, column= 0, ipadx = 20)
        self.noPromotionRButton = Radiobutton(master=self.promotionFrameR2, text="No Promotion", variable=self.varPromotion, value=4)
        self.noPromotionRButton.grid(row= 0, column= 1, ipadx = 0)

    def setupBackupSection(self):
        #backup frames
        self.backupFrame = tk.Frame(master=self.leftFrame)
        self.backupFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        #backup checkbutton
        self.varBackup = IntVar()
        self.backupCButton = Checkbutton(self.backupFrame, text = "Backup images", variable = self.varBackup, onvalue = 1, offvalue = 0, height=1, width = 15)
        self.backupCButton.grid(row= 0, column= 2, ipadx = 3)

    def setupPrefixFrame(self):
        #prefix frames
        self.prefixFrame = tk.Frame(master=self.leftFrame)
        self.prefixFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.prefixFrameL = tk.Frame(master=self.prefixFrame)
        self.prefixFrameL.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 5)
        self.prefixFrameC1 = tk.Frame(master=self.prefixFrame)
        self.prefixFrameC1.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 1)
        self.prefix1Frame = tk.Frame(master=self.prefixFrameC1)
        self.prefix1Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix2Frame = tk.Frame(master=self.prefixFrameC1)
        self.prefix2Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix3Frame = tk.Frame(master=self.prefixFrameC1)
        self.prefix3Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix4Frame = tk.Frame(master=self.prefixFrameC1)
        self.prefix4Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefixFrameC2 = tk.Frame(master=self.prefixFrame)
        self.prefixFrameC2.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 1)
        self.prefix5Frame = tk.Frame(master=self.prefixFrameC2)
        self.prefix5Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix6Frame = tk.Frame(master=self.prefixFrameC2)
        self.prefix6Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix7Frame = tk.Frame(master=self.prefixFrameC2)
        self.prefix7Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)
        self.prefix8Frame = tk.Frame(master=self.prefixFrameC2)
        self.prefix8Frame.pack(side= tk.LEFT, fill= tk.X, padx = 0, pady = 1)

    def setupPrefixLabelButton(self):
        #prefixes label
        self.prefixLabel = tk.Label(master=self.prefixFrameL, text= "Prefixes to use:")
        self.prefixLabel.grid(row= 0, column= 0)
        #prefixes button (Select All)
        self.prefixButton = tk.Button(master=self.prefixFrameL, text= "Select All",width= 10, pady= 0, background= "blue", foreground= "white", command= self.selectAllPrefixes, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.prefixButton.grid(row= 1, column= 0, pady = 10)

    def setupPrefixCheckButtons(self):
        #prefixes checkbuttons (sn4p,s.c - ,snpcht,s:c - ,s.c: ,s.c )
        prefixes = [self.varPrefix1, self.varPrefix2, self.varPrefix3, self.varPrefix4, self.varPrefix5, self.varPrefix6, self.varPrefix7, self.varPrefix8]
        for p in prefixes:
            p = IntVar()
        self.prefix1CButton = Checkbutton(self.prefix1Frame, text = "trade: ", variable = self.varPrefix1, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix1CButton.grid(row= 0, column= 0)
        self.prefix2CButton = Checkbutton(self.prefix2Frame, text = "trade - ", variable = self.varPrefix2, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix2CButton.grid(row= 0, column= 0)
        self.prefix3CButton = Checkbutton(self.prefix3Frame, text = "*trade* ", variable = self.varPrefix3, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix3CButton.grid(row= 0, column= 0)
        self.prefix4CButton = Checkbutton(self.prefix4Frame, text = "/trade\ ", variable = self.varPrefix4, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix4CButton.grid(row= 0, column= 0)
        self.prefix5CButton = Checkbutton(self.prefix5Frame, text = "~trade~ ", variable = self.varPrefix5, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix5CButton.grid(row= 0, column= 0)
        self.prefix6CButton = Checkbutton(self.prefix6Frame, text = "trade -> ", variable = self.varPrefix6, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix6CButton.grid(row= 0, column= 0)
        self.prefix7CButton = Checkbutton(self.prefix7Frame, text = "trade ", variable = self.varPrefix7, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix7CButton.grid(row= 0, column= 0)
        self.prefix8CButton = Checkbutton(self.prefix8Frame, text = "$trade$ ", variable = self.varPrefix8, onvalue = 1, offvalue = 0, height=1, width = 5, bd = 3)
        self.prefix8CButton.grid(row= 0, column= 0)

    def setupPrefixSection(self):
        self.setupPrefixFrame()
        self.setupPrefixLabelButton()
        self.setupPrefixCheckButtons()
        
    def setupFilesFrame(self):
        #files frames
        self.filesFrame = tk.Frame(master=self.middleFrame)
        self.filesFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.filesFrameB = tk.Frame(master=self.filesFrame)
        self.filesFrameB.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 10)
        self.filesFrameC = tk.Frame(master=self.filesFrame)
        self.filesFrameC.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.biographiesFrame = tk.Frame(master=self.filesFrameC)
        self.biographiesFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.jobsFrame = tk.Frame(master=self.filesFrameC)
        self.jobsFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.namesFrame = tk.Frame(master=self.filesFrameC)
        self.namesFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.emailsFrame = tk.Frame(master=self.filesFrameC)
        self.emailsFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        self.tradesFrame = tk.Frame(master=self.filesFrameC)
        self.tradesFrame.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)

    def setupFilesLabelButton(self):
        #files label
        self.filesLabel = tk.Label(master=self.filesFrameB, text= "Select files:")
        self.filesLabel.grid(row= 0, column= 0)
        #files button (Select All)
        self.filesButton = tk.Button(master=self.filesFrameB, text= "Select All",width= 10, pady= 0, background= "blue", foreground= "white", command= self.selectAllFiles, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.filesButton.grid(row= 1, column= 0, pady = 10)

    def setupFilesCheckButton(self):
        #files checkbuttons (biographies, jobs, names, emails, trades)
        self.varBiographies = IntVar()
        self.varJobs = IntVar()
        self.varNames = IntVar()
        self.varEmails = IntVar()
        self.vartrades = IntVar()
        self.biographyCButton = Checkbutton(self.biographiesFrame, text = "Biographies", variable = self.varBiographies, onvalue = 1, offvalue = 0, height=1, width = 10)
        self.biographyCButton.grid(row= 0, column= 0)
        self.jobsCButton = Checkbutton(self.jobsFrame, text = "Jobs", variable = self.varJobs, onvalue = 1, offvalue = 0, height=1, width = 6)
        self.jobsCButton.grid(row= 0, column= 0)
        self.namesCButton = Checkbutton(self.namesFrame, text = "Names", variable = self.varNames, onvalue = 1, offvalue = 0, height=1, width = 8)
        self.namesCButton.grid(row= 0, column= 0)
        self.emailsCButton = Checkbutton(self.emailsFrame, text = "Emails", variable = self.varEmails, onvalue = 1, offvalue = 0, height=1, width = 8)
        self.emailsCButton.grid(row= 0, column= 0)
        self.tradesCButton = Checkbutton(self.tradesFrame, text = "Trades", variable = self.vartrades, onvalue = 1, offvalue = 0, height=1, width = 10)
        self.tradesCButton.grid(row= 0, column= 0)

    def setupFilesSection(self):
        self.setupFilesFrame()
        self.setupFilesLabelButton()
        self.setupFilesCheckButton()

    def setupImageAsSection(self):
        #imageAs label
        self.imageAsLabel = tk.Label(master=self.filesFrameB, text= "Watermarked image as:")
        self.imageAsLabel.grid(row= 0, column= 1, padx = 50)
        #imageAs button (Select All)
        self.imageAsButton = tk.Button(master=self.filesFrameB, text= "Select All",width= 10, pady= 0, background= "blue", foreground= "white", command= self.selectAllImagesAs, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.imageAsButton.grid(row= 1, column= 1, pady = 10)
        #imageAs checkbuttons (first, second, third, fourth, fifth)
        self.varFirst = IntVar()
        self.varSecond = IntVar()
        self.varThird = IntVar()
        self.varFourth = IntVar()
        self.varFifth = IntVar()
        self.firstImageCButton = Checkbutton(self.biographiesFrame, text = "First", variable = self.varFirst, onvalue = 1, offvalue = 0, height=1, width = 25, bd = 3)
        self.firstImageCButton.grid(row= 0, column= 1)
        self.secondImageCButton = Checkbutton(self.jobsFrame, text = "Second", variable = self.varSecond, onvalue = 1, offvalue = 0, height=1, width = 35, bd = 3)
        self.secondImageCButton.grid(row= 0, column= 1)
        self.thirdImageCButton = Checkbutton(self.namesFrame, text = "Third", variable = self.varThird, onvalue = 1, offvalue = 0, height=1, width = 29, bd = 3)
        self.thirdImageCButton.grid(row= 0, column= 1)
        self.fourthImageCButton = Checkbutton(self.emailsFrame, text = "Fourth", variable = self.varFourth, onvalue = 1, offvalue = 0, height=1, width = 30, bd = 3)
        self.fourthImageCButton.grid(row= 0, column= 1)
        self.fifthImageCButton = Checkbutton(self.tradesFrame, text = "Fifth", variable = self.varFifth, onvalue = 1, offvalue = 0, height=1, width = 25, bd = 3)
        self.fifthImageCButton.grid(row= 0, column= 1)

    def setupRedoSection(self):
        #generateRedo frame
        self.generateRedoFrame = tk.Frame(master=self.middleFrame)
        self.generateRedoFrame.pack(side= tk.TOP, fill= tk.X, padx = 17, pady = 20)
        #generate and redo button
        self.generateButton = tk.Button(master=self.generateRedoFrame, text= "Generate",width= 10, pady= 0, background= "green", foreground= "white", command= self.generate, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.generateButton.grid(row= 0, column= 0, padx = 10)
        self.redoButton = tk.Button(master=self.generateRedoFrame, text= "Redo",width= 10, pady= 0, background= "gray", foreground= "white", command= self.redoWrite, bd = 3, font = TkFont.Font(family="Helvetica", size = 8, weight="bold"))
        self.redoButton.grid(row= 0, column= 1, padx = 5, pady = 0)

    def setupProcessLogSection(self):
        #processLog frames
        self.processLogFrame = tk.Frame(master=self.middleFrame)
        self.processLogFrame.pack(side= tk.LEFT, fill= tk.X, padx = 15, pady = 0)
        self.processLogFrameL = tk.Frame(master=self.processLogFrame)
        self.processLogFrameL.pack(side= tk.TOP, fill= tk.X, padx = 70, pady = 5)
        self.processLogFrameT = tk.Frame(master=self.processLogFrame)
        self.processLogFrameT.pack(side= tk.TOP, fill= tk.X, padx = 0, pady = 0)
        #processLog label
        self.processLogLabel = tk.Label(master=self.processLogFrameL, text= "Process Log:")
        self.processLogLabel.grid(row= 0, column= 0)
        #processLog text
        self.processLogText = tk.Text(master=self.processLogFrameT, bd = 3, height = 10, width = 30)
        self.processLogText.grid(row= 0, column= 0)

    def setupPaths(self):
        #paths
        self.trafficPath = '.././'
        self.finalPath = self.trafficPath + '/final'
        self.filesPath = self.trafficPath + '/data/files'
        self.tradersImagesPath = self.trafficPath + '/data/images/folderImages'
        self.watermarkTemplatePath = self.trafficPath + '/data/images/watermarkTemplate.png'
        self.watermarkUsernamesPath = self.trafficPath + '/data/images/watermarkUsernames'
        self.completedPath = self.trafficPath + '/more/completed'
        self.errorsPath = self.trafficPath + '/more/errors.txt'

    def setupVariables(self):
        #variables
        self.username = ''
        self.numTokens = 0
        self.numImagesPerToken = 0
        #for the redo option variables that remember the last state of the GUI
        self.redoUsername = ''
        self.redoMethod = ''
        self.redoNumTokens = 0
        self.redoNumImagesPerToken = 0
        self.redoVarBackup = 0
        self.redoVarPrefixes = []
        self.redoVarFiles = []
        self.redoVarImageAs = []
        self.indexImageForWatermark = 0
        self.traderUserImagesPath = ''
        self.imageForWatermarkPaths = []
        self.dataNames = ['NAMES.txt', 'TRADES.txt', 'EMAILS.txt', 'JOBS.txt', 'BIOS.txt']
        self.dataNamesFlags = [False, False, False, False, False]

    def setupListOfVariables(self):
        #lists that group var variables
        self.varBackup = 0
        self.varPrefixes = [self.varPrefix1, self.varPrefix2, self.varPrefix3, self.varPrefix4, self.varPrefix5, self.varPrefix6, self.varPrefix7, self.varPrefix8]
        for varPrefix in self.varPrefixes:
            varPrefix.set(0)
        self.varFiles = [self.varBiographies, self.varJobs, self.varNames, self.varEmails, self.vartrades]
        for varFile in self.varFiles:
            varFile.set(0)
        self.varImageAs = [self.varFirst, self.varSecond, self.varThird, self.varFourth, self.varFifth]
        for varImageAs in self.varImageAs:
            varImageAs.set(0)

    #initialization of paths and parameters
    def initialize(self):
        self.setupPaths()
        self.setupVariables()
        self.setupListOfVariables()

    #clears the entire GUI with all variables (redo variables are the only ones not deleted)
    def clearGUI(self):
        self.username = ''
        self.numTokens = 0
        self.numImagesPerToken = 0
        self.varPromotion.set(0)
        self.varBackup.set(0)
        for varPrefix in self.varPrefixes:
            varPrefix.set(0)
        for varFile in self.varFiles:
            varFile.set(0)
        for varImageAs in self.varImageAs:
            varImageAs.set(0)
        self.usernameEntry.delete(0, END)
        self.numTokensEntry.delete(0, END)
        self.numImagesPerTokenEntry.delete(0,END)
        self.processLogText.delete(1.0, END)

    #deletes the old one and prints the new text in the processLog
    def processLogTextUpdate(self, text):
        self.processLogText.delete(1.0, END)
        self.processLogText.insert(1.0, text)

    #it is called by the Select All button, it changes the sign of each checkbox from the prefixes section
    def selectAllPrefixes(self):
        for varPrefix in self.varPrefixes:
            varPrefix.set(1 - varPrefix.get())

    #it is called by the Select All button, it changes the sign of each checkbox from the files section
    def selectAllFiles(self):
        for varFile in self.varFiles:
            varFile.set(1 - varFile.get())

    #it is called by the Select All button, it changes the sign of each checkbox from the imageAs section
    def selectAllImagesAs(self):
        for varImage in self.varImageAs:
            varImage.set(1 - varImage.get())

    #calls the Generate button, the main function
    def generate(self):
        if self.checkGUI() == True:
            self.redoRemember()
            self.processLogTextUpdate('Process started. Please wait.')
            startTime = time.time()
            #mainPyQt5.py has the code of generate function
            self.clearGUI()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogTextUpdate('Order finished.\n' + '\nSnapchat username: ' + self.redoUsername + '\nTokens created: ' + str(self.redoNumTokens) + '\nNum images per token: ' + str(self.redoNumImagesPerToken) + '\Promotion: ' + self.redoMethod + '\nTime elapsed: ' + '{:.2f}'.format(elapsedTime) + ' seconds.')
            self.clearGUIButton["state"] = "disabled"
            self.reverseButton["state"] = "disabled"
            self.selectAllPrefixes["state"] = "disabled"
            self.selectAllFiles["state"] = "disabled"
            self.selectAllImagesAs["state"] = "disabled"
            self.usernameEntry["state"] = "disabled"
            self.numTokensEntry["state"] = "disabled"
            self.numImagesPerTokenEntry["state"] = "disabled"

    def checkPromotion(self):
        #checking if any promotion is selected
        if self.varPromotion.get() == 0:
            self.processLogTextUpdate('You haven\'t selected any promotions. Correct the mistake and try again.')
            return False
        #checking if a promotion other than no promo is selected and no prefix is ​​selected
        if self.varPromotion != 4:
            flag = False
            for varPrefix in self.varPrefixes:
                if varPrefix.get() != 0:
                    flag = True
            if flag == False:
                self.processLogTextUpdate('You haven\'t selected any prefix and you are not using no promo, which is a mistake. Correct the mistake and try again.')
                return False
        #checking whether the watermark promotion is not selected, but that the serial number of the image for the watermark is still selected
        if self.varPromotion == 1 or self.varPromotion == 4:
            flag == False
            for varImage in self.varImageAs:
                if varImage.get() != 0:
                    self.processLogTextUpdate('You have chosen to watermark the images but you haven\'t selected the index of the image you are watermarking. Correct the mistake and try again.')
                    return False
        #checks whether a watermark or a watermarkBiography promotion is selected, and that the sequence number of the image for watermarking is not selected
        elif self.varPromotion == 2 or self.varPromotion == 3:
            flag == False
            for varImage in self.varImageAs:
                if varImage.get() != 0:
                    flag = True
            if flag == False:
                self.processLogTextUpdate('You have chosen to watermark the images but you haven\'t selected the index of the image you are watermarking. Correct the mistake and try again.')
                return False

    #checks that the GUI is populated adequately to allow the program to process traffic
    def checkGUI(self):
        #username verification
        if self.usernameEntry.get() == '':
            self.processLogTextUpdate('You didn\'t enter a username. Correct the mistake and try again.')
            return False
        #checking the number of tokens
        if self.numTokensEntry.get() == '':
            self.processLogTextUpdate('You didn\'t enter a token number (Num of tokens). Correct the mistake and try again.')
            return False
        #checking the number of images per token
        if self.numImagesPerTokenEntry.get() == '':
            self.processLogTextUpdate('You didn\'t enter number of images per token (Num images per token). Correct the mistake and try again.')
            return False
        self.checkPromotion()
        return True
        
    #writing to all redo variables
    def redoRemember(self):
        self.redoUsername = ''
        if self.varPromotion == 1:
            self.redoMethod = 'Biography promotion'
        elif self.varPromotion == 2:
            self.redoMethod = 'Watermark + Biography promotion'
        elif self.varPromotion == 3:
            self.redoMethod = 'Watermark promotion'
        elif self.varPromotion == 4:
            self.redoMethod = 'No promotion'
        self.redoNumTokens = self.numTokens
        self.redoNumImagesPerToken = self.numImagesPerToken
        self.redoVarBackup = self.varBackup
        self.redoVarPrefixes.clear()
        for varPrefix in self.varPrefixes:
            self.redoVarPrefixes.append(varPrefix)
        self.redoVarFiles.clear()
        for varFile in self.varFiles:
            self.redoVarFiles.append(varFile)
        self.redoVarImageAs.clear()
        for varImage in self.varImageAs:
            self.redoVarImageAs.append(varImage)
            
    #when clicking the redo button, you should enter those values ​​from the saved redo values ​​into variables that are not redo
    def redoWrite(self):
        self.numTokens = self.redoNumTokens
        self.numTokensEntry.delete(0, END)
        self.numTokensEntry.insert(0, self.numTokens)
        self.numImagesPerToken = self.redoNumImagesPerToken
        self.numImagesPerTokenEntry.delete(0, END)
        self.numImagesPerTokenEntry.insert(0, self.numImagesPerToken)
        self.varBackup.set(self.redoVarBackup)
        self.processLogTextUpdate('')
        self.varPrefixes.clear()
        for varPrefix in self.redoVarPrefixes:
            self.varPrefixes.append(varPrefix)
        self.varFiles.clear()
        for varFile in self.redoVarFiles:
            self.varFiles.append(varFile)
        self.varImageAs.clear()
        for varImage in self.redoVarImageAs:
            self.varImageAs.append(varImage)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
