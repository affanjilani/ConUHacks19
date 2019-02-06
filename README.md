# ConUHacks19 Smart Traffic Lights
## Inspiration behind the madness
We hate having to wait at a red light for hours while the crossing street has no cars. So, what we wanted to achieve was to design a traffic system where the lights would not simply change based off a timer or a primitive car detection technique. We wanted the lights to change based on the dynamic traffic situation. That is if a street is empty and has been empty, while the other street has had constant cars and still has cars coming, then the busy street should not have its light turn red due to a timer.

## Our idea
By sensing the environment and the streets individually, in real time, we generate information based on the number of cars present in the photo/on the street. Using a heuristic function giving weights to the three most pressing aspects for our problem:
* Current volume of cars on the street relative to the other street
* Time a street has been waiting due to a red light
* Car volume history (Average number of cars)
These three aspects were then represented as a single value given by the following heuristic function 

`value(street) = 2 * (numCars(streetNumber)-numCars(otherStreet)) + 2 * waitTime + 3 * averageNumCars(street)`

These values were updated at every second from two mounted cameras (in our case two phones) running on seperate threads, each capturing an image for one street. A third thread synchronized with the camera threads was there in order to update the values of both streets, and the street with the highest value would have the green light. If the other street has no cars and hasn't had any in a while, our value for that street would be lower than our busy street's, and thus the light on the busy street would stay green as long as a few cars haven't arrived on the empty street.
### Demonstration and implementation
![maquette](/road_pics/road2.jpg)

We used Arduino Uno for the lights (file uploaded to arduino was [readDataAndChangeLight](/readDataAndChangeLight/readDataAndChangeLight.ino)). They would change based on the heuristic values of the streets that were obtained and computed through a python [script](/threadExample.py). The image processing was done sending shell commands to both android phones and taking a picture, and then using `adb pull` to bring them into the project folder. From there the images were processed in order to seperate the cars on the streets into different pictures, then sent to a function that used IBM Watson REST API call in order to assess if the pictures had cars in them or not, based on a model we trained. We put everything together on a maquette as shown in the picture above in order to simulate what an intersection with out solution would look like!
