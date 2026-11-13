// BumpersAndBattery.ino - an example that comes with RoverLib: two debounced bumpers and the battery
#include <RoverLib.h>

Debouncer leftBumper(4);               // three objects: each holds its own pin and its own state
Debouncer rightBumper(5);
BatteryMonitor battery(A3, 68000.0, 10000.0);
unsigned long lastReport = 0;

void setup() {
  Serial.begin(115200);
  leftBumper.begin();
  rightBumper.begin();
  battery.begin();
}

void loop() {
  if (leftBumper.update()) {
    Serial.print(millis());
    Serial.println(" ms: left bumper pressed");
  }
  if (rightBumper.update()) {
    Serial.print(millis());
    Serial.println(" ms: right bumper pressed");
  }
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    Serial.print("battery ");
    Serial.print(battery.volts(), 2);
    Serial.print(" V (");
    Serial.print(battery.percent());
    Serial.print(" %), presses: left ");
    Serial.print(leftBumper.presses());
    Serial.print(", right ");
    Serial.println(rightBumper.presses());
  }
}
