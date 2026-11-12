// fade.ino - fade an LED on pin 9 up and then down with PWM
const int LED_PIN = 9;                 // a PWM pin (marked ~ on the board)

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  for (int value = 0; value <= 255; value += 51) {    // 0, 51, 102, 153, 204, 255
    analogWrite(LED_PIN, value);       // HIGH for value/255 of every period
    delay(200);
  }
  for (int value = 204; value >= 51; value -= 51) {   // 204, 153, 102, 51: back down
    analogWrite(LED_PIN, value);
    delay(200);
  }
}
