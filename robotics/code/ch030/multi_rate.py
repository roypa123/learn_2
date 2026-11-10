# multi_rate.py - several jobs, each at its own rate, with no waiting inside them
class Every:
    """Tells you when a job is due. It never makes the program wait."""

    def __init__(self, period_s):
        self.period_s = period_s
        self.next_time = 0.0

    def due(self, now):
        if now >= self.next_time:
            self.next_time += self.period_s
            return True
        return False


sensor_timer = Every(0.1)           # read the sensor 10 times a second
report_timer = Every(0.5)           # report twice a second
led_timer = Every(0.25)             # flip the LED 4 times a second

sensor_count = report_count = led_flips = 0

for tick in range(100):             # 100 ticks of 10 ms: one second of pretend time
    now = tick * 0.01               # count with an int (Chapter 13)
    if sensor_timer.due(now):
        sensor_count += 1
    if report_timer.due(now):
        report_count += 1
        print(f"t = {now:.2f} s: {sensor_count} readings so far")
    if led_timer.due(now):
        led_flips += 1

print("sensor:", sensor_count, "| reports:", report_count, "| LED flips:", led_flips)
