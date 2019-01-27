int character = 0;
// constants won't change. They're used here to set pin numbers:
const int buttonPin1 = 3;     // the number of the pushbutton pin
const int buttonPin2 = 4;

// variables will change:
int buttonState1 = 0;   
int buttonState2 = 0;
// variable for reading the pushbutton status

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // initialize the LED pin as an output:
  pinMode(buttonPin1, INPUT_PULLUP);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin2, INPUT_PULLUP);
  
  pinMode(7,OUTPUT);//red
  pinMode(6,OUTPUT);//yellow
  pinMode(5,OUTPUT);//green

  pinMode(10,OUTPUT);//red
  pinMode(9,OUTPUT);//yellow
  pinMode(8,OUTPUT);//green

  //turn off all the led lights
  switchHigh(5);
  switchHigh(6);
  switchHigh(7);
  switchHigh(8);
  switchHigh(9);
  switchHigh(10);

  delay(1000);//wait for 1 second
  switchLow(5);//init, turn on green light on road 1
  switchLow(10);//init, turn on red light on road 2

  
}

void loop() {
  // put your main code here, to run repeatedly:
  // read the state of the pushbutton value:
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:, ONLY ONE BUTTON CAN BE PRESSED AT A TIME
  if (buttonState1 == HIGH) {
    // turn LED on:
   Serial.println("1");
   delay(2000);//delay
  } 
  else if (buttonState2 == HIGH){
   Serial.println("2");
   delay(2000);//delay
  }

  //if there is input in the buffer
  if(Serial.available() > 0){
    //basically atoi
    character = Serial.read() - 48;
    if(character == 5){
      turnOff1TurnOn2();
    }
    else if(character == 8){
      turnOff2TurnOn1();
    }
  }
}

//function to set the led of a pin to high
void switchHigh(int pinNum){
  digitalWrite(pinNum,HIGH);
}

//function to set the led of a pin to low
void switchLow(int pinNum){
  digitalWrite(pinNum,LOW);
}


//function that turns off the green traffic light (pin 5) from road 1...
void turnOff1TurnOn2(){
      switchHigh(5);//turn off green from road 1
      switchLow(6);//trun on yellow from road 1
      delay(3000);//wait 3 seconds
      switchHigh(6);//turn off yellow from road 1
      switchLow(7);//trun on red from road 1
      delay(500);//wait 0.5 seconds
      switchHigh(10);//turn on red from road 2
      switchLow(8);//turn on green from road 2
}

//function that turns off the green traffic light (pin 8) from road 2...
void turnOff2TurnOn1(){
      switchHigh(8);//turn off green from road 2
      switchLow(9);//trun on yellow from road 2
      delay(3000);//wait 3 seconds
      switchHigh(9);//turn off yellow from road 2
      switchLow(10);//trun on red from road 2
      delay(500);//wait 0.5 seconds
      switchHigh(7);//turn off red from road 1
      switchLow(5);//turn on green from road 1
}
