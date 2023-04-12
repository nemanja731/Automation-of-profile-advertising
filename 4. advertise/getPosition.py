import win32api
from win32con import *
import pyautogui
import time

x, y = pyautogui.position()
#print('x = ', x, ', y = ', y)
print(str(x) + ', ' + str(y))


