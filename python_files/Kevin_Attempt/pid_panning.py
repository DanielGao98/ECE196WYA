import cv2
import sys
import time
import RPi.GPIO as gpio
from simple_pid import PID
# pan_servo setup
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
pan_servo = gpio.PWM(11, 50)
pan_servo.start(7.5)
pan_servo.ChangeDutyCycle(0)


#arrays and such
currentPos = 7.5
CFace = 0
max_right_pos = False
max_left_pos = True
minPos = 3  # This is the most left position within non-breakage range for the pan_servo
maxPos = 11.5  # This is the most right position within non-breakage range for the pan_servo
rangeRight = 230  # This refers the the X range for the face detection
rangeLeft = 140  # Same as reangeRight.

# If it's moving to fast and not stoping on a face mess with this variable The higher the number
# the bigger the increment it will move.
incrementpan_Servo = .15

# webcam face detection
#cascPath = sys.argv[1]
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
#camera = picamera.PiCamera()
time.sleep(2)


#video_capture.set(3, 320)
#video_capture.set(4, 240)

# Functions

# Moves the pan_servo to the left once. But if its already at its max left position (minPos)
# then it won't move left anymore

def pid_track_face(face_position):
    global currentPos
    if not (-50 < face_position < 50):
        diff = -(face_position)*0.00025
        print(f'diff = {diff}')
        currentPos = currentPos + diff
        pan_servo.ChangeDutyCycle(currentPos)
        time.sleep(.01)
        pan_servo.ChangeDutyCycle(0)

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
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
        CFace = (w/2+x) - 640/2

    # display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == 27:
        break


    # if we found a face send the position to the pan_servo
    if CFace != 0:
        pid_track_face(CFace)
        print(CFace)
    CFace = 0


# clean up
gpio.cleanup()
video_capture.release()
cv2.destroyAllWindows()
