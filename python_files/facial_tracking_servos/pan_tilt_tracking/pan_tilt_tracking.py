# USAGE
# python3 pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml

# import necessary packages
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
import argparse
import signal
import time
import sys
import cv2

from servo_controller import servo_controller as sc

sc_pan = sc()
sc_tilt = None

# initialize servo controllers
def init_servos():
	sc_pan = sc()
	#sc_tilt = sc()

	print("pan and tilt servos initialized")

# function to handle keyboard interrupt
def signal_handler(sig, frame):
	# print a status message
	print("Signal interrupt was detected")

	#sc_pan.reset()
	#sc_pan.stop()

	#sc_tilt.reset()
	#sc_tilt.stop()

	print("both servos have been terminated")

	# exit
	sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# start the video stream and wait for the camera to warm up
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# initialize the object center finder
	obj = ObjCenter(args["cascade"])

	# loop indefinitely
	while True:
		# grab the frame from the threaded video stream and flip it
		# vertically (since our camera was upside down)
		frame = vs.read()

		# calculate the center of the frame as this is where we will
		# try to keep the object
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# find the object's location
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc

		# extract the bounding box and draw it
		if rect is not None:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
				2)

		# display the frame to the screen
		cv2.imshow("Pan-Tilt Face Tracking", frame)
		cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# create a PID and initialize it
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# calculate the error
		error = centerCoord.value - objCoord.value

		# update the value
		output.value = p.update(error)

def set_servos(pan, tlt):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# loop indefinitely
	while True:
		print("pan value is " + str(pan.value))
		print(type(pan.value))
		#print("tilt value is " + str(tlt.value))
		#pan to rotation angle
		time.sleep(0.5)	
		if sc_pan is not None:
			print("HERE")
			sc_pan.rotate(pan.value)
		#tilt to rotation angle
	#	sc_tilt.rotate(tlt.value)

# check to see if this is the main body of execution
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade", type=str, required=True,
		help="path to input Haar cascade for face detection")
	args = vars(ap.parse_args())

	#print bc idk what args are
	print(str(args))

	# start a manager for managing process-safe variables
	with Manager() as manager:
		# enable the servos
		#init_servos()

		# set integer values for the object center (x, y)-coordinates
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# set integer values for the object's (x, y)-coordinates
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# pan and tilt values will be managed by independed PIDs
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)

		# set PID values for panning
		panP = manager.Value("f", 0.09)
		panI = manager.Value("f", 0.08)
		panD = manager.Value("f", 0.002)

		# set PID values for tilting
		tiltP = manager.Value("f", 0.11)
		tiltI = manager.Value("f", 0.10)
		tiltD = manager.Value("f", 0.002)

		# we have 4 independent processes
		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))
		processPanning = Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX))
	#	processTilting = Process(target=pid_process,
	#		args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos = Process(target=set_servos, args=(pan, tlt))

		# initalize the 4 processes
		processObjectCenter.start()
		processPanning.start()
	#	processTilting.start()
		processSetServos.start()

		# set the process to run until interrupt
		processObjectCenter.join()
		processPanning.join()
	#	processTilting.join()
		processSetServos.join()

