// maths.ino - whole-number and decimal maths on the Uno
void setup() {
  Serial.begin(9600);
  int a = 7;
  int b = 2;

  Serial.print("7 / 2        = ");  Serial.println(a / b);        // whole numbers: the remainder is dropped
  Serial.print("7 % 2        = ");  Serial.println(a % b);        // the remainder
  Serial.print("-7 / 2       = ");  Serial.println(-a / b);       // rounds towards zero
  Serial.print("-7 % 360     = ");  Serial.println(-a % 360);     // C++ keeps the sign (Python gives 353)

  float half = a / b;                                             // the division happens BEFORE the float
  Serial.print("float = 7/2  = ");  Serial.println(half);
  float half2 = (float)a / b;                                     // make one side a float first
  Serial.print("(float)7 / 2 = ");  Serial.println(half2);
  Serial.print("7 / 2.0      = ");  Serial.println(a / 2.0);
  Serial.print("2.0 / 3      = ");  Serial.println(2.0 / 3, 4);   // 4 decimal places

  int cut = 2.7;                                                  // a float into an int: the decimals are cut off
  int rounded = (int)(2.7 + 0.5);                                 // add 0.5 first to round
  Serial.print("int from 2.7 = ");  Serial.print(cut);
  Serial.print(", rounded = ");     Serial.println(rounded);

  int heading = -30;
  int wrapped = (heading % 360 + 360) % 360;                      // always 0 to 359, even for negatives
  Serial.print("-30 degrees wrapped = ");  Serial.println(wrapped);
}

void loop() {
}
