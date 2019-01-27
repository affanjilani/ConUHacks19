// constants won't change. They're used here to set pin numbers:
const int buttonPin1 = 3;     // the number of the pushbutton pin
const int buttonPin2 = 4;

// variables will change:
int buttonState1 = 0;   
int buttonState2 = 0;
// variable for reading the pushbutton status

void setup() {
  // initialize the LED pin as an output:
  pinMode(buttonPin1, INPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin2, INPUT);
}

void loop() {
  // read the state of the pushbutton value:
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState1 == HIGH) {
    // turn LED on:
   Serial.println("2");
  } else if (buttonState2==HIGH)
  {
   Serial.println("1");
  }
}
