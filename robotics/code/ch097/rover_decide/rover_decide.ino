// rover_decide.ino - Rover's first decisions: what to do for each distance and bumper reading
const int GO = 0;                      // the four actions, as numbers with names
const int SLOW = 1;
const int TURN = 2;
const int BACK_UP = 3;

const int N = 7;                       // seven test situations
int distances[N] = {150, 80, 45, 25, 12, 60, 30};             // distance to the nearest obstacle, cm
bool bumped[N] = {false, false, false, false, false, true, false};

int decide(int cm, bool bump) {
  if (bump) {
    return BACK_UP;                    // touching something: the most important rule comes first
  } else if (cm < 20) {
    return TURN;                       // very close: turn away
  } else if (cm < 50) {
    return SLOW;                       // close: slow down
  }
  return GO;                           // nothing near
}

void printAction(int action) {
  switch (action) {
    case GO:
      Serial.println("GO: full speed");
      break;
    case SLOW:
      Serial.println("SLOW: half speed");
      break;
    case TURN:
      Serial.println("TURN: spin left");
      break;
    case BACK_UP:
      Serial.println("BACK UP: reverse for 0.5 s");
      break;
    default:
      Serial.println("unknown action");
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < N; i++) {
    Serial.print("distance ");
    Serial.print(distances[i]);
    Serial.print(" cm, bumper ");
    if (bumped[i]) {
      Serial.print("pressed");
    } else {
      Serial.print("free   ");
    }
    Serial.print(" -> ");
    printAction(decide(distances[i], bumped[i]));
  }
}

void loop() {
}
