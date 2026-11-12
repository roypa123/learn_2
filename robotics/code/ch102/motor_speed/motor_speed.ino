// motor_speed.ino - a knob sets a motor's speed: analogRead -> map -> PWM -> MOSFET -> motor
const int KNOB_PIN = A0;
const int MOTOR_PIN = 5;               // a PWM pin, driving the MOSFET's gate (Chapter 98)
const int DEAD_ZONE = 50;              // below about 20% the motor cannot start anyway (Chapter 93)

void setup() {
  Serial.begin(115200);
  pinMode(MOTOR_PIN, OUTPUT);
  analogWrite(MOTOR_PIN, 0);           // start with the motor stopped
}

void loop() {
  int knob = analogRead(KNOB_PIN);               // 0 to 1023
  int pwm = map(knob, 0, 1023, 0, 255);          // 0 to 255 (whole numbers only, Chapter 43)
  if (pwm < DEAD_ZONE) {
    pwm = 0;                                     // too little to turn: switch off instead of humming
  }
  analogWrite(MOTOR_PIN, pwm);
  Serial.print("knob ");
  Serial.print(knob);
  Serial.print(" -> PWM ");
  Serial.print(pwm);
  Serial.print(" = ");
  Serial.print(pwm * 100 / 255);
  Serial.println("%");
  delay(200);
}
