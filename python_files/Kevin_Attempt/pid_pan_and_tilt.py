import cv2
import sys
import time
import RPi.GPIO as gpio
from simple_pid import PID

display = False

currentPosX = 8.5
currentPosY = 7.5

# pan_servo setup
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
pan_servo = gpio.PWM(11, 50)
pan_servo.start(currentPosX)
time.sleep(0.1)
pan_servo.ChangeDutyCycle(0)
time.sleep(0.1)

gpio.setup(7, gpio.OUT)
tilt_servo = gpio.PWM(7, 50)
tilt_servo.start(currentPosY)
time.sleep(0.1)
tilt_servo.ChangeDutyCycle(0)
time.sleep(0.1)

#arrays and such
minPos = 3  # This is the most left position within non-breakage range for the pan_servo
maxPos = 11.5  # This is the most right position within non-breakage range for the pan_servo
#currentPosX = 7.5
#currentPosY = 7.5
CFaceX = 0
CFaceY = 0

# webcam face detection
#cascPath = sys.argv[1]
cascPath = '/home/wya/Desktop/ECE196WYA/python_files/Kevin_Attempt/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
#camera = picamera.PiCamera()
time.sleep(2)


#video_capture.set(3, 320)
#video_capture.set(4, 240)

# Functions

# Moves the pan_servo to the left once. But if its already at its max left position (minPos)
# then it won't move left anymore

def pid_track_face_X(X_position):
    global currentPosX
    if not (-50 < X_position < 50):
        X_diff = -(X_position)*0.00045
        #print(f'X_diff = {X_diff}')
        if minPos < (currentPosX+X_diff) < maxPos:
            #print(f"X = {currentPosX} ")
            currentPosX = currentPosX + X_diff
        pan_servo.ChangeDutyCycle(currentPosX)
        time.sleep(0.01)
        pan_servo.ChangeDutyCycle(0)
        time.sleep(0.02)
def pid_track_face_Y(Y_position):
    global currentPosY
    if not (-30 < Y_position < 30):
        Y_diff = -(Y_position)*0.0004
        #print(f'Y_diff = {Y_diff}')
        if minPos < (currentPosY+Y_diff) < maxPos:
            #print(f"Y = {currentPosY}")
            currentPosY = currentPosY + Y_diff
            #print(f'currentY = {currentPosY}')
        tilt_servo.ChangeDutyCycle(currentPosY)
        time.sleep(0.01)
        tilt_servo.ChangeDutyCycle(0)
        time.sleep(0.02)
while True:
    # capture frame by frame
    ret, frame = video_capture.read()

    # find the position of the face
    face = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.3,
        minNeighbors=1,
        minSize=(40, 40),
        flags=(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH + cv2.CASCADE_SCALE_IMAGE))
    # draw the rectangle around and face find the center of the face (CFace)
    try:
        (x, y, w, h) =face[0]
        if display:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness = 5)
        CFaceX = (w/2+x) - 640/2
        CFaceY = (h/2+y) - 480/2
    except:
        pass
    # display the resulting frame
    
    if display:    
        cv2.imshow('Video', cv2.flip(frame, 1))
        print(f"X = {currentPosX} Y = {currentPosY}") 
    if cv2.waitKey(1) == 27:
        break


    # if we found a face send the position to the pan_servo
    if CFaceX != 0:
        pid_track_face_X(CFaceX)
    if CFaceY != 0:
        pid_track_face_Y(CFaceY)
        #print(CFaceX, CFaceY)
    CFaceX = 0
    CFaceY = 0


# clean up
gpio.cleanup()
video_capture.release()
cv2.destroyAllWindows()
