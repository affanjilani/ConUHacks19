import os
import cv2

camera1 = "172.30.147.124:5555"
camera2 = None

openCamera = 'adb -s 9b28cb0d shell \"am start -a android.media.action.IMAGE_CAPTURE\"'

takePicture = 'adb -s '+camera1+' shell \"input keyevent KEYCODE_CAMERA\"'

# accept =  'adb shell \"input keyevent KEYCODE_ENTER\"'

#os.system(openCamera)

# Load picture
def pullPicture1():
	os.system('sleep 1')
	os.system('adb -s '+camera1+' shell mv /sdcard/DCIM/Camera/IMG_20190126*.jpg /sdcard/DCIM/Camera/road1.jpg')
	os.system('adb -s '+camera1+' pull /sdcard/DCIM/Camera/road1.jpg C:\\Users\\obiaf\\Documents\\ConUHacks19\\road_pics')
	os.system('adb -s '+camera1+' shell rm /sdcard/DCIM/Camera/road1.jpg')

os.system(takePicture)

pullPicture1()

