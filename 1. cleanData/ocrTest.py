import cv2

img_file = "./1.jpg"
img = cv2.imread(img_file)
eye_classifier = './venv/Lib/site-packages/cv2/data/haarcascade_eye.xml'
eye_glasses_classifier = './venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml'
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
eye_tracker = cv2.CascadeClassifier(eye_classifier)
eye_glasses_tracker = cv2.CascadeClassifier(eye_glasses_classifier)
eye = eye_tracker.detectMultiScale(gray_img)
glasses = eye_glasses_tracker.detectMultiScale(gray_img)
print(eye)
print(len(eye))
#print(glasses)
#for (x,y,w,h) in eye:
    #cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), -1)
    #cv2.putText(img, 'Eye', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
for (x,y,w,h) in glasses:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
    cv2.putText(img, 'Glasses', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.imshow('my detection', img)
cv2.waitKey()