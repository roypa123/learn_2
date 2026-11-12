// plotter.ino - send two signals to the Serial Plotter: a slow wave, and a noisy copy of it
float angle = 0;

void setup() {
  Serial.begin(115200);
  randomSeed(100);
}

void loop() {
  float wave = 50 * sin(angle);                     // a wave between -50 and +50
  float noisy = wave + random(-15, 16);             // the same wave with up to 15 of noise added
  Serial.print("wave:");                            // "name:value" gives each line a name in the plotter
  Serial.print(wave);
  Serial.print(",");                                // a comma (or a space) between values
  Serial.print("noisy:");
  Serial.println(noisy);                            // a new line ends one set of values
  angle = angle + 0.1;
  delay(20);                                        // 50 sets of values per second
}
