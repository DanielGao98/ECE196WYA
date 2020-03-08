import cv2
import sys
import time
import RPi.GPIO as gpio
from simple_pid import PID
pid = PID(1,0.1,0.05, setpoint = 0)
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

# Checks if the pan_servo is in the max position to the left or right. If its not then it just
# moves the pan_servo to the right until it's in the max right position and then moves it to the
# the max left position.
def scan():
    global currentPos
    global max_right_pos
    global max_left_pos

    if not max_right_pos:
        pan_servo_right()
        if currentPos >= maxPos:
            max_right_pos = True
            max_left_pos = False
    if not max_left_pos:
        pan_servo_left()
        if currentPos <= minPos:
            max_right_pos = False
            max_left_pos = True

# Moves the pan_servo to the left once. But if its already at its max left position (minPos)
# then it won't move left anymore


def pan_servo_left():
    global currentPos
    # Checks to see if its already at the max left (minPos) posistion
    if currentPos > minPos:
        currentPos = currentPos - incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPos)
    time.sleep(.02)  # Sleep because it reduces jitter
    pan_servo.ChangeDutyCycle(0)  # Stop sending a signal pan_servo also to stop jitter

def pid_pan_servo_left():
    global currentPos
    # Checks to see if its already at the max left (minPos) posistion
    if currentPos > minPos:
        currentPos = currentPos - incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPos)
    time.sleep(.02)  # Sleep because it reduces jitter
    pan_servo.ChangeDutyCycle(0)  # Stop sending a signal pan_servo also to stop jitter
# Moves the pan_servo to the left once. But if its already at its max right position (maxPos)
# then it won't move right anymore


def pan_servo_right():
    global currentPos
    # Checks to see if its already at the max right (maxPos) posistion
    if currentPos < maxPos:
        currentPos = currentPos + incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPos)
    time.sleep(.02)  # Sleep because it reduces jitter
    pan_servo.ChangeDutyCycle(0)  # Stop sending a signal pan_servo also to stop jitter

def pid_pan_servo_right():
    global currentPos
    # Checks to see if its already at the max right (maxPos) posistion
    if currentPos < maxPos:
        currentPos = currentPos + incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPos)
    time.sleep(.02)  # Sleep because it reduces jitter
    pan_servo.ChangeDutyCycle(0)  # Stop sending a signal pan_servo also to stop jitter


# If the face is within the predetermined range don't do anything. If its outside of the range
# Adjust the pan_servo so that the face is back in the range again. This is misleading though
# because the pan_SERVO is turning left, however its left is our right and vice-verca.


def track_face(face_position):

    # turn the pan_SERVO to the left (our right)
    if face_position > 100:
        pan_servo_left()

    # turn the pan_SERVO to the right (our left)
    if face_position < -100:
        pan_servo_right()

    time.sleep(.01)
    pan_servo.ChangeDutyCycle(0)

def pid_track_face(face_position):
    global currentPos
    if not (-100 < face_position < 100):
        diff = pid(face_position)
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(CFace)

    # if we found a face send the position to the pan_servo
    if CFace != 0:
        #track_face(CFace)
        pid_track_face(CFace)
    else:
        pass
        # scan()
        # set the value back to zero for the next pass
    CFace = 0


# clean up
gpio.cleanup()
video_capture.release()
cv2.destroyAllWindows()
