// encoder_poll.ino - count a wheel encoder's pulses by POLLING, in a loop that also has other work to do
const int ENC_A = 2;                   // the encoder's channel A

long count = 0;
int lastA = LOW;
unsigned long lastReport = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ENC_A, INPUT_PULLUP);
}

void loop() {
  int a = digitalRead(ENC_A);
  if (lastA == LOW && a == HIGH) {     // a rising edge: one pulse
    count++;
  }
  lastA = a;
  delayMicroseconds(800);              // the rest of Rover's work in each pass: sensors, control, messages
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    Serial.print("pulses counted: ");
    Serial.println(count);
  }
}
