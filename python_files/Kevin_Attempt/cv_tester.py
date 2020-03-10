import cv2
import time
import pyrebase

config = {
  "apiKey": "AIzaSyDQUF3pJGSI_CEflk2n8OV1DOa3m_R72uE",
  "authDomain": "ece196wya.firebaseapp.com",
  "databaseURL": "https://ece196wya.firebaseio.com",
  "storageBucket": "ece196wya.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


data = {"name": "mortimer morty smith"}
data = {"arr": [[1,2], [3,4]]}
db.update(data)


cam = cv2.VideoCapture(0)

while True:
    _ , frame = cam.read()
    data = frame
    db.update(data)
    #cv2.imshow("frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()

