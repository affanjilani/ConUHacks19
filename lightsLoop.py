# main loop that will keep on running, taking pictures every n seconds

import os
import time
import cv2

import threading

from DataStructs import Road

from trafficAlg import changeLight
from carSeparator import carSeparator
from autoPicture import pullPicture1, pullPicture2
from machine_function import machine_function

# Global variables
intersection = {
	1: Road(0, 'green', 0, 0, False),
	2: Road(0, 'red', None, 0, False),
	'totalTime': 0
}

dirpath = os.path.abspath(os.path.dirname(__file__))

camera1 = "172.30.147.124:5555"
camera2 = "988b9d3151484c554c"

takePicture1 = 'adb -s '+camera1+' shell \"input keyevent KEYCODE_CAMERA\"'
takePicture2 = 'adb -s '+camera2+' shell \"input keyevent KEYCODE_CAMERA\"'

roadPicture1 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road1.jpg'
roadPicture2 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road2.jpg'

carPics = os.path.join(dirpath,'.\\car_pics')

regularRedLightTime = 5

def countCars():
	numCars = 0
	for i in range(1,6):
		#check the intersection if we are at the last iteration
		if(i == 5):
			numCars = numCars + machine_function(os.path.join(carPics, '.\\road' + str(greenRoad) + '\\intersection.jpg'))
		else:
			numCars = numCars + machine_function(os.path.join(carPics, '.\\road'+str(greenRoad)+'\\quad'+str(i)+'.jpg'))

	intersection[greenRoad].numCars = numCars

	intersection[greenRoad].avgNumCars = float(((intersection[greenRoad].avgNumCars * (timeElapsed -1)) + numCars)/timeElapsed)

	return numCars

def pedestrianFunc():
	import serial
	import time

	#establish a connection with the arduino
	ser = serial.Serial('COM3',9600)

	time.sleep(2)#sleep for 2 seconds

	while True:
	    #read a line from arduino
	    line = str(ser.readline())
	    #split the line
	    line = line.split('\'')
	    #get the index that has the road number
	    line = line[1]
	    #retreive the road number
	    roadNumber = line[0]

	    if (roadNumber == 1):
	        intersection[1].pedestrianWaiting = True
	    elif (roadNumber == 2):
	    	intersection[2].pedestrianWaiting = True

# Start pedestrian thread ##############################
pedestrianThread = threading.Thread(target=pedestrianFunc)
pedestrianThread.start()
########################################################

def pedestrians() :
	import serial

	#establish a connection with the arduino
	ser = serial.Serial('COM3',9600)
	#read a line from arduino
	try:
		line = str(ser.readline())
		#split the line
		line = line.split('\'')
		#get the index that has the road number
		line = line[1]
		#retreive the road number
		roadNumber = line[0]

	except:
		roadNumber = 3

	if (roadNumber == 1):

		print('Pedestrian pressed road number 1')
		os.system(takePicture1)

		pullPicture1()
		
		img = cv2.imread(roadPicture1)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)

		numCars = countCars()

		if numCars > 3:
			time.sleep(5)


		changeLight(intersection)

		return True

	elif (roadNumber == 2):
		print('Pedestrian pressed road number 2')

		os.system(takePicture2)

		pullPicture2()

		img = cv2.imread(roadPicture2)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)

		numCars = countCars()

		if numCars > 3:
			time.sleep(5)

		changeLight(intersection)

		return True
	elif (roadNumber == 3):
		return False

while True:
	timeElapsed = intersection['totalTime'] + 1
	intersection['totalTime'] = timeElapsed

	greenRoad = 1 if intersection[1].trafficLight == 'green' else 2
	redRoad = 2 if intersection[2].trafficLight == 'red' else 1
	
	time.sleep(regularRedLightTime)

	if(greenRoad == 1):
		os.system(takePicture1)

		pullPicture1()

		img = cv2.imread(roadPicture1)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)

	else:
		os.system(takePicture2)

		pullPicture2()

		img = cv2.imread(roadPicture2)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)
		
	countCars()

	changeLight(intersection)

	
