import RPi.GPIO as GPIO
import time

class servo_controller:

    def __init__(self):
        print("init servo_controller")
        self.servoPIN = 11  # change
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        
        self.servo = GPIO.PWM(self.servoPIN, 50)  # GPIO 11 for PWM with 50Hz
        self.servo.start(0)  # Initialization
        time.sleep(2) # wait 2 seconds
        self.reset()
        print("servo initialized and reset")

    def show(self):
        print("show()")

    def rotate(self, amount):
        if float(amount) < 0 or float(amount) > 180:
            print("invalid rotation angle")
        else:
            duty = 2 + float(amount/18) #duty 2 to 12 range 
            self.servo.ChangeDutyCycle(duty)
            time.sleep(0.5)
            print("rotated servo position to " + str(amount) + "degrees")
            self.wait()
    
    #move servo back to angle of zero
    def reset(self):
        self.servo.ChangeDutyCycle(2)
        time.sleep(0.5)
        print("reset servo position to 0 degrees")
        self.wait()

    def wait(self):
        self.servo.ChangeDutyCycle(0)
        time.sleep(0.5)
        print("in wait")

    def stop(self):
        print("terminating servo")
        self.servo.stop()
        GPIO.cleanup()
