// odometry.ino - Rover counts encoder ticks: which type should hold the count, and the distance?
const float METERS_PER_TICK = 0.207f / 540;   // one wheel turn = 0.207 m = 540 ticks (Chapters 16 and 47)

int ticksInt = 0;                      // the WRONG type for a tick count
long ticksLong = 0;                    // the right type
float distanceAdded = 0;               // the WRONG way to get the distance: add a tiny step at every tick

void setup() {
  Serial.begin(9600);
  Serial.println("ticks      int count   long count   from count (m)   added up (m)");
  for (long n = 1; n <= 1000000; n++) {           // pretend Rover drives one million ticks
    ticksInt++;
    ticksLong++;
    distanceAdded = distanceAdded + METERS_PER_TICK;
    if (n == 32767 || n == 32768 || n == 100000 || n == 1000000) {
      Serial.print(n);
      Serial.print("      ");
      Serial.print(ticksInt);
      Serial.print("      ");
      Serial.print(ticksLong);
      Serial.print("      ");
      Serial.print(ticksLong * METERS_PER_TICK, 3);
      Serial.print("      ");
      Serial.println(distanceAdded, 3);
    }
  }
}

void loop() {
}
