# simrun.py - build and run a PC test of an Arduino sketch with g++ (the PC test bench)
# usage:  python simrun.py path/to/test_something.cpp
#
# If the test file includes "avr_int.h", the sketch it includes is built with the Uno's 16-bit int:
# a copy of the sketch's text is changed (int -> avr_int, const int -> const int16_t,
# unsigned int -> uint16_t), leaving strings and comments alone. The sketch file is never changed.
# python simrun.py test.cpp --exe out.exe   only builds, and keeps the program (Chapter 111 runs it itself).
# A test can add include folders (for a library's src folder) with lines like:  // simrun-include: ../MyLib/src
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
keep_exe = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--exe" else None   # build only, keep the program
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
extra = []                                                # "// simrun-include: folder" lines add include folders (libraries)
for m in re.finditer(r"^// simrun-include: (.+)$", source, re.M):
    extra += ["-I", os.path.normpath(os.path.join(os.path.dirname(test), m.group(1).strip()))]
cmd = ["g++", "-std=c++17", "-O1", "-Wall", "-Wno-unused-variable", "-I", HERE, "-I", os.path.dirname(test)] + extra + [src, "-o", exe]
build = subprocess.run(cmd, capture_output=True, text=True)
if build.returncode != 0:
    print(build.stderr)
    sys.exit("build failed")
if build.stderr.strip():
    print(build.stderr)                                   # warnings: show them, they often point at bugs
if keep_exe:
    os.replace(exe, keep_exe)
    os.remove(src)
    os.rmdir(work)
    sys.exit(0)
out = subprocess.run([exe], capture_output=True)
text = out.stdout.replace(b"\r\r\n", b"\n").replace(b"\r\n", b"\n")   # Serial.println ends lines with \r\n
sys.stdout.flush()
sys.stdout.buffer.write(text)                             # raw bytes: works whatever the console's encoding
sys.stdout.buffer.flush()
os.remove(exe)
os.remove(src)
os.rmdir(work)
