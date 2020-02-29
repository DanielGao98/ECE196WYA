from servo_controller import servo_controller as sc
import time
#servo controller module tester

sc1 = sc()
time.sleep(3)
sc1.rotate(30)
time.sleep(3)
sc1.rotate(45)
time.sleep(3)
sc1.rotate(90)
time.sleep(3)
sc1.rotate(135)
time.sleep(3)
sc1.reset()
time.sleep(3)
sc1.stop()
