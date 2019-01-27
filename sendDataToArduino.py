def sendData(byte):
    import serial
    import time
    #establishing a connection with the arduino
    ser = serial.Serial('/dev/cu.usbmodem14401',9600)
    time.sleep(2)

    if(byte == 2):
        #sending a byte to arduino
        ser.write(b'8')

    elif(byte == 1):
        # sending a byte to arduino
        ser.write(b'5')

    time.sleep(3)