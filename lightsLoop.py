# main loop that will keep on running, taking pictures every n seconds

import os
import time
import cv2

from DataStructs import Road

from trafficAlg import changeLight
from carSeperator import carSeperator,imageCropper
from autoPicture import pullPicture1, pullPicture2
from machine_function import machine_function

# Global variables
intersection = {
	1: Road(0, 'green', 0, 0),
	2: Road(0, 'red', None, 0),
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


while True:
	timeElapsed = intersection['totalTime'] + 1
	intersection['totalTime'] = timeElapsed

	greenRoad = 1 if intersection[1].trafficLight == 'green' else 2
	redRoad = 2 if intersection[2].trafficLight == 'red' else 1

	if(greenRoad == 1):
		os.system(takePicture1)

		pullPicture1()

		img = cv2.imread(roadPicture1)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeperator(greyIm,greenRoad)

	else:
		os.system(takePicture2)

		pullPicture2()

		img = cv2.imread(roadPicture2)
		greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

		carSeperator(greyIm,greenRoad)
		
	numCars = 0
	for i in range(1,4):
		numCars = numCars + machine_function(os.path.join(carPics, '.\\road'+str(greenRoad)+'\\quad'+str(i)+'.jpg'))

	intersection[greenRoad].numCars = numCars

	intersection[greenRoad].avgNumCars = float(((intersection[greenRoad].avgNumCars * (timeElapsed -1)) + numCars)/timeElapsed)

	changeLight(intersection)

	
