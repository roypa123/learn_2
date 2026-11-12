// print_cost.ino - how long does Serial.print take? Time it with micros() for different amounts of text
const long BAUD = 9600;                // try 115200

void printCost(int chars) {
  Serial.flush();                      // wait until everything earlier has been sent: start empty
  unsigned long start = micros();
  for (int i = 0; i < chars; i++) {
    Serial.print('x');                 // one character
  }
  unsigned long took = micros() - start;
  Serial.println();
  Serial.print(chars);
  Serial.print(" characters: print took ");
  Serial.print(took);
  Serial.println(" us");
}

void setup() {
  Serial.begin(BAUD);
  printCost(10);
  printCost(60);
  printCost(100);
  printCost(200);
}

void loop() {
}
