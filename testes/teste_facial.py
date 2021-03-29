import cv2

img = cv2.imread("3.jpg")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
faces = face_cascade.detectMultiScale(img, 1.3)

for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_color, 1.2, 20)
        for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        smile = smile_cascade.detectMultiScale(roi_color, 1.8, 30)
        print(len(smile))
        for (sx,sy,sw,sh) in smile:
                cv2.rectangle(roi_color, (sx,sy),(sx+sw,sy+sh),(0,0,255),2)    

        
cv2.imshow("test", img)

