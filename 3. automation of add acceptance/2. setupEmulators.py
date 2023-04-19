import os
import pyautogui
import random
import shutil
import subprocess
import time
from ppadb.client import Client as AdbClient
from PyQt5 import QtCore, QtWidgets         # type: ignore 
from PyQt5.QtWidgets import *               # type: ignore 
from PyQt5.QtCore import *                  # type: ignore 
from PyQt5.QtGui import *                   # type: ignore 

#Window is the main class that represents our GUI. It contains tabs, and each tab is created as a separate class
class Window(QTabWidget):                   # type: ignore 
   def __init__(self, parent = None):
      super(Window, self).__init__(parent)

      self.left = 500
      self.top = 190
      self.width = 800
      self.height = 800
      self.setGeometry(self.left, self.top, self.width, self.height)
      self.setWindowTitle("GUI")
      self.tab1 = Tab1()
      self.addTab(self.tab1, 'Acceptor')
      self.show()

#Tab3 is a class that represents the third tab on the GUI, handled by spintax
class Tab1(QWidget):                        # type: ignore 
    def __init__(self):
        super(Tab1, self).__init__()
        self.title = 'Acceptor'
        self.left = 500
        self.top = 190
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupSnaps()
        self.setupCreationOfEmulators()
        self.setupEmulatorsLabelAndInput()
        self.setupEmulatorsButton()
        self.setupOtherButtons()
        self.setupNumAddsAndProcess()
        self.setupVariables()
        self.readSnaps()

    #exit the application
    def exitFunction(self):
        QApplication.quit()                                                                 # type: ignore 

    def setupSnaps(self):
        self.getAvailableSnapUsernameButton = QPushButton('Get snap\nusername', self)       # type: ignore 
        self.getAvailableSnapUsernameButton.clicked.connect(self.getAvailableSnapUsername)
        self.getAvailableSnapUsernameButton.adjustSize()
        self.getAvailableSnapUsernameButton.move(20, 60)
        self.snapUsernameLabel = QLabel('Snap username:', self)                             # type: ignore 
        self.snapUsernameLabel.adjustSize()
        self.snapUsernameLabel.move(130, 70)
        self.snapUsernameLineEdit = QLineEdit('', self)                                     # type: ignore 
        self.snapUsernameLineEdit.adjustSize()
        self.snapUsernameLineEdit.move(235, 68)

    def setupCreationOfEmulators(self):
        self.createNewEmulatorsLabel = QLabel('Num emulators:', self)                       # type: ignore 
        self.createNewEmulatorsLabel.adjustSize()
        self.createNewEmulatorsLabel.move(20, 130)
        self.createNewEmulatorsLineEdit = QLineEdit('', self)                               # type: ignore 
        self.createNewEmulatorsLineEdit.adjustSize()
        self.createNewEmulatorsLineEdit.move(125, 128)
        self.createNewEmulatorsLabel2 = QLabel('From position:', self)                      # type: ignore 
        self.createNewEmulatorsLabel2.adjustSize()
        self.createNewEmulatorsLabel2.move(20, 160)
        self.createNewEmulatorsLineEdit2 = QLineEdit('', self)                              # type: ignore 
        self.createNewEmulatorsLineEdit2.adjustSize()
        self.createNewEmulatorsLineEdit2.move(125, 158)
        self.createNewEmulatorsButton = QPushButton('Create new\nemulators', self)          # type: ignore 
        self.createNewEmulatorsButton.clicked.connect(self.createNewEmulators)
        self.createNewEmulatorsButton.adjustSize()
        self.createNewEmulatorsButton.move(280, 135)

    def setupEmulatorsLabelAndInput(self):
        self.emulatorsLabelInfo = QLabel('Two possible formats for specific emulators. First is [2-5] and\nsecond one is 2 3 4 5. The first format is provided if the emulators\nare listed in order to make input easier, while the second format\nis for the specified emulators.', self) # type: ignore 
        self.emulatorsLabelInfo.adjustSize()
        self.emulatorsLabelInfo.move(20, 200)
        self.emulatorsLabel = QLabel('Emulators:', self)                                # type: ignore 
        self.emulatorsLabel.adjustSize()
        self.emulatorsLabel.move(20, 300)
        self.emulatorsLineEdit = QLineEdit('', self)                                    # type: ignore 
        self.emulatorsLineEdit.adjustSize()
        self.emulatorsLineEdit.move(90, 298)

    def setupEmulatorsButton(self):
        #start button
        self.startEmulatorsButton = QPushButton('Start\nemulators', self)               # type: ignore 
        self.startEmulatorsButton.clicked.connect(self.startEmulators)
        self.startEmulatorsButton.setStyleSheet("color: white; background-color : green")
        self.startEmulatorsButton.adjustSize()
        self.startEmulatorsButton.move(40, 350)
        #stop button
        self.stopEmulatorsButton = QPushButton('Stop\nemulators', self)                 # type: ignore 
        self.stopEmulatorsButton.clicked.connect(self.stopEmulators)
        self.stopEmulatorsButton.setStyleSheet("background-color : red")
        self.stopEmulatorsButton.adjustSize()
        self.stopEmulatorsButton.move(40, 400)
        #delete button
        self.deleteEmulatorsButton = QPushButton('Delete\nemulators', self)             # type: ignore 
        self.deleteEmulatorsButton.clicked.connect(self.deleteEmulators)
        self.deleteEmulatorsButton.adjustSize()
        self.deleteEmulatorsButton.move(160,375)

    def setupVariables(self):
        self.snapsPath = './' + '/snaps.txt'
        self.LDMultiplayerPath = 'C:/LDPlayer/LDPlayer64/dnmultiplayer.exe'
        self.snaps = []
        self.currentSnapID = 0
        self.LDMultiplayerFirstStartxy = [1075, 360]
        self.LDMultiplayerBlankxy = [1261, 358]
        self.LDMultiplayerFirstTextxy = [860, 360]
        self.LDMultiplayerClonexy = [1257, 843]
        self.LDMultiplayerCloneAcceptxy = [1100, 501]
        self.LDMultiplayerDeletexy = [1332, 361]
        self.LDMultiplayerDeleteAcceptxy = [884, 606]
        self.LDMultiplayerDeltaY = 65
        self.emulators = []
        self.devices = []
        self.startFrom = 1

    def setupOtherButtons(self):
        #accept button
        self.accceptButton = QPushButton('Accept\nadds', self)                          # type: ignore 
        self.accceptButton.clicked.connect(self.acceptAdds)
        self.accceptButton.adjustSize()
        self.accceptButton.move(160, 550)
        #automate accept button
        self.acceptAutomateButton = QPushButton('Accept\nadds A', self)                 # type: ignore 
        self.acceptAutomateButton.clicked.connect(self.acceptAddsAutomate)
        self.acceptAutomateButton.adjustSize()
        self.acceptAutomateButton.move(40, 550)
        #clear button
        self.clearGUIButton = QPushButton('Clear\nGUI', self)                           # type: ignore 
        self.clearGUIButton.clicked.connect(self.clearGUI)
        self.clearGUIButton.adjustSize()
        self.clearGUIButton.move(470, 275)
        #exit button
        self.exitButton = QPushButton('Exit', self)                                     # type: ignore 
        self.exitButton.clicked.connect(self.exitFunction)
        self.exitButton.setStyleSheet("background-color : red")
        self.exitButton.adjustSize()
        self.exitButton.move(600, 280)

    def setupNumAddsAndProcess(self):
        #number adds for accepting
        self.numAddsToAcceptLabel = QLabel('Num adds to accept:', self)                 # type: ignore 
        self.numAddsToAcceptLabel.adjustSize()
        self.numAddsToAcceptLabel.move(20, 500)
        self.numAddsToAcceptLineEdit = QLineEdit('', self)                              # type: ignore 
        self.numAddsToAcceptLineEdit.adjustSize()
        self.numAddsToAcceptLineEdit.move(150, 498)
        #log for process
        self.processLogLabel = QLabel('Process log', self)                              # type: ignore 
        self.processLogLabel.setStyleSheet("background-color : yellow")
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(540, 20)
        self.processLogContent = QTextEdit('Have a good day my friend.', self)          # type: ignore 
        self.processLogContent.adjustSize()
        self.processLogContent.move(450, 50)

    def clearGUI(self):
        self.snaps = []
        self.snapUsernameLineEdit.setText('')
        self.processLogContent.setText('')
        self.emulatorsLineEdit.setText('')
        self.createNewEmulatorsLineEdit.setText('')
        self.numAddsToAcceptLineEdit.setText('')
    
    #reads which snap usernames we have available from the snaps.txt file
    def readSnaps(self):
        with open(self.snapsPath, 'r') as Reader:
            lines = Reader.readlines()
        with open(self.snapsPath, 'r') as Reader:
            for i in range(len(lines)):
                self.snaps.append(lines[i].strip('\n'))

    #if we want to display on the gui the generated available snap username
    def getAvailableSnapUsername(self):
        if len(self.snaps) == 0:
            self.processLogContent.setText('No more snap username available.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
        else:
            self.currentSnapID += 1
            self.currentSnapID %= len(self.snaps)
            self.snapUsernameLineEdit.setText(self.snaps[self.currentSnapID])
            self.snapUsernameLineEdit.adjustSize()

    def inputEmulators(self):
        s = self.emulatorsLineEdit.text()
        if s[0] == '[':
            nums = s[1:].split('-')
            nums[1] = nums[1].strip(']')
            for i in range(int(nums[0]), int(nums[1]) + 1):
                self.emulators.append(str(i))
        else:
            self.emulators = s.split(' ')

    def cloningInCreation(self, e):
        #cloning
        pyautogui.moveTo(self.LDMultiplayerClonexy[0], self.LDMultiplayerClonexy[1], 1)
        time.sleep(0.5)
        pyautogui.click(self.LDMultiplayerClonexy[0], self.LDMultiplayerClonexy[1])
        time.sleep(2)
        #cloning confirmation
        pyautogui.moveTo(self.LDMultiplayerCloneAcceptxy[0], self.LDMultiplayerCloneAcceptxy[1], 1)
        time.sleep(0.5)
        pyautogui.click(self.LDMultiplayerCloneAcceptxy[0], self.LDMultiplayerCloneAcceptxy[1])
        o = 10 + e*15
        if 10 + e*15 > 45:
            o = 45
        time.sleep(o)

    def highlightingInCreation(self, e):
        startingPosition = int(self.createNewEmulatorsLineEdit2.text())
        #highlighting the text that says Snapchat-x
        pyautogui.moveTo(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1), 1)
        time.sleep(0.5)
        pyautogui.click(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1))
        time.sleep(1)
        #highlighting the text that says Snapchat-x again
        pyautogui.click(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1))
        time.sleep(1)

    def create(self):
        subprocess.Popen(self.LDMultiplayerPath)
        startTime = time.time()
        i = 0
        numEmulatorsForCreating = int(self.createNewEmulatorsLineEdit.text())
        for e in range(numEmulatorsForCreating): 
            self.processLogContent.setText('Process started. Please wait.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            time.sleep(3)
            self.cloningInCreation(e)
            self.highlightingInCreation(e)
            #deleting number x
            pyautogui.hotkey('backspace')
            time.sleep(2)
            #snapchat username entry
            pyautogui.write(self.snaps[i], interval = 0.1)
            i += 1
            self.processLogContent.setText(str(e) + '. emulator was created. Please wait for others.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
        endTime = time.time()
        elapsedTime = endTime - startTime
        self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
        QApplication.processEvents()                    # type: ignore 
        self.processLogContent.adjustSize()

    def createNewEmulators(self):
        if self.createNewEmulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter the number of emulators you want to create.')
            self.processLogContent.adjustSize
            QApplication.processEvents()                # type: ignore 
        elif self.createNewEmulatorsLineEdit2.text() == '':
            self.processLogContent.setText('Please enter a first empty position for creating emulators.')
            self.processLogContent.adjustSize
            QApplication.processEvents()                # type: ignore 
        else:
            self.create()

    def deleteEmulatorsFunction(self):
        for e in self.emulators: 
            self.processLogContent.setText('Process started. Please wait.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            #delete the emulator
            pyautogui.moveTo(self.LDMultiplayerDeletexy[0], self.LDMultiplayerDeletexy[1] + self.LDMultiplayerDeltaY * (int(e) - 1 - k), 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerDeletexy[0], self.LDMultiplayerDeletexy[1] + self.LDMultiplayerDeltaY * (int(e) - 1 - k))
            time.sleep(1)
            #confirmation of deleting the emulator
            pyautogui.moveTo(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1], 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1])
            time.sleep(4)
            k += 1
            self.processLogContent.setText(str(e) + '. emulator was deleted. Please wait for others.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()

    def deleteEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to delete.')
            self.processLogContent.adjustSize()
            QApplication.processEvents()                # type: ignore 
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            startTime = time.time()
            first = True
            k = 0
            time.sleep(1)
            self.deleteEmulatorsFunction()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()

    def startEmulatorsFunction(self):
        for e in self.emulators:  
            self.processLogContent.setText('Process started. Please wait.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            #running the emulator
            pyautogui.moveTo(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY, 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY)
            time.sleep(3)
            #click on the side
            pyautogui.moveTo(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1], 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1])
            self.processLogContent.setText(str(e) + '. emulator is running. Please wait for others.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            o = 17
            if k>2:
                o = 17 + (k-2)*8
            time.sleep(o)
            k += 1

    def startEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to run.')
            self.processLogContent.adjustSize
            QApplication.processEvents()                # type: ignore 
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            time.sleep(1)
            startTime = time.time()
            k = 1
            self.startEmulatorsFunction()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()

    def stopEmulatorsFunction(self):
        for e in self.emulators:
            self.processLogContent.setText('Process started. Please wait.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            #stop running emulator, same button as start
            pyautogui.moveTo(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY, 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY)
            time.sleep(1)
            #the stop accept button is the same as the delete accept button
            pyautogui.moveTo(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1], 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1])
            time.sleep(3)
            #click on the side
            pyautogui.moveTo(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1], 1)
            time.sleep(0.5)
            pyautogui.click(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1])
            self.processLogContent.setText(str(e) + '. emulator is stopped. Please wait for others.')
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
            time.sleep(3)

    def stopEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to stop.')
            self.processLogContent.adjustSize
            QApplication.processEvents()                # type: ignore 
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            time.sleep(1)
            startTime = time.time()
            self.stopEmulatorsFunction()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()                # type: ignore 
            self.processLogContent.adjustSize()
        
    def turnOnProxy(self, device):
        time.sleep(2)
        device.shell('input keyevent 3')
        time.sleep(3)
        device.shell('input touchscreen tap 315 175')
        time.sleep(8)
        device.shell('input touchscreen tap 465 215')
        time.sleep(1)
        device.shell('input touchscreen tap 465 290')
        time.sleep(5)
        device.shell('input keyevent 4')
        time.sleep(1)

    def goToAdds(self, device):
        #enter the snapchat app
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))
        time.sleep(3)
        x = random.randint(-5, 5) + 25
        y = random.randint(-5, 5) + 67
        #enter the my profile section
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))
        x1 = random.randint(-20, 20) + 107
        x2 = x1
        time.sleep(2)
        #swipes down to adds
        device.shell("input swipe " + str(x1) + " 572 " + str(x2) + " 174 2000")
        time.sleep(2)
        x = random.randint(50, 400)
        y = random.randint(630, 670)
        #opens a list of adds
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))
        time.sleep(3)
        x = random.randint(-10, 10) + 253
        y = random.randint(-1, 1) + 583
        #click the view more button
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))

    def goToSnapchat(self, device, flag, lastTime):
        x = random.randint(-10, 10) + 440
        y = random.randint(-10, 10) + 175
        time.sleep(1)
        device.shell('input keyevent 3')
        time.sleep(3)
        self.goToAdds(device)
        #every time except last
        if flag == False:
            self.add(device, 360, 290)
            self.add(device, 360, 400)
            self.add(device, 360, 500)
            self.add(device, 360, 605)
            self.add(device, 360, 710)
            self.add(device, 360, 810)
            self.add(device, 360, 905)
        #last accepting is different
        else:
            if lastTime >= 1:
                self.add(device, 360, 290)
            if lastTime >= 2:
                self.add(device, 360, 400)
            if lastTime >= 3:
                self.add(device, 360, 500)
            if lastTime >= 4:
                self.add(device, 360, 605)
            if lastTime >= 5:
                self.add(device, 360, 710)
            if lastTime >= 6:
                self.add(device, 360, 810)
            if lastTime == 7:
                self.add(device, 360, 905)

        time.sleep(3)
        #returns to the profile with the back button
        device.shell('input keyevent 4')
        time.sleep(2)
        #returns to the camera with the back button
        device.shell('input keyevent 4')
        time.sleep(2)
        #returns to the home screen
        device.shell('input keyevent 4')

    def add(self, device, x, y):
        time.sleep(3)
        x1 = random.randint(-10, 10) + x
        y1 = random.randint(-1, 1) + y
        #accepts the 7th add
        device.shell('input touchscreen tap ' + str(x1) + ' ' + str(y1))

    def acceptAdds(self):
        client = AdbClient(host = "127.0.0.1", port = 5037)
        device = client.device("emulator-5556")
        self.turnOnProxy(device)
        time.sleep(5)
        numAdds = int(self.numAddsToAcceptLineEdit.text())
        numTimes = numAdds//7   
        lastTime = numAdds - numTimes*7
        for i in range(numTimes):
            self.goToSnapchat(device, False, lastTime)
        self.goToSnapchat(device, True, lastTime)

    def acceptAddsAutomate(self):
        subprocess.Popen(self.LDMultiplayerPath)
        client = AdbClient(host = "127.0.0.1", port = 5037)
        if len(client) == 0:
            print("No devices attached")
            quit()
        device = client.device("emulator-5556")
        time.sleep(2)
        device.shell('input touchscreen tap 400 403')
        device.shell("input swipe 20 260 20 200 2000")
        device.shell('input touchscreen tap 372 338')
        x, y = pyautogui.position()

if __name__ == "__main__":
    app = QApplication([])      # type: ignore 
    w = Window()
    app.exec_()