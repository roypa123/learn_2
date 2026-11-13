# run_with_mock_gpio.py - run a Raspberry Pi gpiozero program on any computer, with pretend button presses
# usage:  python run_with_mock_gpio.py --press 17:1.0-1.4 --press 17:3.0-3.2 --end 5 program.py
#         (--press PIN:DOWN-UP in seconds, as many as you like; --end: when pause() returns)
import os
import runpy
import signal
import sys
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mock_gpiozero                             # noqa: E402

args = sys.argv[1:]
while args and args[0].startswith("--"):
    if args[0] == "--press":
        pin, span = args[1].split(":")
        down, up = span.split("-")
        mock_gpiozero.presses.setdefault(int(pin), []).append((float(down), float(up)))
    elif args[0] == "--end":
        mock_gpiozero.end_s = float(args[1])
    args = args[2:]

module = types.ModuleType("gpiozero")
for name in ("LED", "PWMLED", "Button"):
    setattr(module, name, getattr(mock_gpiozero, name))
sys.modules["gpiozero"] = module
time.sleep = mock_gpiozero.sleep
signal.pause = mock_gpiozero.pause

sys.argv = args
runpy.run_path(args[0], run_name="__main__")
