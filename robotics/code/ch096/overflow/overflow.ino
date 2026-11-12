// overflow.ino - what happens when a number does not fit in its type
void setup() {
  Serial.begin(9600);

  int big = 32767;                     // the largest int on the Uno
  big = big + 1;
  Serial.print("32767 + 1 as an int:   ");
  Serial.println(big);

  byte b = 255;
  b = b + 1;
  Serial.print("255 + 1 as a byte:     ");
  Serial.println(b);

  int rpm = 300;
  int seconds = 200;
  long turns = rpm * seconds;          // the multiplication is done in int, THEN stored in the long
  Serial.print("300 * 200 into a long: ");
  Serial.println(turns);

  long turnsFixed = (long)rpm * seconds;   // make one side a long first: now it is done in long
  Serial.print("(long)300 * 200:       ");
  Serial.println(turnsFixed);

  unsigned int u = 0;
  u = u - 1;
  Serial.print("0 - 1 as unsigned int: ");
  Serial.println(u);
}

void loop() {
}
