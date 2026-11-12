// status_leds.ino - Rover's battery lights: green = fine, yellow = low, red flashing = go home now
const int GREEN_PIN = 10;
const int YELLOW_PIN = 11;
const int RED_PIN = 12;

const int N = 5;                       // five test readings, from a full to an almost empty battery
float batteryVolts[N] = {8.2, 7.5, 7.0, 6.7, 6.3};

void setLights(bool green, bool yellow, bool red) {
  digitalWrite(GREEN_PIN, green);      // true is HIGH, false is LOW
  digitalWrite(YELLOW_PIN, yellow);
  digitalWrite(RED_PIN, red);
}

void showBattery(float volts) {
  if (volts >= 7.2) {
    setLights(true, false, false);     // fine: green on, steady
    delay(1000);
  } else if (volts >= 6.6) {
    setLights(false, true, false);     // low: yellow on, steady
    delay(1000);
  } else {
    for (int i = 0; i < 5; i++) {      // empty: red flashes 5 times a second, for one second
      setLights(false, false, true);
      delay(100);
      setLights(false, false, false);
      delay(100);
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  for (int i = 0; i < N; i++) {
    Serial.print("battery ");
    Serial.print(batteryVolts[i]);
    Serial.println(" V");
    showBattery(batteryVolts[i]);
  }
  setLights(false, false, false);      // all off at the end
}

void loop() {
}
