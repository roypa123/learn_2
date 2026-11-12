// blink_external.ino - blink an LED on pin 8 (through a 220 ohm resistor), and say what the pin is doing
const int LED_PIN = 8;
const int ON_MS = 300;
const int OFF_MS = 700;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);            // pin 8 becomes an output: LOW (0 V) until we change it
}

void loop() {
  digitalWrite(LED_PIN, HIGH);         // 5 V: current flows through the resistor and the LED
  Serial.println("LED on");
  delay(ON_MS);
  digitalWrite(LED_PIN, LOW);          // 0 V: no current, LED off
  Serial.println("LED off");
  delay(OFF_MS);
}
