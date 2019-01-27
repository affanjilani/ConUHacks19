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

#from sendDataToArduino import sendData

import serial
import time

#establish a connection with the arduino
global ser 
ser = serial.Serial('COM3',9600)

time.sleep(2)#sleep for 2 seconds

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
	if cameraNumber==1:
		os.system(takePicture1)
		# took picture
		pullPicture1()
		
		img = cv2.imread(roadPicture1)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,cameraNumber)

	if cameraNumber==2:
		os.system(takePicture2)

		pullPicture2()

		img = cv2.imread(roadPicture2)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeparator(greyIm,cameraNumber)

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

		barrierMutex.acquire()
		takePic(1)
		barrierMutex.release()
		time.sleep(1)
	return

def camera2():
	while True:
		
		barrierMutex.acquire()
		takePic(2)
		barrierMutex.release()
		time.sleep(1)	
	return

def valueEval():
	while True:

		barrierMutex.acquire()
		test = eval()
		barrierMutex.release()
		time.sleep(1)
	return

def pedestrians():
	

	while True:
	    #read a line from arduino
	    line = str(ser.readline())
	    #split the line
	    line = line.split('\'')
	    #get the index that has the road number
	    line = line[1]
	    #retreive the road number
	    roadNumber = line[0]

	    if (roadNumber == '1'):
	    	print('RoadNumber 1 Pedestrian waiting')
	        intersection[1].pedestrianWaiting = True
	    elif (roadNumber == '2'):
	    	print('RoadNumber 2 Pedestrian waiting')
	    	intersection[2].pedestrianWaiting = True


camera1Thread = threading.Thread(target=camera1)
camera2Thread = threading.Thread(target=camera2)
valueThread = threading.Thread(target=valueEval)
pedestrianThread = threading.Thread(target=pedestrians)

camera1Thread.start()
camera2Thread.start()
valueThread.start()
pedestrianThread.start()



def countCars(roadNumber):
	timeElapsed = intersection['totalTime']
	numCars = 0
	for i in range(1,5):
		numCars = numCars + machine_function(os.path.join(carPics, '.\\road'+str(roadNumber)+'\\quad'+str(i)+'.jpg'))
	
	intersection[roadNumber].numCars = numCars

	intersection[roadNumber].avgNumCars = float(((intersection[roadNumber].avgNumCars * (timeElapsed -1)) + numCars)/float(timeElapsed))

	return numCars



def eval():
	intersection['totalTime'] = intersection['totalTime'] + 1
	if intersection[1].trafficLight == 'red':
		intersection[1].waitTime = intersection[1].waitTime + 1
		waitTime1 = intersection[1].waitTime
		waitTime2 = 0
	else:
		intersection[2].waitTime = intersection[2].waitTime + 1
		waitTime2 = intersection[2].waitTime
		waitTime1 = 0

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
	print("VALUE OF ROAD 1: " + str(value1))
	print("VALUE OF ROAD 2: " + str(value2)+'\n')
	return (value1,value2, numCars1, numCars2, intersection[1].waitTime, intersection[2].waitTime, intersection[1].avgNumCars, intersection[2].avgNumCars)

def changeLights(roadNumberToTurnOff, roadNumberToTurnOn):
	time.sleep(3)
	sendData(roadNumberToTurnOff)

	intersection[roadNumberToTurnOff].trafficLight = 'red'
	intersection[roadNumberToTurnOn].trafficLight = 'green'

	intersection[roadNumberToTurnOff].waitTime = 0
	intersection[roadNumberToTurnOn].waitTime = 0

def sendData(byte):

    if(byte == 2):
        #sending a byte to arduino
        ser.write(b'8')

    elif(byte == 1):
        # sending a byte to arduino
        ser.write(b'5')

    time.sleep(3)

