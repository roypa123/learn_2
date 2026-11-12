// button_isr.ino - count a button's falling edges with an interrupt: the hardware calls a function at each one
const int BUTTON_PIN = 2;              // on the Uno, only pins 2 and 3 have their own interrupts
volatile long edges = 0;               // changed inside the interrupt: it must be volatile

void onFall() {                        // the interrupt service routine (ISR): keep it very short
  edges++;
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onFall, FALLING);
}

void loop() {
  delay(1000);                         // the loop may even sleep: the interrupt still counts every edge
  noInterrupts();                      // copy the 4-byte count with interrupts paused (section 105.5)
  long copy = edges;
  interrupts();
  Serial.print("falling edges counted: ");
  Serial.println(copy);
}
