import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
while True:
        _, img = cap.read()
        faces = face_cascade.detectMultiScale(img, 1.1)

        for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_color = img[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_color, 1.2, 20)
                for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                smile = smile_cascade.detectMultiScale(roi_color, 1.8, 33)
                for (sx,sy,sw,sh) in smile:
                        cv2.rectangle(roi_color, (sx,sy),(sx+sw,sy+sh),(0,0,255),2)    

                
        cv2.imshow("test", img)
        k =cv2.waitKey(15)
        if k ==27:
                break

cap.release()
cv2.destroyAllWindows()

