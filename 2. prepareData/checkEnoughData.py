import os
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

#class for spintax
class Window(QWidget): # type: ignore
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.initUI()
        self.check()
        self.show()

    def initUI(self):
        self.left = 700
        self.top = 300
        self.width = 480
        self.height = 210
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(QSize(self.width, self.height))       # type: ignore 
        self.setWindowTitle('Check enough data')

        x = 0
        y = 0

        self.processLogLabel = QLabel('', self)       # type: ignore
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(x + 10, y + 10)
        self.processLogContent = QTextEdit('', self)       # type: ignore
        self.processLogContent.adjustSize()
        self.processLogContent.move(x + 90, y + 40)
        self.processLogContent.resize(300,130)

    def check(self):
        gmxPath = './First Processor/gmx.txt'
        mailsPath = './Traffic Processor/data/files/EmailAddresses.txt'
        biographiesPath = './Traffic Processor/data/files/BioData.txt'
        firstNamesPath = './Traffic Processor/data/files/FirstNames.txt'
        with open(gmxPath, 'r') as Reader:
            lines = Reader.readlines()
        numGmx = len(lines)
        with open(mailsPath, 'r') as Reader:
            lines = Reader.readlines()
        numMails = len(lines)
        with open(biographiesPath, 'r') as Reader:
            lines = Reader.readlines()
        numBiographies = len(lines)
        with open(firstNamesPath, 'r') as Reader:
            lines = Reader.readlines()
        numNames = len(lines)
        msg = '\t       There are:\n\n'
        msg += str(numGmx) + ' lines available from file gmx.txt\n'
        msg += str(numMails) + ' lines available from file EmailAddresses.txt\n'
        msg += str(numNames) + ' lines available from file FirstNames.txt\n'
        msg += str(numBiographies) + ' lines available from file BioData.txt'
        self.processLogContent.setText(msg)

if __name__ == "__main__":
        # Enable high DPI scaling
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])       # type: ignore
    w = Window()
    app.exec_()
