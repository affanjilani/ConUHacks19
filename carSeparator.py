import cv2
import numpy as np

def imageCropper(imagePath,startH,endH,startW,endW):
    # read the image
    img = cv2.imread(imagePath)

    #convert to grey image
    greyIm = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    #return the region of interest
    return greyIm[startH:endH,startW:endW]


def carSeparator(croppedIm):
    #cut the cropped  image to 4 quadrants
    quad1 = croppedIm[0:275,150:370]
    quad2 = croppedIm[0:320,379:]
    quad3 = croppedIm[280:585,0:225]
    quad4 = croppedIm[340:,230:480]

    return (quad1,quad2,quad3,quad4)

#function to show image
def show(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    croppedGrey = imageCropper("./cars.jpg",780,1430,165,745)
    quadrants = carSeparator(croppedGrey)

    for i in quadrants:
        show(i)

