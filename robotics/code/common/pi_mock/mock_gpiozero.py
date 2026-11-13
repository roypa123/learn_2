# mock_gpiozero.py - a stand-in for the gpiozero library (Chapter 112) that runs on any computer
#
# Programs for the Raspberry Pi in this course use gpiozero (it comes with Raspberry Pi OS).
# run_with_mock_gpio.py puts this module in its place, so the same program runs on a PC:
#   - time is SIMULATED: time.sleep() and signal.pause() move a pretend clock forward;
#   - every change of an output pin is printed, with the pretend time;
#   - button presses come from a list given on the command line, with 3 ms of contact bounce;
#   - Button(bounce_time=...) ignores changes that come too soon after the last one, as gpiozero does.
# Only the parts of gpiozero used in this course are here. Real gpiozero also has a mock pin
# factory of its own (GPIOZERO_PIN_FACTORY=mock) for testing on a PC.
import heapq

presses = {}                                     # pin -> list of (down_s, up_s), set by the runner
end_s = 10.0                                     # pause() returns at this time


class _Clock:
    now = 0.0
    queue = []                                   # (time, order, function)
    order = 0

    @classmethod
    def at(cls, t, fn):
        cls.order += 1
        heapq.heappush(cls.queue, (t, cls.order, fn))

    @classmethod
    def run_until(cls, t):
        while cls.queue and cls.queue[0][0] <= t:
            when, _, fn = heapq.heappop(cls.queue)
            cls.now = when
            fn()
        cls.now = max(cls.now, t)


def sleep(seconds):
    _Clock.run_until(_Clock.now + max(0.0, seconds))


def pause():
    _Clock.run_until(end_s)


def _say(text):
    print(f"[{_Clock.now:8.3f} s] {text}")


class LED:
    def __init__(self, pin, active_high=True):
        self.pin = pin
        self._lit = False
        self._blink_id = 0                       # changes when a blink is cancelled

    def _set(self, lit):
        if lit != self._lit:
            self._lit = lit
            _say(f"GPIO{self.pin} -> {'HIGH' if lit else 'LOW'}  (LED {'on' if lit else 'off'})")

    def on(self):
        self._blink_id += 1
        self._set(True)

    def off(self):
        self._blink_id += 1
        self._set(False)

    def toggle(self):
        self._blink_id += 1
        self._set(not self._lit)

    @property
    def is_lit(self):
        return self._lit

    def blink(self, on_time=1.0, off_time=1.0, n=None, background=True):
        self._blink_id += 1
        my_id = self._blink_id                   # a later on(), off() or blink() cancels this blink

        def turn_on(left):
            if self._blink_id != my_id or left == 0:
                return
            self._set(True)
            _Clock.at(_Clock.now + on_time, lambda: turn_off(left))

        def turn_off(left):
            if self._blink_id != my_id:
                return
            self._set(False)
            _Clock.at(_Clock.now + off_time, lambda: turn_on(None if left is None else left - 1))

        turn_on(n)
        if not background:
            sleep((on_time + off_time) * (n or 1))

    def close(self):
        self.off()


class PWMLED(LED):
    def __init__(self, pin, active_high=True, frequency=100):
        super().__init__(pin, active_high)
        self._value = 0.0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        _say(f"GPIO{self.pin} PWM {v * 100:.0f} %")


class Button:
    def __init__(self, pin, pull_up=True, bounce_time=None):
        self.pin = pin
        self.bounce_time = bounce_time
        self.when_pressed = None
        self.when_released = None
        self._pressed = False
        self._last_change = -1e9
        for down, up in presses.get(pin, []):    # schedule the raw edges, with contact bounce
            for k, frac in enumerate([0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85]):
                _Clock.at(down + frac * 0.003, lambda level=(k % 2 == 0): self._edge(level))
                _Clock.at(up + frac * 0.003, lambda level=(k % 2 == 1): self._edge(level))

    def _edge(self, pressed):
        if pressed == self._pressed:
            return
        if self.bounce_time is not None and _Clock.now - self._last_change < self.bounce_time:
            return                               # too soon after the last accepted change: bounce
        self._pressed = pressed
        self._last_change = _Clock.now
        cb = self.when_pressed if pressed else self.when_released
        if cb:
            cb()

    @property
    def is_pressed(self):
        return self._pressed

    def wait_for_press(self, timeout=None):
        limit = _Clock.now + (timeout if timeout is not None else 1e9)
        while not self._pressed and _Clock.now < limit and _Clock.queue:
            _Clock.run_until(_Clock.queue[0][0])
        return self._pressed
