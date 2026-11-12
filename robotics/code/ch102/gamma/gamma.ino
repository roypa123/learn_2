// gamma.ino - LED brightness that the eye sees as even steps: gamma-corrected PWM values
const float GAMMA = 2.2;               // how the eye responds to light (section 102.3)

void setup() {
  Serial.begin(115200);
  Serial.println("level   linear PWM   corrected PWM");
  for (int level = 0; level <= 10; level++) {
    int linear = level * 255 / 10;                                 // equal steps of PWM value
    int corrected = (int)(255 * pow(level / 10.0, GAMMA) + 0.5);   // equal steps of SEEN brightness
    Serial.print(level * 10);
    Serial.print("%      ");
    Serial.print(linear);
    Serial.print("          ");
    Serial.println(corrected);
  }
}

void loop() {
}
