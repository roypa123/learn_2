// thermistor.ino - a motor driver's temperature from a 10 k NTC thermistor (Chapters 74 and 79)
const int THERM_PIN = A1;
const float R_FIXED = 1500.0;          // the fixed resistor (top of the divider): good for 70-85 C (Chapter 79)
const float R_25 = 10000.0;            // the thermistor: 10 k at 25 C ...
const float B = 3950.0;                // ... and its B value (Chapter 74)

// Returns the temperature in C, or -999 if the reading is impossible (a broken or shorted wire).
float readTemperature() {
  int count = analogRead(THERM_PIN);
  if (count < 5 || count > 1018) {
    return -999;                                   // stuck near 0 V or 5 V: the sensor is not connected
  }
  float ratio = count / 1024.0;                    // the pin's share of the supply: no volts needed
  float r = R_FIXED * ratio / (1.0 - ratio);       // the thermistor's resistance (Chapter 79, turned round)
  float invT = 1.0 / 298.15 + log(r / R_25) / B;   // Chapter 74's formula, turned round
  return 1.0 / invT - 273.15;                      // kelvin to degrees C
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  float t = readTemperature();
  if (t < -100) {
    Serial.println("sensor fault: stop the motors");
  } else {
    Serial.print("driver ");
    Serial.print(t, 1);
    Serial.print(" C  ");
    if (t >= 85) {
      Serial.println("TOO HOT: stop the motors");
    } else if (t >= 70) {
      Serial.println("warm: slow down");
    } else {
      Serial.println("ok");
    }
  }
  delay(1000);
}
