// ultrasonic_isr.ino - measure distance with an ultrasonic sensor WITHOUT waiting for the echo:
// an interrupt on the echo pin notes when the echo starts and ends; loop() never waits
const int TRIG_PIN = 9;
const int ECHO_PIN = 3;                // an interrupt pin
const unsigned long PING_MS = 60;      // one measurement every 60 ms

volatile unsigned long echoStart = 0;
volatile unsigned long echoWidth = 0;  // how long the echo pin was HIGH, in microseconds
volatile bool echoReady = false;       // set by the ISR when a new width is ready
unsigned long lastPing = 0;
long passes = 0;                       // passes of loop() between pings: how free the loop is

void onEcho() {                        // runs at every change of the echo pin
  if (digitalRead(ECHO_PIN) == HIGH) {
    echoStart = micros();              // the echo pulse begins
  } else {
    echoWidth = micros() - echoStart;  // the echo pulse ends: its width is the sound's travel time
    echoReady = true;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(ECHO_PIN), onEcho, CHANGE);
}

void loop() {
  passes++;
  if (millis() - lastPing >= PING_MS) {          // time for a new measurement
    lastPing += PING_MS;
    digitalWrite(TRIG_PIN, HIGH);                // a 10 us trigger pulse starts the sensor
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
  }
  if (echoReady) {                               // the ISR has a new answer
    noInterrupts();
    unsigned long width = echoWidth;
    echoReady = false;
    interrupts();
    Serial.print(millis());
    Serial.print(" ms: ");
    Serial.print(width / 58.0, 1);               // 58 us of echo per cm (Chapter 119)
    Serial.print(" cm   (loop ran ");
    Serial.print(passes);
    Serial.println(" times since the last answer)");
    passes = 0;
  }
}
