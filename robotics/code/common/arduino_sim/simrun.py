# simrun.py - build and run a PC test of an Arduino sketch with g++ (the PC test bench)
# usage:  python simrun.py path/to/test_something.cpp
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))       # the folder that holds Arduino.h and run.h
test = os.path.abspath(sys.argv[1])
exe = os.path.splitext(test)[0] + ".exe"
cmd = ["g++", "-std=c++17", "-O1", "-Wall", "-Wno-unused-variable", "-I", HERE, test, "-o", exe]
build = subprocess.run(cmd, capture_output=True, text=True)
if build.returncode != 0:
    print(build.stderr)
    sys.exit("build failed")
if build.stderr.strip():
    print(build.stderr)                                   # warnings: show them, they often point at bugs
out = subprocess.run([exe], capture_output=True)
text = out.stdout.replace(b"\r\r\n", b"\n").replace(b"\r\n", b"\n")   # Serial.println ends lines with \r\n
print(text.decode("utf-8", "replace"), end="")
os.remove(exe)
