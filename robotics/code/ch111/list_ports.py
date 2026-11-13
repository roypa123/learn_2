# list_ports.py - which serial ports does this computer have, and which one is the Arduino?
from serial.tools import list_ports              # part of pyserial

for p in list_ports.comports():
    print(f"{p.device:12s} {p.description}")
