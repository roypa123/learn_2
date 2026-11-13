# run_on_bench.py - run a Python program written for pyserial against a sketch on the PC test bench
# usage:  python run_on_bench.py --sketch path/to/sketch.ino [--world world.h] program.py [program arguments]
#
# It puts bench_serial in the place of the "serial" module (pyserial), and makes time.sleep and
# time.monotonic use the bench's simulated clock, then runs the program unchanged.
import os
import runpy
import sys
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench_serial                            # noqa: E402

args = sys.argv[1:]
while args and args[0].startswith("--"):
    key, value = args[0][2:], args[1]
    bench_serial.config[key] = value
    args = args[2:]
program = args[0]

serial_module = types.ModuleType("serial")
serial_module.Serial = bench_serial.Serial
serial_module.SerialException = bench_serial.SerialException
tools = types.ModuleType("serial.tools")
list_ports = types.ModuleType("serial.tools.list_ports")
list_ports.comports = bench_serial.comports
tools.list_ports = list_ports
serial_module.tools = tools
sys.modules["serial"] = serial_module
sys.modules["serial.tools"] = tools
sys.modules["serial.tools.list_ports"] = list_ports
time.sleep = bench_serial.sleep
time.monotonic = bench_serial.monotonic

sys.argv = args
sys.path.insert(0, os.path.dirname(os.path.abspath(program)))
runpy.run_path(program, run_name="__main__")
