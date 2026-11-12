# memory_budget.py - will Rover's data fit in the Arduino Uno's 2,048 bytes of SRAM?
SRAM = 2048                     # bytes of working memory in the ATmega328P

used = {
    "Arduino core + Serial buffers": 190,      # what an almost empty sketch that uses Serial needs
    "Rover's variables (speeds, state)": 60,
    "free space kept for the stack": 300,      # function calls need room while they run (Chapter 97)
}
fixed = sum(used.values())
for name, size in used.items():
    print(f"{name:36s} {size:5d} bytes")
print(f"{'left for a sensor log':36s} {SRAM - fixed:5d} bytes")
print()

kinds = {"byte (0-255)": 1, "int (2 bytes)": 2, "float (4 bytes)": 4, "time + 2 distances": 8}
print(f"{'one reading is a':20s} {'fits':>6s} {'at 10 per second':>18s}")
for name, size in kinds.items():
    n = (SRAM - fixed) // size                 # how many whole readings fit
    print(f"{name:20s} {n:6d} {n / 10:15.1f} s")
print()

wanted = 1000                                   # Rover's first idea: keep the last 1,000 int readings
need = wanted * 2
print(f"a log of {wanted} ints needs {need} bytes: "
      f"{'fits' if need <= SRAM - fixed else f'too big by {need - (SRAM - fixed)} bytes'}")
