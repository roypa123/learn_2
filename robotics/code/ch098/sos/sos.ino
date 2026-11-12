// sos.ino - blink SOS in Morse code: three short flashes, three long, three short
const int LED_PIN = 8;
const int UNIT = 200;                  // ms: the length of one dot; a dash is 3 units

const int S_CODE[3] = {1, 1, 1};       // S = dot dot dot (lengths in units)
const int O_CODE[3] = {3, 3, 3};       // O = dash dash dash

void flash(int units) {
  digitalWrite(LED_PIN, HIGH);
  delay(units * UNIT);
  digitalWrite(LED_PIN, LOW);
  delay(UNIT);                         // a one-unit gap after every dot or dash
}

void letter(const int code[], int n) {
  for (int i = 0; i < n; i++) {
    flash(code[i]);
  }
  delay(2 * UNIT);                     // the gap between letters is 3 units: 1 already waited, 2 more
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  letter(S_CODE, 3);
  letter(O_CODE, 3);
  letter(S_CODE, 3);
  delay(4 * UNIT);                     // the gap between words is 7 units: 3 already waited, 4 more
}
