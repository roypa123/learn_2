// rover_link.ino - Rover's Arduino side of its link with the Raspberry Pi: binary packets with a checksum
// packet: START (0xAA), LEN, TYPE, LEN payload bytes, CHECKSUM = (LEN + TYPE + payload bytes) & 0xFF
const byte START = 0xAA;
const byte TYPE_MOTOR = 'M';           // Pi -> Arduino: int16 left, int16 right (-255 to 255)
const byte TYPE_STATUS = 'S';          // Arduino -> Pi: int16 left, int16 right, good count, bad count
const unsigned long FAILSAFE_MS = 500; // no good command for this long: stop the motors

enum State { WAIT_START, READ_LEN, READ_TYPE, READ_PAYLOAD, READ_CHECK };
State state = WAIT_START;
byte len = 0;
byte type = 0;
byte got = 0;                          // payload bytes received so far
byte sum = 0;                          // checksum worked out so far
byte payload[16];

int16_t leftCmd = 0;
int16_t rightCmd = 0;
byte goodCount = 0;
byte badCount = 0;
unsigned long lastGood = 0;
bool stopped = true;

void sendStatus() {
  byte p[6];
  p[0] = leftCmd & 0xFF;               // low byte first
  p[1] = (leftCmd >> 8) & 0xFF;
  p[2] = rightCmd & 0xFF;
  p[3] = (rightCmd >> 8) & 0xFF;
  p[4] = goodCount;
  p[5] = badCount;
  byte check = 6 + TYPE_STATUS;
  for (int i = 0; i < 6; i++) {
    check += p[i];                     // a byte keeps only the low 8 bits: the "& 0xFF" happens by itself
  }
  Serial.write(START);
  Serial.write(6);
  Serial.write(TYPE_STATUS);
  Serial.write(p, 6);
  Serial.write(check);
}

void handlePacket() {
  if (type == TYPE_MOTOR && len == 4) {
    leftCmd = payload[0] | (payload[1] << 8);
    rightCmd = payload[2] | (payload[3] << 8);
    goodCount++;
    lastGood = millis();
    stopped = false;
    // setMotors(leftCmd, rightCmd);   the motor driver comes in Chapter 141
    sendStatus();
  } else {
    badCount++;                        // a type we do not know, or the wrong length
  }
}

void readLink() {                      // a state machine (Chapter 104), fed one byte at a time
  while (Serial.available() > 0) {
    byte b = Serial.read();
    switch (state) {
      case WAIT_START:
        if (b == START) state = READ_LEN;
        break;
      case READ_LEN:
        if (b > sizeof(payload)) {     // impossible length: this was not a real start byte
          badCount++;
          state = WAIT_START;
        } else {
          len = b;
          sum = b;
          state = READ_TYPE;
        }
        break;
      case READ_TYPE:
        type = b;
        sum += b;
        got = 0;
        state = (len > 0) ? READ_PAYLOAD : READ_CHECK;
        break;
      case READ_PAYLOAD:
        payload[got] = b;
        got++;
        sum += b;
        if (got == len) state = READ_CHECK;
        break;
      case READ_CHECK:
        if (b == sum) {
          handlePacket();
        } else {
          badCount++;                  // damaged on the way: ignore the whole packet
        }
        state = WAIT_START;
        break;
    }
  }
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  readLink();
  if (!stopped && millis() - lastGood >= FAILSAFE_MS) {   // the Pi has gone quiet: stop safely
    leftCmd = 0;
    rightCmd = 0;
    stopped = true;
    // setMotors(0, 0);
    sendStatus();
  }
}
