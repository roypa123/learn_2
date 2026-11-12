// commands.ino - drive a pretend Rover by typing commands: F 120, B 80, S, ?
// F n = forward at speed n, B n = backward at speed n, S = stop, ? = report. Speeds are 0 to 255.
char command = 0;                      // the letter of the command being read (0 = none yet)
long number = 0;                       // the number after it, built digit by digit
bool hasNumber = false;
int speed = 0;                         // Rover's pretend speed: positive = forward, negative = backward

void runCommand() {
  if ((command == 'F' || command == 'B') && !hasNumber) {
    Serial.println("error: F and B need a speed, e.g. F 120");
    return;
  }
  int n = constrain(number, 0, 255);   // never trust a number typed by a person
  switch (command) {
    case 'F':
      speed = n;
      Serial.print("forward at ");
      Serial.println(speed);
      break;
    case 'B':
      speed = -n;
      Serial.print("backward at ");
      Serial.println(n);
      break;
    case 'S':
      speed = 0;
      Serial.println("stop");
      break;
    case '?':
      Serial.print("speed is ");
      Serial.println(speed);
      break;
    default:
      Serial.print("unknown command: ");
      Serial.println(command);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("ready: F n, B n, S, ?");
}

void loop() {
  while (Serial.available() > 0) {     // handle every character that has arrived; never wait
    char c = Serial.read();
    if (c == '\n') {                   // the end of a line: run the command
      if (command != 0) {
        runCommand();
      }
      command = 0;                     // get ready for the next line
      number = 0;
      hasNumber = false;
    } else if (c >= '0' && c <= '9') {
      number = number * 10 + (c - '0');   // one more digit: '7' - '0' is 7
      hasNumber = true;
    } else if (c != ' ' && c != '\r' && command == 0) {
      command = c;                     // the first letter on the line is the command
    }
  }
  // the rest of Rover's work would go here: this loop never stops to wait for the user
}
