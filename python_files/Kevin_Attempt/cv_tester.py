import cv2
import time
import pyrebase
import threading
import numpy as np


class MyThread(threading.Thread):
    '''
    def __init__(self):
        super().__init__()
        self.config = {
                    "apiKey": "AIzaSyDQUF3pJGSI_CEflk2n8OV1DOa3m_R72uE",
                    "authDomain": "ece196wya.firebaseapp.com",
                    "databaseURL": "https://ece196wya.firebaseio.com",
                    "storageBucket": "ece196wya.appspot.com"
                }

        self.firebase = pyrebase.initialize_app(config)

        self.db = firebase.database()

        self.frame = np.zeros([1,1])
        self.data = {"arr": [[1,2], [3,4]]}

    '''
    def run(self):
        global frame_resize
        global db
        data = {"frame": frame_resize.tolist()}
        #self.data = {"frame": list(self.frame)}
        db.update(data)


def callback():
    global frame
    global db

    data = {"frame": frame.tolist()}
    if data is not None:
        db.update(data)


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
frame = np.zeros([1,1])


'''
temp = np.ones([2,2])
print(list(temp))

exit()
'''

'''
thread = threading.Thread(target = callback)
thread.start()
'''
count = 0
frame_resize = []

while True:
    _ , frame = cam.read()
    '''
    data = {"frame": list(frame)}
    if data is not None:
        db.update(data)
    ''' 

    '''
    data = {"arr": count}
    db.update(data)
    count += 1
    '''
    #thread.run(target = callback)

    if frame is not None:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resize = cv2.resize(frame_gray, (100,100), interpolation = cv2.INTER_AREA)   

        myThread = MyThread(name = "Thread-{}".format(count))
        #myThread.frame = frame
        myThread.run()
        count += 1
        #time.sleep(0.5)

    print("frame...count = ", count)
    #cv2.imshow("frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()

