import os
import pyperclip
import shutil
from datetime import date
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#class for spintax
class Window(QWidget): # type: ignore
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.initUI()
        self.popUp()
        self.show()

    def initUI(self):
        self.left = 700
        self.top = 300
        self.width = 490
        self.height = 390
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(QSize(self.width, self.height))       # type: ignore 
        self.setWindowTitle('First Processor')

        x = 100
        y = 20

        self.copyMailButton = QPushButton('Copy\nmail', self)       # type: ignore
        self.copyMailButton.clicked.connect(self.copyMail)
        self.copyMailButton.adjustSize()
        self.copyMailButton.move(x + 45, y)
        self.copyMailPasswordButton = QPushButton('Copy mail\npassword', self)       # type: ignore
        self.copyMailPasswordButton.clicked.connect(self.copyMailPassword)
        self.copyMailPasswordButton.adjustSize()
        self.copyMailPasswordButton.move(x + 45, y + 55)
        self.copySnapNameButton = QPushButton('Copy snap\nfirstname', self)       # type: ignore
        self.copySnapNameButton.clicked.connect(self.copySnapName)
        self.copySnapNameButton.adjustSize()
        self.copySnapNameButton.move(x + 150, y)
        self.copySnapPasswordButton = QPushButton('Copy snap\npassword', self)       # type: ignore
        self.copySnapPasswordButton.clicked.connect(self.copySnapPassword)
        self.copySnapPasswordButton.adjustSize()
        self.copySnapPasswordButton.move(x + 150, y + 55)
        self.copySnapUsernameButton = QPushButton('Copy snap\nusername', self)       # type: ignore
        self.copySnapUsernameButton.clicked.connect(self.copySnapUsername)
        self.copySnapUsernameButton.adjustSize()
        self.copySnapUsernameButton.move(x + 95, y + 110)
        
        x += 100
        y += 130

        self.processLogLabel = QLabel('', self)       # type: ignore
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(x + 10, y + 10)
        self.processLogContent = QTextEdit('', self)       # type: ignore
        self.processLogContent.adjustSize()
        self.processLogContent.move(x - 85, y + 40)
        self.processLogContent.resize(260, 90)

        self.gmxMailLabel = QLabel('Gmx mail:', self)       # type: ignore
        self.gmxMailLabel.adjustSize()
        self.gmxMailLabel.move(10, y + 45)
        self.gmxPasswordLabel = QLabel('Gmx password:', self)       # type: ignore
        self.gmxPasswordLabel.adjustSize()
        self.gmxPasswordLabel.move(10, y + 61)
        self.snapFirstNameLabel = QLabel('Snap firstName:', self)       # type: ignore
        self.snapFirstNameLabel.adjustSize()
        self.snapFirstNameLabel.move(10, y + 77)
        self.snapPasswordLabel = QLabel('Snap password:', self)       # type: ignore
        self.snapPasswordLabel.adjustSize()
        self.snapPasswordLabel.move(10, y + 93)
        self.snapUsernameLabel = QLabel('Snap username:', self)       # type: ignore
        self.snapUsernameLabel.adjustSize()
        self.snapUsernameLabel.move(10, y + 109)

        y -= 140
        x += 7

        self.nextButton = QPushButton('Next', self)       # type: ignore
        self.nextButton.clicked.connect(self.nextFunction)
        self.nextButton.adjustSize()
        self.nextButton.move(x - 60, y + 290)
        self.finishButton = QPushButton('Finish', self)       # type: ignore
        self.finishButton.clicked.connect(self.finishFunction)
        self.finishButton.adjustSize()
        self.finishButton.move(x + 40, y + 290)
        self.finishButton.setDisabled(True)
        self.tryAgainButton = QPushButton('Try again', self)       # type: ignore
        self.tryAgainButton.clicked.connect(self.popUp)
        self.tryAgainButton.adjustSize()
        self.tryAgainButton.move(x - 10, y + 330)

        self.numEmulators = 0
        self.index = 0
        self.indexSnapUsername = 0
        self.fullGmx = []
        self.gmxMails = []
        self.gmxPasswords = []
        self.snapNames = []
        self.snapPasswords = []
        self.snapUsernames = []
        self.usedSnapUsernames = []
        self.fileName = ''
        self.usernames = []

    def popUp(self):
        text, ok = QInputDialog.getText(self, 'Num emulators', 'Enter the number of emulators you want to process:') # type: ignore
        if text.isdigit() == False or text == '0':
            self.processLogContent.setText('You entered the desired number of emulators incorrectly.\nPress button \'Try again\'')
            QApplication.processEvents()       # type: ignore
            self.changeButtons(True)
        else:
            self.numEmulators = int(text)
            self.tryAgainButton.hide()
            self.changeButtons(False)
            self.processLogContent.setText('')
            QApplication.processEvents()       # type: ignore
            self.checkEnoughData()

    def changeButtons(self, flag):
        self.nextButton.setDisabled(flag)
        self.processLogLabel.setDisabled(flag)
        self.copyMailButton.setDisabled(flag)
        self.copyMailPasswordButton.setDisabled(flag)
        self.copySnapNameButton.setDisabled(flag)
        self.copySnapUsernameButton.setDisabled(flag)
        self.copySnapPasswordButton.setDisabled(flag)

    def checkEnoughData(self):
        with open('./gmx.txt', "r") as Reader:
            lines = Reader.readlines()
            if len(lines) < self.numEmulators:
                self.processLogContent.setText('There are not enough gmx mails. You need ' + str(self.numEmulators) + ' mails, but you have only ' + str(len(lines)) + ' mails.')
                QApplication.processEvents()       # type: ignore
                self.changeButtons(True)
                return
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
            self.processLogContent.setText('There are not enough snap usernames. You need ' + str(self.numEmulators) + ' usernames, but you have only ' + str(len(self.snapUsernames)) + ' usernames.')
            QApplication.processEvents()       # type: ignore
            self.changeButtons(True)
            return
        msg = self.gmxMails[self.index] + '\n' + self.gmxPasswords[self.index] + '\n' + self.snapNames[self.index] + '\n' + self.snapPasswords[self.index] + '\n'
        self.msg = self.gmxMails[self.index] + '\n' + self.gmxPasswords[self.index] + '\n' + self.snapNames[self.index] + '\n' + self.snapPasswords[self.index]
        self.processLogContent.setText(msg)
        if self.numEmulators == 1:
            self.nextButton.setDisabled(True)
            self.finishButton.setDisabled(False)

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

    def copyMail(self):
        pyperclip.copy(self.gmxMails[self.index])

    def copyMailPassword(self):
        pyperclip.copy(self.gmxPasswords[self.index])

    def copySnapName(self):
        pyperclip.copy(self.snapNames[self.index])

    def copySnapPassword(self):
        pyperclip.copy(self.snapPasswords[self.index])

    def copySnapUsername(self):
        while True:
            if self.snapUsernames[self.indexSnapUsername] in self.usedSnapUsernames:
                self.indexSnapUsername += 1
                self.indexSnapUsername %= len(self.snapUsernames)
            else:
                break
        if len(self.snapUsernames) > 0:
            pyperclip.copy(self.snapUsernames[self.indexSnapUsername])
            self.snapUsername = self.snapUsernames[self.indexSnapUsername]
            self.processLogContent.setText(self.msg + '\n' + self.snapUsernames[self.indexSnapUsername])
            self.indexSnapUsername += 1
            self.indexSnapUsername %= len(self.snapUsernames)
            QApplication.processEvents()       # type: ignore
        else:
            self.processLogContent.setText('You don\'t have available snap usernames. You have to devise it.')
            QApplication.processEvents()       # type: ignore
            self.copySnapUsernameButton.setDisabled(True)

    def nextFunction(self):
        if self.snapUsername != '':
            self.usedSnapUsernames.append(self.snapUsername)
        with open(self.fileName, 'a') as Writer:
            Writer.write(self.fullGmx[self.index])
            Writer.write(self.snapUsername + ':' + self.snapPasswords[self.index] + '\n' + '\n' + '\n')
        if self.index < self.numEmulators - 1:
            self.index += 1
        msg = self.gmxMails[self.index] + '\n' + self.gmxPasswords[self.index] + '\n' + self.snapNames[self.index] + '\n' + self.snapPasswords[self.index] + '\n' + self.snapUsername
        self.msg = self.gmxMails[self.index] + '\n' + self.gmxPasswords[self.index] + '\n' + self.snapNames[self.index] + '\n' + self.snapPasswords[self.index]
        self.processLogContent.setText(msg)
        if self.index == self.numEmulators - 1:
            self.nextButton.setDisabled(True)
            self.finishButton.setDisabled(False)
        self.usernames.append(self.snapUsername)
        self.snapUsername = ''

    def finishFunction(self):
        self.nextFunction()
        self.finishButton.setDisabled(True)
        self.changeButtons(True)
        with open(self.fileName, 'r') as Reader:
            lines = Reader.readlines()
        with open(self.fileName, 'w') as Writer:
            Writer.writelines(lines[:-2])
        self.processLogContent.setText('Program finished.')
        QApplication.processEvents()       # type: ignore
        with open('../' + self.fileName[3:-4] + ' messages.txt', 'w') as Writer2:
            with open('../Traffic Processor/orders/alba.txt', 'w') as Writer:
                for i in range(0, len(self.usernames)):
                    if i == len(self.usernames) - 1:
                        Writer.write(self.usernames[i])
                        Writer2.write('{hit me up on|add my|add me up on|follow me on|join me on} s.c: ' + self.usernames[i])
                    else:
                        Writer.write(self.usernames[i] + '\n')
                        Writer2.write('{hit me up on|add my|add me up on|follow me on|join me on} s.c: ' + self.usernames[i] + '\n')
        for username in self.usedSnapUsernames:
            if username != '':
                self.snapUsernames.remove(username)
        for i in range(0, len(self.snapUsernames) - 1):
            self.snapUsernames[i] = self.snapUsernames[i] + '\n' 
        with open('./snapUsernames.txt', 'w') as Writer:
            Writer.writelines(self.snapUsernames)

if __name__ == "__main__":
    # Enable high DPI scaling
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])       # type: ignore
    w = Window()
    app.exec_()