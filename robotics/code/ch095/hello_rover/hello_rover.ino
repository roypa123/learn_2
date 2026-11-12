// hello_rover.ino - Rover's first sketch: say hello, blink the board's LED, count the seconds
void setup() {
  Serial.begin(9600);                  // start talking to the computer at 9600 bits per second
  Serial.println("Hello from Rover!");
  pinMode(LED_BUILTIN, OUTPUT);        // the small LED marked "L" on the board (pin 13)
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);     // LED on
  delay(500);                          // wait 500 ms
  digitalWrite(LED_BUILTIN, LOW);      // LED off
  delay(500);
  Serial.print("seconds since power-on: ");
  Serial.println(millis() / 1000);
}
