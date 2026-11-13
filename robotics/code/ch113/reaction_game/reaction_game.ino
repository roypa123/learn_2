// reaction_game.ino - how fast can you react? A random wait, then GO: press the button as fast as you can.
// The button is on interrupt pin 2, so the moment of the press is caught to the microsecond (Chapter 105).
const int BUTTON_PIN = 2;              // button to GND
const int LED_PIN = 9;                 // a PWM pin: a dim glow while waiting, full brightness for GO (Chapter 102)
const int BUZZER_PIN = 8;              // a passive buzzer, played with tone() (Chapter 102)
const int ROUNDS = 5;

enum State { WAITING, GO, RESULT, DONE };
State state = DONE;
volatile unsigned long pressMicros = 0;
volatile bool pressed = false;
unsigned long goMicros = 0;
unsigned long stateStart = 0;
unsigned long waitMs = 0;
int roundNo = 0;
int scored = 0;
float total = 0;
float best = 99999;

void onPress() {                       // the ISR: only the first edge counts; the bounce after it is ignored
  if (!pressed) {
    pressMicros = micros();
    pressed = true;
  }
}

void enter(State s) {
  state = s;
  stateStart = millis();
}

void startRound() {
  roundNo++;
  noInterrupts();
  pressed = false;
  interrupts();
  waitMs = random(1500, 4000);         // a random wait, so nobody can guess the moment
  analogWrite(LED_PIN, 15);            // a dim glow: get ready
  enter(WAITING);
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onPress, FALLING);
  randomSeed(analogRead(A0));          // A0 left unconnected: its noise makes every game different
  Serial.println("round,reaction_ms");
  startRound();
}

void loop() {
  switch (state) {
    case WAITING:
      if (pressed) {                   // pressed before GO: a false start
        Serial.print(roundNo);
        Serial.println(",false start");
        tone(BUZZER_PIN, 200, 400);    // a low "wrong" sound
        analogWrite(LED_PIN, 0);
        enter(RESULT);
      } else if (millis() - stateStart >= waitMs) {
        analogWrite(LED_PIN, 255);     // GO!
        tone(BUZZER_PIN, 2000, 100);
        goMicros = micros();
        enter(GO);
      }
      break;
    case GO:
      if (pressed) {
        noInterrupts();
        unsigned long p = pressMicros; // a safe copy (Chapter 105)
        interrupts();
        float ms = (p - goMicros) / 1000.0;
        Serial.print(roundNo);
        Serial.print(',');
        Serial.println(ms, 1);
        scored++;
        total += ms;
        if (ms < best) best = ms;
        analogWrite(LED_PIN, 0);
        enter(RESULT);
      } else if (millis() - stateStart >= 1500) {
        Serial.print(roundNo);
        Serial.println(",too slow");
        analogWrite(LED_PIN, 0);
        enter(RESULT);
      }
      break;
    case RESULT:
      if (millis() - stateStart >= 1000) {   // a pause before the next round
        if (roundNo < ROUNDS) {
          startRound();
        } else {
          Serial.print("best ");
          Serial.print(best, 1);
          Serial.print(" ms, average ");
          Serial.print(scored > 0 ? total / scored : 0.0, 1);
          Serial.print(" ms over ");
          Serial.print(scored);
          Serial.println(" good rounds");
          enter(DONE);
        }
      }
      break;
    case DONE:
      break;
  }
}
