// counter.ino - a variable made inside loop() is made again every time loop() runs
int globalCount = 0;                   // made once, before setup(); it keeps its value

void setup() {
  Serial.begin(9600);
}

void loop() {
  int localCount = 0;                  // made again, and set to 0, on every pass of loop()
  globalCount = globalCount + 1;
  localCount = localCount + 1;
  Serial.print("global: ");
  Serial.print(globalCount);
  Serial.print("   local: ");
  Serial.println(localCount);
  delay(500);
}
