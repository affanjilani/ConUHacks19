import cv2
import numpy as np
import os.path

from machine_function import machine_function

dirpath = os.path.abspath(os.path.dirname(__file__))

my_path = os.path.abspath(os.path.dirname(__file__))

carPics = os.path.join(dirpath,'.\\car_pics')

def imageCropper(imagePath,startH,endH,startW,endW):
    # read the image
    img = cv2.imread(imagePath)

    #convert to grey image
    greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    #return the region of interest
    return greyIm[startH:endH,startW:endW]


def carSeparator(croppedIm, roadNumber):

    #cut the cropped  image to 4 quadrants and the intersection
    if roadNumber == 1:
        quad1 = croppedIm[2950:3460,972:1282]
        quad2 = croppedIm[2646:3012,1136:1394]
        quad3 = croppedIm[2590:2916,754:1084]
        quad4 = croppedIm[2912:3306,518:870]
        intersection = croppedIm[3670:, 0:970]
    else:
        quad1 = croppedIm[1520:1876,1732:2060]
        quad2 = croppedIm[1224:1540,1812:2112]
        quad3 = croppedIm[1204:1512,1464:1772]
        quad4 = croppedIm[1472:1848,1340:1676]
        intersection = croppedIm[2060:2850,830:1990]

    #save the images
    cv2.imwrite(os.path.join(my_path,'.\\car_pics\\road'+str(roadNumber)+'\\quad1.jpg'),quad1)
    cv2.imwrite(os.path.join(my_path,'.\\car_pics\\road'+str(roadNumber)+'\\quad2.jpg'),quad2)
    cv2.imwrite(os.path.join(my_path,'.\\car_pics\\road'+str(roadNumber)+'\\quad3.jpg'),quad3)
    cv2.imwrite(os.path.join(my_path,'.\\car_pics\\road'+str(roadNumber)+'\\quad4.jpg'),quad4)
    cv2.imwrite(os.path.join(my_path,'.\\car_pics\\road'+str(roadNumber)+'\\intersection.jpg'), intersection)


    return (quad1,quad2,quad3,quad4,intersection)

#function to show image
def show(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     #croppedGrey = imageCropper("./road_pics/road1.jpg",780,1430,165,745)
#     img = cv2.imread('./road_pics/road2.jpg')
#     greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#     quadrants = carSeparator(greyIm,2)

#     img = cv2.imread('./road_pics/road1.jpg')
#     greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#     quadrants = carSeparator(greyIm,1)

#     numCars = 0
#     print 'here'
#     for i in range(1,5):
#         numCars = numCars + machine_function(os.path.join(carPics, '.\\road'+str(2)+'\\quad'+str(i)+'.jpg'))
#     print numCars, 'numCars'

#     # for i in quadrants:
#     #     show(i)

