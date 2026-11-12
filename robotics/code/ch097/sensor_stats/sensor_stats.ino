// sensor_stats.ino - an array of readings, and functions that work on it
const int N = 10;
int readings[N] = {512, 518, 509, 530, 497, 515, 521, 508, 940, 513};   // one reading is a glitch

long total(int values[], int n) {
  long sum = 0;                        // a long: ten readings of up to 1023 can pass 32,767
  for (int i = 0; i < n; i++) {
    sum = sum + values[i];
  }
  return sum;
}

int largest(int values[], int n) {
  int best = values[0];                // start with the first one
  for (int i = 1; i < n; i++) {
    if (values[i] > best) {
      best = values[i];                // found a bigger one
    }
  }
  return best;
}

void setup() {
  Serial.begin(9600);
  Serial.print("bytes in the array: ");
  Serial.println(sizeof(readings));
  Serial.print("first: ");
  Serial.print(readings[0]);
  Serial.print("   last: ");
  Serial.println(readings[N - 1]);
  Serial.print("sum: ");
  Serial.print(total(readings, N));
  Serial.print("   average: ");
  Serial.print((float)total(readings, N) / N);
  Serial.print("   largest: ");
  Serial.println(largest(readings, N));

  long sum = 0;                        // the average again, without the glitch
  int used = 0;
  for (int i = 0; i < N; i++) {
    if (readings[i] > 900) {
      continue;                        // skip this one and go on with the next i
    }
    sum = sum + readings[i];
    used++;
  }
  Serial.print("without readings over 900: ");
  Serial.print(used);
  Serial.print(" readings, average ");
  Serial.println((float)sum / used);
}

void loop() {
}
