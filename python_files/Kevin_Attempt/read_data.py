import pyrebase
import cv2
import numpy as np
import time
config = {
  "apiKey": "AIzaSyDQUF3pJGSI_CEflk2n8OV1DOa3m_R72uE",
  "authDomain": "ece196wya.firebaseapp.com",
  "databaseURL": "https://ece196wya.firebaseio.com",
  "storageBucket": "ece196wya.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


while True:
  time.sleep(0.1)
  frame = np.asarray(db.child("frame").get().val())
  print(frame)
  print(frame.shape)
  cv2.imshow('frame',frame)
  cv2.waitKey(0)
  '''
  try:
    cv2.imshow('frame',frame)

    key = cv2.waitKey(1) & 0xFF
    if key == '27':
      break
    print("frame = ", frame)
  except:
    print("Empty arrays")

cv2.destroyAllWindows()
'''

