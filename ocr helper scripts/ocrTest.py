import cv2

imgFile = "./1.jpg"
img = cv2.imread(imgFile)
eyeClassifier = './venv/Lib/site-packages/cv2/data/haarcascade_eye.xml'
eyeGlassesClassifier = './venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml'
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
eyeTracker = cv2.CascadeClassifier(eyeClassifier)
eyeGlassesTracker = cv2.CascadeClassifier(eyeGlassesClassifier)
eye = eyeTracker.detectMultiScale(grayImg)
glasses = eyeGlassesTracker.detectMultiScale(grayImg)
print(eye)
print(len(eye))
print(glasses)
for (x,y,w,h) in eye:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), -1)
    cv2.putText(img, 'Eye', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
for (x,y,w,h) in glasses:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
    cv2.putText(img, 'Glasses', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.imshow('my detection', img)
cv2.waitKey()