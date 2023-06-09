import codecs
import os
import pyperclip
import re
from PyQt5 import QtWidgets, QtCore             # type: ignore
from PyQt5 import QtWidgets                     # type: ignore
from PyQt5.QtWidgets import *                   # type: ignore
from PyQt5.QtCore import *                      # type: ignore
from PyQt5.QtGui import *                       # type: ignore

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
        self.width = 330
        self.height = 190
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(QSize(self.width, self.height))       # type: ignore 
        self.setWindowTitle('Export Processor')
        self.setPositions()
        self.numTokens = []
        self.numGhosts = []
        self.numAdds = []

    def setPositions(self):
        x = 70
        y = 20

        self.copyDataButton = QPushButton('Copy\ndata', self)       # type: ignore
        self.copyDataButton.clicked.connect(self.copyData)
        self.copyDataButton.adjustSize()
        self.copyDataButton.move(x + 42, y)
        
        x += 30
        y += 20

        self.processLogLabel = QLabel('', self)       # type: ignore
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(x + 10, y + 10)
        self.processLogContent = QTextEdit('', self)       # type: ignore
        self.processLogContent.adjustSize()
        self.processLogContent.move(x - 85, y + 40)
        self.processLogContent.resize(298, 90)

    def checkButton(self, box, buttonC, buttonY, buttonN, buttonCl):
        if box.clickedButton() == buttonC:
            self.processLogContent.setText("Export canceled.")
            QApplication.processEvents()       # type: ignore
        else:
            if box.clickedButton() == buttonY:
                self.indexes = [1, 2, 3, 4, 5, 6]
            elif box.clickedButton() == buttonN:
                self.indexes = [7, 8, 9, 10, 11, 12]
            elif box.clickedButton() == buttonCl:
                text, ok = QInputDialog.getText(self, 'Custom range', 'Enter the range in the specified format, example: 9-12\nJust number-number, don\'t add space anywhere.')     # type: ignore
                x = re.search("^[1-9]+[0-9]*\-[1-9]+[0-9]*$", text)
                if x == None:
                    self.processLogContent.setText('Custom didn\'t execute because of incorrect input. Try again.')
                    QApplication.processEvents()       # type: ignore
                    return False
                begin, end = text.split("-")
                for i in range(int(begin), int(end) + 1):
                    self.indexes.append(i)

    def otherChecks(self):
        if len(self.indexes) == 0:
            self.processLogContent.setText('You have aborted export operation. Try again.')
            QApplication.processEvents()       # type: ignore
            return False
        if os.path.isfile(self.ATPath) == False:
            self.processLogContent.setText("There are not AT.txt file on desktop.")
            QApplication.processEvents()       # type: ignore
            self.copyDataButton.setDisabled(True)
            return False
        with open(self.ATPath, 'r') as Reader:
            lines = Reader.readlines()
            if len(lines) < 3:
                self.processLogContent.setText("There are not at least 3 lines in AT.txt file on desktop.")
                QApplication.processEvents()       # type: ignore
                self.copyDataButton.setDisabled(True)
                return False

    def popUp(self):
        desktopRealPath = os.path.expanduser("~/Desktop")
        desktopPath = ''
        for i in range(0, len(desktopRealPath)):
            if desktopRealPath[i] == '\\':
                desktopPath += '/'
            else:
                desktopPath += desktopRealPath[i]
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Question)
        box.setWindowTitle('Export')
        box.setText('To which instances do you want to export the final folder?')
        box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Close|QtWidgets.QMessageBox.Cancel)
        buttonY = box.button(QtWidgets.QMessageBox.Yes)
        buttonY.setText('1-6')
        buttonN = box.button(QtWidgets.QMessageBox.No)
        buttonN.setText('7-12')
        buttonCl = box.button(QtWidgets.QMessageBox.Close)
        buttonCl.setText('Custom')
        buttonC = box.button(QtWidgets.QMessageBox.Cancel)
        box.exec_()
        self.indexes = []
        self.execute(box, buttonC, buttonY, buttonN, buttonCl, desktopPath)

    def execute(self, box, buttonC, buttonY, buttonN, buttonCl, desktopPath):
        self.ATPath = desktopPath + '/AT.txt'
        self.desktopUnusedEmailsPath = desktopPath + '/unused emails.txt'
        self.checkButton()
        self.otherChecks()
        self.ATFunction()
        for i in range(0, len(self.indexes)):
            self.accountPath = desktopPath + '/Instances/Instance #' + str(self.indexes[i]) + '/datastore/session/Accounts.txt'
            self.unusedEmailsPath = desktopPath + '/Instances/Instance #' + str(self.indexes[i]) + '/datastore/UnusedEmailAddresses.txt'
            self.accountsFunction()
            self.emailsFunction()
        self.processLogContent.setText("Export finished.")
        QApplication.processEvents()       # type: ignore

    def accountsFunction(self):
        if os.path.isfile(self.accountPath) == False:
            self.numTokens.append('0')
            return
        lines = codecs.open(self.accountPath, "r", "utf-16").readlines()
        if len(lines) < 2:
            self.numTokens.append('0')
            return
        self.numTokens.append(str(len(lines) - 1))
        ghost = 0
        for i in range(0, len(lines) - 1):
            found = re.search(r":\d+:\d+:", lines[i])
            if found is not None:
                found = found.group(0).split(':')
                like, match = int(found[1]), int(found[2])
            else:
                print('Problem with finding adds in line ' + str(i))
                return False
            if like == 99 and match > 0 or like >= 50 and match >= 30:
                pass
            else:
                ghost += 1
        self.numGhosts.append(str(ghost))

    def emailsFunction(self):
        if os.path.isfile(self.unusedEmailsPath) == False:
            return
        lines = codecs.open(self.unusedEmailsPath, "r", "utf-16").readlines()
        if len(lines) < 2:
            return
        with open(self.desktopUnusedEmailsPath, 'a') as Appender:
            for line in lines:
                Appender.write('\n' + line[:-2])

    def ATFunction(self):
        with open(self.ATPath, 'r') as Reader:
            lines = Reader.readlines()
        for i in range(3, 4*len(self.indexes), 4):
            num = lines[i - 1].split(' ')
            self.numAdds.append(num[0])
            
    def copyData(self):
        msg = ''
        print('List of tokens:')
        print(self.numTokens)
        print('Lista of ghosts:')
        print(self.numGhosts)
        print('Lista of adds:')
        print(self.numAdds)
        for i in range(0, len(self.numTokens)):
            msg += self.numTokens[i] + ':' + self.numGhosts[i] + ':' + self.numAdds[i] + '\n'
        msg = msg.rstrip('\n')
        pyperclip.copy(msg)

if __name__ == "__main__":
    # Enable high DPI scaling
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])       # type: ignore
    w = Window()
    app.exec_()
