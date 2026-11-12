# toy_cpu.py - a pretend microcontroller: a program of numbers in "flash", run by fetch, decode, execute
NAMES = {0: "HALT", 1: "LOAD", 2: "ADD", 3: "SUB", 4: "OUT", 5: "JMP", 6: "JNZ", 7: "WAIT"}
CLOCK_HZ = 16_000_000                  # 16 million clock ticks per second, like the Arduino Uno

# The blink program. Each instruction is two numbers: what to do, and a number to do it with.
FLASH = [1, 1,       # 0: LOAD 1     put 1 in register A
         4, 0,       # 1: OUT        copy A to the LED pin (LED on)
         7, 500,     # 2: WAIT 500   wait 500 ms
         1, 0,       # 3: LOAD 0     put 0 in A
         4, 0,       # 4: OUT        LED off
         7, 500,     # 5: WAIT 500
         5, 0]       # 6: JMP 0      go back to instruction 0, for ever


def run(flash, max_steps):
    pc, a, led, cycles = 0, 0, 0, 0          # program counter, register A, LED pin, clock ticks so far
    for step in range(max_steps):
        op, arg = flash[2 * pc], flash[2 * pc + 1]       # FETCH: read two numbers from flash
        name = NAMES[op]                                  # DECODE: which instruction is it?
        next_pc = pc + 1
        if op == 0:                                       # EXECUTE
            print(f"{step:4d}  pc={pc}  HALT")
            break
        elif op == 1:
            a = arg
        elif op == 2:
            a = a + arg
        elif op == 3:
            a = a - arg
        elif op == 4:
            led = a
        elif op == 5:
            next_pc = arg
        elif op == 6 and a != 0:
            next_pc = arg
        elif op == 7:
            cycles += arg * CLOCK_HZ // 1000              # waiting 1 ms = 16,000 ticks
        cycles += 1                                       # every instruction itself takes one tick
        print(f"{step:4d}  pc={pc}  {name:4s} {arg:3d}   A={a}  LED={led}  ticks={cycles:>10,}")
        pc = next_pc
    print(f"time on a {CLOCK_HZ // 1_000_000} MHz clock: {cycles / CLOCK_HZ * 1000:.4f} ms")


print("flash holds:", " ".join(str(n) for n in FLASH))
run(FLASH, 14)
