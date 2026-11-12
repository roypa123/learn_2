// types_tour.ino - every basic type on the Uno: how many bytes it takes, and the numbers it can hold
void setup() {
  Serial.begin(9600);

  bool ready = true;                   // true or false
  char letter = 'R';                   // one character (really a small number)
  byte level = 200;                    // a whole number from 0 to 255
  int speed = -1500;                   // a whole number from -32768 to 32767
  unsigned int count = 60000;          // a whole number from 0 to 65535
  long ticks = -2000000;               // a whole number of about +- 2 billion
  unsigned long ms = 4000000000UL;     // a whole number from 0 to about 4.29 billion
  float volts = 7.42;                  // a number with a decimal point, about 7 digits

  Serial.print("bool          ");  Serial.print(sizeof(ready));  Serial.print(" byte(s)  ");  Serial.println(ready);
  Serial.print("char          ");  Serial.print(sizeof(letter)); Serial.print(" byte(s)  ");  Serial.println(letter);
  Serial.print("byte          ");  Serial.print(sizeof(level));  Serial.print(" byte(s)  ");  Serial.println(level);
  Serial.print("int           ");  Serial.print(sizeof(speed));  Serial.print(" byte(s)  ");  Serial.println(speed);
  Serial.print("unsigned int  ");  Serial.print(sizeof(count));  Serial.print(" byte(s)  ");  Serial.println(count);
  Serial.print("long          ");  Serial.print(sizeof(ticks));  Serial.print(" byte(s)  ");  Serial.println(ticks);
  Serial.print("unsigned long ");  Serial.print(sizeof(ms));     Serial.print(" byte(s)  ");  Serial.println(ms);
  Serial.print("float         ");  Serial.print(sizeof(volts));  Serial.print(" byte(s)  ");  Serial.println(volts);
  Serial.print("the letter R is the number ");
  Serial.println((int)letter);
}

void loop() {
}
