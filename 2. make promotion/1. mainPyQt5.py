import os
import openpyxl
import PIL
import random
import shutil
import sys
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PyQt5 import QtCore, QtWidgets         # type: ignore
from PyQt5.QtWidgets import *               # type: ignore
from PyQt5.QtCore import *                  # type: ignore
from PyQt5.QtGui import *                   # type: ignore

#Window is the main class that represents the GUI. It contains tabs, and each tab is created as a separate class
class Window(QTabWidget):                   # type: ignore
   def __init__(self, parent = None):
      super(Window, self).__init__(parent)
      self.left = 500
      self.top = 190
      self.width = 800
      self.height = 800
      self.setGeometry(self.left, self.top, self.width, self.height)
      self.setWindowTitle("PyQt5 GUI")
      self.tab1 = Tab1()
      self.tab2 = Tab2()
      self.tab3 = Tab3()
      self.addTab(self.tab1, 'Generator')
      self.addTab(self.tab2, 'Locations')
      self.addTab(self.tab3, 'Profit')
      self.show()

#Tab1 is the class that represents the first tab of the GUI, it is the most complex
class Tab1(QWidget):                        # type: ignore
    def __init__(self):
        super(Tab1, self).__init__()
        self.title = 'Generator'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupClearSection()
        self.setupUsernameSection()
        self.setupNumSection()
        self.setupMethodSection()
        self.setupFilesSection()
        self.setupPrefixSection()
        self.setupIndexImageSection()
        self.setupProcessLogSection()
        self.setupMainButtonsSection()
        self.setupPaths()
        self.setupVariables()

    def setupVariables(self):
        #variables used for class Tab1 operation
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.indexImageForWatermark = 0
        self.username = ''
        self.traderUserImagesPath = ''
        self.imageForWatermarkPaths = []
        self.dataNames = ['NAMES.txt', 'LOCATIONS.txt', 'EMAILS.txt', 'JOBS.txt', 'BIOS.txt']
        #dataNamesFlags is used for easy checking of dataNames files,
        #in terms of easy recognition of which file needs to be processed or checked
        self.dataNamesFlags = [False, False, False, False, False]
        #when the redo button is clicked, it restores everything from before
        self.redoUsername = ''
        self.redoTokens = 30
        self.redoImagesPerFolder = 5
        redo = [self.redoMethod, self.redoBios, self.redoJobs, self.redoNames, self.redoEmails, self.redoLocations, self.redoFirst, self.redoSecond, self.redoThird, self.redoFourth, self.redoFifth]
        for r in redo:
            r = 0

    def setupPaths(self):
        #watermarkSnapPath changes depending on the username of the snap, so it is undefined at the start
        self.watermarkSnapPath = ''
        #paths used to run the Tab1 class, all paths are located somewhere in the Traffic folder,
        #all paths except watermarkSnapPath are fixed
        self.trafficPath = '.././'
        self.ordersPath = self.trafficPath + '/orders'
        self.finalPath = self.trafficPath + '/final'
        self.dataPath = self.trafficPath + '/data'
        self.morePath = self.trafficPath + '/more'
        self.completedPath = self.morePath + '/completed'
        self.tradersImagesPath = self.dataPath + '/tradersImages'
        self.watermarkTemplatePath = self.dataPath + '/watermarkTemplate.png'

    def setupProcessLogSection(self):
        self.processLogLabel = QLabel('Process Log', self)                      # type: ignore
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(420, 480)
        self.processLogLabel.setStyleSheet("background-color : yellow")
        self.processLogContent = QTextEdit('Good day my friend!', self)         # type: ignore
        self.processLogContent.adjustSize()
        self.processLogContent.move(330, 510)

    def setupMainButtonsSection(self):
        self.generateButton = QPushButton('Generate', self)                     # type: ignore
        self.generateButton.clicked.connect(self.generateFunction)
        self.generateButton.setStyleSheet("background-color : green")
        self.generateButton.adjustSize()
        self.generateButton.move(100, 650)

        self.exitButton = QPushButton('Exit', self)                             # type: ignore
        self.exitButton.clicked.connect(self.exitFunction)
        self.exitButton.setStyleSheet("background-color : red")
        self.exitButton.adjustSize()
        self.exitButton.move(650, 650)

        self.RedoButton = QPushButton('Redo', self)                             # type: ignore
        self.RedoButton.clicked.connect(self.redoWrite)
        self.RedoButton.adjustSize()
        self.RedoButton.move(330, 80)

    def setupFilesSection(self):
        self.selectAllFilesButton = QPushButton('Select All', self)             # type: ignore
        self.selectAllFilesButton.clicked.connect(self.selectAllFilesFunction)
        self.selectAllFilesButton.adjustSize()
        self.selectAllFilesButton.move(350, 250)

        self.biosCheckBox = QCheckBox("Bios", self)                             # type: ignore
        self.biosCheckBox.adjustSize()
        self.biosCheckBox.move(370, 290)

        self.jobsCheckBox = QCheckBox("Jobs", self)                             # type: ignore
        self.jobsCheckBox.adjustSize()
        self.jobsCheckBox.move(370, 320)

        self.namesCheckBox = QCheckBox("Names", self)                           # type: ignore
        self.namesCheckBox.adjustSize()
        self.namesCheckBox.move(370, 350)

        self.emailsCheckBox = QCheckBox("Emails", self)                         # type: ignore
        self.emailsCheckBox.adjustSize()
        self.emailsCheckBox.move(370, 380)

        self.locationsCheckBox = QCheckBox("Locations", self)                   # type: ignore
        self.locationsCheckBox.adjustSize()
        self.locationsCheckBox.move(370, 410)

    def setupPrefixSection(self):
        self.setImageAsLabel = QLabel('Set watermarked\n   Image as:', self)    # type: ignore
        self.setImageAsLabel.adjustSize()
        self.setImageAsLabel.move(490, 250)

        self.selectAllPrefixesButton = QPushButton('Select All', self)          # type: ignore
        self.selectAllPrefixesButton.clicked.connect(self.selectAllPrefixesFunction)
        self.selectAllPrefixesButton.adjustSize()
        self.selectAllPrefixesButton.move(20, 110)

        self.prefix1 = QCheckBox("trade ", self)                                # type: ignore
        self.prefix1.adjustSize()
        self.prefix1.move(20, 150)

        self.prefix2 = QCheckBox("trade - ", self)                              # type: ignore
        self.prefix2.adjustSize() 
        self.prefix2.move(20, 180)

        self.prefix3 = QCheckBox("trade: ", self)                               # type: ignore
        self.prefix3.adjustSize()
        self.prefix3.move(100, 150)

        self.prefix4 = QCheckBox("$trade$ ", self)                              # type: ignore
        self.prefix4.adjustSize()
        self.prefix4.move(100, 180)

    def setupIndexImageSection(self):
        self.FirstImageBox = QCheckBox("First", self)                           # type: ignore
        self.FirstImageBox.adjustSize()
        self.FirstImageBox.move(510, 300)

        self.SecondImageBox = QCheckBox("Second", self)                         # type: ignore
        self.SecondImageBox.adjustSize()
        self.SecondImageBox.move(510, 330)

        self.ThirdImageBox = QCheckBox("Third", self)                           # type: ignore
        self.ThirdImageBox.adjustSize()
        self.ThirdImageBox.move(510, 360)
        
        self.FourthImageBox = QCheckBox("Fourth", self)                         # type: ignore
        self.FourthImageBox.adjustSize()
        self.FourthImageBox.move(510, 390)

        self.FifthImageBox = QCheckBox("Fifth", self)                           # type: ignore
        self.FifthImageBox.adjustSize()
        self.FifthImageBox.move(510, 420)

    def setupUsernameSection(self):
        self.usernameLabel = QLabel('Username:', self)                          # type: ignore
        self.usernameLabel.adjustSize()
        self.usernameLabel.move(20, 20)
        self.usernameLineEdit = QLineEdit('', self)                             # type: ignore
        self.usernameLineEdit.adjustSize()
        self.usernameLineEdit.move(135, 18)

    def setupNumSection(self):
        self.numTokensLabel = QLabel('Tokens:', self)                           # type: ignore
        self.numTokensLabel.adjustSize()
        self.numTokensLabel.move(20, 50)
        self.numTokensLineEdit = QLineEdit('30', self)                          # type: ignore
        self.numTokensLineEdit.adjustSize()
        self.numTokensLineEdit.move(135, 48)

        self.numImagesPerFolderLabel = QLabel('Images per folder:', self)       # type: ignore
        self.numImagesPerFolderLabel.adjustSize()
        self.numImagesPerFolderLabel.move(20, 80)
        self.numImagesPerFolderLineEdit = QLineEdit('5', self)                  # type: ignore
        self.numImagesPerFolderLineEdit.adjustSize()
        self.numImagesPerFolderLineEdit.move(135, 78)

    def setupMethodSection(self):
        self.methodsLabel = QLabel('Choose method:', self)                      # type: ignore
        self.methodsLabel.adjustSize()
        self.methodsLabel.move(20, 230)
        self.setupBioPromotionSection()
        self.setupWatermarkPromotionSection()
        self.setupBWPromotionSection()
        self.setupNoPromotionSection()

    def setupBWPromotionSection(self):
        self.watermarkBioRandomBox = QRadioButton ("Watermark + Bio --> Random", self)                  # type: ignore
        self.watermarkBioRandomBox.adjustSize()
        self.watermarkBioRandomBox.move(50, 430)

        self.watermarkBioOneBox = QRadioButton ("Watermark + Bio --> One trader", self)                 # type: ignore
        self.watermarkBioOneBox.adjustSize()
        self.watermarkBioOneBox.move(50, 460)

        self.watermarkBioOneBackupBox = QRadioButton ("Watermark + Bio --> One trader + Backup", self)  # type: ignore
        self.watermarkBioOneBackupBox.adjustSize()
        self.watermarkBioOneBackupBox.move(50, 490)

    def setupWatermarkPromotionSection(self):
        self.watermarkRandomBox = QRadioButton ("Watermark Promotion --> Random", self)                 # type: ignore
        self.watermarkRandomBox.adjustSize()
        self.watermarkRandomBox.move(50, 340)

        self.watermarkOneBox = QRadioButton ("Watermark Promotion --> One trader", self)                # type: ignore
        self.watermarkOneBox.adjustSize()
        self.watermarkOneBox.move(50, 370)

        self.watermarkOneBackupBox = QRadioButton ("Watermark Promotion --> One trader + Backup", self) # type: ignore
        self.watermarkOneBackupBox.adjustSize()
        self.watermarkOneBackupBox.move(50, 400)

    def setupBioPromotionSection(self):
        self.bioRandomBox = QRadioButton ("Bio Promotion --> Random", self)                             # type: ignore
        self.bioRandomBox.adjustSize()
        self.bioRandomBox.move(50, 280)

        self.bioOneBox = QRadioButton ("Bio Promotion --> One trader", self)                            # type: ignore
        self.bioOneBox.adjustSize()
        self.bioOneBox.move(50, 310)

    def setupNoPromotionSection(self):
        self.justRandomBox = QRadioButton ("No Promotion --> Random", self)                             # type: ignore
        self.justRandomBox.adjustSize()
        self.justRandomBox.move(50, 520)

        self.justOneBox = QRadioButton ("No Promotion --> One trader", self)                            # type: ignore
        self.justOneBox.adjustSize()
        self.justOneBox.move(50, 550)

        self.justOneBackupBox = QRadioButton ("No Promotion --> One trader + Backup", self)             # type: ignore
        self.justOneBackupBox.adjustSize()
        self.justOneBackupBox.move(50, 580)

    def setupClearSection(self):
        self.clearGUIButton = QPushButton('Clear\nGUI', self)                                           # type: ignore
        self.clearGUIButton.clicked.connect(self.clearGUI)
        self.clearGUIButton.adjustSize()
        self.clearGUIButton.move(330, 20)

        self.clearErrorsAndResultsButton = QPushButton('Clear errors\nand results', self)               # type: ignore
        self.clearErrorsAndResultsButton.clicked.connect(self.clearErrorsAndResults)
        self.clearErrorsAndResultsButton.adjustSize()
        self.clearErrorsAndResultsButton.move(650, 500)

        self.clearFinalButton = QPushButton('Clear\nfinal folder', self)                                # type: ignore
        self.clearFinalButton.clicked.connect(self.clearFinalFolder)
        self.clearFinalButton.adjustSize()
        self.clearFinalButton.move(650, 550)

    #exit the application
    def exitFunction(self):
        QApplication.quit()     # type: ignore

    #clears everything written or marked on the GUI to make it more readable
    def clearGUI(self):
        self.setDefaultValues()
        self.clearVisual()

    def setDefaultValues(self):
        #first, set the values in the program to their default values
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.indexImageForWatermark = 1
        self.username = ''
        self.traderUserImagesPath = ''
        self.watermarkSnapPath = ''
        self.imageForWatermarkPaths = []
        self.dataNamesFlags = [False, False, False, False, False]

    def clearVisual(self):
        #then, clear the GUI to make it more readable
        self.usernameLineEdit.setText('')
        self.numTokensLineEdit.setText('')
        self.numImagesPerFolderLineEdit.setText('')
        self.processLogContent.setText('')
        self.processLogContent.adjustSize()
        self.bioRandomBox.setChecked(True)
        self.FirstImageBox.setChecked(False)
        self.SecondImageBox.setChecked(False)
        self.ThirdImageBox.setChecked(False)
        self.FourthImageBox.setChecked(False)
        self.FifthImageBox.setChecked(False)
        self.biosCheckBox.setChecked(False)
        self.jobsCheckBox.setChecked(False)
        self.namesCheckBox.setChecked(False)
        self.emailsCheckBox.setChecked(False)
        self.locationsCheckBox.setChecked(False)

    #if the 'final' folder exists, delete all of its contents
    def clearFinalFolder(self):
        for fileName in os.listdir(self.finalPath):
            filePath = self.finalPath + '/' + fileName
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        self.processLogContent.setText('Folder final is empty.')
        QApplication.processEvents()                # type: ignore
        self.processLogContent.adjustSize()

    #delete all of the contents of the 'completed' folder and the 'errors.txt' file
    def clearErrorsAndResults(self):
        with open(self.morePath + '/errors.txt', 'w') as Writer:
            pass
        shutil.rmtree(self.completedPath)
        os.mkdir(self.completedPath)
        self.processLogContent.setText('File \'errors.txt\' and folder \'completed\' are empty.')
        QApplication.processEvents()                # type: ignore
        self.processLogContent.adjustSize()
            
    def redoRead(self):
        self.redoUsername = self.username
        self.redoTokens = self.numTokens
        self.redoImagesPerFolder = self.numImagesPerFolder
        self.checkBoxesGUI()
        checkBoxes = [self.biosCheckBox, self.jobsCheckBox, self.namesCheckBox, self.emailsCheckBox, self.locationsCheckBox, self.FirstImageBox, self.SecondImageBox, self.ThirdImageBox, self.FourthImageBox, self.FifthImageBox]
        redoList = [self.redoBios, self.redoJobs, self.redoNames, self.redoEmails, self.redoLocations, self.redoFirst, self.redoSecond, self.redoThird, self.redoFourth, self.redoFifth]
        for i in range(len(checkBoxes)):
            if checkBoxes[i].isChecked():
                redoList[i] = 1
            else:
                redoList[i] = 0

    def checkBoxesGUI(self):
        methods = [self.bioRandomBox, self.bioOneBox, self.watermarkRandomBox, self.watermarkOneBox, self.watermarkOneBackupBox, self.watermarkBioRandomBox, self.watermarkBioOneBox, self.watermarkBioOneBackupBox, self.justRandomBox, self.justOneBox, self.justOneBackupBox]
        for i in range(len(methods)):
            if methods[i].isChecked():
                self.redoMethod = i

    def redoWrite(self):
        self.numTokensLineEdit.setText(str(self.redoTokens))
        self.numImagesPerFolderLineEdit.setText(str(self.redoImagesPerFolder))
        self.numTokens = self.redoTokens
        self.numImagesPerFolder = self.redoImagesPerFolder
        self.redoIndexesWrite()
        listBox = self.redoFilesWrite()
        self.redoPromotionWrite(listBox)

    def redoPromotionWrite(self, listBox):
        list = [self.bioRandomBox, self.bioOneBox, self.watermarkRandomBox, self.watermarkOneBox, self.watermarkOneBackupBox, self.watermarkBioRandomBox, self.watermarkBioOneBox, self.watermarkBioOneBackupBox, self.justRandomBox, self.justOneBox, self.justOneBackupBox]
        for i in range(len(list)):
            if self.redoMethod == i:
                listBox[i].setChecked(True)

    def redoFilesWrite(self):
        list = [self.redoBios, self.redoJobs, self.redoNames, self.redoEmails, self.redoLocations]
        listBox = [self.biosCheckBox, self.jobsCheckBox, self.namesCheckBox, self.emailsCheckBox, self.locationsCheckBox]
        for i in range(len(list)):
            if list[i] == 1:
                listBox[i].setChecked(True)
            else:
                listBox[i].setChecked(False)
        return listBox

    def redoIndexesWrite(self):
        list = [self.redoFirst, self.redoSecond, self.redoThird, self.redoFourth, self.redoFifth]
        listBox = [self.FirstImageBox, self.SecondImageBox, self.ThirdImageBox, self.FourthImageBox, self.FifthImageBox]
        for i in range(len(list)):
            if list[i] == 1:
                listBox[i].setChecked(True)
            else:
                listBox[i].setChecked(False)

    #clicking the Select All button selects all files from the data folder (dataNames files) for extractData()
    def selectAllFilesFunction(self):
        if self.biosCheckBox.isChecked() and self.namesCheckBox.isChecked() and self.locationsCheckBox.isChecked() and self.emailsCheckBox.isChecked() and self.jobsCheckBox.isChecked():
            self.biosCheckBox.setChecked(False)
            self.namesCheckBox.setChecked(False)
            self.locationsCheckBox.setChecked(False)
            self.emailsCheckBox.setChecked(False)
            self.jobsCheckBox.setChecked(False)
            self.dataNamesFlags = [False, False, False, False, False]
        else:
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.locationsCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]

    def selectAllPrefixesFunction(self):
        if self.prefix1.isChecked() and self.prefix2.isChecked() and self.prefix3.isChecked() and self.prefix4.isChecked():
            self.prefix1.setChecked(False)
            self.prefix2.setChecked(False)
            self.prefix3.setChecked(False)
            self.prefix4.setChecked(False)
            self.prefixes = [False, False, False, False, False]
        else:
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.locationsCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]

    #sets in the dataNamesFlags list which files from dataNames should be processed
    def setDataFlags(self):
        if self.namesCheckBox.isChecked():
            self.dataNamesFlags[0] = True
        if self.locationsCheckBox.isChecked():
            self.dataNamesFlags[1] = True
        if self.emailsCheckBox.isChecked():
            self.dataNamesFlags[2] = True
        if self.jobsCheckBox.isChecked():
            self.dataNamesFlags[3] = True
        if self.biosCheckBox.isChecked():
            self.dataNamesFlags[4] = True

    #it is determined what is the serial number of the image in each image folder of the account,
    #only the image with that serial number in each account image folder will be watermarked
    def setIndexImageForWatermark(self):
        if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.justOneBackupBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBox.isChecked():
            if self.validBioPromotion():
                return True
            else:
                return False
        if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            if self.validWatermarkPromotion():
                return True
            else:
                return False

    def validBioPromotion(self):
        if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
            return True
        else:
            self.processLogContent.setText('You can\'t use bio method with checking which image in folders you want to watermark. Uncheck it and try again.')
            QApplication.processEvents()            # type: ignore
            self.indexImageForWatermark = 0
            return False

    def validWatermarkPromotion(self):
        if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
            self.processLogContent.setText('You can\'t use watermark method without checking which image in folders you want to watermark. Check exactly 1 and try again.')
            QApplication.processEvents()            # type: ignore
            self.indexImageForWatermark = 0
            return False
        if self.setIndexImageForWatermark() == False:
            self.processLogContent.setText('You can\'t use watermark method with checking more than 1 images per folder to watermark.  Check exactly 1 and try again.')
            QApplication.processEvents()            # type: ignore
            self.indexImageForWatermark = 0
            return False

    def setIndexImageForWatermark(self):
        if self.FirstImageBox.isChecked() and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
            self.indexImageForWatermark = 1
            return True
        elif self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
            self.indexImageForWatermark = 2
            return True
        elif self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
            self.indexImageForWatermark = 3
            return True
        elif self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() and self.FifthImageBox.isChecked() == False:
            self.indexImageForWatermark = 4
            return True
        elif self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked():
            self.indexImageForWatermark = 5
            return True
        return False

    def readFromGUI(self):
        self.username = self.usernameLineEdit.text()
        self.numTokens = int(self.numTokensLineEdit.text())
        self.numImagesPerFolder = int(self.numImagesPerFolderLineEdit.text())
        self.setDataFlags()
        checkData = self.checkEnoughData() and self.setIndexImageForWatermark()
        self.redoRead()
        return checkData

    def modifyAndExtract(self):
        #the necessary folders are created in the final folder
        self.makeUsernameFolders()
        #the selected files are extracted from the dataNames list and transferred to the final folder
        self.extractData()
        #if the 'Random' method is selected, i.e. a method that extracts images from different traders,
        #then the extractRandomTraders() method is called
        if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
            self.extractRandomTraders()
        #if the 'One' method is selected, i.e. a method that extracts images from only one trader,
        #then the extractOneTrader() method is called
        elif self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
            self.extractOneTrader()
        #images are cropped (flipped if necessary), renamed and if a watermark is used
        #remember images that need to be watermarked
        self.modifyImages()

    def callPromotion(self, startTime):
        #if a bio method is selected, the function callBioMethod() is called
        if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            self.callBioMethod()
        #if a watermark method is selected, the callWatermarkMethod() function is called
        if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            self.callWatermarkMethod()
        endTime = time.time()
        elapsedTime = endTime - startTime
        #the order is completed, so the GUI is cleared
        return self.findMethod(), elapsedTime

    def finishGUI(self, method, elapsedTime):
        self.clearGUIButton.setDisabled(False)
        self.selectAllFilesButton.setDisabled(False)
        self.clearErrorsAndResultsButton.setDisabled(False)
        self.clearFinalButton.setDisabled(False)
        self.generateButton.setDisabled(False)
        self.processLogContent.setText('Order finished.\n' + '\nSnapchat username: ' + self.redoUsername + '\nTokens created: ' + str(self.redoTokens) + '\nMethod: ' + method + '\nTime elapsed: ' + '{:.2f}'.format(elapsedTime) + ' seconds.')
        QApplication.processEvents()            # type: ignore
        self.processLogContent.adjustSize()
        with open(self.completedPath + '/' + self.redoUsername + '.txt', 'w') as Writer:
            Writer.write(self.processLogContent.toPlainText())

    def startProcess(self, startTime):
        self.modifyAndExtract()
        method, elapsedTime = self.callPromotion(startTime)
        self.clearGUI()
        self.finishGUI(method, elapsedTime)

    #the main function of this GUI is the Generate button, which is used to process the currently selected order
    def generateFunction(self):
        startTime = time.time()
        #if there are necessary data to process the current order, processing begins
        if self.readFromGUI() == True:
            self.processLogContent.setText('Process started. Please wait.')
            self.clearGUIButton.setDisabled(True)
            self.selectAllFilesButton.setDisabled(True)
            self.clearErrorsAndResultsButton.setDisabled(True)
            self.clearFinalButton.setDisabled(True)
            self.generateButton.setDisabled(True)
            QApplication.processEvents()        # type: ignore
            self.startProcess(startTime)

    def findMethod(self):
        if self.bioRandomBox.isChecked():
            return 'Bio --> Random'
        if self.bioOneBox.isChecked():
            return 'Bio --> One trader'
        if self.watermarkRandomBox.isChecked():
            return 'Watermark --> Random'
        if self.watermarkOneBox.isChecked():
            return 'Watermark --> One trader'
        if self.watermarkOneBackupBox.isChecked():
            return 'Watermark --> One trader + Backup'
        if self.watermarkBioRandomBox.isChecked():
            return 'Watermark + Bio --> Random'
        if self.watermarkBioOneBox.isChecked():
            return 'Watermark + Bio --> One trader'
        if self.watermarkBioOneBackupBox.isChecked():
            return 'Watermark + Bio --> One trader + Backup'
        if self.justRandomBox.isChecked():
            return 'No Promotion --> Random'
        if self.justOneBox.isChecked():
            return 'No Promotion --> One trader'
        if self.justOneBackupBox.isChecked():
            return 'No Promotion --> One trader + Backup'

    def errorInGUI(self, checkGUI, checkGUIMethods):
        if checkGUI == False:
            if  self.usernameLineEdit.text() == '':
                self.processLogContent.setText('You didn\'t input username. Try again.')
            elif  self.numTokensLineEdit.text() == '':
                self.processLogContent.setText('You didn\'t input number of tokens. Try again.')
            elif  self.numImagesPerFolderLineEdit.text() == '':
                self.processLogContent.setText('You didn\'t input number of images per folder. Try again.')
            elif checkGUIMethods == False:
                self.processLogContent.setText('You didn\'t choose method. Try again.')
            #elif checkIndexImageForWatermark == False:
                #self.processLogContent.setText('You want watermark method but you didn\'t choose serial number of the image in folders for watermarking. Try again.')
            QApplication.processEvents()        # type: ignore
            self.processLogContent.adjustSize()
            return False

    def checkGUIIsTrue(self):
        #first it is checked that the GUI is adequately filled
        checkGUILineEdits = self.usernameLineEdit.text() != '' and self.numTokensLineEdit.text() != '' and self.numImagesPerFolderLineEdit.text() != ''
        checkGUIMethods = self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBackupBox.isChecked()
        #if at least 1 condition is not fulfilled, the order cannot be processed immediately,
        #it is necessary to fix the error
        checkGUI = checkGUILineEdits and checkGUIMethods
        if self.errorInGUI(checkGUI, checkGUIMethods):
            return False
        return True

    def enoughDataInFiles(self):
        i = 0
        #checking for files from dataNames if they have enough lines to process the current order
        for fileName in self.dataNames:
            #the check is only performed if the current file is selected for extraction
            if self.dataNamesFlags[i] == True:
                self.checkCurrentFile(fileName)
                i += 1

    def checkCurrentFile(self, fileName):
        path = self.dataPath + '/' + fileName
        with open(path, 'r') as Reader:
            lines = Reader.readlines()
                #if there are not enough lines for the current order, this is recorded in errors.txt in the orders folder
        if len(lines) < self.numTokens:
            errorMsg = "File " + fileName + " has not enough lines for creating " + str(self.numTokens) + " tokens for customer " + self.customer + " with his username " + self.username
            with open(self.morePath + '/errors.txt', 'a') as Writer:
                if os.path.getsize(self.morePath + '/errors.txt') == 0:
                    Writer.write(errorMsg)
                else:
                    Writer.write('\n' + errorMsg)
            print(errorMsg)
                    #an exception is thrown to skip further examination
            raise Exception(errorMsg)

    def enoughImagesRandom(self):
        #if a 'Random' method is selected, a check is made to see if there are enough images
        pathsForDelete = []
        if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
            acc = 0
            for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                path = self.tradersImagesPath + '/' + fileName
                if len(os.listdir(path)) < 5:
                    pathsForDelete.append(path)
                else:
                    acc += len(os.listdir(path))//self.numImagesPerFolder
            #if there are not enough images, an exception is thrown
            for path in pathsForDelete:
                shutil.rmtree(path)
            if acc < self.numTokens:
                self.notEnoughImages()
            else:
                #if there are enough images, all checking is done
                return True

    def isThereEnoughData(self):
        self.numImagesPerFolder = int(self.numImagesPerFolderLineEdit.text())
        self.numTokens = int(self.numTokensLineEdit.text())
        self.enoughDataInFiles()
        if (self.enoughImagesRandom()):
            return True
        if (self.enoughImagesOne()):
            return True

    def enoughImagesOne(self):
        #if a 'One' or 'OneBackup' method is selected, a check is made to see if there are enough images
        if self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
            for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                path = self.tradersImagesPath + '/' + fileName
                if (self.watermarkOneBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.justOneBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder:
                    self.traderUserImagesPath = path
                    return True
                elif (self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder + self.numTokens:
                    self.traderUserImagesPath = path
                    return True
            #if there are not enough images, an exception is thrown
            self.notEnoughImages()

    #before starting the processing of the order, it should be checked whether the conditions for processing have been met
    def checkEnoughData(self):
        #if there was no error in filling out the GUI
        if self.checkGUIIsTrue():
            try:
                if (self.isThereEnoughData()):
                    return True
            #if an exception is thrown, it is caught here, the program reports an error and is ready to try again
            except Exception as e:
                print('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                self.processLogContent.setText('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                QApplication.processEvents()            # type: ignore
                self.processLogContent.adjustSize()
                return False

    #a function that is called if there are not enough images to process the order
    def notEnoughImages(self):
        errorMsg = "Not enough images for creating " + str(self.numTokens) + " for username " + self.username
        with open(self.morePath + '/errors.txt', 'a') as Writer:
            if os.path.getsize(self.morePath + '/errors.txt') == 0:
                Writer.write(errorMsg)
            else:
                Writer.write("\n" + errorMsg)
        raise Exception(errorMsg)

    #all necessary folders of the current order are created in the final folder
    def makeUsernameFolders(self):
        if os.path.isdir(self.finalPath + '/' + self.username) == True:
            shutil.rmtree(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username + '/' + 'images')
        for i in range(self.numTokens):
            os.mkdir(self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(i + 1))
        #if the 'Backup' method is selected, additional folders should be created
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            if os.path.isdir(self.finalPath + '/' + self.username + 'BACKUP') == True:
                shutil.rmtree(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP' + '/' + 'images')

    def transferLines(self, fileName, name):
        with open(self.dataPath + '/' + fileName, "r") as Reader:
            with open(self.finalPath + '/' + self.username + '/' + name, "w") as Writer:
                for i in range(self.numTokens - 1):
                    Writer.write(Reader.readline())
                Writer.write(Reader.readline().strip('\n'))
            otherLines = Reader.readlines()
        #writes the remaining lines to files
        with open(self.dataPath + '/' + fileName, "w") as Writer:
            Writer.writelines(otherLines)

    #extracts lines from the selected dataNames files and transfers them to the final folder
    def extractData(self):
        otherLines = []
        r = 0
        for fileName in self.dataNames:
            #if the current file needs to be processed
            if self.dataNamesFlags[r] == True:
                name = fileName[0] + fileName[1:].lower()
                self.transferLines(fileName, name)
            r += 1

    #extracts images from the tradersImages folder, but only from one trader, and transfers them to the final folder
    def extractOneTrader(self):
        oldPath = self.traderUserImagesPath
        for countTokens in range(self.numTokens):
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
        #if the 'Backup' method is selected, images should be extracted for them as well
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            for countTokens in range(self.numTokens):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + 'BACKUP/' + 'images'
                shutil.move(oldPath + '/' + firstImageInFile, newPath)

    def countFunction(self, numUsers, BORING, dataUserNames):
        while len(os.listdir(oldPath)) < self.numImagesPerFolder:
            if countUsers >= numUsers:
                countUsers = 0
            if BORING[countUsers] == False:
                print('In folder ', dataUserNames[countUsers],' there is not enough images for account.')
                BORING[countUsers] = True
            countUsers += 1
            if countUsers >= numUsers:
                countUsers = 0
            oldPath = self.tradersImagesPath + '/' + dataUserNames[countUsers]

    #extracts images from the tradersImages folder, but more traders and transfers them to the final folder
    def extractRandomTraders(self):
        countUsers = 0
        numUsers = len(os.listdir(self.tradersImagesPath))
        dataUserNames = []
        BORING = numUsers * [False]
        for j, userFileName in enumerate(os.listdir(self.tradersImagesPath)):
            dataUserNames.append(userFileName)
        for countTokens in range(self.numTokens):
            if countUsers >= numUsers:
                    countUsers = 0
            oldPath = self.tradersImagesPath + '/' + dataUserNames[countUsers]
            self.countFunction(numUsers, BORING, dataUserNames)
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
            countUsers += 1

    def modifyBackupImages(self):
        token = 0 
        folderPath = self.finalPath + '/' + self.username + 'BACKUP/images'
        for i, fileName in enumerate(os.listdir(folderPath)):
            token += 1
            if token <= self.numTokens:
                num = random.randint(1000, 10000)
                oldImagePath = folderPath + "/" + fileName
                newImagePath = folderPath + '/' + 'IMG_' + str(num) + ".jpg"
                os.rename(oldImagePath, newImagePath)
                image = Image.open(newImagePath)
                cropedImage = image.resize((1125, 1364))
                newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                cropedImage.save(newImagePath)
                cropedImage.close()
            else:
                break

    def modify(self, folderPath):
        for i, fileName in enumerate(os.listdir(folderPath)):
            num = num + 1
            oldImagePath = folderPath + "/" + fileName
            newImagePath = folderPath + '/' + 'IMG_' + str(num) + ".jpg"
            os.rename(oldImagePath, newImagePath)
            image = Image.open(newImagePath)
            if i == (self.indexImageForWatermark - 1) and (self.watermarkOneBackupBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked()):
                self.imageForWatermarkPaths.append(newImagePath)
            cropedImage = image.resize((1125, 1364))
            newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            cropedImage.save(newImagePath)
            cropedImage.close()

    #changes the dimensions of the images from the final folder (if necessary, they can be flipped) and rename them
    def modifyImages(self):
        for token in range(self.numTokens):
            folderPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(token + 1)
            num = random.randint(1000, 10000)
            self.modify(folderPath)
        #if the 'Backup' method is selected, such images should also be modified
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            self.modifyBackupImages()

    #function that is called for all types of bio methods
    def callBioMethod(self):
        #the Bios.txt file is required in the final folder of the current order so that the snapshot can be appended to the biography
        bioPath = self.finalPath + '/' + self.username + '/' + 'Bios.txt'
        snaps = [r'\nS.C: ', r'\nS.C - ', r'\nS.C ']
        h = 0
        lines = []
        #username is separated by letters so that it changes from michael555 to m i c h a e l 5 5 5
        s = ""
        for char in self.username:
            s = s + char + ' '
        trickUsername = s.rstrip(' ')
        lines = ""
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            numLines = len(Reader.readlines())
        #appending snaps to biographies is done line by line
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            for i in range(numLines - 1):
                lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername + '\n'
                h += 1
                if h == 3:
                    h = 0
            lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername
        with open(bioPath, "w") as Writer:
            Writer.write(lines)
    
    #real username template for watermark
    def makeUsernameWatermark(self):
        #the template is created only if it does not already exist
        #to the image watermarkTemplatePath which represents a black rectangle,
        #Paste the text that represents the snap's username
        if os.path.isdir(self.watermarkSnapPath) == False:
            with Image.open(self.watermarkTemplatePath) as image:
                width, height = image.size
                height = height - 5
            photo = Image.open(self.watermarkTemplatePath)
            drawing = ImageDraw.Draw(photo)
            font = ImageFont.truetype("./CONSOLA.TTF", 35)
            w, h = font.getsize(self.username)
            drawing.text(((width-w)/2,(height-h)/2), self.username, fill = "white", font = font)
            photo.save(self.watermarkSnapPath)

    def watermarkImages(self):
        width = 0
        #watermarks are made for those images that have been selected for watermarking
        #the username template is pasted on the image that is intended for the watermark
        self.paste(width)
        #if the backup option is selected, those images should also be watermarked, all images in that folder
        self.watermarkBackupImages(width)

    def watermarkBackupImages(self, width):
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            backupPath = self.finalPath + '/' + self.username  + 'BACKUP' + '/' + 'images'
            imagesInBackupPath = []
            for i in os.listdir(backupPath):
                imagesInBackupPath.append(backupPath + '/' + i)
            for inputImagePath in imagesInBackupPath:
                height = 0 + random.randint(-100, 100)
                originalImage = Image.open(inputImagePath)
                originalWidth, originalHeight = originalImage.size
                watermarkImage = Image.open(self.watermarkSnapPath).convert("RGBA")
                transparent = Image.new('RGBA', (originalWidth, originalHeight), (0,0,0,0))
                transparent.paste(originalImage, (0,0))
                transparent.paste(watermarkImage, (width, height), mask=watermarkImage)
                transparent.save(inputImagePath, format="png")

    def paste(self, width):
        for inputImagePath in self.imageForWatermarkPaths:
            height = 0 + random.randint(-100, 100)
            originalImage = Image.open(inputImagePath)
            originalWidth, originalHeight = originalImage.size
            watermarkImage = Image.open(self.watermarkSnapPath).convert("RGBA")
            transparent = Image.new('RGBA', (originalWidth, originalHeight), (0,0,0,0))
            transparent.paste(originalImage, (0,0))
            transparent.paste(watermarkImage, (width, height), mask=watermarkImage)
            transparent.save(inputImagePath, format="png")

    #function that is called for all kinds of watermark methods
    def callWatermarkMethod(self):
        self.watermarkSnapPath = self.dataPath + '/usernameTemplates/' + self.username + '.png'
        self.makeUsernameWatermark()
        self.watermarkImages()

    #method testing function
    def test(self):
        if self.getCustomer() == True:
            self.numImagesPerFolder = 5
            self.numTokensLineEdit.setText(str(self.numTokens))
            self.numImagesPerFolderLineEdit.setText(str(self.numImagesPerFolder))
            self.bioRandomBox.setChecked(True)
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.locationsCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]
            self.generateFunction()

#Tab2 is a class that represents the second tab on the GUI, handling locations
class Tab2(QWidget):                        # type: ignore
    def __init__(self):
        super(Tab2, self).__init__()
        self.title = 'Locations'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupPopulationSection()
        self.setupMainButtonsSection()
        self.setupProcessLogSection()
        self.fromPopulation = 0
        self.toPopulation = 0
        self.numCities = 0
        self.locationsXlsxPath = '.././' + '/data/locations.xlsx'
        self.locationsTxtPath = '.././' + '/data/locations.txt'

    def setupProcessLogSection(self):
        self.processLogLocationsLabel = QLabel('Process log', self)                     # type: ignore
        self.processLogLocationsLabel.setStyleSheet("background-color : yellow")
        self.processLogLocationsLabel.adjustSize()
        self.processLogLocationsLabel.move(490, 20)

        self.processLogLocationsContent = QTextEdit('Nice to see you bro.', self)      # type: ignore
        self.processLogLocationsContent.adjustSize()
        self.processLogLocationsContent.move(400, 50)

    def setupMainButtonsSection(self):
        self.generateOrderButton = QPushButton('Generate\nlocations', self)             # type: ignore
        self.generateOrderButton.clicked.connect(self.generateLocation)
        self.generateOrderButton.setStyleSheet("background-color : green")
        self.generateOrderButton.adjustSize()
        self.generateOrderButton.move(130, 100)

        self.clearGUILocationsButton = QPushButton('Clear\nGUI', self)                  # type: ignore
        self.clearGUILocationsButton.clicked.connect(self.clearGUI)
        self.clearGUILocationsButton.adjustSize()
        self.clearGUILocationsButton.move(420, 275)

        self.exitLocationsButton = QPushButton('Exit', self)                            # type: ignore
        self.exitLocationsButton.clicked.connect(self.exitFunction)
        self.exitLocationsButton.setStyleSheet("background-color : red")
        self.exitLocationsButton.adjustSize()
        self.exitLocationsButton.move(550, 280)

    def setupPopulationSection(self):
        self.populationFromLabel = QLabel('From:', self)                                # type: ignore
        self.populationFromLabel.adjustSize()
        self.populationFromLabel.move(70, 20)
        self.populationFromLineEdit = QLineEdit('', self)                               # type: ignore
        self.populationFromLineEdit.adjustSize()
        self.populationFromLineEdit.move(20, 50)

        self.populationToLabel = QLabel('To:', self)                                    # type: ignore
        self.populationToLabel.adjustSize()
        self.populationToLabel.move(260, 20)
        self.populationToLineEdit = QLineEdit('', self)                                 # type: ignore
        self.populationToLineEdit.adjustSize()
        self.populationToLineEdit.move(200, 50)

    #exit the application
    def exitFunction(self):
        QApplication.quit()                 # type: ignore

    def clearGUI(self):
        self.fromPopulation = 0
        self.toPopulation = 0
        self.numCities = 0
        self.populationFromLineEdit.setText('')
        self.populationToLineEdit.setText('')
        self.processLogLocationsContent.setText('')

    def generateLocation(self):
        workbook = openpyxl.load_workbook(self.locationsXlsxPath)
        sheet = workbook.get_sheet_by_name('Sheet2')
        startTime = time.time()
        self.processLogLocationsContent.setText('Generate started. Please wait.')
        self.clearGUILocationsButton.setDisabled(True)
        self.generateOrderButton.setDisabled(True)
        QApplication.processEvents()        # type: ignore
        with open(self.locationsTxtPath, 'w') as Writer:
            pass
        if self.populationFromLineEdit.text().isnumeric() and int(self.populationFromLineEdit.text()) > 0 and self.populationToLineEdit.text().isnumeric() and int(self.populationToLineEdit.text()) > 0:
            self.startProcess(sheet, startTime)

    def startProcess(self, sheet, startTime):
        self.fromPopulation = int(self.populationFromLineEdit.text())
        self.toPopulation = int(self.populationToLineEdit.text())
        countCities = 0
        self.workWithExcel(sheet, countCities)
        self.finishGenerating(startTime, countCities)

    def workWithExcel(self, sheet, countCities):
        for i in range(3, 17084):
            if sheet['A' + str(i)].value == None:
                continue
            population = sheet['C' + str(i)].value
            if population <= self.toPopulation and population >= self.fromPopulation:
                self.writePopulation(sheet, countCities, i)

    def writePopulation(self, sheet, countCities, i):
        countCities += 1
        with open(self.locationsTxtPath, 'a') as Writer:
            num1 = random.uniform(0.001, 0.002)
            if random.random() < 0.5:
                num1 *= -1   
            num2 = random.uniform(0.001, 0.002)
            if random.random() < 0.5:
                num2 *= -1    
            lat = round(sheet['D' + str(i)].value + num1, 5)
            lon = round(sheet['E' + str(i)].value + num2, 5)
            if os.path.getsize(self.locationsTxtPath) == 0:
                Writer.write(str(lat) + ',' + str(lon))
            else:
                Writer.write('\n' + str(lat) + ',' + str(lon))

    def finishGenerating(self, startTime, countCities):
        with open(self.locationsTxtPath) as Reader:
            lines = Reader.readlines()
        random.shuffle(lines)
        with open(self.locationsTxtPath, 'w') as Writer:
            Writer.writelines(lines)
        with open(self.locationsTxtPath, 'r') as Reader:
            data = Reader.read()
        with open(self.locationsTxtPath, 'w') as Writer:
            Writer.write(data[:-1])
        endTime = time.time()
        elapsedTime = endTime - startTime
        cities = countCities
        self.numCities = countCities
        fromPopulation = self.fromPopulation
        toPopulation = self.toPopulation
        self.clearGUI()
        self.processLogLocationsContent.setText("locations generated."+ '\nNumber of cities: ' + str(cities) + '.\nPopulation from: ' + str(fromPopulation) + ' to: ' + str(toPopulation) + '.' + "\nTime elapsed: " + '{:.2f}'.format(elapsedTime) + ' seconds.')
        self.clearGUILocationsButton.setDisabled(False)
        self.generateOrderButton.setDisabled(False)
        QApplication.processEvents()        # type: ignore

#Tab3 is a class that represents the third tab on the GUI, it handles the profit
class Tab3(QWidget):                        # type: ignore
    def __init__(self):
        super(Tab3, self).__init__()
        self.title = 'Profit'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.inputProfitSection()
        self.setupMainButtonsSection()
        self.setupProcessLogSection()
        self.sentencesPath = '.././' + '/data/sentences.txt'
        self.groups = []
        self.sentences = []
        self.sentence = ''

    def inputProfitSection(self):
        self.inputProfitLabel = QLabel('Input profit:', self)                       # type: ignore
        self.inputProfitLabel.adjustSize()
        self.inputProfitLabel.move(70, 40)
        self.inputProfitLineEdit = QLineEdit('', self)                              # type: ignore
        self.inputProfitLineEdit.adjustSize()
        self.inputProfitLineEdit.move(70, 70)

    def setupMainButtonsSection(self):
        self.GenerateSentencesButton = QPushButton('Generate\nSentences', self)     # type: ignore
        self.GenerateSentencesButton.clicked.connect(self.generateSentences)
        self.GenerateSentencesButton.setStyleSheet("background-color : green")
        self.GenerateSentencesButton.adjustSize()
        self.GenerateSentencesButton.move(95, 140)

        self.clearGUIprofitButton = QPushButton('Clear\nGUI', self)                 # type: ignore
        self.clearGUIprofitButton.clicked.connect(self.clearGUI)
        self.clearGUIprofitButton.adjustSize()
        self.clearGUIprofitButton.move(420, 275)

        self.exitprofitButton = QPushButton('Exit', self)                           # type: ignore
        self.exitprofitButton.clicked.connect(self.exitFunction)
        self.exitprofitButton.setStyleSheet("background-color : red")
        self.exitprofitButton.adjustSize()
        self.exitprofitButton.move(550, 280)

    def setupProcessLogSection(self):
        self.processLogprofitLabel = QLabel('Process log', self)                    # type: ignore
        self.processLogprofitLabel.setStyleSheet("background-color : yellow")
        self.processLogprofitLabel.adjustSize()
        self.processLogprofitLabel.move(490, 20)

        self.processLogprofitContent = QTextEdit('Don\'t be too dirty babe.', self) # type: ignore
        self.processLogprofitContent.adjustSize()
        self.processLogprofitContent.move(400, 50)

    #exit the application
    def exitFunction(self):
        QApplication.quit()                 # type: ignore

    def clearGUI(self):
        self.groups = []
        self.sentences = []
        self.sentence = ''
        self.inputProfitLineEdit.setText('')
        self.processLogprofitContent.setText('')

    def generateSentences(self):
        self.processLogprofitContent.setText('Process started. Please wait.')
        self.GenerateSentencesButton.setDisabled(True)
        self.clearGUIprofitButton.setDisabled(True)
        QApplication.processEvents()        # type: ignore
        self.groups = []
        self.sentences = []
        self.extractSentence()
        self.makeSentences("", self.groups)
        countGroups = 0
        self.processFiles(countGroups)
        self.processLogprofitContent.setText('Number of groups in sentence: ' + str(countGroups) + '\nNumber of sentences generated: ' + str(len(self.sentences)))
        self.GenerateSentencesButton.setDisabled(False)
        self.clearGUIprofitButton.setDisabled(False)
        QApplication.processEvents()        # type: ignore

    def processFiles(self, countGroups):
        for i in range(len(self.groups)):
            if isinstance(self.groups[i], list) == True:
                countGroups += 1
        with open('.././' + '/data/sentences.txt', 'w') as Writer:
            pass
        with open('.././' + '/data/sentences.txt', 'w') as Writer:
            for i in range(len(self.sentences)):
                if i != 0:
                    Writer.write('\n' + self.sentences[i])
                else:
                    Writer.write(self.sentences[i])

    def extractSentence(self):
        self.sentence = self.inputProfitLineEdit.text()
        flagGroup = False
        indexGroup = 0
        word = ''
        for i in range(0, len(self.sentence)):
            c = self.sentence[i]
            if (self.processCharacter(i)):
                continue
            word += c
        if word != '':
            if len(self.groups) == 0:
                self.groups.append([])
            self.groups[indexGroup].append(word)

    def processCharacter(self, c, i):
        if c == '{':
            if i != 0:
                if len(self.groups) == 0:
                    self.groups.append([])
                self.groups[indexGroup].append(word)
                indexGroup += 1
            self.groups.append([])
            flagGroup = True
            word = ''
            return True
        if c == '}' and flagGroup:
            self.groups[indexGroup].append(word)
            indexGroup += 1
            self.groups.append([])
            flagGroup = False
            word = ''
            return True
        if flagGroup == True and c == '|':
            self.groups[indexGroup].append(word)
            word = ''
            return True
        return False

    def makeSentences(self, w, groups):
        for x in groups[0]:
            if len(groups) > 1:
                self.makeSentences(w + str(x), groups[1:])
            else:
                self.sentences.append(w + str(x))

if __name__ == "__main__":
    app = QApplication([])      # type: ignore
    w = Window()
    app.exec_()
