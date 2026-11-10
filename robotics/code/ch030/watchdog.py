# watchdog.py - if commands stop arriving, the robot must stop by itself
class Watchdog:
    def __init__(self, timeout_s):
        self.timeout_s = timeout_s
        self.last_feed = 0.0

    def feed(self, now):
        """Call this every time a good command arrives."""
        self.last_feed = now

    def expired(self, now):
        return now - self.last_feed > self.timeout_s


dog = Watchdog(timeout_s=0.25)
command_ticks = [0, 1, 2, 3, 8, 9]    # the radio drops out after tick 3

speed_ms = 0.5
for tick in range(11):              # pretend clock: one step every 0.1 s
    now = tick / 10
    if tick in command_ticks:         # compare ints, not floats (Chapter 17)
        dog.feed(now)
    if dog.expired(now):
        output = 0.0                # no recent command: STOP
    else:
        output = speed_ms
    print(f"t = {now:.1f} s  fed {now - dog.last_feed:.1f} s ago  speed {output}")
