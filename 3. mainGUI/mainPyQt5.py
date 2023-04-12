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
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#Window je glavna klasa koja predstavlja GUI. Sadrzi tabove, a svaki tab je napravljen kao zasebna klasa
class Window(QTabWidget):
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
      self.tab4 = Tab4()
      self.addTab(self.tab1, 'Generator')
      self.addTab(self.tab2, 'Trades')
      self.addTab(self.tab3, 'Profit')
      self.addTab(self.tab4, 'Discord')

      self.show()

#Tab1 je klasa koja predstavlja prvi tab GUI-a, najkompleksnija je
class Tab1(QWidget):
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
        
        self.clearGUIButton = QPushButton('Clear\nGUI', self)
        self.clearGUIButton.clicked.connect(self.clearGUI)
        self.clearGUIButton.adjustSize()
        self.clearGUIButton.move(330, 20)

        self.RedoButton = QPushButton('Redo', self)
        self.RedoButton.clicked.connect(self.redoWrite)
        self.RedoButton.adjustSize()
        self.RedoButton.move(330, 80)

        self.usernameLabel = QLabel('Username:', self)
        self.usernameLabel.adjustSize()
        self.usernameLabel.move(20, 20)
        self.usernameLineEdit = QLineEdit('', self)
        self.usernameLineEdit.adjustSize()
        self.usernameLineEdit.move(135, 18)

        self.numTokensLabel = QLabel('Tokens:', self)
        self.numTokensLabel.adjustSize()
        self.numTokensLabel.move(20, 50)
        self.numTokensLineEdit = QLineEdit('30', self)
        self.numTokensLineEdit.adjustSize()
        self.numTokensLineEdit.move(135, 48)

        self.numImagesPerFolderLabel = QLabel('Images per folder:', self)
        self.numImagesPerFolderLabel.adjustSize()
        self.numImagesPerFolderLabel.move(20, 80)
        self.numImagesPerFolderLineEdit = QLineEdit('5', self)
        self.numImagesPerFolderLineEdit.adjustSize()
        self.numImagesPerFolderLineEdit.move(135, 78)

        self.methodsLabel = QLabel('Choose method:', self)
        self.methodsLabel.adjustSize()
        self.methodsLabel.move(20, 230)

        self.bioRandomBox = QRadioButton ("Bio Promotion --> Random", self)
        self.bioRandomBox.adjustSize()
        self.bioRandomBox.move(50, 280)

        self.bioOneBox = QRadioButton ("Bio Promotion --> One trader", self)
        self.bioOneBox.adjustSize()
        self.bioOneBox.move(50, 310)

        self.watermarkRandomBox = QRadioButton ("Watermark Promotion --> Random", self)
        self.watermarkRandomBox.adjustSize()
        self.watermarkRandomBox.move(50, 340)

        self.watermarkOneBox = QRadioButton ("Watermark Promotion --> One trader", self)
        self.watermarkOneBox.adjustSize()
        self.watermarkOneBox.move(50, 370)

        self.watermarkOneBackupBox = QRadioButton ("Watermark Promotion --> One trader + Backup", self)
        self.watermarkOneBackupBox.adjustSize()
        self.watermarkOneBackupBox.move(50, 400)

        self.watermarkBioRandomBox = QRadioButton ("Watermark + Bio --> Random", self)
        self.watermarkBioRandomBox.adjustSize()
        self.watermarkBioRandomBox.move(50, 430)

        self.watermarkBioOneBox = QRadioButton ("Watermark + Bio --> One trader", self)
        self.watermarkBioOneBox.adjustSize()
        self.watermarkBioOneBox.move(50, 460)

        self.watermarkBioOneBackupBox = QRadioButton ("Watermark + Bio --> One trader + Backup", self)
        self.watermarkBioOneBackupBox.adjustSize()
        self.watermarkBioOneBackupBox.move(50, 490)

        self.justRandomBox = QRadioButton ("No Promotion --> Random", self)
        self.justRandomBox.adjustSize()
        self.justRandomBox.move(50, 520)

        self.justOneBox = QRadioButton ("No Promotion --> One trader", self)
        self.justOneBox.adjustSize()
        self.justOneBox.move(50, 550)

        self.justOneBackupBox = QRadioButton ("No Promotion --> One trader + Backup", self)
        self.justOneBackupBox.adjustSize()
        self.justOneBackupBox.move(50, 580)

        self.selectAllFilesButton = QPushButton('Select All', self)
        self.selectAllFilesButton.clicked.connect(self.selectAllFilesFunction)
        self.selectAllFilesButton.adjustSize()
        self.selectAllFilesButton.move(350, 250)

        self.biosCheckBox = QCheckBox("Bios", self)
        self.biosCheckBox.adjustSize()
        self.biosCheckBox.move(370, 290)

        self.jobsCheckBox = QCheckBox("Jobs", self)
        self.jobsCheckBox.adjustSize()
        self.jobsCheckBox.move(370, 320)

        self.namesCheckBox = QCheckBox("Names", self)
        self.namesCheckBox.adjustSize()
        self.namesCheckBox.move(370, 350)

        self.emailsCheckBox = QCheckBox("Emails", self)
        self.emailsCheckBox.adjustSize()
        self.emailsCheckBox.move(370, 380)

        self.tradesCheckBox = QCheckBox("Trades", self)
        self.tradesCheckBox.adjustSize()
        self.tradesCheckBox.move(370, 410)

        self.setImageAsLabel = QLabel('Set watermarked\n   Image as:', self)
        self.setImageAsLabel.adjustSize()
        self.setImageAsLabel.move(490, 250)

        self.selectAllPrefixesButton = QPushButton('Select All', self)
        self.selectAllPrefixesButton.clicked.connect(self.selectAllPrefixesFunction)
        self.selectAllPrefixesButton.adjustSize()
        self.selectAllPrefixesButton.move(20, 110)

        self.prefix1 = QCheckBox("trade ", self)
        self.prefix1.adjustSize()
        self.prefix1.move(20, 150)

        self.prefix2 = QCheckBox("trade - ", self)
        self.prefix2.adjustSize()
        self.prefix2.move(20, 180)

        self.prefix3 = QCheckBox("trade: ", self)
        self.prefix3.adjustSize()
        self.prefix3.move(100, 150)

        self.prefix4 = QCheckBox("$trade$ ", self)
        self.prefix4.adjustSize()
        self.prefix4.move(100, 180)

        self.FirstImageBox = QCheckBox("First", self)
        self.FirstImageBox.adjustSize()
        self.FirstImageBox.move(510, 300)

        self.SecondImageBox = QCheckBox("Second", self)
        self.SecondImageBox.adjustSize()
        self.SecondImageBox.move(510, 330)

        self.ThirdImageBox = QCheckBox("Third", self)
        self.ThirdImageBox.adjustSize()
        self.ThirdImageBox.move(510, 360)
        
        self.FourthImageBox = QCheckBox("Fourth", self)
        self.FourthImageBox.adjustSize()
        self.FourthImageBox.move(510, 390)

        self.FifthImageBox = QCheckBox("Fifth", self)
        self.FifthImageBox.adjustSize()
        self.FifthImageBox.move(510, 420)

        self.processLogLabel = QLabel('Process Log', self)
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(420, 480)
        self.processLogLabel.setStyleSheet("background-color : yellow")
        self.processLogContent = QTextEdit('Good day my friend!', self)
        self.processLogContent.adjustSize()
        self.processLogContent.move(330, 510)

        self.generateButton = QPushButton('Generate', self)
        self.generateButton.clicked.connect(self.generateFunction)
        self.generateButton.setStyleSheet("background-color : green")
        self.generateButton.adjustSize()
        self.generateButton.move(100, 650)

        self.clearErrorsAndResultsButton = QPushButton('Clear errors\nand results', self)
        self.clearErrorsAndResultsButton.clicked.connect(self.clearErrorsAndResults)
        self.clearErrorsAndResultsButton.adjustSize()
        self.clearErrorsAndResultsButton.move(650, 500)

        self.clearFinalButton = QPushButton('Clear\nfinal folder', self)
        self.clearFinalButton.clicked.connect(self.clearFinalFolder)
        self.clearFinalButton.adjustSize()
        self.clearFinalButton.move(650, 550)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.exitFunction)
        self.exitButton.setStyleSheet("background-color : red")
        self.exitButton.adjustSize()
        self.exitButton.move(650, 650)

        #putanje koje se koriste za rad klase Tab1, sve putanje se nalaze negde u folderu Traffic
        #sve putanje sem watermarkSnapPath su fiksne,
        self.trafficPath = '.././'
        self.ordersPath = self.trafficPath + '/orders'
        self.finalPath = self.trafficPath + '/final'
        self.dataPath = self.trafficPath + '/data'
        self.morePath = self.trafficPath + '/more'
        self.completedPath = self.morePath + '/completed'
        self.tradersImagesPath = self.dataPath + '/tradersImages'
        self.watermarkTemplatePath = self.dataPath + '/watermarkTemplate.png'
        #watermarkSnapPath se menja u zavisnosti od username-a snepa, zato je nedefinisana u startu
        self.watermarkSnapPath = ''
        #promenljive koje se koriste za rad klase Tab1
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.indexImageForWatermark = 0
        self.username = ''
        self.traderUserImagesPath = ''
        self.imageForWatermarkPaths = []
        self.dataNames = ['NAMES.txt', 'TRADES.txt', 'EMAILS.txt', 'JOBS.txt', 'BIOS.txt']
        #dataNamesFlags sluzi za laksu proveru fajlova dataNames,
        #u smislu lakseg prepoznavanja koji fajl treba da se obradjuje ili provera
        self.dataNamesFlags = [False, False, False, False, False]
        #kad se klikne na dugme redo da vrati sve od pre zapamceno
        self.redoUsername = ''
        self.redoTokens = 30
        self.redoImagesPerFolder = 5
        self.redoMethod = 0
        self.redoBios = 0
        self.redoJobs = 0
        self.redoNames = 0
        self.redoEmails = 0
        self.redotrades = 0
        self.redoFirst = 0
        self.redoSecond = 0
        self.redoThird = 0
        self.redoFourth = 0
        self.redoFifth = 0
        
        self.function()

    def function(self):
        self.processLogContent.setText('Uspeo')
        QtWidgets.qApp.processEvents()

    #izlaz iz aplikacije
    def exitFunction(self):
        QApplication.quit()

    #brise sve sto je ispisano ili oznaceno na GUI-u kako bi bilo preglednije
    def clearGUI(self):
        #prvo se vrednosti u programu postavljaju na difoltne
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.indexImageForWatermark = 1
        self.username = ''
        self.traderUserImagesPath = ''
        self.watermarkSnapPath = ''
        self.imageForWatermarkPaths = []
        self.dataNamesFlags = [False, False, False, False, False]
        #potom se i vizualno GUI brise kako bi bio pregledniji
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
        self.tradesCheckBox.setChecked(False)

    #ukoliko postoji, brise sav sadrzaj iz foldera final
    def clearFinalFolder(self):
        for fileName in os.listdir(self.finalPath):
            filePath = self.finalPath + '/' + fileName
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        self.processLogContent.setText('Folder final is empty.')
        QApplication.processEvents()
        self.processLogContent.adjustSize()

    #brise sav sadrzaj iz foldera completed i errors.txt
    def clearErrorsAndResults(self):
        with open(self.morePath + '/errors.txt', 'w') as Writer:
            pass
        shutil.rmtree(self.completedPath)
        os.mkdir(self.completedPath)
        self.processLogContent.setText('File \'errors.txt\' and folder \'completed\' are empty.')
        QApplication.processEvents()
        self.processLogContent.adjustSize()
            
    def redoRead(self):
        self.redoUsername = self.username
        self.redoTokens = self.numTokens
        self.redoImagesPerFolder = self.numImagesPerFolder

        if self.bioRandomBox.isChecked():
            self.redoMethod = 1
        if self.bioOneBox.isChecked():
            self.redoMethod = 2
        if self.watermarkRandomBox.isChecked():
            self.redoMethod = 3
        if self.watermarkOneBox.isChecked():
            self.redoMethod = 4
        if self.watermarkOneBackupBox.isChecked():
            self.redoMethod = 5
        if self.watermarkBioRandomBox.isChecked():
            self.redoMethod = 6
        if self.watermarkBioOneBox.isChecked():
            self.redoMethod = 7
        if self.watermarkBioOneBackupBox.isChecked():
            self.redoMethod = 8
        if self.justRandomBox.isChecked():
            self.redoMethod = 9
        if self.justOneBox.isChecked():
            self.redoMethod = 10
        if self.justOneBackupBox.isChecked():
            self.redoMethod = 11

        if self.biosCheckBox.isChecked():
            self.redoBios = 1
        else:
            self.redoBios = 0
        if self.jobsCheckBox.isChecked():
            self.redoJobs = 1
        else:
            self.redoJobs = 0
        if self.namesCheckBox.isChecked():
            self.redoNames = 1
        else:
            self.redoNames = 0
        if self.emailsCheckBox.isChecked():
            self.redoEmails = 1
        else:
            self.redoEmails = 0
        if self.tradesCheckBox.isChecked():
            self.redotrades = 1
        else:
            self.redotrades = 0

        if self.FirstImageBox.isChecked():
            self.redoFirst = 1
        else:
            self.redoFirst = 0
        if self.SecondImageBox.isChecked():
            self.redoSecond = 1
        else:
            self.redoSecond = 0
        if self.ThirdImageBox.isChecked():
            self.redoThird = 1
        else:
            self.redoThird = 0
        if self.FourthImageBox.isChecked():
            self.redoFourth = 1
        else:
            self.redoFourth = 0
        if self.FifthImageBox.isChecked():
            self.redoFifth = 1   
        else:
            self.redoFifth = 0

    def redoWrite(self):
        self.numTokensLineEdit.setText(str(self.redoTokens))
        self.numImagesPerFolderLineEdit.setText(str(self.redoImagesPerFolder))
        self.numTokens = self.redoTokens
        self.numImagesPerFolder = self.redoImagesPerFolder

        if self.redoFirst == 1:
            self.FirstImageBox.setChecked(True)
        else:
            self.FirstImageBox.setChecked(False)
        if self.redoSecond == 1:
            self.SecondImageBox.setChecked(True)
        else:
            self.SecondImageBox.setChecked(False)
        if self.redoThird == 1:
            self.ThirdImageBox.setChecked(True)
        else:
            self.ThirdImageBox.setChecked(False)
        if self.redoFourth == 1:
            self.FourthImageBox.setChecked(True)
        else:
            self.FourthImageBox.setChecked(False)
        if self.redoFifth == 1:
            self.FifthImageBox.setChecked(True)
        else:
            self.FifthImageBox.setChecked(False)

        if self.redoBios == 1:
            self.biosCheckBox.setChecked(True)
        else:
            self.biosCheckBox.setChecked(False)
        if self.redoJobs == 1:
            self.jobsCheckBox.setChecked(True)
        else:
            self.jobsCheckBox.setChecked(False)
        if self.redoNames == 1:
            self.namesCheckBox.setChecked(True)
        else:
            self.namesCheckBox.setChecked(False)
        if self.redoEmails == 1:
            self.emailsCheckBox.setChecked(True)
        else:
            self.emailsCheckBox.setChecked(False)
        if self.redotrades == 1:
            self.tradesCheckBox.setChecked(True)
        else:
            self.tradesCheckBox.setChecked(False)

        if self.redoMethod == 1:
            self.bioRandomBox.setChecked(True)
        if self.redoMethod == 2:
            self.bioOneBox.setChecked(True)
        if self.redoMethod == 3:
            self.watermarkRandomBox.setChecked(True)
        if self.redoMethod == 4:
            self.watermarkOneBox.setChecked(True)
        if self.redoMethod == 5:
            self.watermarkOneBackupBox.setChecked(True)
        if self.redoMethod == 6:
            self.watermarkBioRandomBox.setChecked(True)
        if self.redoMethod == 7:
            self.watermarkBioOneBox.setChecked(True)
        if self.redoMethod == 8:
            self.watermarkBioOneBackupBox.setChecked(True)
        if self.redoMethod == 9:
            self.justRandomBox.setChecked(True)
        if self.redoMethod == 10:
            self.justOneBox.setChecked(True)
        if self.redoMethod == 11:
            self.justOneBackupBox.setChecked(True)


    #kiktanjem dugmeta Select All, biraju se svi fajlovi iz foldera data (dataNames fajlovi) za extractData()
    def selectAllFilesFunction(self):
        if self.biosCheckBox.isChecked() and self.namesCheckBox.isChecked() and self.tradesCheckBox.isChecked() and self.emailsCheckBox.isChecked() and self.jobsCheckBox.isChecked():
            self.biosCheckBox.setChecked(False)
            self.namesCheckBox.setChecked(False)
            self.tradesCheckBox.setChecked(False)
            self.emailsCheckBox.setChecked(False)
            self.jobsCheckBox.setChecked(False)
            self.dataNamesFlags = [False, False, False, False, False]
        else:
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.tradesCheckBox.setChecked(True)
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
            self.tradesCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]

    #podesava u listi dataNamesFlags koji fajlovi iz dataNames treba da se obrade
    def setDataFlags(self):
        if self.namesCheckBox.isChecked():
            self.dataNamesFlags[0] = True
        if self.tradesCheckBox.isChecked():
            self.dataNamesFlags[1] = True
        if self.emailsCheckBox.isChecked():
            self.dataNamesFlags[2] = True
        if self.jobsCheckBox.isChecked():
            self.dataNamesFlags[3] = True
        if self.biosCheckBox.isChecked():
            self.dataNamesFlags[4] = True

    #odredjuje se koj je redni broj slike u svakom folderu slika akaunteva,
    #samo ce slika sa tim rednim brojem u svakom folderu slika akaunteva biti watermarkovana
    def setIndexImageForWatermark(self):
        if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.justOneBackupBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBox.isChecked():
            if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
                return True
            else:
                self.processLogContent.setText('You can\'t use bio method with checking which image in folders you want to watermark. Uncheck it and try again.')
                QApplication.processEvents()
                self.indexImageForWatermark = 0
                return False
        if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
                self.processLogContent.setText('You can\'t use watermark method without checking which image in folders you want to watermark. Check exactly 1 and try again.')
                QApplication.processEvents()
                self.indexImageForWatermark = 0
                return False
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
            else:
                self.processLogContent.setText('You can\'t use watermark method with checking more than 1 images per folder to watermark.  Check exactly 1 and try again.')
                QApplication.processEvents()
                self.indexImageForWatermark = 0
                return False

    def readFromGui(self):
        self.username = self.usernameLineEdit.text()
        self.numTokens = int(self.numTokensLineEdit.text())
        self.numImagesPerFolder = int(self.numImagesPerFolderLineEdit.text())
        self.setDataFlags()
        checkData = self.checkEnoughData() and self.setIndexImageForWatermark()
        self.redoRead()
        return checkData

    #glavna funkcija ovog GUI-a, pokrece je dugme Generate i sluzi da obradi trenutno izabranu porudzbinu
    def generateFunction(self):
        startTime = time.time()
        #ukoliko ima potrebnih podataka za obradu trenutne porudzbine, obrada pocinje
        if self.readFromGui() == True:
            self.processLogContent.setText('Process started. Please wait.')
            self.clearGUIButton.setDisabled(True)
            self.selectAllFilesButton.setDisabled(True)
            self.clearErrorsAndResultsButton.setDisabled(True)
            self.clearFinalButton.setDisabled(True)
            self.generateButton.setDisabled(True)
            QApplication.processEvents()
            #prave se potrebni folderi u folderu final
            self.makeUsernameFolders()
            #izvlace se izabrani fajlovi iz dataNames liste i prebacuju se u folder final
            self.extractData()
            #ukoliko je izabrana 'Random' metoda odnosno metoda koja izvlaci slike iz razlicitih trejdera,
            #onda se poziva metoda extractRandomtraders()
            if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
                self.extractRandomtraders()
            #ukoliko je izabrana 'One' metoda odnosno metoda koja izvlaci slike samo od jednog trejdera,
            #onda se poziva metoda extractOnetrader()
            elif self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
                self.extractOnetrader()
            #slike se kropuju (po potrebi flipuju), preimenjuju se i ukoliko se radi watermark
            #pamte se slike koje treba da se watermarkuju
            self.modifyImages()
            #ukoliko je izabrana neka bio metoda, zove se funkcija callBioMethod()
            if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                self.callBioMethod()
            #ukoliko je izabrana neka watermark metoda, zove se funkcija callWatermarkMethod()
            if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                self.callWatermarkMethod()
            endTime = time.time()
            elapsedTime = endTime - startTime
            #porudzbina je zavrsena pa se GUI cisti
            method = self.findMethod()
            self.clearGUI()
            self.clearGUIButton.setDisabled(False)
            self.selectAllFilesButton.setDisabled(False)
            self.clearErrorsAndResultsButton.setDisabled(False)
            self.clearFinalButton.setDisabled(False)
            self.generateButton.setDisabled(False)
            self.processLogContent.setText('Order finished.\n' + '\nSnapchat username: ' + self.redoUsername + '\nTokens created: ' + str(self.redoTokens) + '\nMethod: ' + method + '\nTime elapsed: ' + '{:.2f}'.format(elapsedTime) + ' seconds.')
            QApplication.processEvents()
            self.processLogContent.adjustSize()
            with open(self.completedPath + '/' + self.redoUsername + '.txt', 'w') as Writer:
                Writer.write(self.processLogContent.toPlainText())

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

    #pre pocetka obrade porudzbine, treba proveriti da li su ispunjeni uslovi za obradu
    def checkEnoughData(self):
        #prvo se proverava da li je GUI adekvatno popunjen
        checkGUILineEdits = self.usernameLineEdit.text() != '' and self.numTokensLineEdit.text() != '' and self.numImagesPerFolderLineEdit.text() != ''
        checkGUIMethods = self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBackupBox.isChecked()
        #ukoliko je bar 1 uslov neispunjen, porudzbina se ne moze trenutno obraditi, potrebno je popraviti gresku
        checkGUI = checkGUILineEdits and checkGUIMethods
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
            QApplication.processEvents()
            self.processLogContent.adjustSize()
        #ukoliko nije doslo do greske u popunjavanju GUI-a
        else:
            try:
                self.numImagesPerFolder = int(self.numImagesPerFolderLineEdit.text())
                self.numTokens = int(self.numTokensLineEdit.text())
                i = 0
                #provera za fajlove iz dataNames da li imaju dovoljno linija za obradu trenutne porudzbine
                for fileName in self.dataNames:
                    #provera se vrsi samo ako je trenutni fajl izabran za ekstrakovanje
                    if self.dataNamesFlags[i] == True:
                        path = self.dataPath + '/' + fileName
                        with open(path, 'r') as Reader:
                            lines = Reader.readlines()
                        #ukoliko nema dovoljno linija za trenutnu porudzbinu, to se belezi u errors.txt u folderu orders
                        if len(lines) < self.numTokens:
                            errorMsg = "File " + fileName + " has not enough lines for creating " + str(self.numTokens) + " tokens for customer " + self.customer + " with his username " + self.username
                            with open(self.morePath + '/errors.txt', 'a') as Writer:
                                if os.path.getsize(self.morePath + '/errors.txt') == 0:
                                    Writer.write(errorMsg)
                                else:
                                    Writer.write('\n' + errorMsg)
                            print(errorMsg)
                            #baca se izuzetak kako bi se preskocilo dalje ispitivanje
                            raise Exception(errorMsg)
                        i += 1
                #ukoliko je izabrana neka 'Random' metoda, vrsi se provera da li ima dovoljno slika
                pathsForDelete = []
                if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
                    acc = 0
                    for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                        path = self.tradersImagesPath + '/' + fileName
                        if len(os.listdir(path)) < 5:
                            pathsForDelete.append(path)
                        else:
                            acc += len(os.listdir(path))//self.numImagesPerFolder
                    #ukoliko nema dovoljno slika, baca se izuzetak
                    for path in pathsForDelete:
                        shutil.rmtree(path)
                    if acc < self.numTokens:
                        self.notEnoughImages()
                    else:
                        #ukoliko ima dovoljno slika, sva provera je zavrsena
                        return True
                #ukoliko je izabrana neka 'One' ili 'OneBackup' metoda, vrsi se provera da li ima dovoljno slika
                elif self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
                    for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                        path = self.tradersImagesPath + '/' + fileName
                        if (self.watermarkOneBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.justOneBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder:
                            self.traderUserImagesPath = path
                            return True
                        elif (self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder + self.numTokens:
                            self.traderUserImagesPath = path
                            return True
                    #ukoliko nema dovoljno slika, baca se izuzetak
                    self.notEnoughImages()
            #ukoliko je izuzetak bacen, hvata se ovde, program javlja gresku i spreman je za ponovni pokusaj
            except Exception as e:
                    print('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                    self.processLogContent.setText('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                    QApplication.processEvents()
                    self.processLogContent.adjustSize()
                    return False

    #funkcija koja se poziva ukoliko nema dovoljno slika za obradu porudzbine
    def notEnoughImages(self):
        errorMsg = "Not enough images for creating " + str(self.numTokens) + " for username " + self.username
        with open(self.morePath + '/errors.txt', 'a') as Writer:
            if os.path.getsize(self.morePath + '/errors.txt') == 0:
                Writer.write(errorMsg)
            else:
                Writer.write("\n" + errorMsg)
        raise Exception(errorMsg)

    #prave se se svi potrebni folderi trenutne porudzbine u final folderu
    def makeUsernameFolders(self):
        if os.path.isdir(self.finalPath + '/' + self.username) == True:
            shutil.rmtree(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username + '/' + 'images')
        for i in range(self.numTokens):
            os.mkdir(self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(i + 1))
        #ukoliko je izabrana 'Backup' metoda, treba napraviti dodatne foldere
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            if os.path.isdir(self.finalPath + '/' + self.username + 'BACKUP') == True:
                shutil.rmtree(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP' + '/' + 'images')

    #izvlaci linije iz izabranih dataNames fajlova i prebacuje ih u final folder
    def extractData(self):
        otherLines = []
        r = 0
        for fileName in self.dataNames:
            #ukoliko trenutni fajl treba da se obradi
            if self.dataNamesFlags[r] == True:
                name = fileName[0] + fileName[1:].lower()
                with open(self.dataPath + '/' + fileName, "r") as Reader:
                    with open(self.finalPath + '/' + self.username + '/' + name, "w") as Writer:
                        for i in range(self.numTokens - 1):
                            Writer.write(Reader.readline())
                        Writer.write(Reader.readline().strip('\n'))
                    otherLines = Reader.readlines()
                #ispisuje preostale linije u fajlove
                with open(self.dataPath + '/' + fileName, "w") as Writer:
                    Writer.writelines(otherLines)
            r += 1

    #izvlaci slike iz tradersImages foldera, ali samo od jednog trejdera i prebacuje ih u final folder
    def extractOnetrader(self):
        oldPath = self.traderUserImagesPath
        for countTokens in range(self.numTokens):
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
        #ukoliko je izabrana 'Backup' metoda, treba izvuci slike i za njih
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            for countTokens in range(self.numTokens):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + 'BACKUP/' + 'images'
                shutil.move(oldPath + '/' + firstImageInFile, newPath)

    #izvlaci slike iz tradersImages foldera, ali vise trejdera i prebacuje ih u final folder
    def extractRandomtraders(self):
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
            while len(os.listdir(oldPath)) < self.numImagesPerFolder:
                if countUsers >= numUsers:
                    countUsers = 0
                if BORING[countUsers] == False:
                    print('U folderu ', dataUserNames[countUsers],' nema dovoljno slika za akaunt.')
                    BORING[countUsers] = True
                countUsers += 1
                if countUsers >= numUsers:
                    countUsers = 0
                oldPath = self.tradersImagesPath + '/' + dataUserNames[countUsers]
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
            countUsers += 1

    #vrsi promenu dimenzija slika iz final foldera (po potrebi mogu da se flipuju) i preimenuju se
    def modifyImages(self):
        for token in range(self.numTokens):
            folderPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(token + 1)
            num = random.randint(1000, 10000)
            for i, fileName in enumerate(os.listdir(folderPath)):
                num = num + 1
                oldImagePath = folderPath + "/" + fileName
                newImagePath = folderPath + '/' + 'IMG_' + str(num) + ".jpg"
                os.rename(oldImagePath, newImagePath)
                image = Image.open(newImagePath)
                if i == (self.indexImageForWatermark - 1) and (self.watermarkOneBackupBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked()):
                    self.imageForWatermarkPaths.append(newImagePath)
                cropedImage = image.resize((1125, 1364))
                #newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                cropedImage.save(newImagePath)
                cropedImage.close()
        #ukoliko je izabrana 'Backup' metoda, treba modifikovati i takve slike
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
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
                    #newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                    cropedImage.save(newImagePath)
                    cropedImage.close()
                else:
                    break

    #funkcija koja se zove za sve vrste bio metoda
    def callBioMethod(self):
        #trazi se file Bios.txt u final folderu trenutne porudzbine kako bi mogao da se apenduje snep u biografiju
        bioPath = self.finalPath + '/' + self.username + '/' + 'Bios.txt'
        snaps = [r'\nS.C: ', r'\nS.C - ', r'\nS.C ']
        h = 0
        lines = []
        #username-u se razdvajaju slova tako da iz sara555 prelazi u s a r a 5 5 5
        s = ""
        for char in self.username:
            s = s + char + ' '
        trickUsername = s.rstrip(' ')
        lines = ""
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            numLines = len(Reader.readlines())
        #vrsi se apendovanje snepa u biografije liniju po liniju
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            for i in range(numLines - 1):
                lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername + '\n'
                h += 1
                if h == 3:
                    h = 0
            lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername
        with open(bioPath, "w") as Writer:
            Writer.write(lines)
    
    #pravi username template za watermark
    def makeUsernameWatermark(self):
        #templejt se pravi samo ukoliko on vec ne postoji
        #na sliku watermarkTemplatePath koja predstavlja crni pravougaonik,
        #vrsi se lepljenje teksta koji prestavlja username snepa
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
        #radi se watermark onih slika koje su izdvojene za watermark
        #lepi se template username-a na sliku koja je predvidjena za watermark
        for inputImagePath in self.imageForWatermarkPaths:
            height = 0 + random.randint(-100, 100)
            originalImage = Image.open(inputImagePath)
            originalWidth, originalHeight = originalImage.size
            watermarkImage = Image.open(self.watermarkSnapPath).convert("RGBA")
            transparent = Image.new('RGBA', (originalWidth, originalHeight), (0,0,0,0))
            transparent.paste(originalImage, (0,0))
            transparent.paste(watermarkImage, (width, height), mask=watermarkImage)
            transparent.save(inputImagePath, format="png")
        #ukoliko je izabrana i opcija za backup, te slike takodje treba da se watermarkuju, sve slike u tom folderu
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

    #funkcija koja se zove za sve vrste watermark metoda
    def callWatermarkMethod(self):
        self.watermarkSnapPath = self.dataPath + '/usernameTemplates/' + self.username + '.png'
        self.makeUsernameWatermark()
        self.watermarkImages()

    #funkcija za testiranje metoda
    def test(self):
        if self.getCustomer() == True:
            self.numImagesPerFolder = 5
            self.numTokensLineEdit.setText(str(self.numTokens))
            self.numImagesPerFolderLineEdit.setText(str(self.numImagesPerFolder))
            self.bioRandomBox.setChecked(True)
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.tradesCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]
            self.generateFunction()

#Tab2 je klasa koja predstavlja drugi tab na GUI-u, obradjuje lokacije
class Tab2(QWidget):
    def __init__(self):
        super(Tab2, self).__init__()
        self.title = 'trades'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.populationFromLabel = QLabel('From:', self)
        self.populationFromLabel.adjustSize()
        self.populationFromLabel.move(70, 20)
        self.populationFromLineEdit = QLineEdit('', self)
        self.populationFromLineEdit.adjustSize()
        self.populationFromLineEdit.move(20, 50)

        self.populationToLabel = QLabel('To:', self)
        self.populationToLabel.adjustSize()
        self.populationToLabel.move(260, 20)
        self.populationToLineEdit = QLineEdit('', self)
        self.populationToLineEdit.adjustSize()
        self.populationToLineEdit.move(200, 50)

        self.GeneratetradesButton = QPushButton('Generate\ntrades', self)
        self.GeneratetradesButton.clicked.connect(self.generatetrades)
        self.GeneratetradesButton.setStyleSheet("background-color : green")
        self.GeneratetradesButton.adjustSize()
        self.GeneratetradesButton.move(130, 100)

        self.clearGUItradesButton = QPushButton('Clear\nGUI', self)
        self.clearGUItradesButton.clicked.connect(self.clearGUI)
        self.clearGUItradesButton.adjustSize()
        self.clearGUItradesButton.move(420, 275)

        self.exittradesButton = QPushButton('Exit', self)
        self.exittradesButton.clicked.connect(self.exitFunction)
        self.exittradesButton.setStyleSheet("background-color : red")
        self.exittradesButton.adjustSize()
        self.exittradesButton.move(550, 280)

        self.processLogtradesLabel = QLabel('Process log', self)
        self.processLogtradesLabel.setStyleSheet("background-color : yellow")
        self.processLogtradesLabel.adjustSize()
        self.processLogtradesLabel.move(490, 20)

        self.processLogtradesContent = QTextEdit('Nice to see you baby.', self)
        self.processLogtradesContent.adjustSize()
        self.processLogtradesContent.move(400, 50)

        self.fromPopulation = 0
        self.toPopulation = 0
        self.numCities = 0

        self.tradesXlsxPath = '.././' + '/data/trades.xlsx'
        self.tradesTxtPath = '.././' + '/data/trades.txt'

    #izlaz iz aplikacije
    def exitFunction(self):
        QApplication.quit()

    def clearGUI(self):
        self.fromPopulation = 0
        self.toPopulation = 0
        self.numCities = 0
        self.populationFromLineEdit.setText('')
        self.populationToLineEdit.setText('')
        self.processLogtradesContent.setText('')

    def generatetrades(self):
        workbook = openpyxl.load_workbook(self.tradesXlsxPath)
        sheet = workbook.get_sheet_by_name('Sheet2')
        startTime = time.time()
        self.processLogtradesContent.setText('Generate started. Please wait.')
        self.clearGUItradesButton.setDisabled(True)
        self.GeneratetradesButton.setDisabled(True)
        QApplication.processEvents()
        with open(self.tradesTxtPath, 'w') as Writer:
            pass
        if self.populationFromLineEdit.text().isnumeric() and int(self.populationFromLineEdit.text()) > 0 and self.populationToLineEdit.text().isnumeric() and int(self.populationToLineEdit.text()) > 0:
            self.fromPopulation = int(self.populationFromLineEdit.text())
            self.toPopulation = int(self.populationToLineEdit.text())
            countCities = 0
            for i in range(3, 17084):
                if sheet['A' + str(i)].value == None:
                    continue
                population = sheet['C' + str(i)].value
                if population <= self.toPopulation and population >= self.fromPopulation:
                    countCities += 1
                    with open(self.tradesTxtPath, 'a') as Writer:
                        num1 = random.uniform(0.001, 0.002)
                        if random.random() < 0.5:
                            num1 *= -1   
                        num2 = random.uniform(0.001, 0.002)
                        if random.random() < 0.5:
                            num2 *= -1    
                        lat = round(sheet['D' + str(i)].value + num1, 5)
                        lon = round(sheet['E' + str(i)].value + num2, 5)
                        if os.path.getsize(self.tradesTxtPath) == 0:
                            Writer.write(str(lat) + ',' + str(lon))
                        else:
                            Writer.write('\n' + str(lat) + ',' + str(lon))
            with open(self.tradesTxtPath) as Reader:
                lines = Reader.readlines()
            random.shuffle(lines)
            with open(self.tradesTxtPath, 'w') as Writer:
                Writer.writelines(lines)
            with open(self.tradesTxtPath, 'r') as Reader:
                data = Reader.read()
            with open(self.tradesTxtPath, 'w') as Writer:
                Writer.write(data[:-1])
            endTime = time.time()
            elapsedTime = endTime - startTime
            cities = countCities
            self.numCities = countCities
            fromPopulation = self.fromPopulation
            toPopulation = self.toPopulation
            self.clearGUI()
            self.processLogtradesContent.setText("trades generated."+ '\nNumber of cities: ' + str(cities) + '.\nPopulation from: ' + str(fromPopulation) + ' to: ' + str(toPopulation) + '.' + "\nTime elapsed: " + '{:.2f}'.format(elapsedTime) + ' seconds.')
            self.clearGUItradesButton.setDisabled(False)
            self.GeneratetradesButton.setDisabled(False)
            QApplication.processEvents()

#Tab3 je klasa koja predstavlja treci tab na GUI-u, obradjuje profit
class Tab3(QWidget):
    def __init__(self):
        super(Tab3, self).__init__()
        self.title = 'profit'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.inputprofitLabel = QLabel('Input profit:', self)
        self.inputprofitLabel.adjustSize()
        self.inputprofitLabel.move(70, 40)
        self.inputprofitLineEdit = QLineEdit('', self)
        self.inputprofitLineEdit.adjustSize()
        self.inputprofitLineEdit.move(70, 70)

        self.GenerateSentencesButton = QPushButton('Generate\nSentences', self)
        self.GenerateSentencesButton.clicked.connect(self.generateSentences)
        self.GenerateSentencesButton.setStyleSheet("background-color : green")
        self.GenerateSentencesButton.adjustSize()
        self.GenerateSentencesButton.move(95, 140)

        self.clearGUIprofitButton = QPushButton('Clear\nGUI', self)
        self.clearGUIprofitButton.clicked.connect(self.clearGUI)
        self.clearGUIprofitButton.adjustSize()
        self.clearGUIprofitButton.move(420, 275)

        self.exitprofitButton = QPushButton('Exit', self)
        self.exitprofitButton.clicked.connect(self.exitFunction)
        self.exitprofitButton.setStyleSheet("background-color : red")
        self.exitprofitButton.adjustSize()
        self.exitprofitButton.move(550, 280)

        self.processLogprofitLabel = QLabel('Process log', self)
        self.processLogprofitLabel.setStyleSheet("background-color : yellow")
        self.processLogprofitLabel.adjustSize()
        self.processLogprofitLabel.move(490, 20)

        self.processLogprofitContent = QTextEdit('Don\'t be too dirty babe.', self)
        self.processLogprofitContent.adjustSize()
        self.processLogprofitContent.move(400, 50)

        self.sentencesPath = '.././' + '/data/sentences.txt'
        self.groups = []
        self.sentences = []
        self.sentence = ''

    #izlaz iz aplikacije
    def exitFunction(self):
        QApplication.quit()

    def clearGUI(self):
        self.groups = []
        self.sentences = []
        self.sentence = ''
        self.inputprofitLineEdit.setText('')
        self.processLogprofitContent.setText('')

    def generateSentences(self):
        self.processLogprofitContent.setText('Process started. Please wait.')
        self.GenerateSentencesButton.setDisabled(True)
        self.clearGUIprofitButton.setDisabled(True)
        QApplication.processEvents()
        self.groups = []
        self.sentences = []
        self.extractSentence()
        self.makeSentences("", self.groups)
        countGroups = 0
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
        self.processLogprofitContent.setText('Number of groups in sentence: ' + str(countGroups) + '\nNumber of sentences generated: ' + str(len(self.sentences)))
        self.GenerateSentencesButton.setDisabled(False)
        self.clearGUIprofitButton.setDisabled(False)
        QApplication.processEvents()

    def extractSentence(self):
        #sentence = input('Unesite recenicu: ')
        self.sentence = self.inputprofitLineEdit.text()
        flagGroup = False
        indexGroup = 0
        word = ''
        for i in range(0, len(self.sentence)):
            c = self.sentence[i]
            if c == '{':
                if i != 0:
                    if len(self.groups) == 0:
                        self.groups.append([])
                    self.groups[indexGroup].append(word)
                    indexGroup += 1
                self.groups.append([])
                flagGroup = True
                word = ''
                continue
            if c == '}' and flagGroup:
                self.groups[indexGroup].append(word)
                indexGroup += 1
                self.groups.append([])
                flagGroup = False
                word = ''
                continue
            if flagGroup == True and c == '|':
                self.groups[indexGroup].append(word)
                word = ''
                continue
            word += c
        if word != '':
            if len(self.groups) == 0:
                self.groups.append([])
            self.groups[indexGroup].append(word)

    def makeSentences(self, w, groups):
        for x in groups[0]:
            if len(groups) > 1:
                self.makeSentences(w + str(x), groups[1:])
            else:
                self.sentences.append(w + str(x))

    #Tab3 je klasa koja predstavlja treci tab na GUI-u, obradjuje profit
class Tab4(QWidget):
    def __init__(self):
        super(Tab4, self).__init__()
        self.title = 'Discord'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #slede svi vidzeti koji su dodati na GUI-u(label, push button, radio button, checkbox, line edit, text edit)
        self.getCustomerButton = QPushButton('Get\n customer', self)
        self.getCustomerButton.clicked.connect(self.getCustomer)
        self.getCustomerButton.adjustSize()
        self.getCustomerButton.move(20, 55)

        self.browseButton = QPushButton('Browse\nCustomer', self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.browseButton.adjustSize()
        self.browseButton.move(170, 20)
        self.browseLineEdit = QLineEdit('', self)
        self.browseLineEdit.adjustSize()
        self.browseLineEdit.move(150, 70)
        
        self.clearGUIButton = QPushButton('Clear\nGUI', self)
        self.clearGUIButton.clicked.connect(self.clearGUI)
        self.clearGUIButton.adjustSize()
        self.clearGUIButton.move(330, 20)

        self.RedoButton = QPushButton('Redo', self)
        self.RedoButton.clicked.connect(self.redoWrite)
        self.RedoButton.adjustSize()
        self.RedoButton.move(330, 80)

        self.usernameLabel = QLabel('Username:', self)
        self.usernameLabel.adjustSize()
        self.usernameLabel.move(20, 120)
        self.usernameLineEdit = QLineEdit('', self)
        self.usernameLineEdit.adjustSize()
        self.usernameLineEdit.move(135, 118)

        self.numTokensLabel = QLabel('Tokens:', self)
        self.numTokensLabel.adjustSize()
        self.numTokensLabel.move(20, 150)
        self.numTokensLineEdit = QLineEdit('30', self)
        self.numTokensLineEdit.adjustSize()
        self.numTokensLineEdit.move(135, 148)

        self.numImagesPerFolderLabel = QLabel('Images per folder:', self)
        self.numImagesPerFolderLabel.adjustSize()
        self.numImagesPerFolderLabel.move(20, 180)
        self.numImagesPerFolderLineEdit = QLineEdit('5', self)
        self.numImagesPerFolderLineEdit.adjustSize()
        self.numImagesPerFolderLineEdit.move(135, 178)

        self.methodsLabel = QLabel('Choose method:', self)
        self.methodsLabel.adjustSize()
        self.methodsLabel.move(20, 230)

        self.bioRandomBox = QRadioButton ("Bio Promotion --> Random", self)
        self.bioRandomBox.adjustSize()
        self.bioRandomBox.move(50, 280)

        self.bioOneBox = QRadioButton ("Bio Promotion --> One trader", self)
        self.bioOneBox.adjustSize()
        self.bioOneBox.move(50, 310)

        self.watermarkRandomBox = QRadioButton ("Watermark Promotion --> Random", self)
        self.watermarkRandomBox.adjustSize()
        self.watermarkRandomBox.move(50, 340)

        self.watermarkOneBox = QRadioButton ("Watermark Promotion --> One trader", self)
        self.watermarkOneBox.adjustSize()
        self.watermarkOneBox.move(50, 370)

        self.watermarkOneBackupBox = QRadioButton ("Watermark Promotion --> One trader + Backup", self)
        self.watermarkOneBackupBox.adjustSize()
        self.watermarkOneBackupBox.move(50, 400)

        self.watermarkBioRandomBox = QRadioButton ("Watermark + Bio --> Random", self)
        self.watermarkBioRandomBox.adjustSize()
        self.watermarkBioRandomBox.move(50, 430)

        self.watermarkBioOneBox = QRadioButton ("Watermark + Bio --> One trader", self)
        self.watermarkBioOneBox.adjustSize()
        self.watermarkBioOneBox.move(50, 460)

        self.watermarkBioOneBackupBox = QRadioButton ("Watermark + Bio --> One trader + Backup", self)
        self.watermarkBioOneBackupBox.adjustSize()
        self.watermarkBioOneBackupBox.move(50, 490)

        self.justRandomBox = QRadioButton ("No Promotion --> Random", self)
        self.justRandomBox.adjustSize()
        self.justRandomBox.move(50, 520)

        self.justOneBox = QRadioButton ("No Promotion --> One trader", self)
        self.justOneBox.adjustSize()
        self.justOneBox.move(50, 550)

        self.justOneBackupBox = QRadioButton ("No Promotion --> One trader + Backup", self)
        self.justOneBackupBox.adjustSize()
        self.justOneBackupBox.move(50, 580)

        self.selectAllFilesButton = QPushButton('Select All', self)
        self.selectAllFilesButton.clicked.connect(self.selectAllFilesFunction)
        self.selectAllFilesButton.adjustSize()
        self.selectAllFilesButton.move(350, 250)

        self.biosCheckBox = QCheckBox("Bios", self)
        self.biosCheckBox.adjustSize()
        self.biosCheckBox.move(370, 290)

        self.jobsCheckBox = QCheckBox("Jobs", self)
        self.jobsCheckBox.adjustSize()
        self.jobsCheckBox.move(370, 320)

        self.namesCheckBox = QCheckBox("Names", self)
        self.namesCheckBox.adjustSize()
        self.namesCheckBox.move(370, 350)

        self.emailsCheckBox = QCheckBox("Emails", self)
        self.emailsCheckBox.adjustSize()
        self.emailsCheckBox.move(370, 380)

        self.tradesCheckBox = QCheckBox("trades", self)
        self.tradesCheckBox.adjustSize()
        self.tradesCheckBox.move(370, 410)

        self.setImageAsLabel = QLabel('Set watermarked\n   Image as:', self)
        self.setImageAsLabel.adjustSize()
        self.setImageAsLabel.move(490, 250)

        self.FirstImageBox = QCheckBox("First", self)
        self.FirstImageBox.adjustSize()
        self.FirstImageBox.move(510, 300)

        self.SecondImageBox = QCheckBox("Second", self)
        self.SecondImageBox.adjustSize()
        self.SecondImageBox.move(510, 330)

        self.ThirdImageBox = QCheckBox("Third", self)
        self.ThirdImageBox.adjustSize()
        self.ThirdImageBox.move(510, 360)
        
        self.FourthImageBox = QCheckBox("Fourth", self)
        self.FourthImageBox.adjustSize()
        self.FourthImageBox.move(510, 390)

        self.FifthImageBox = QCheckBox("Fifth", self)
        self.FifthImageBox.adjustSize()
        self.FifthImageBox.move(510, 420)

        self.processLogLabel = QLabel('Process Log', self)
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(420, 480)
        self.processLogLabel.setStyleSheet("background-color : yellow")
        self.processLogContent = QTextEdit('Good day my friend. There is a lot of work waiting for you.', self)
        self.processLogContent.adjustSize()
        self.processLogContent.move(330, 510)

        self.generateButton = QPushButton('Generate', self)
        self.generateButton.clicked.connect(self.generateFunction)
        self.generateButton.setStyleSheet("background-color : green")
        self.generateButton.adjustSize()
        self.generateButton.move(100, 650)

        self.generateBulkButton = QPushButton('Generate\nBulk', self)
        self.generateBulkButton.clicked.connect(self.generateBulkFunction)
        self.generateBulkButton.setStyleSheet("background-color : blue")
        self.generateBulkButton.adjustSize()
        self.generateBulkButton.move(100, 700)

        self.clearErrorsAndResultsButton = QPushButton('Clear errors\nand results', self)
        self.clearErrorsAndResultsButton.clicked.connect(self.clearErrorsAndResults)
        self.clearErrorsAndResultsButton.adjustSize()
        self.clearErrorsAndResultsButton.move(650, 500)

        self.clearFinalButton = QPushButton('Clear\nfinal folder', self)
        self.clearFinalButton.clicked.connect(self.clearFinalFolder)
        self.clearFinalButton.adjustSize()
        self.clearFinalButton.move(650, 550)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.exitFunction)
        self.exitButton.setStyleSheet("background-color : red")
        self.exitButton.adjustSize()
        self.exitButton.move(650, 650)

        #putanje koje se koriste za rad klase Tab1, sve putanje se nalaze negde u folderu Traffic
        #sve putanje sem watermarkSnapPath su fiksne,
        self.trafficPath = '.././'
        self.ordersPath = self.trafficPath + '/orders'
        self.finalPath = self.trafficPath + '/final'
        self.dataPath = self.trafficPath + '/data'
        self.morePath = self.trafficPath + '/more'
        self.completedPath = self.morePath + '/completed'
        self.tradersImagesPath = self.dataPath + '/tradersImages'
        self.watermarkTemplatePath = self.dataPath + '/watermarkTemplate.png'
        #watermarkSnapPath se menja u zavisnosti od username-a snepa, zato je nedefinisana u startu
        self.watermarkSnapPath = ''
        #promenljive koje se koriste za rad klase Tab1
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.currentCustomerID = 0
        self.indexImageForWatermark = 0
        self.username = ''
        self.traderUserImagesPath = ''
        #numCustomers se smanjuje kako se porudzbine obradjuju
        self.numCustomers = len(os.listdir(self.ordersPath + '/customers'))
        self.imageForWatermarkPaths = []
        self.dataNames = ['NAMES.txt', 'trades.txt', 'EMAILS.txt', 'JOBS.txt', 'BIOS.txt']
        #dataNamesFlags sluzi za laksu proveru fajlova dataNames,
        #u smislu lakseg prepoznavanja koji fajl treba da se obradjuje ili provera
        self.dataNamesFlags = [False, False, False, False, False]
        self.bulk = False
        self.bulkUsernames = []

    def redoRead(self):
        self.redoUsername = self.username
        self.redoTokens = self.numTokens
        self.redoImagesPerFolder = self.numImagesPerFolder

        if self.bioRandomBox.isChecked():
            self.redoMethod = 1
        if self.bioOneBox.isChecked():
            self.redoMethod = 2
        if self.watermarkRandomBox.isChecked():
            self.redoMethod = 3
        if self.watermarkOneBox.isChecked():
            self.redoMethod = 4
        if self.watermarkOneBackupBox.isChecked():
            self.redoMethod = 5
        if self.watermarkBioRandomBox.isChecked():
            self.redoMethod = 6
        if self.watermarkBioOneBox.isChecked():
            self.redoMethod = 7
        if self.watermarkBioOneBackupBox.isChecked():
            self.redoMethod = 8
        if self.justRandomBox.isChecked():
            self.redoMethod = 9
        if self.justOneBox.isChecked():
            self.redoMethod = 10
        if self.justOneBackupBox.isChecked():
            self.redoMethod = 11

        if self.biosCheckBox.isChecked():
            self.redoBios = 1
        else:
            self.redoBios = 0
        if self.jobsCheckBox.isChecked():
            self.redoJobs = 1
        else:
            self.redoJobs = 0
        if self.namesCheckBox.isChecked():
            self.redoNames = 1
        else:
            self.redoNames = 0
        if self.emailsCheckBox.isChecked():
            self.redoEmails = 1
        else:
            self.redoEmails = 0
        if self.tradesCheckBox.isChecked():
            self.redotrades = 1
        else:
            self.redotrades = 0

        if self.FirstImageBox.isChecked():
            self.redoFirst = 1
        else:
            self.redoFirst = 0
        if self.SecondImageBox.isChecked():
            self.redoSecond = 1
        else:
            self.redoSecond = 0
        if self.ThirdImageBox.isChecked():
            self.redoThird = 1
        else:
            self.redoThird = 0
        if self.FourthImageBox.isChecked():
            self.redoFourth = 1
        else:
            self.redoFourth = 0
        if self.FifthImageBox.isChecked():
            self.redoFifth = 1   
        else:
            self.redoFifth = 0

    def redoWrite(self):
        self.numTokensLineEdit.setText(str(self.redoTokens))
        self.numImagesPerFolderLineEdit.setText(str(self.redoImagesPerFolder))
        self.numTokens = self.redoTokens
        self.numImagesPerFolder = self.redoImagesPerFolder

        if self.redoFirst == 1:
            self.FirstImageBox.setChecked(True)
        else:
            self.FirstImageBox.setChecked(False)
        if self.redoSecond == 1:
            self.SecondImageBox.setChecked(True)
        else:
            self.SecondImageBox.setChecked(False)
        if self.redoThird == 1:
            self.ThirdImageBox.setChecked(True)
        else:
            self.ThirdImageBox.setChecked(False)
        if self.redoFourth == 1:
            self.FourthImageBox.setChecked(True)
        else:
            self.FourthImageBox.setChecked(False)
        if self.redoFifth == 1:
            self.FifthImageBox.setChecked(True)
        else:
            self.FifthImageBox.setChecked(False)

        if self.redoBios == 1:
            self.biosCheckBox.setChecked(True)
        else:
            self.biosCheckBox.setChecked(False)
        if self.redoJobs == 1:
            self.jobsCheckBox.setChecked(True)
        else:
            self.jobsCheckBox.setChecked(False)
        if self.redoNames == 1:
            self.namesCheckBox.setChecked(True)
        else:
            self.namesCheckBox.setChecked(False)
        if self.redoEmails == 1:
            self.emailsCheckBox.setChecked(True)
        else:
            self.emailsCheckBox.setChecked(False)
        if self.redotrades == 1:
            self.tradesCheckBox.setChecked(True)
        else:
            self.tradesCheckBox.setChecked(False)

        if self.redoMethod == 1:
            self.bioRandomBox.setChecked(True)
        if self.redoMethod == 2:
            self.bioOneBox.setChecked(True)
        if self.redoMethod == 3:
            self.watermarkRandomBox.setChecked(True)
        if self.redoMethod == 4:
            self.watermarkOneBox.setChecked(True)
        if self.redoMethod == 5:
            self.watermarkOneBackupBox.setChecked(True)
        if self.redoMethod == 6:
            self.watermarkBioRandomBox.setChecked(True)
        if self.redoMethod == 7:
            self.watermarkBioOneBox.setChecked(True)
        if self.redoMethod == 8:
            self.watermarkBioOneBackupBox.setChecked(True)
        if self.redoMethod == 9:
            self.justRandomBox.setChecked(True)
        if self.redoMethod == 10:
            self.justOneBox.setChecked(True)
        if self.redoMethod == 11:
            self.justOneBackupBox.setChecked(True)

    #funkcija koja se proziva kliktanjem na dugme Browse Customers
    #bira se tekstualni fajl porudzbine koju zelimo da obradimo i prikazuje se putanja tog fajla,
    #a zatim se i automatski odatle izvuku i prikazu username i adds
    def browsefiles(self):
        self.clearGUI()
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.ordersPath, 'Text (*.txt)')
        browsePath = fname[0]
        self.browseLineEdit.setText(browsePath)
        ind = browsePath.rfind('/')
        fileName = browsePath[ind + 1:]
        self.isBulkCustomer()
        if browsePath != '':
            if self.bulk == False:    
                with open(browsePath, 'r') as Reader:
                    self.username = Reader.readline().strip('\n')
                self.usernameLineEdit.setText(self.username)
            else:
                lines = []
                with open(browsePath, 'r') as Reader:
                    lines = Reader.readlines()
                with open(browsePath, 'r') as Reader:
                    for i in range(1, len(lines)):
                        self.bulkUsernames.append(lines[i].strip('\n'))
                self.usernameLineEdit.setText('')
            self.processLogContent.setText('Customer fetched.')
            QApplication.processEvents()
            self.processLogContent.adjustSize()

    #izlaz iz aplikacije
    def exitFunction(self):
        QApplication.quit()

    #kiktanjem dugmeta Select All, biraju se svi fajlovi iz foldera data (dataNames fajlovi) za extractData()
    def selectAllFilesFunction(self):
        if self.biosCheckBox.isChecked() or self.namesCheckBox.isChecked() or self.tradesCheckBox.isChecked() or self.emailsCheckBox.isChecked() or self.jobsCheckBox.isChecked():
            self.biosCheckBox.setChecked(False)
            self.namesCheckBox.setChecked(False)
            self.tradesCheckBox.setChecked(False)
            self.emailsCheckBox.setChecked(False)
            self.jobsCheckBox.setChecked(False)
            self.dataNamesFlags = [False, False, False, False, False]
        else:
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.tradesCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]

    #ukoliko postoji, brise sav sadrzaj iz foldera final
    def clearFinalFolder(self):
        for fileName in os.listdir(self.finalPath):
            filePath = self.finalPath + '/' + fileName
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        self.processLogContent.setText('Folder final is empty.')
        QApplication.processEvents()
        self.processLogContent.adjustSize()

    #brise sav sadrzaj iz foldera completed i errors.txt
    def clearErrorsAndResults(self):
        with open(self.morePath + '/errors.txt', 'w') as Writer:
            pass
        shutil.rmtree(self.completedPath)
        os.mkdir(self.completedPath)
        self.processLogContent.setText('File \'errors.txt\' and folder \'completed\' are empty.')
        QApplication.processEvents()
        self.processLogContent.adjustSize()
    
    #brise sve sto je ispisano ili oznaceno na GUI-u kako bi bilo preglednije
    def clearGUI(self):
        #prvo se vrednosti u programu postavljaju na difoltne
        self.numTokens = 0
        self.numImagesPerFolder = 0
        self.indexImageForWatermark = 1
        self.username = ''
        self.traderUserImagesPath = ''
        self.watermarkSnapPath = ''
        self.imageForWatermarkPaths = []
        self.dataNamesFlags = [False, False, False, False, False]
        #potom se i vizualno GUI brise kako bi bio pregledniji
        self.usernameLineEdit.setText('')
        self.numTokensLineEdit.setText('')
        self.numImagesPerFolderLineEdit.setText('')
        self.browseLineEdit.setText('')
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
        self.tradesCheckBox.setChecked(False)
        self.bulk = False
        self.bulkUsernames = []
            
    #dohvata random porudzbinu iz foldera orders
    def getCustomer(self):
        #za dohvatanje nove porudzbine, brisu se zapamceni podaci o prosloj pomocu funkcije clearGUI()
        self.clearGUI()
        #ukoliko postoji porudzbina koja ceka u folderu orders, dohvata se njen usename i broj adova
        if self.numCustomers == 0:
            self.processLogContent.setText('No more customers waiting')
            QApplication.processEvents()
            self.processLogContent.adjustSize()
        else:
            if len(os.listdir(self.ordersPath + '/customers')) != 0:
                self.currentCustomerID %= self.numCustomers
                fileName = os.listdir(self.ordersPath + '/customers')[self.currentCustomerID]
                self.browseLineEdit.setText(self.ordersPath + '/customers' + '/' + fileName)
                self.currentCustomerID += 1
                self.currentCustomerID %= self.numCustomers
                self.customer = fileName[:-4]
                usernamePath = self.ordersPath + '/customers' + '/' + fileName
                with open(usernamePath, 'r') as Reader:
                    self.username = Reader.readline().strip('\n')
                self.usernameLineEdit.setText(self.username)
                self.processLogContent.setText('Customer fetched.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                return True
            #ukoliko je folder orders prazan, nema porudzbine koja ceka
            else:
                self.processLogContent.setText('There are no more customers waiting')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                return False

    #podesava u listi dataNamesFlags koji fajlovi iz dataNames treba da se obrade
    def setDataFlags(self):
        if self.namesCheckBox.isChecked():
            self.dataNamesFlags[0] = True
        if self.tradesCheckBox.isChecked():
            self.dataNamesFlags[1] = True
        if self.emailsCheckBox.isChecked():
            self.dataNamesFlags[2] = True
        if self.jobsCheckBox.isChecked():
            self.dataNamesFlags[3] = True
        if self.biosCheckBox.isChecked():
            self.dataNamesFlags[4] = True

    #odredjuje se koj je redni broj slike u svakom folderu slika akaunteva,
    #samo ce slika sa tim rednim brojem u svakom folderu slika akaunteva biti watermarkovana
    def setIndexImageForWatermark(self):
        if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.justOneBackupBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBox.isChecked():
            if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
                return True
            else:
                self.processLogContent.setText('You can\'t use bio method with checking which image in folders you want to watermark. Uncheck it and try again.')
                QApplication.processEvents()
                return False
        if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
            if self.FirstImageBox.isChecked() == False and self.SecondImageBox.isChecked() == False and self.ThirdImageBox.isChecked() == False and self.FourthImageBox.isChecked() == False and self.FifthImageBox.isChecked() == False:
                self.processLogContent.setText('You can\'t use watermark method without checking which image in folders you want to watermark. Check exactly 1 and try again.')
                QApplication.processEvents()
                return False
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
            else:
                self.processLogContent.setText('You can\'t use watermark method with checking more than 1 images per folder to watermark.  Check exactly 1 and try again.')
                QApplication.processEvents()
                self.indexImageForWatermark = 0
                return False
        
    def isBulkCustomer(self):
        s = self.browseLineEdit.text()
        ind = s.rfind('/')
        a = ''
        for i in range(ind - 1, -1, -1):
            if s[i] == '/':
                break
            a += s[i]
        a = a[::-1]
        if a == 'customersBULK':
            self.bulk = True
        else:
            self.bulk = False

    def generateBulkFunction(self):
        self.isBulkCustomer()
        if self.bulk == False:
            self.processLogContent.setText('Can\'t use Generate Bulk button for no bulk customer. Try with Generate button.')
            QApplication.processEvents()
        else:
            startTime = time.time()
            self.setDataFlags()
            ind = self.setIndexImageForWatermark()
            checkData = self.checkEnoughData() and ind
            self.usernameLineEdit.setText('')
            #ukoliko ima potrebnih podataka za obradu trenutne porudzbine, obrada pocinje
            if checkData == True:
                self.processLogContent.setText('Process started. Please wait.')
                self.AutomateButton.setDisabled(True)
                self.getCustomerButton.setDisabled(True)
                self.browseButton.setDisabled(True)
                self.clearGUIButton.setDisabled(True)
                self.selectAllFilesButton.setDisabled(True)
                self.clearErrorsAndResultsButton.setDisabled(True)
                self.clearFinalButton.setDisabled(True)
                self.generateButton.setDisabled(True)
                self.generateBulkButton.setDisabled(True)
                QApplication.processEvents()
                numBulkUsernames = int(len(self.bulkUsernames))
                numTokens = str(self.numTokens)
                self.numTokens = self.numTokens // numBulkUsernames
                for username in self.bulkUsernames:
                    self.username = username
                    #prave se potrebni folderi u folderu final
                    self.makeUsernameFolders()
                    #izvlace se izabrani fajlovi iz dataNames liste i prebacuju se u folder final
                    self.extractData()
                    #ukoliko je izabrana 'Random' metoda odnosno metoda koja izvlaci slike iz razlicitih trejdera,
                    #onda se poziva metoda extractRandomtraders()
                    if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
                        self.extractRandomtraders()
                    #ukoliko je izabrana 'One' metoda odnosno metoda koja izvlaci slike samo od jednog trejdera,
                    #onda se poziva metoda extractOnetrader()
                    elif self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
                        self.extractOnetrader()
                    #slike se kropuju (po potrebi flipuju), preimenjuju se i ukoliko se radi watermark
                    #pamte se slike koje treba da se watermarkuju
                    self.modifyImages()
                    #ukoliko je izabrana neka bio metoda, zove se funkcija callBioMethod()
                    if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                        self.callBioMethod()
                    #ukoliko je izabrana neka watermark metoda, zove se funkcija callWatermarkMethod()
                    if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                        self.callWatermarkMethod()
                    self.processLogContent.setText('Processed username: ' + self.username + '. Wait for others.')
                    QApplication.processEvents()
                    self.processLogContent.adjustSize()
                    #time.sleep(2)
                endTime = time.time()
                elapsedTime = endTime - startTime
                #porudzbina se iz foldera customers prebacuje u folder completed
                if os.path.isfile(self.completedPath + '/' + self.customer + '.txt'):
                    os.remove(self.completedPath + '/' + self.customer + '.txt')
                if os.path.isfile(self.ordersPath + '/customersBULK' + '/' + self.customer + '.txt'):
                    os.remove(self.ordersPath + '/customersBULK' + '/' + self.customer + '.txt')
                #sada ima jedna porudzbina manje na cekanju
                self.numCustomers -= 1
                customer = self.customer
                username = self.username
                #porudzbina je zavrsena pa se GUI cisti
                method = self.findMethod()
                indexImage = self.findIndexImageWatermark()
                files = self.findWhichFileDidntUse()
                j = 0
                usernames = ''
                for i in self.bulkUsernames:
                    if j == 0:
                        usernames += i
                        j = 1
                    else:
                        usernames += ', ' + i
                self.AutomateButton.setDisabled(False)
                self.getCustomerButton.setDisabled(False)
                self.browseButton.setDisabled(False)
                self.clearGUIButton.setDisabled(False)
                self.selectAllFilesButton.setDisabled(False)
                self.clearErrorsAndResultsButton.setDisabled(False)
                self.clearFinalButton.setDisabled(False)
                self.generateButton.setDisabled(False)
                self.generateBulkButton.setDisabled(False)
                self.clearGUI()
                self.processLogContent.setText('Order finished.\n' + 'Customer: ' + customer + '\nSnapchat usernames: ' + usernames + '\nDesired adds: ' + adds + '\nNumber tokens created for him: ' + numTokens + '\nMethod: ' + method + indexImage + files + '\nTime elapsed: ' + '{:.2f}'.format(elapsedTime) + ' seconds.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                with open(self.completedPath + '/' + customer + '.txt', 'w') as Writer:
                    Writer.write(self.processLogContent.toPlainText())

    #glavna funkcija ovog GUI-a, pokrece je dugme Generate i sluzi da obradi trenutno izabranu porudzbinu
    def generateFunction(self):
        self.isBulkCustomer()
        if self.bulk == True:
            self.processLogContent.setText('Can\'t use Generate button for bulk customer. Try with Generate Bulk button.')
            QApplication.processEvents()
        else:
            startTime = time.time()
            self.username = self.usernameLineEdit.text()
            self.setDataFlags()
            ind = self.setIndexImageForWatermark()
            checkData = self.checkEnoughData() and ind
            #ukoliko ima potrebnih podataka za obradu trenutne porudzbine, obrada pocinje
            if checkData == True:
                self.processLogContent.setText('Process started. Please wait.')
                self.AutomateButton.setDisabled(True)
                self.getCustomerButton.setDisabled(True)
                self.browseButton.setDisabled(True)
                self.clearGUIButton.setDisabled(True)
                self.selectAllFilesButton.setDisabled(True)
                self.clearErrorsAndResultsButton.setDisabled(True)
                self.clearFinalButton.setDisabled(True)
                self.generateButton.setDisabled(True)
                self.generateBulkButton.setDisabled(True)
                QApplication.processEvents()
                #prave se potrebni folderi u folderu final
                self.makeUsernameFolders()
                #izvlace se izabrani fajlovi iz dataNames liste i prebacuju se u folder final
                self.extractData()
                #ukoliko je izabrana 'Random' metoda odnosno metoda koja izvlaci slike iz razlicitih trejdera,
                #onda se poziva metoda extractRandomtraders()
                if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
                    self.extractRandomtraders()
                #ukoliko je izabrana 'One' metoda odnosno metoda koja izvlaci slike samo od jednog trejdera,
                #onda se poziva metoda extractOnetrader()
                elif self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
                    self.extractOnetrader()
                #slike se kropuju (po potrebi flipuju), preimenjuju se i ukoliko se radi watermark
                #pamte se slike koje treba da se watermarkuju
                self.modifyImages()
                #ukoliko je izabrana neka bio metoda, zove se funkcija callBioMethod()
                if self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                    self.callBioMethod()
                #ukoliko je izabrana neka watermark metoda, zove se funkcija callWatermarkMethod()
                if self.watermarkRandomBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked():
                    self.callWatermarkMethod()
                endTime = time.time()
                elapsedTime = endTime - startTime
                #porudzbina se iz foldera customers prebacuje u folder completed
                if os.path.isfile(self.completedPath + '/' + self.username + '.txt'):
                    os.remove(self.completedPath + '/' + self.username + '.txt')
                if os.path.isfile(self.ordersPath + '/' + self.username + '.txt'):
                    os.remove(self.ordersPath + '/' + self.username + '.txt')
                #sada ima jedna porudzbina manje na cekanju
                self.numCustomers -= 1
                username = self.username
                #porudzbina je zavrsena pa se GUI cisti
                method = self.findMethod()
                indexImage = self.findIndexImageWatermark()
                files = self.findWhichFileDidntUse()
                numTokens = str(self.numTokens)
                self.clearGUI()
                self.AutomateButton.setDisabled(False)
                self.getCustomerButton.setDisabled(False)
                self.browseButton.setDisabled(False)
                self.clearGUIButton.setDisabled(False)
                self.selectAllFilesButton.setDisabled(False)
                self.clearErrorsAndResultsButton.setDisabled(False)
                self.clearFinalButton.setDisabled(False)
                self.generateButton.setDisabled(False)
                self.generateBulkButton.setDisabled(False)
                self.processLogContent.setText('Order finished.\n' + '\nSnapchat username: ' + username + '\nTokens created: ' + numTokens + '\nMethod: ' + method + indexImage + files + '\nTime elapsed: ' + '{:.2f}'.format(elapsedTime) + ' seconds.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                with open(self.completedPath + '/' + username + '.txt', 'w') as Writer:
                    Writer.write(self.processLogContent.toPlainText())

    def findWhichFileDidntUse(self):
        s = ''
        if self.biosCheckBox.isChecked() and self.jobsCheckBox.isChecked() and self.namesCheckBox.isChecked() and self.emailsCheckBox.isChecked() and self.tradesCheckBox.isChecked():
            return s
        s += '\nWithout:'
        i = 0
        if self.biosCheckBox.isChecked() == False:
            if i == 0:
                s += ' bios'
                i = 1
            else:
                s += ', bios'
        if self.jobsCheckBox.isChecked() == False:
            if i == 0:
                s += ' jobs'
                i = 1
            else:
                s += ', jobs'
        if self.namesCheckBox.isChecked() == False:
            if i == 0:
                s += ' names'
                i = 1
            else:
                s += ', names'
        if self.emailsCheckBox.isChecked() == False:
            if i == 0:
                s += ' emails'
                i = 1
            else:
                s += ', emails'
        if self.tradesCheckBox.isChecked() == False:
            if i == 0:
                s += ' trades'
                i = 1
            else:
                s += ', trades'
        s += '.'
        return s

    def findIndexImageWatermark(self):
        if self.FirstImageBox.isChecked():
            return '\nWatermarked 1. image in folders.'
        if self.SecondImageBox.isChecked():
            return '\nWatermarked 2. image in folders.'
        if self.ThirdImageBox.isChecked():
            return '\nWatermarked 3. image in folders.'
        if self.FourthImageBox.isChecked():
            return '\nWatermarked 4. image in folders.'
        if self.FifthImageBox.isChecked():
            return '\nWatermarked 5. image in folders.'
        return ''

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

    #pre pocetka obrade porudzbine, treba proveriti da li su ispunjeni uslovi za obradu
    def checkEnoughData(self):
        #prvo se proverava da li je GUI adekvatno popunjen
        if self.bulk == True:
            checkGUILineEdits = self.numTokensLineEdit.text() != '' and self.numImagesPerFolderLineEdit.text() != ''
        else:
            checkGUILineEdits = self.usernameLineEdit.text() != '' and self.numTokensLineEdit.text() != '' and self.numImagesPerFolderLineEdit.text() != ''
        checkGUIMethods = self.bioRandomBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justRandomBox.isChecked() or self.justOneBackupBox.isChecked()
        #ako je izabrana neka bio metoda, potrebno je da je izabran fajl bios iz dataNames za ekstrakovanje
        if self.biosCheckBox.isChecked() or (self.bioRandomBox.isChecked() == False and self.bioOneBox.isChecked() == False and self.watermarkBioRandomBox.isChecked() == False and self.watermarkBioOneBox.isChecked() == False and self.watermarkBioOneBackupBox.isChecked() == False):
            checkGUIBioMethods = True
        else:
            checkGUIBioMethods = False
        #ukoliko je bar 1 uslov neispunjen, porudzbina se ne moze trenutno obraditi, potrebno je popraviti gresku
        checkGUI = checkGUILineEdits and checkGUIMethods and checkGUIBioMethods
        if checkGUI == False:
            if checkGUILineEdits == False:
                self.processLogContent.setText('You didn\'t fill first 4 boxes. Try again.')
                QApplication.processEvents()
            elif checkGUIMethods == False:
                self.processLogContent.setText('You didn\'t choose method. Try again.')
                QApplication.processEvents()
            elif checkGUIBioMethods == False:
                self.processLogContent.setText('You want bio method but you didn\'t choose bio file to extract from data folder. Try again.')
                QApplication.processEvents()
            #elif checkIndexImageForWatermark == False:
                #self.processLogContent.setText('You want watermark method but you didn\'t choose serial number of the image in folders for watermarking. Try again.')
            self.processLogContent.adjustSize()
        #ukoliko nije doslo do greske u popunjavanju GUI-a
        else:
            try:
                self.numImagesPerFolder = int(self.numImagesPerFolderLineEdit.text())
                self.numTokens = int(self.numTokensLineEdit.text())
                i = 0
                #provera za fajlove iz dataNames da li imaju dovoljno linija za obradu trenutne porudzbine
                for fileName in self.dataNames:
                    #provera se vrsi samo ako je trenutni fajl izabran za ekstrakovanje
                    if self.dataNamesFlags[i] == True:
                        path = self.dataPath + '/' + fileName
                        with open(path, 'r') as Reader:
                            lines = Reader.readlines()
                        #ukoliko nema dovoljno linija za trenutnu porudzbinu, to se belezi u errors.txt u folderu orders
                        if len(lines) < self.numTokens:
                            errorMsg = "File " + fileName + " has not enough lines for creating " + str(self.numTokens) + " tokens for customer " + self.customer + " with his username " + self.username
                            with open(self.morePath + '/errors.txt', 'a') as Writer:
                                if os.path.getsize(self.morePath + '/errors.txt') == 0:
                                    Writer.write(errorMsg)
                                else:
                                    Writer.write('\n' + errorMsg)
                            print(errorMsg)
                            #baca se izuzetak kako bi se preskocilo dalje ispitivanje
                            raise Exception(errorMsg)
                        i += 1
                #ukoliko je izabrana neka 'Random' metoda, vrsi se provera da li ima dovoljno slika
                if self.bioRandomBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.justRandomBox.isChecked():
                    acc = 0
                    for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                        path = self.tradersImagesPath + '/' + fileName
                        acc += len(os.listdir(path))//self.numImagesPerFolder
                    #ukoliko nema dovoljno slika, baca se izuzetak
                    if acc < self.numTokens:
                        self.notEnoughImages()
                    else:
                        #ukoliko ima dovoljno slika, sva provera je zavrsena
                        return True
                #ukoliko je izabrana neka 'One' ili 'OneBackup' metoda, vrsi se provera da li ima dovoljno slika
                elif self.watermarkOneBox.isChecked() or self.watermarkOneBackupBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBox.isChecked() or self.justOneBackupBox.isChecked():
                    for j, fileName in enumerate(os.listdir(self.tradersImagesPath)):
                        path = self.tradersImagesPath + '/' + fileName
                        if (self.watermarkOneBox.isChecked() or self.bioOneBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.justOneBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder:
                            self.traderUserImagesPath = path
                            return True
                        elif (self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked()) and len(os.listdir(path)) > self.numTokens * self.numImagesPerFolder + self.numTokens:
                            self.traderUserImagesPath = path
                            return True
                    #ukoliko nema dovoljno slika, baca se izuzetak
                    self.notEnoughImages()
            #ukoliko je izuzetak bacen, hvata se ovde, program javlja gresku i spreman je za ponovni pokusaj
            except Exception as e:
                    print('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                    self.processLogContent.setText('There are not enough data for\nprocessing this account.\n' + str(e.args[0]))
                    QApplication.processEvents()
                    self.processLogContent.adjustSize()
                    return False

    #funkcija koja se poziva ukoliko nema dovoljno slika za obradu porudzbine
    def notEnoughImages(self):
        errorMsg = "Not enough images for creating " + str(self.numTokens) + " for username " + self.username
        with open(self.morePath + '/errors.txt', 'a') as Writer:
            if os.path.getsize(self.morePath + '/errors.txt') == 0:
                Writer.write(errorMsg)
            else:
                Writer.write("\n" + errorMsg)
        raise Exception(errorMsg)

    #prave se se svi potrebni folderi trenutne porudzbine u final folderu
    def makeUsernameFolders(self):
        if os.path.isdir(self.finalPath + '/' + self.username) == True:
            shutil.rmtree(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username)
        os.mkdir(self.finalPath + '/' + self.username + '/' + 'images')
        for i in range(self.numTokens):
            os.mkdir(self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(i + 1))
        #ukoliko je izabrana 'Backup' metoda, treba napraviti dodatne foldere
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            if os.path.isdir(self.finalPath + '/' + self.username + 'BACKUP') == True:
                shutil.rmtree(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP')
            os.mkdir(self.finalPath + '/' + self.username + 'BACKUP' + '/' + 'images')

    #izvlaci linije iz izabranih dataNames fajlova i prebacuje ih u final folder
    def extractData(self):
        otherLines = []
        r = 0
        for fileName in self.dataNames:
            #ukoliko trenutni fajl treba da se obradi
            if self.dataNamesFlags[r] == True:
                name = fileName[0] + fileName[1:].lower()
                with open(self.dataPath + '/' + fileName, "r") as Reader:
                    with open(self.finalPath + '/' + self.username + '/' + name, "w") as Writer:
                        for i in range(self.numTokens - 1):
                            Writer.write(Reader.readline())
                        Writer.write(Reader.readline().strip('\n'))
                    otherLines = Reader.readlines()
                #ispisuje preostale linije u fajlove
                with open(self.dataPath + '/' + fileName, "w") as Writer:
                    Writer.writelines(otherLines)
            r += 1

    #izvlaci slike iz tradersImages foldera, ali samo od jednog trejdera i prebacuje ih u final folder
    def extractOnetrader(self):
        oldPath = self.traderUserImagesPath
        for countTokens in range(self.numTokens):
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
        #ukoliko je izabrana 'Backup' metoda, treba izvuci slike i za njih
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
            for countTokens in range(self.numTokens):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + 'BACKUP/' + 'images'
                shutil.move(oldPath + '/' + firstImageInFile, newPath)

    #izvlaci slike iz tradersImages foldera, ali vise trejdera i prebacuje ih u final folder
    def extractRandomtraders(self):
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
            while len(os.listdir(oldPath)) < self.numImagesPerFolder:
                if countUsers >= numUsers:
                    countUsers = 0
                if BORING[countUsers] == False:
                    print('U folderu ', dataUserNames[countUsers],' nema dovoljno slika za akaunt.')
                    BORING[countUsers] = True
                countUsers += 1
                if countUsers >= numUsers:
                    countUsers = 0
                oldPath = self.tradersImagesPath + '/' + dataUserNames[countUsers]
            for countImages in range(self.numImagesPerFolder):
                firstImageInFile = os.listdir(oldPath)[0]
                newPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(countTokens + 1)
                shutil.move(oldPath + '/' + firstImageInFile, newPath)
            countUsers += 1

    #vrsi promenu dimenzija slika iz final foldera (po potrebi mogu da se flipuju) i preimenuju se
    def modifyImages(self):
        for token in range(self.numTokens):
            folderPath = self.finalPath + '/' + self.username + '/' + 'images' + '/' + str(token + 1)
            num = random.randint(1000, 10000)
            for i, fileName in enumerate(os.listdir(folderPath)):
                num = num + 1
                oldImagePath = folderPath + "/" + fileName
                newImagePath = folderPath + '/' + 'IMG_' + str(num) + ".jpg"
                os.rename(oldImagePath, newImagePath)
                image = Image.open(newImagePath)
                if i == (self.indexImageForWatermark - 1) and (self.watermarkOneBackupBox.isChecked() or self.watermarkOneBox.isChecked() or self.watermarkRandomBox.isChecked() or self.watermarkBioRandomBox.isChecked() or self.watermarkBioOneBox.isChecked() or self.watermarkBioOneBackupBox.isChecked()):
                    self.imageForWatermarkPaths.append(newImagePath)
                cropedImage = image.resize((1125, 1364))
                #newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                cropedImage.save(newImagePath)
                cropedImage.close()
        #ukoliko je izabrana 'Backup' metoda, treba modifikovati i takve slike
        if self.watermarkOneBackupBox.isChecked() or self.watermarkBioOneBackupBox.isChecked() or self.justOneBackupBox.isChecked():
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
                    #newImage = cropedImage.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                    cropedImage.save(newImagePath)
                    cropedImage.close()
                else:
                    break

    #funkcija koja se zove za sve vrste bio metoda
    def callBioMethod(self):
        #trazi se file Bios.txt u final folderu trenutne porudzbine kako bi mogao da se apenduje snep u biografiju
        bioPath = self.finalPath + '/' + self.username + '/' + 'Bios.txt'
        snaps = [r'\nS.C: ', r'\nS.C - ', r'\nS.C ']
        h = 0
        lines = []
        #username-u se razdvajaju slova tako da iz sara555 prelazi u s a r a 5 5 5
        s = ""
        for char in self.username:
            s = s + char + ' '
        trickUsername = s.rstrip(' ')
        lines = ""
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            numLines = len(Reader.readlines())
        #vrsi se apendovanje snepa u biografije liniju po liniju
        with open(self.finalPath + '/' + self.username + '/' + 'Bios.txt', "r") as Reader:
            for i in range(numLines - 1):
                lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername + '\n'
                h += 1
                if h == 3:
                    h = 0
            lines = lines + Reader.readline().strip('\n') + snaps[h] + trickUsername
        with open(bioPath, "w") as Writer:
            Writer.write(lines)
    
    #pravi username template za watermark
    def makeUsernameWatermark(self):
        #templejt se pravi samo ukoliko on vec ne postoji
        #na sliku watermarkTemplatePath koja predstavlja crni pravougaonik,
        #vrsi se lepljenje teksta koji prestavlja username snepa
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
        #radi se watermark onih slika koje su izdvojene za watermark
        #lepi se template username-a na sliku koja je predvidjena za watermark
        for inputImagePath in self.imageForWatermarkPaths:
            height = 0 + random.randint(-100, 100)
            originalImage = Image.open(inputImagePath)
            originalWidth, originalHeight = originalImage.size
            watermarkImage = Image.open(self.watermarkSnapPath).convert("RGBA")
            transparent = Image.new('RGBA', (originalWidth, originalHeight), (0,0,0,0))
            transparent.paste(originalImage, (0,0))
            transparent.paste(watermarkImage, (width, height), mask=watermarkImage)
            transparent.save(inputImagePath, format="png")
        #ukoliko je izabrana i opcija za backup, te slike takodje treba da se watermarkuju, sve slike u tom folderu
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

    #funkcija koja se zove za sve vrste watermark metoda
    def callWatermarkMethod(self):
        self.watermarkSnapPath = self.dataPath + '/usernameTemplates/' + self.username + '.png'
        self.makeUsernameWatermark()
        self.watermarkImages()

    #funkcija za testiranje metoda
    def test(self):
        if self.getCustomer() == True:
            self.numImagesPerFolder = 5
            self.numTokensLineEdit.setText(str(self.numTokens))
            self.numImagesPerFolderLineEdit.setText(str(self.numImagesPerFolder))
            self.bioRandomBox.setChecked(True)
            self.biosCheckBox.setChecked(True)
            self.namesCheckBox.setChecked(True)
            self.tradesCheckBox.setChecked(True)
            self.emailsCheckBox.setChecked(True)
            self.jobsCheckBox.setChecked(True)
            self.dataNamesFlags = [True, True, True, True, True]
            self.generateFunction()

if __name__ == "__main__":
    app = QApplication([])
    w = Window()
    app.exec_()
