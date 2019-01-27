import serial
import time

#establish a connection with the arduino
ser = serial.Serial('/dev/cu.usbmodem14401',9600)

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
        pass
        #TODO: Affan, call the function that capture an image of road 1..
    elif (roadNumber == 2):
        pass
        #TODO: Affan, call the function that capture an image of road 2...
