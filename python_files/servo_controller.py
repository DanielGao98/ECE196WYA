import RPi.GPIO as GPIO
import time

class servo_controller:

    #servo = None

    def __init__(self):
        print("init servo_controller")
        self.servoPIN = 11  # change
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        
        self.servo = GPIO.PWM(self.servoPIN, 50)  # GPIO 11 for PWM with 50Hz
        self.servo.start(0)  # Initialization
        time.sleep(2)
        #print("in init 1")
        #self.servo.ChangeDutyCycle(2)
        #time.sleep(0.5)
        #print("in init 2")
        #self.servo.ChangeDutyCycle(4) 
        #time.sleep(0.5)
        #self.servo.ChangeDutyCycle(11)
        #time.sleep(0.5)

    def show(self):
        print("show()")


    def rotate(self, amount):
        self.servo.ChangeDutyCycle(2 + float(amount/18))
        print("in rotate 1")
        #self.servo.ChangeDutyCycle(5)
        #print("in rotate 2")
        time.sleep(0.5)
        self.wait()

    def wait(self):
        #print("in wait 1")
        self.servo.ChangeDutyCycle(0)
        time.sleep(0.5)
        #print("in wait 2")

    def stop(self):
        self.servo.stop()
        GPIO.cleanup()

#if __name__ == "__main__":
    #sc = servo_controller()
    #sc.rotate(20)
    #sc.stop()

