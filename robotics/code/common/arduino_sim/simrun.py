# simrun.py - build and run a PC test of an Arduino sketch with g++ (the PC test bench)
# usage:  python simrun.py path/to/test_something.cpp
#
# If the test file includes "avr_int.h", the sketch it includes is built with the Uno's 16-bit int:
# a copy of the sketch's text is changed (int -> avr_int, const int -> const int16_t,
# unsigned int -> uint16_t), leaving strings and comments alone. The sketch file is never changed.
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))       # the folder that holds Arduino.h and run.h
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/|\bunsigned\s+int\b|\bconst\s+int\b|\bint\b',
                    re.S)


def uno_ints(code):
    def change(m):
        t = m.group(0)
        if t[0] in "\"'/":
            return t                                      # a string, a character or a comment: keep it
        if t.startswith("unsigned"):
            return "uint16_t"
        if t.startswith("const"):
            return "const int16_t"
        return "avr_int"
    return TOKENS.sub(change, code)


test = os.path.abspath(sys.argv[1])
source = open(test, encoding="utf-8").read()
if '#include "avr_int.h"' in source:
    def inline(m):
        path = os.path.join(os.path.dirname(test), m.group(1))
        return uno_ints(open(path, encoding="utf-8").read())
    source = re.sub(r'#include "([^"]+\.ino)"', inline, source)
work = tempfile.mkdtemp()
src = os.path.join(work, os.path.basename(test))
open(src, "w", encoding="utf-8").write(source)
exe = os.path.join(work, "test.exe")
cmd = ["g++", "-std=c++17", "-O1", "-Wall", "-Wno-unused-variable", "-I", HERE, "-I", os.path.dirname(test), src, "-o", exe]
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
os.remove(src)
os.rmdir(work)
