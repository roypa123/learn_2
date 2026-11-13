// pwm20k.ino - 20 kHz PWM on pin 9 from Timer1: a motor drive you cannot hear (Chapter 102 promised it)
const int MOTOR_PIN = 9;               // OC1A: the pin Timer1's output A drives
const unsigned int TOP = 799;          // 16,000,000 / (1 x (799 + 1)) = 20,000 Hz
const int SPEEDS[] = {0, 25, 50, 75, 100};
int step = 0;
unsigned long lastChange = 0;

void setMotor(int percent) {           // 0 to 100 %
  if (percent <= 0) {
    TCCR1A &= ~(1 << COM1A1);          // disconnect the timer from the pin ...
    digitalWrite(MOTOR_PIN, LOW);      // ... and hold it LOW: really off
  } else {
    OCR1A = (unsigned long)TOP * percent / 100;   // the pin is HIGH while the count is up to OCR1A
    TCCR1A |= (1 << COM1A1);           // connect the timer to the pin again
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(MOTOR_PIN, OUTPUT);
  TCCR1A = (1 << WGM11);               // fast PWM with TOP = ICR1 (mode 14) ...
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS10);   // ... and prescaler 1: 16 MHz
  ICR1 = TOP;
  setMotor(SPEEDS[0]);
}

void loop() {
  if (millis() - lastChange >= 200) {  // a new speed every 0.2 s
    lastChange += 200;
    step = (step + 1) % 5;
    setMotor(SPEEDS[step]);
    Serial.print("set ");
    Serial.print(SPEEDS[step]);
    Serial.println(" %");
  }
}
