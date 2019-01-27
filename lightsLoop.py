# main loop that will keep on running, taking pictures every n seconds

import os
import time

from DataStructs import Road

from trafficAlg import changeLight
from carSeperator import carSeperator,imageCropper
from autoPicture import pullPicture1

# Global variables
intersection = {
	1: Road(0, 'green', 0, 0),
	2: Road(0, 'red', None, 0),
	'totalTime': 0
}

regularRedLightTime = 15

##########TODO: PUT IN THESE VALUES#######################
cropHeightStart1 = 0
cropHeightEnd1 = 0
cropWidthStart1 = 0
cropWidthEnd1 = 0

cropHeightStart2 = 0
cropHeightEnd2 = 0
cropWidthStart2 = 0
cropWidthEnd2 = 0
##########################################################

takePicture1 = 'adb -s 9b28cb0d shell \"input keyevent KEYCODE_CAMERA\"'
takePicture2 = 'adb -s 9b28cb0d shell \"input keyevent KEYCODE_CAMERA\"'

roadPicture1 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road1.jpg'
roadPicture2 = 'C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics\\road2.jpg'


while 1:
	timeElapsed = intersection['totalTime'] + 1
	intersection['totalTime'] = timeElapsed

	greenRoad = 1 if intersection[1].trafficLight == 'green' else 2
	redRoad = 2 if intersection[2].trafficLight == 'red' else 1

	if(greenRoad == 1):
		os.system(takePicture1)

		pullPicture1()

		cropped = imageCropper(roadPicture1, cropHeightStart1, cropHeightEnd1, cropWidthStart1, cropWidthEnd1)

	else:
		os.system(takePicture2)

		roadPicture = None

		cropped = imageCropper(roadPicture2, cropHeightStart2, cropHeightEnd2, cropWidthStart2, cropWidthEnd2)

	#seperate into 4 cars
	carSeperator(cropped)

	#################TODO: Send to Abdul's function to know car info##############

	numCars = 0
	##############################################################################

	#Returns tuple (numCars)
	intersection[greenRoad].numCars = numCars

	intersection[greenRoad].avgNumCars = float(((intersection[greenRoad].avgNumCars * (timeElapsed -1)) + numCars)/timeElapsed)

	changeLight(intersection)

	#sleep for a given amount of time then reassess
	time.sleep(regularRedLightTime)
