from ppadb.client import Client as AdbClient
import time
import subprocess

#path = 'C:/LDPlayer/LDPlayer64/dnmultiplayer.exe'
#subprocess.Popen(path)

client = AdbClient(host = "127.0.0.1", port = 5037)
#if len(client) == 0:
    #print("No devices attached")
    #quit()
device = client.device("emulator-5556")
time.sleep(2)
#device.shell('input touchscreen tap 400 403')
#device.shell("input swipe 20 260 20 200 2000")
device.shell('input touchscreen tap 372 338')
"""
time.sleep(1)
device.shell('input touchscreen tap 440 172')
time.sleep(1)
device.shell('input keyevent 4')
time.sleep(1)
device.shell('input keyevent 4')
time.sleep(1)
#koordinate za ulaz u adove
#UBACI RANDOM
device.shell('input touchscreen tap 410 60')
"""


"""
time.sleep(1)
device.shell('input touchscreen tap 145 195')
time.sleep(1)
device.shell('input touchscreen tap 135 165')
time.sleep(1)
device.shell('input touchscreen tap 1240 65')
time.sleep(1)
device.shell('input touchscreen tap 200 73')
time.sleep(1)
device.shell('input text "Neca%scar"')
time.sleep(1)
device.shell('input keyevent 66')

#mis na odredjenu poziciju t vremena se prebacuje tu
pyautogui.moveTo(x, y, t)
#kliktanje jednom
pyautogui.click(x, y)
#dupli klik
pyautogui.click(x, y, clicks = 2)
#skrol na dole
pyautogui.scroll(-100)
#nadji poziciju misa
x, y = pyautogui.position()

#emulator
#klikni na x, y poziciju
device.shell('input touchscreen tap x y')
#unesi tekst (%s je razmak)
device.shell('input text "Neca%scar"')
#uradi naredbu key = 66 sto je enter
device.shell('input keyevent 66')
#skroluje misa na dole
device.shell("input swipe " + x22 + y22 + x11 + y11 + swipeTime2)

0 -->  "KEYCODE_UNKNOWN" 
1 -->  "KEYCODE_MENU" 
2 -->  "KEYCODE_SOFT_RIGHT" 
3 -->  "KEYCODE_HOME" 
4 -->  "KEYCODE_BACK" 
5 -->  "KEYCODE_CALL" 
6 -->  "KEYCODE_ENDCALL" 
7 -->  "KEYCODE_0" 
8 -->  "KEYCODE_1" 
9 -->  "KEYCODE_2" 
10 -->  "KEYCODE_3" 
11 -->  "KEYCODE_4" 
12 -->  "KEYCODE_5" 
13 -->  "KEYCODE_6" 
14 -->  "KEYCODE_7" 
15 -->  "KEYCODE_8" 
16 -->  "KEYCODE_9" 
17 -->  "KEYCODE_STAR" 
18 -->  "KEYCODE_POUND" 
19 -->  "KEYCODE_DPAD_UP" 
20 -->  "KEYCODE_DPAD_DOWN" 
21 -->  "KEYCODE_DPAD_LEFT" 
22 -->  "KEYCODE_DPAD_RIGHT" 
23 -->  "KEYCODE_DPAD_CENTER" 
24 -->  "KEYCODE_VOLUME_UP" 
25 -->  "KEYCODE_VOLUME_DOWN" 
26 -->  "KEYCODE_POWER" 
27 -->  "KEYCODE_CAMERA" 
28 -->  "KEYCODE_CLEAR" 
29 -->  "KEYCODE_A" 
30 -->  "KEYCODE_B" 
31 -->  "KEYCODE_C" 
32 -->  "KEYCODE_D" 
33 -->  "KEYCODE_E" 
34 -->  "KEYCODE_F" 
35 -->  "KEYCODE_G" 
36 -->  "KEYCODE_H" 
37 -->  "KEYCODE_I" 
38 -->  "KEYCODE_J" 
39 -->  "KEYCODE_K" 
40 -->  "KEYCODE_L" 
41 -->  "KEYCODE_M" 
42 -->  "KEYCODE_N" 
43 -->  "KEYCODE_O" 
44 -->  "KEYCODE_P" 
45 -->  "KEYCODE_Q" 
46 -->  "KEYCODE_R" 
47 -->  "KEYCODE_S" 
48 -->  "KEYCODE_T" 
49 -->  "KEYCODE_U" 
50 -->  "KEYCODE_V" 
51 -->  "KEYCODE_W" 
52 -->  "KEYCODE_X" 
53 -->  "KEYCODE_Y" 
54 -->  "KEYCODE_Z" 
55 -->  "KEYCODE_COMMA" 
56 -->  "KEYCODE_PERIOD" 
57 -->  "KEYCODE_ALT_LEFT" 
58 -->  "KEYCODE_ALT_RIGHT" 
59 -->  "KEYCODE_SHIFT_LEFT" 
60 -->  "KEYCODE_SHIFT_RIGHT" 
61 -->  "KEYCODE_TAB" 
62 -->  "KEYCODE_SPACE" 
63 -->  "KEYCODE_SYM" 
64 -->  "KEYCODE_EXPLORER" 
65 -->  "KEYCODE_ENVELOPE" 
66 -->  "KEYCODE_ENTER"
67 -->  "KEYCODE_DEL" 
68 -->  "KEYCODE_GRAVE" 
69 -->  "KEYCODE_MINUS" 
70 -->  "KEYCODE_EQUALS" 
71 -->  "KEYCODE_LEFT_BRACKET" 
72 -->  "KEYCODE_RIGHT_BRACKET" 
73 -->  "KEYCODE_BACKSLASH" 
74 -->  "KEYCODE_SEMICOLON" 
75 -->  "KEYCODE_APOSTROPHE" 
76 -->  "KEYCODE_SLASH" 
77 -->  "KEYCODE_AT" 
78 -->  "KEYCODE_NUM" 
79 -->  "KEYCODE_HEADSETHOOK" 
80 -->  "KEYCODE_FOCUS" 
81 -->  "KEYCODE_PLUS" 
82 -->  "KEYCODE_MENU" 
83 -->  "KEYCODE_NOTIFICATION" 
84 -->  "KEYCODE_SEARCH" 
85 -->  "TAG_LAST_KEYCODE"
"""