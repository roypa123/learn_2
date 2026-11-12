// button_basic.ino - read a button on pin 2 ten times a second and show its state
const int BUTTON_PIN = 2;              // button between pin 2 and GND

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);   // input, with the chip's own pull-up resistor switched on
}

void loop() {
  int level = digitalRead(BUTTON_PIN); // HIGH or LOW
  if (level == LOW) {
    Serial.println("pressed");         // LOW = the button connects the pin to GND
  } else {
    Serial.println("free");            // HIGH = the pull-up holds the pin at 5 V
  }
  delay(100);
}
