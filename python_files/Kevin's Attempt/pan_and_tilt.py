import cv2
import sys
import time
import RPi.GPIO as gpio

# pan_servo setup
gpio.setmode(gpio.BOARD)

gpio.setup(11, gpio.OUT)
pan_servo = gpio.PWM(11, 50)
pan_servo.start(7.5)
pan_servo.ChangeDutyCycle(0)

# tilt servo setup
gpio.setup(7, gpio.OUT)
tilt_servo = gpio.PWM(7, 50)
tilt_servo.start(7.5)
tilt_servo.ChangeDutyCycle(0)


#arrays and such
currentPosX = 7.5
currentPosY = 7.5
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

# Moves the pan_servo to the left once. But if its already at its max left position (minPos)
# then it won't move left anymore


def pan_servo_left():
    global currentPosX
    # Checks to see if its already at the max left (minPos) posistion
    print('go left')
    if currentPosX > minPos:
        print("GOING LEFT")
        currentPosX = currentPosX - incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPosX)
    time.sleep(.02)  # Sleep because it reduces jitter
    # Stop sending a signal pan_servo also to stop jitter
    pan_servo.ChangeDutyCycle(0)

# Moves the pan_servo to the left once. But if its already at its max right position (maxPos)
# then it won't move right anymore


def pan_servo_right():
    global currentPosX
    print('go right')
    # Checks to see if its already at the max right (maxPos) posistion
    if currentPosX < maxPos:
        print('GOING RIGHT')
        currentPosX = currentPosX + incrementpan_Servo
        pan_servo.ChangeDutyCycle(currentPosX)
    time.sleep(.02)  # Sleep because it reduces jitter
    # Stop sending a signal pan_servo also to stop jitter
    pan_servo.ChangeDutyCycle(0)


def tilt_servo_up():
    global currentPosY
    # Checks to see if its already at the max left (minPos) posistion
    if currentPosY > minPos:
        currentPosY = currentPosY - incrementpan_Servo
        tilt_servo.ChangeDutyCycle(currentPosY)
    time.sleep(.02)  # Sleep because it reduces jitter
    # Stop sending a signal pan_servo also to stop jitter
    tilt_servo.ChangeDutyCycle(0)

# Moves the pan_servo to the left once. But if its already at its max right position (maxPos)
# then it won't move right anymore


def tilt_servo_down():
    global currentPosY
    # Checks to see if its already at the max right (maxPos) posistion
    if currentPosY < maxPos:
        currentPosY = currentPosY + incrementpan_Servo
        tilt_servo.ChangeDutyCycle(currentPosY)
    time.sleep(.02)  # Sleep because it reduces jitter
    # Stop sending a signal pan_servo also to stop jitter
    tilt_servo.ChangeDutyCycle(0)


# If the face is within the predetermined range don't do anything. If its outside of the range
# Adjust the pan_servo so that the face is back in the range again. This is misleading though
# because the pan_SERVO is turning left, however its left is our right and vice-verca.


def track_face(face_positionX, face_positionY):

    # turn the pan_SERVO to the left (our right)
    if face_positionX > 100:
        pan_servo_left()

    # turn the pan_SERVO to the right (our left)
    if face_positionX < -100:
        pan_servo_right()

    # turn the pan_SERVO to the left (our right)
    if face_positionY > 100:
        tilt_servo_down()

    # turn the pan_SERVO to the right (our left)
    if face_positionY < -100:
        tilt_servo_up()

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
        CFaceX = (w/2+x) - 640/2
        CFaceY = (h/2+y) - 480/2

    # display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(CFaceX, CFaceY)

    # if we found a face send the position to the pan_servo
    if CFace != 0:
        track_face(CFaceX, CFaceY)

    else:
        pass
        # stay

    CFaceX = 0
    CFaceY = 0

# clean up
gpio.cleanup()
video_capture.release()
cv2.destroyAllWindows()
