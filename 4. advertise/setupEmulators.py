import os
import pyautogui
import random
import shutil
import subprocess
import time
from ppadb.client import Client as AdbClient
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#Window je glavna klasa koja predstavlja nas GUI. Sadrzi tabove, a svaki tab je napravljen kao zasebna klasa
class Window(QTabWidget):
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

#Tab3 je klasa koja predstavlja treci tab na GUI-u, obradjuje spintax
class Tab1(QWidget):
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

        self.getAvailableSnapUsernameButton = QPushButton('Get snap\nusername', self)
        self.getAvailableSnapUsernameButton.clicked.connect(self.getAvailableSnapUsername)
        self.getAvailableSnapUsernameButton.adjustSize()
        self.getAvailableSnapUsernameButton.move(20, 60)
        self.snapUsernameLabel = QLabel('Snap username:', self)
        self.snapUsernameLabel.adjustSize()
        self.snapUsernameLabel.move(130, 70)
        self.snapUsernameLineEdit = QLineEdit('', self)
        self.snapUsernameLineEdit.adjustSize()
        self.snapUsernameLineEdit.move(235, 68)

        self.createNewEmulatorsLabel = QLabel('Num emulators:', self)
        self.createNewEmulatorsLabel.adjustSize()
        self.createNewEmulatorsLabel.move(20, 130)
        self.createNewEmulatorsLineEdit = QLineEdit('', self)
        self.createNewEmulatorsLineEdit.adjustSize()
        self.createNewEmulatorsLineEdit.move(125, 128)
        self.createNewEmulatorsLabel2 = QLabel('From position:', self)
        self.createNewEmulatorsLabel2.adjustSize()
        self.createNewEmulatorsLabel2.move(20, 160)
        self.createNewEmulatorsLineEdit2 = QLineEdit('', self)
        self.createNewEmulatorsLineEdit2.adjustSize()
        self.createNewEmulatorsLineEdit2.move(125, 158)
        self.createNewEmulatorsButton = QPushButton('Create new\nemulators', self)
        self.createNewEmulatorsButton.clicked.connect(self.createNewEmulators)
        self.createNewEmulatorsButton.adjustSize()
        self.createNewEmulatorsButton.move(280, 135)

        self.emulatorsLabelInfo = QLabel('Two possible formats for specific emulators. First is [2-5] and\nsecond one is 2 3 4 5. The first format is provided if the emulators\nare listed in order to make input easier, while the second format\nis for the specified emulators.', self)
        self.emulatorsLabelInfo.adjustSize()
        self.emulatorsLabelInfo.move(20, 200)

        self.emulatorsLabel = QLabel('Emulators:', self)
        self.emulatorsLabel.adjustSize()
        self.emulatorsLabel.move(20, 300)
        self.emulatorsLineEdit = QLineEdit('', self)
        self.emulatorsLineEdit.adjustSize()
        self.emulatorsLineEdit.move(90, 298)

        self.startEmulatorsButton = QPushButton('Start\nemulators', self)
        self.startEmulatorsButton.clicked.connect(self.startEmulators)
        self.startEmulatorsButton.setStyleSheet("color: white; background-color : green")
        self.startEmulatorsButton.adjustSize()
        self.startEmulatorsButton.move(40, 350)

        self.stopEmulatorsButton = QPushButton('Stop\nemulators', self)
        self.stopEmulatorsButton.clicked.connect(self.stopEmulators)
        self.stopEmulatorsButton.setStyleSheet("background-color : red")
        self.stopEmulatorsButton.adjustSize()
        self.stopEmulatorsButton.move(40, 400)

        self.deleteEmulatorsButton = QPushButton('Delete\nemulators', self)
        self.deleteEmulatorsButton.clicked.connect(self.deleteEmulators)
        self.deleteEmulatorsButton.adjustSize()
        self.deleteEmulatorsButton.move(160,375)

        self.numAddsToAcceptLabel = QLabel('Num adds to accept:', self)
        self.numAddsToAcceptLabel.adjustSize()
        self.numAddsToAcceptLabel.move(20, 500)
        self.numAddsToAcceptLineEdit = QLineEdit('', self)
        self.numAddsToAcceptLineEdit.adjustSize()
        self.numAddsToAcceptLineEdit.move(150, 498)

        self.accceptButton = QPushButton('Accept\nadds', self)
        self.accceptButton.clicked.connect(self.acceptAdds)
        self.accceptButton.adjustSize()
        self.accceptButton.move(160, 550)
        
        self.acceptAutomateButton = QPushButton('Accept\nadds A', self)
        self.acceptAutomateButton.clicked.connect(self.acceptAddsAutomate)
        self.acceptAutomateButton.adjustSize()
        self.acceptAutomateButton.move(40, 550)

        self.processLogLabel = QLabel('Process log', self)
        self.processLogLabel.setStyleSheet("background-color : yellow")
        self.processLogLabel.adjustSize()
        self.processLogLabel.move(540, 20)
        self.processLogContent = QTextEdit('Have a good day my friend.', self)
        self.processLogContent.adjustSize()
        self.processLogContent.move(450, 50)

        self.clearGUIButton = QPushButton('Clear\nGUI', self)
        self.clearGUIButton.clicked.connect(self.clearGUI)
        self.clearGUIButton.adjustSize()
        self.clearGUIButton.move(470, 275)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.exitFunction)
        self.exitButton.setStyleSheet("background-color : red")
        self.exitButton.adjustSize()
        self.exitButton.move(600, 280)

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

        self.readSnaps()

    #izlaz iz aplikacije
    def exitFunction(self):
        QApplication.quit()

    def clearGUI(self):
        self.snaps = []
        self.snapUsernameLineEdit.setText('')
        self.processLogContent.setText('')
        self.emulatorsLineEdit.setText('')
        self.createNewEmulatorsLineEdit.setText('')
        self.numAddsToAcceptLineEdit.setText('')
    
    #cita koje usernameove snepova imamo na raspolaganju iz fajla snaps.txt
    def readSnaps(self):
        with open(self.snapsPath, 'r') as Reader:
            lines = Reader.readlines()
        with open(self.snapsPath, 'r') as Reader:
            for i in range(len(lines)):
                self.snaps.append(lines[i].strip('\n'))

    #ukoliko zelimo da prikazemo na gui-u proizvljan dostupan username snepa
    def getAvailableSnapUsername(self):
        if len(self.snaps) == 0:
            self.processLogContent.setText('No more snap username available.')
            QApplication.processEvents()
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

    def createNewEmulators(self):
        if self.createNewEmulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter the number of emulators you want to create.')
            self.processLogContent.adjustSize
            QApplication.processEvents()
        elif self.createNewEmulatorsLineEdit2.text() == '':
            self.processLogContent.setText('Please enter a first empty position for creating emulators.')
            self.processLogContent.adjustSize
            QApplication.processEvents()
        else:
            subprocess.Popen(self.LDMultiplayerPath)
            startTime = time.time()
            i = 0
            numEmulatorsForCreating = int(self.createNewEmulatorsLineEdit.text())
            startingPosition = int(self.createNewEmulatorsLineEdit2.text())
            for e in range(numEmulatorsForCreating): 
                self.processLogContent.setText('Process started. Please wait.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                time.sleep(3)
                #kloniranje
                pyautogui.moveTo(self.LDMultiplayerClonexy[0], self.LDMultiplayerClonexy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerClonexy[0], self.LDMultiplayerClonexy[1])
                time.sleep(2)
                #potvrda kloniranja
                pyautogui.moveTo(self.LDMultiplayerCloneAcceptxy[0], self.LDMultiplayerCloneAcceptxy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerCloneAcceptxy[0], self.LDMultiplayerCloneAcceptxy[1])
                o = 10 + e*15
                if 10 + e*15 > 45:
                    o = 45
                time.sleep(o)
                #oznacavanje teksta gde pise Snapchat-x
                pyautogui.moveTo(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1), 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1))
                time.sleep(1)
                #ponovno oznacavanje teksta gde pise Snapchat-x
                pyautogui.click(self.LDMultiplayerFirstTextxy[0], self.LDMultiplayerFirstTextxy[1] + self.LDMultiplayerDeltaY * (e + startingPosition - 1))
                time.sleep(1)
                #brisanje broja x
                pyautogui.hotkey('backspace')
                time.sleep(2)
                #upis snapchat username-a
                pyautogui.write(self.snaps[i], interval = 0.1)
                i += 1
                self.processLogContent.setText(str(e) + '. emulator was created. Please wait for others.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()
            self.processLogContent.adjustSize()

    def deleteEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to delete.')
            self.processLogContent.adjustSize
            QApplication.processEvents()
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            startTime = time.time()
            first = True
            k = 0
            time.sleep(1)
            for e in self.emulators: 
                self.processLogContent.setText('Process started. Please wait.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                #brisanje emulatora
                pyautogui.moveTo(self.LDMultiplayerDeletexy[0], self.LDMultiplayerDeletexy[1] + self.LDMultiplayerDeltaY * (int(e) - 1 - k), 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerDeletexy[0], self.LDMultiplayerDeletexy[1] + self.LDMultiplayerDeltaY * (int(e) - 1 - k))
                time.sleep(1)
                #potvrda brisanja emulatora
                pyautogui.moveTo(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1])
                time.sleep(4)
                k += 1
                self.processLogContent.setText(str(e) + '. emulator was deleted. Please wait for others.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()
            self.processLogContent.adjustSize()

    def startEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to run.')
            self.processLogContent.adjustSize
            QApplication.processEvents()
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            time.sleep(1)
            startTime = time.time()
            k = 1
            for e in self.emulators:  
                self.processLogContent.setText('Process started. Please wait.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                #pokretanje emulatora
                pyautogui.moveTo(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY, 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY)
                time.sleep(3)
                #kliktaj sa strane
                pyautogui.moveTo(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1])
                self.processLogContent.setText(str(e) + '. emulator is running. Please wait for others.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                o = 17
                if k>2:
                    o = 17 + (k-2)*8
                time.sleep(o)
                k += 1
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()
            self.processLogContent.adjustSize()

    def stopEmulators(self):
        if self.emulatorsLineEdit.text() == '':
            self.processLogContent.setText('Please enter which emulators you want to stop.')
            self.processLogContent.adjustSize
            QApplication.processEvents()
        else:
            self.inputEmulators()
            subprocess.Popen(self.LDMultiplayerPath)
            time.sleep(1)
            startTime = time.time()
            for e in self.emulators:
                self.processLogContent.setText('Process started. Please wait.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                #zaustavljanje pokrenutog emulatora, isto dugme kao i za pokretanje
                pyautogui.moveTo(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY, 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerFirstStartxy[0], self.LDMultiplayerFirstStartxy[1] + (int(e) - 1)*self.LDMultiplayerDeltaY)
                time.sleep(1)
                #dugme za prihvatanje zaustavljanja je isto kao i za prihvatanje brisanja
                pyautogui.moveTo(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerDeleteAcceptxy[0], self.LDMultiplayerDeleteAcceptxy[1])
                time.sleep(3)
                #kliktaj sa strane
                pyautogui.moveTo(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1], 1)
                time.sleep(0.5)
                pyautogui.click(self.LDMultiplayerBlankxy[0], self.LDMultiplayerBlankxy[1])
                self.processLogContent.setText(str(e) + '. emulator is stopped. Please wait for others.')
                QApplication.processEvents()
                self.processLogContent.adjustSize()
                time.sleep(3)
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.processLogContent.setText('The process is complete. Time elapsed: ' + '{:.2f}'.format(elapsedTime))
            QApplication.processEvents()
            self.processLogContent.adjustSize()

    def connectDevices(self):
        #najgluplje resenje ikada
        client = AdbClient(host = "127.0.0.1", port = 5037)
        self.devices = []
        if len(client.devices()) == 1:
            e1 = client.devices()
            self.devices.append(e1)
        elif len(client.devices()) == 2:
            e1, e2 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
        elif len(client.devices()) == 3:
            e1, e2, e3 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
        elif len(client.devices()) == 4:
            e1, e2, e3, e4 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
        elif len(client.devices()) == 5:
            e1, e2, e3, e4, e5 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
        elif len(client.devices()) == 6:
            e1, e2, e3, e4, e5, e6 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
            self.devices.append(e6)
        elif len(client.devices()) == 7:
            e1, e2, e3, e4, e5, e6, e7 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
            self.devices.append(e6)
            self.devices.append(e7)
        elif len(client.devices()) == 8:
            e1, e2, e3, e4, e5, e6, e7, e8 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
            self.devices.append(e6)
            self.devices.append(e7)
            self.devices.append(e8)
        elif len(client.devices()) == 9:
            e1, e2, e3, e4, e5, e6, e7, e8, e9 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
            self.devices.append(e6)
            self.devices.append(e7)
            self.devices.append(e8)
            self.devices.append(e9)
        elif len(client.devices()) == 10:
            e1, e2, e3, e4, e5, e6, e7, e8, e9, e10 = client.devices()
            self.devices.append(e1)
            self.devices.append(e2)
            self.devices.append(e3)
            self.devices.append(e4)
            self.devices.append(e5)
            self.devices.append(e6)
            self.devices.append(e7)
            self.devices.append(e8)
            self.devices.append(e9)
            self.devices.append(e10)
        else:
            self.processLogContent.setText('There are not emulator on.')
            self.processLogContent.adjustSize()
            QApplication.processEvents()
        print(self.devices)
        
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

    def snapchat(self, device, flag, lastTime):
        x = random.randint(-10, 10) + 440
        y = random.randint(-10, 10) + 175
        time.sleep(1)
        device.shell('input keyevent 3')
        time.sleep(3)
        #ulazi u aplikaciju snapchat
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))
        time.sleep(3)
        x = random.randint(-5, 5) + 25
        y = random.randint(-5, 5) + 67
        #ulazi u deo my profile
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))
        x1 = random.randint(-20, 20) + 107
        x2 = x1
        time.sleep(2)
        #svajpuje dole do adova
        device.shell("input swipe " + str(x1) + " 572 " + str(x2) + " 174 2000")
        time.sleep(2)
        x = random.randint(50, 400)
        y = random.randint(630, 670)
        #otvara listu adova
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))

        time.sleep(3)
        x = random.randint(-10, 10) + 253
        y = random.randint(-1, 1) + 583
        #klikce dugme view more
        device.shell('input touchscreen tap ' + str(x) + ' ' + str(y))

        if flag == False:
            self.add(device, 360, 290)
            self.add(device, 360, 400)
            self.add(device, 360, 500)
            self.add(device, 360, 605)
            self.add(device, 360, 710)
            self.add(device, 360, 810)
            self.add(device, 360, 905)
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
        #vraca se sa back dugmetom na profil
        device.shell('input keyevent 4')
        time.sleep(2)
        #vraca se sa back dugmetom na kameru
        device.shell('input keyevent 4')
        time.sleep(2)
        #vraca se na pocetni ekran
        device.shell('input keyevent 4')

    def add(self, device, x, y):
        time.sleep(3)
        x1 = random.randint(-10, 10) + x
        y1 = random.randint(-1, 1) + y
        #prihvata 7. add
        device.shell('input touchscreen tap ' + str(x1) + ' ' + str(y1))

    def logInToSnapchat(self):
        pass

    def acceptAdds(self):
        #self.connectDevices()
        client = AdbClient(host = "127.0.0.1", port = 5037)
        device = client.device("emulator-5556")
        #self.turnOnProxy(device)
        time.sleep(5)
        numAdds = int(self.numAddsToAcceptLineEdit.text())
        numTimes = numAdds//7   
        lastTime = numAdds - numTimes*7
        for i in range(numTimes):
            self.snapchat(device, False, lastTime)
        self.snapchat(device, True, lastTime)

    def acceptAddsAutomate(self):
        subprocess.Popen(self.LDMultiplayerPath)
        client = AdbClient(host = "127.0.0.1", port = 5037)
        #if len(client) == 0:
            #print("No devices attached")
            #quit()
        device = client.device("emulator-5556")
        time.sleep(2)
        #device.shell('input touchscreen tap 400 403')
        #device.shell("input swipe 20 260 20 200 2000")
        device.shell('input touchscreen tap 372 338')
        #x, y = pyautogui.position()

if __name__ == "__main__":
    app = QApplication([])
    w = Window()
    app.exec_()