// startup_beep.ino - Rover says "ready" with three rising notes on a passive buzzer on pin 8
const int BUZZER_PIN = 8;
const int NOTES[3] = {523, 659, 784};  // the notes C, E and G: frequencies in Hz

void setup() {
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, NOTES[i], 150);   // a square wave at this frequency, for 150 ms
    delay(200);                        // tone() does not wait: wait for the note and a short gap
  }
}

void loop() {
}
