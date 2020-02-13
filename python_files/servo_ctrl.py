import RPi.GPIO as GPIO
import time

# rotate to that angle


def rotate(self, amount):
    servo.ChangeDutyCycle(2 + float(amount/18))


servoPIN = 11  # change
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

servo = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
servo.start(0)  # Initialization
time.sleep(2)

servo.ChangeDutyCycle(5)
time.sleep(0.5)  # wait to reach
servo.ChangeDutyCycle(0)  # no pulse
time.sleep(0.7)
