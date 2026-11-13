# bench_serial.py - a stand-in for pyserial that connects Python code to a sketch on the PC test bench (Chapter 111)
#
# Python programs in this course talk to a real Arduino with the pyserial library (pip install pyserial).
# When there is no Arduino (or no pyserial), run_on_bench.py puts this module in pyserial's place:
#   - serial.Serial(...) builds the sketch, starts it on the PC test bench, and connects to its Serial;
#   - time.sleep() and time.monotonic() run on SIMULATED time, so the sketch and the Python program
#     share one clock, and a run takes a moment, however long it pretends to last;
#   - opening the port resets the pretend Uno, as opening a real Uno's port does (Chapter 95):
#     the sketch starts BOOT_MS later, and bytes sent before that are lost.
# Only the parts of pyserial used in this course are here.
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "..", "arduino_sim")
BOOT_MS = 500                                   # the Uno's bootloader waits about half a second after a reset (Chapter 95)
CALL_MS = 0.05                                  # each in_waiting / read call costs 50 us of simulated time

config = {"sketch": None, "world": None}        # set by run_on_bench.py


class Clock:
    now_s = 0.0                                 # simulated seconds since the Python program started
    ports = []                                  # open ports: they must follow the clock

    @classmethod
    def advance(cls, seconds):
        if seconds <= 0:
            return
        cls.now_s += seconds
        for p in cls.ports:
            p._advance(seconds * 1000.0)


def sleep(seconds):
    Clock.advance(seconds)


def monotonic():
    return Clock.now_s


class SerialException(Exception):
    pass


class Serial:
    def __init__(self, port=None, baudrate=9600, timeout=None, **kwargs):
        self.port, self.baudrate, self.timeout = port, baudrate, timeout
        self.lost_during_boot = 0
        self._buf = bytearray()
        self._boot_left = BOOT_MS
        self._start_bench()
        self.is_open = True
        Clock.ports.append(self)

    # ---- the bench program
    def _start_bench(self):
        sketch = os.path.abspath(config["sketch"])
        work = tempfile.mkdtemp()
        test = os.path.join(work, "pipe_test.cpp")
        lines = ["#include \"run.h\"", "#include \"avr_int.h\""]
        if config["world"]:
            lines.append(f"#include \"{os.path.abspath(config['world'])}\"")
        lines.append(f"#include \"{sketch}\"")
        if not config["world"]:
            lines.append("void world_setup() {}")
        lines.append("#include \"pipe_main.h\"")
        open(test, "w", encoding="utf-8").write("\n".join(lines).replace("\\", "/") + "\n")
        exe = os.path.join(work, "bench.exe")
        build = subprocess.run([sys.executable, os.path.join(SIM, "simrun.py"), test, "--exe", exe],
                               capture_output=True, text=True)
        if not os.path.exists(exe):
            raise SerialException("the bench could not build the sketch:\n" + build.stdout + build.stderr)
        self._proc = subprocess.Popen([exe], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self._work, self._exe, self._test = work, exe, test

    def _cmd(self, line):
        self._proc.stdin.write(line + "\n")
        self._proc.stdin.flush()
        return self._proc.stdout.readline().strip()

    def _advance(self, ms):                      # let simulated time pass for the pretend Uno
        if self._boot_left > 0:                  # still in the bootloader: the sketch has not started
            used = min(ms, self._boot_left)
            self._boot_left -= used
            ms -= used
        if ms > 0:
            reply = self._cmd(f"R {ms:.4f}")
            self._buf += bytes.fromhex(reply[1:].strip())

    # ---- the parts of pyserial used in this course
    @property
    def in_waiting(self):
        Clock.advance(CALL_MS / 1000.0)
        return len(self._buf)

    def write(self, data):
        data = bytes(data)
        if self._boot_left > 0:
            self.lost_during_boot += len(data)   # the sketch is not running yet: these bytes are lost
        else:
            self._cmd("S " + " ".join(f"{b:02X}" for b in data))
        return len(data)

    def _wait_for(self, done):
        waited = 0.0
        limit = self.timeout if self.timeout is not None else 60.0
        while not done() and waited < limit:
            Clock.advance(0.001)
            waited += 0.001

    def read(self, size=1):
        Clock.advance(CALL_MS / 1000.0)
        self._wait_for(lambda: len(self._buf) >= size)
        out = bytes(self._buf[:size])
        del self._buf[:size]
        return out

    def readline(self):
        Clock.advance(CALL_MS / 1000.0)
        self._wait_for(lambda: b"\n" in self._buf)
        k = self._buf.find(b"\n")
        k = len(self._buf) if k < 0 else k + 1
        out = bytes(self._buf[:k])
        del self._buf[:k]
        return out

    def reset_input_buffer(self):
        self._buf.clear()

    def close(self):
        if self.is_open:
            self._proc.stdin.write("Q\n")
            self._proc.stdin.flush()
            self._proc.wait()
            Clock.ports.remove(self)
            self.is_open = False
            for f in (self._exe, self._test):
                if os.path.exists(f):
                    os.remove(f)
            os.rmdir(self._work)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class _Port:
    def __init__(self, device, description):
        self.device, self.description = device, description


def comports():
    return [_Port("COM7", "Arduino Uno (PC test bench: " + os.path.basename(config["sketch"] or "no sketch") + ")")]
