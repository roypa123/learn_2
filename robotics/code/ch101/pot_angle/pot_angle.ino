// pot_angle.ino - a potentiometer on a robot arm's joint: turn its reading into an angle
const int POT_PIN = A1;
const int MAX_ANGLE = 270;             // this potentiometer turns 270 degrees from end to end

void setup() {
  Serial.begin(115200);
}

void loop() {
  int count = analogRead(POT_PIN);
  int angle = map(count, 0, 1023, 0, MAX_ANGLE);   // a straight line from counts to degrees (Chapter 43)
  Serial.print("count ");
  Serial.print(count);
  Serial.print(" -> angle ");
  Serial.print(angle);
  Serial.println(" degrees");
  delay(500);
}
