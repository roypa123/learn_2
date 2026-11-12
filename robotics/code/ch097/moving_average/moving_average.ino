// moving_average.ino - smooth a noisy distance sensor by averaging its last 8 readings
const int SENSOR_PIN = A0;
const int WINDOW = 8;                  // how many readings to average

int smooth(int newReading) {
  static int history[WINDOW];          // static: kept from one call to the next; starts as all zeros
  static int next = 0;                 // where the next reading will go
  static int count = 0;                // how many readings we have so far (up to WINDOW)
  static long sum = 0;                 // the sum of the readings in history
  sum = sum - history[next] + newReading;   // take out the oldest reading, put in the newest
  history[next] = newReading;
  next = (next + 1) % WINDOW;          // go round the ring: 0, 1, ... 7, 0, 1, ...
  if (count < WINDOW) {
    count++;
  }
  return sum / count;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(SENSOR_PIN);
  int smoothed = smooth(raw);
  Serial.print(raw);                   // two numbers on a line, for the Serial Plotter (Chapter 100)
  Serial.print(" ");
  Serial.println(smoothed);
  delay(100);                          // 10 readings per second
}
