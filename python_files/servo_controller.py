import RPi.GPIO as GPIO
import time

# rotate to that angle


class servo_controller:
    def __init__(self):
        self.servoPIN = 11  # change
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servoPIN, GPIO.OUT)

        self.servo = GPIO.PWM(self.servoPIN, 50)  # GPIO 11 for PWM with 50Hz
        self.servo.start(0)  # Initialization
        time.sleep(2)

    def rotate(self, amount):
        self.servo.ChangeDutyCycle(2 + float(amount/18))
        self.wait()

    def wait(self):
        self.servo.ChangeDutyCycle(0)
        time.sleep(0.5)

    def stop(self):
        servo.stop()
        GPIO.cleanup()
