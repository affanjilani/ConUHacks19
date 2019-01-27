import os
import time
import cv2

import threading
import time

from DataStructs import Road

from trafficAlg import changeLight
from carSeparator import carSeparator
from autoPicture import pullPicture1, pullPicture2
from machine_function import machine_function

from sendDataToArduino import sendData

# Global variables
intersection = {
	1: Road(0, 'green', 0, 0, False),
	2: Road(0, 'red', 0, 0, False),
	'totalTime': 0,
}

barrierMutex = threading.Semaphore(1)

barrierLoad = 3
barrierCount = 0
theBarrier = threading.Semaphore(0)

dirpath = os.path.abspath(os.path.dirname(__file__))

camera1 = "172.30.147.124:5555"
camera2 = "988b9d3151484c554c"

takePicture1 = 'adb -s '+camera1+' shell \"input keyevent KEYCODE_CAMERA\"'
takePicture2 = 'adb -s '+camera2+' shell \"input keyevent KEYCODE_CAMERA\"'

roadPicture1 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road1.jpg'
roadPicture2 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road2.jpg'

carPics = os.path.join(dirpath,'.\\car_pics')

#takes picture
def takePic(cameraNumber):
	print('in take Pic')
	return 
	greenRoad = 1 if intersection[1].trafficLight == 'green' else 2
	if cameraNumber==1:
		os.system(takePicture1)

		pullPicture1()
		
		img = cv2.imread(roadPicture1)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)

	if cameraNumber==2:
		os.system(takePicture2)

		pullPicture2()

		img = cv2.imread(roadPicture2)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,greenRoad)

def barrier():
	barrierMutex.acquire()
	global barrierCount
	barrierCount = barrierCount + 1
	barrierMutex.release()

	if (barrierCount == barrierLoad):
		barrierCount = 0
		theBarrier.release()
	else:
		theBarrier.acquire()
	theBarrier.release()

def camera1():
	while True:
		print 'camera1'

		barrierMutex.acquire()
		takePic(1)
		barrierMutex.release()
		time.sleep(1)
	return

def camera2():
	for i in range(0,10):
		print 'camera2'
		barrier()
		time.sleep(1)
	return

def valueEval():
	while True:
		print 'eval'

		barrierMutex.acquire()
		test = eval()
		print (test)
		barrierMutex.release()
		time.sleep(1)
	return


camera1Thread = threading.Thread(target=camera1)
camera2Thread = threading.Thread(target=camera2)
valueThread = threading.Thread(target=valueEval)

camera1Thread.start()
camera2Thread.start()
valueThread.start()



def countCars(roadNumber):
	timeElapsed = intersection['totalTime']
	numCars = 0
	for i in range(1,5):
		numCars = numCars + machine_function(os.path.join(carPics, '.\\road'+str(roadNumber)+'\\quad'+str(i)+'.jpg'))
	
	intersection[roadNumber].numCars = numCars

	intersection[roadNumber].avgNumCars = float(((intersection[roadNumber].avgNumCars * (timeElapsed -1)) + numCars)/float(timeElapsed))

	return numCars



def eval():
	print (str(intersection))
	print ('Wait time 1' + str(intersection[1].trafficLight))
	intersection['totalTime'] = intersection['totalTime'] + 1
	if intersection[1].trafficLight == 'red':
		intersection[1].waitTime = intersection[1].waitTime + 1
		waitTime1 = intersection[1].waitTime
		waitTime2 = 0
		print(str(waitTime1)+'helo')
	else:
		intersection[2].waitTime = intersection[2].waitTime + 1
		waitTime2 = intersection[2].waitTime
		waitTime1 = 0
		print(str(waitTime1)+'helo')

	numCars1 = countCars(1)
	numCars2 = countCars(2)

	intersection[1].numCars = numCars1
	intersection[2].numCars = numCars2

	value1 = 2 * (intersection[1].numCars - intersection[2].numCars) + 2 * waitTime1 + 3 *intersection[1].avgNumCars

	value2 = 2 * (intersection[2].numCars - intersection[1].numCars) + 2 * waitTime2 + 3 * intersection[2].avgNumCars

	#if the stopped road has achieved a higher value
	if (value1>value2 and intersection[1].trafficLight == 'red'):
		changeLights( 2, 1)

	elif (value2>value1 and intersection[2].trafficLight == 'red'):
		changeLights( 1, 2)

	#print(int(intersection[1].trafficLight))
	return (value1,value2, numCars1, numCars2, intersection[1].waitTime, intersection[2].waitTime, intersection[1].avgNumCars, intersection[2].avgNumCars)

def changeLights(roadNumberToTurnOff, roadNumberToTurnOn):
	time.sleep(7)
	sendData(roadNumberToTurnOff)

	intersection[roadNumberToTurnOff].trafficLight = 'red'
	intersection[roadNumberToTurnOn].trafficLight = 'green'

	intersection[roadNumberToTurnOff].waitTime = 0
	intersection[roadNumberToTurnOn].waitTime = 0

