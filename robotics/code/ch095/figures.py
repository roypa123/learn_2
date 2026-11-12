# Figures for Chapter 95 - The Arduino board, the Arduino IDE and the Wokwi simulator.
# Run:  python figures.py      (saves PNG files in ../../images/ch095/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch095")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"
BOARD = "#1B6E8A"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=BLACK, fs=11, weight="normal", color=BLACK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, color=color)


def arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.8, style="-|>", ms=16):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=color, lw=lw))


def uno(ax, label_pins=True):
    """Draw an Arduino Uno from above, USB on the left. Units: mm. Returns pin positions."""
    ax.add_patch(FancyBboxPatch((0, 0), 68.6, 53.3, boxstyle="round,pad=0,rounding_size=2", fc=BOARD, ec=BLACK, lw=2))
    ax.add_patch(Rectangle((-6, 33), 16, 12, fc="#C0C0C0", ec=BLACK, lw=1.5))          # USB socket
    ax.add_patch(Rectangle((-2, 3), 14, 9, fc="#222222", ec=BLACK, lw=1.5))            # barrel jack
    pos = {}
    top = ["SCL", "SDA", "AREF", "GND", "13", "12", "~11", "~10", "~9", "8", "7", "~6", "~5", "4", "~3", "2", "1", "0"]
    xs = [17 + i * 2.54 for i in range(10)] + [45 + i * 2.54 for i in range(8)]
    for name, x in zip(top, xs):
        ax.add_patch(Rectangle((x - 1.1, 49.2), 2.2, 2.6, fc="#111111", ec="#555555"))
        pos[name.strip("~")] = (x, 50.5)
        if label_pins:
            ax.text(x, 47.6, name, rotation=90, ha="center", va="top", fontsize=7.5, color="white")
    bottom = ["IOREF", "RESET", "3.3V", "5V", "GND", "GND", "VIN", "A0", "A1", "A2", "A3", "A4", "A5"]
    xs = [27 + i * 2.54 for i in range(7)] + [50 + i * 2.54 for i in range(6)]
    for name, x in zip(bottom, xs):
        ax.add_patch(Rectangle((x - 1.1, 1.5), 2.2, 2.6, fc="#111111", ec="#555555"))
        pos[name] = (x, 2.8)
        if label_pins:
            ax.text(x, 5.6, name, rotation=90, ha="center", va="bottom", fontsize=7.5, color="white")
    return pos


# Figure 1: a tour of the Uno board
fig, ax = plt.subplots(figsize=(12, 8.2))
uno(ax)
ax.add_patch(Rectangle((30, 15), 34, 9, fc="#202020", ec="#888888", lw=1.5))       # ATmega328P (DIP-28)
ax.text(47, 19.5, "ATmega328P", color="white", ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((17, 33), 7, 7, fc="#202020", ec="#888888"))                # 16U2
ax.add_patch(Rectangle((23, 22), 5, 2.5, fc="#D8D8D8", ec=BLACK))                   # 16 MHz part
ax.add_patch(Rectangle((5, 18), 5, 4, fc="#202020", ec="#888888"))                  # regulator
ax.add_patch(Circle((8, 48), 2.2, fc="#E0E0E0", ec=BLACK))                          # reset button
for (x, y, c) in [(40, 41, "#FFD54F"), (40, 38.5, "#FFD54F"), (40, 36, "#FFD54F"), (60, 34, "#7CFC00")]:
    ax.add_patch(Rectangle((x, y), 2.4, 1.4, fc=c, ec=BLACK))
labels = [
    ((-2, 39), (-14, 47), "USB socket: power + program + Serial"),
    ((5, 7.5), (-14, 1), "barrel jack: 7-12 V in"),
    ((7.5, 20), (-14, 22), "5 V regulator"),
    ((20.5, 36.5), (-14, 33), "USB chip (ATmega16U2 or CH340)"),
    ((25.5, 23), (-14, 27.5), "16 MHz clock part"),
    ((8, 48), (-14, 55), "reset button"),
    ((47, 15), (74, 13), "THE MICROCONTROLLER:\nATmega328P"),
    ((41, 41.7), (74, 46), "LED 'L' on pin 13"),
    ((41, 37), (74, 40), "TX and RX LEDs:\nflash when Serial is busy"),
    ((61, 34.7), (74, 33), "ON LED: the board has power"),
    ((40, 51.5), (74, 58), "digital pins 0-13 (~ = PWM)"),
    ((37, 2.5), (74, -4), "power pins: 3.3V, 5V, GND, VIN"),
    ((57, 2.5), (74, 3.5), "analog inputs A0-A5"),
]
for (px, py), (tx, ty), t in labels:
    ax.annotate(t, xy=(px, py), xytext=(tx, ty), fontsize=10.5, ha="left" if tx > 0 else "right", va="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.3))
ax.set_xlim(-48, 112); ax.set_ylim(-8, 60); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-uno-tour.png")

# Figure 2: the ways to power the Uno
fig, ax = plt.subplots(figsize=(12, 5.6))
box(ax, 0, 3.6, 2.6, 1.0, "USB from a\ncomputer: 5 V", L_BLUE)
box(ax, 0, 1.6, 2.6, 1.0, "barrel jack\n7-12 V", L_ORANGE)
box(ax, 0, 0.0, 2.6, 1.0, "VIN pin\n7-12 V", L_ORANGE)
box(ax, 3.6, 3.6, 2.0, 1.0, "fuse\n500 mA", L_GREY)
box(ax, 3.6, 1.6, 2.0, 1.0, "diode\n(-0.8 V)", L_GREY)
box(ax, 6.6, 1.6, 2.4, 1.0, "regulator\n5 V (gets hot)", L_RED)
box(ax, 10.2, 2.6, 2.6, 1.2, "5 V for the\nATmega328P\nand the 5V pin", L_GREEN, weight="bold")
box(ax, 13.6, 2.6, 2.4, 1.2, "3.3 V\nregulator\n(150 mA max)", L_GREY)
box(ax, 13.6, 0.6, 2.4, 1.0, "3.3V pin", L_GREEN)
arrow(ax, 2.65, 4.1, 3.55, 4.1); arrow(ax, 5.65, 4.1, 10.15, 3.5)
arrow(ax, 2.65, 2.1, 3.55, 2.1); arrow(ax, 5.65, 2.1, 6.55, 2.1)
arrow(ax, 2.65, 0.5, 6.0, 0.5, style="-"); arrow(ax, 6.0, 0.5, 6.0, 2.05, style="-"); ax.plot([6.0], [2.1], "ko", ms=5)
arrow(ax, 9.05, 2.1, 10.15, 2.9)
arrow(ax, 12.85, 3.2, 13.55, 3.2); arrow(ax, 14.8, 2.55, 14.8, 1.65)
ax.text(6.0, 0.15, "VIN joins after the diode", ha="center", fontsize=10)
ax.text(8.0, 4.4, "when both are plugged in, the board\nswitches to the jack automatically", ha="center", fontsize=10)
ax.text(8.0, -0.5, "power IN through the 5V pin skips every protection: only from a good, regulated 5 V supply",
        ha="center", fontsize=10.5, color=RED)
ax.set_xlim(-0.2, 16.2); ax.set_ylim(-0.8, 5.0); ax.axis("off")
save(fig, "fig02-power-paths.png")

# Figure 3: regulator heat against input voltage (same model as uno_power.py)
fig, ax = plt.subplots(figsize=(10, 5.2))
vs = [6.9 + 0.05 * k for k in range(103)]
for ma, c, ls in [(50, GREEN, "-"), (150, BLUE, "--"), (300, ORANGE, "-."), (500, RED, ":")]:
    ax.plot(vs, [(v - 0.8 - 5.0) * ma / 1000 for v in vs], color=c, ls=ls, lw=2.5, label=f"{ma} mA from the 5 V rail")
ax.axhline(1.0, color=BLACK, ls="--", lw=1.5); ax.text(7.0, 1.05, "about 1 W: the most the small regulator should burn", fontsize=10.5)
ax.axvspan(6.0, 6.9, color=L_GREY); ax.text(6.45, 2.6, "too low:\nno 5 V", ha="center", fontsize=10)
ax.set_xlim(6.0, 12.0); ax.set_ylim(0, 3.2)
ax.set_xlabel("input voltage at the barrel jack or VIN (V)"); ax.set_ylabel("heat in the regulator (W)")
ax.legend(loc="upper center", bbox_to_anchor=(0.4, 1.0), fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig03-regulator-heat.png")

# Figure 4: from sketch to running chip
fig, ax = plt.subplots(figsize=(13, 4.6))
steps = [("your sketch\nblink.ino", L_BLUE), ("add prototypes\n+ #include\n<Arduino.h>", L_GREY),
         ("compiler\n(avr-gcc):\nC++ into\nnumbers", L_ORANGE), ("linker: add the\nArduino core\n(digitalWrite...)", L_ORANGE),
         ("blink.hex\n(about 924\nbytes)", L_GREEN), ("upload tool\n(avrdude)\nover USB", L_GREY),
         ("bootloader\nwrites flash", L_RED), ("the chip runs\nyour program", L_GREEN)]
for k, (t, c) in enumerate(steps):
    box(ax, k * 1.75, 1.0, 1.55, 1.6, t, c, fs=9.5)
    if k:
        arrow(ax, k * 1.75 - 0.19, 1.8, k * 1.75 - 0.02, 1.8)
ax.annotate("", xy=(0.0, 3.0), xytext=(6.85, 3.0), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=2))
ax.text(3.4, 3.2, "VERIFY (the check-mark button): on your computer", ha="center", fontsize=11, color=BLUE)
ax.annotate("", xy=(7.0, 3.0), xytext=(13.8, 3.0), arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
ax.text(10.4, 3.2, "UPLOAD (the arrow button): verify, then send it to the board", ha="center", fontsize=11, color=RED)
ax.text(6.9, 0.45, "The board is reset first, so the bootloader is listening; then the program starts by itself.", ha="center", fontsize=10.5)
ax.set_xlim(-0.2, 14.0); ax.set_ylim(0.2, 3.6); ax.axis("off")
save(fig, "fig04-build-upload.png")

# Figure 5: the Arduino IDE window (a simplified drawing)
fig, ax = plt.subplots(figsize=(12, 7))
ax.add_patch(Rectangle((0, 0), 12, 7.6, fc="#FAFAFA", ec=BLACK, lw=2))
ax.add_patch(Rectangle((0, 6.8), 12, 0.8, fc="#E8EEF0", ec=BLACK))
for k, (sym, name) in enumerate([("v", "Verify"), (">", "Upload")]):
    ax.add_patch(Circle((0.6 + k * 0.9, 7.2), 0.3, fc=GREEN if k else "#4CAF50", ec=BLACK))
    ax.text(0.6 + k * 0.9, 7.2, sym, ha="center", va="center", color="white", fontsize=13, weight="bold")
ax.add_patch(FancyBboxPatch((2.4, 6.95), 3.0, 0.5, boxstyle="round,pad=0.02", fc="white", ec=GREY))
ax.text(2.55, 7.2, "Arduino Uno   on   COM3", va="center", fontsize=10.5)
ax.add_patch(Circle((11.4, 7.2), 0.3, fc="white", ec=BLACK)); ax.text(11.4, 7.2, "o", ha="center", va="center", fontsize=12)
ax.add_patch(Rectangle((0.0, 6.4), 2.0, 0.4, fc="white", ec=GREY)); ax.text(0.15, 6.6, "blink.ino", va="center", fontsize=10)
code = ["void setup() {", "  pinMode(LED_BUILTIN, OUTPUT);", "}", "", "void loop() {", "  digitalWrite(LED_BUILTIN, HIGH);",
        "  delay(1000);", "  digitalWrite(LED_BUILTIN, LOW);", "  delay(1000);", "}"]
for k, line in enumerate(code):
    ax.text(0.3, 6.1 - k * 0.33, f"{k + 1:2d}", fontsize=9.5, color=GREY, family="monospace", va="center")
    ax.text(0.8, 6.1 - k * 0.33, line, fontsize=10, family="monospace", va="center")
ax.add_patch(Rectangle((0, 0), 12, 2.4, fc="#263238", ec=BLACK))
ax.text(0.2, 2.15, "Output", color="white", fontsize=10, weight="bold", va="center")
msgs = ["Sketch uses 924 bytes (2%) of program storage space.", "Maximum is 32256 bytes.",
        "Global variables use 9 bytes (0%) of dynamic memory, leaving", "2039 bytes for local variables. Maximum is 2048 bytes."]
for k, m in enumerate(msgs):
    ax.text(0.2, 1.75 - k * 0.32, m, color="#C8E6C9", fontsize=9, family="monospace", va="center")
ax.text(0.2, 0.3, "Done uploading.", color="#C8E6C9", fontsize=9.5, family="monospace", va="center")
notes = [((0.6, 6.85), (-0.2, 8.7), "1. Verify:\nbuild only"), ((1.5, 6.85), (2.4, 9.1), "2. Upload:\nbuild + send"),
         ((3.9, 6.95), (6.4, 8.9), "3. the board and its port"), ((11.4, 6.85), (11.4, 8.9), "4. Serial Monitor"),
         ((6.0, 4.6), (13.2, 4.6), "5. the editor:\nyour sketch"), ((10.0, 1.4), (13.2, 1.4), "6. messages and\nthe memory report")]
for (px, py), (tx, ty), t in notes:
    ax.annotate(t, xy=(px, py), xytext=(tx, ty), fontsize=11, ha="center" if ty > 8 else "left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3))
ax.set_xlim(-1.2, 16.5); ax.set_ylim(-0.3, 9.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-ide-window.png")

# Figure 6: the Wokwi simulator (a simplified drawing)
fig, ax = plt.subplots(figsize=(12, 6.4))
ax.add_patch(Rectangle((0, 0), 16, 9, fc="#FAFAFA", ec=BLACK, lw=2))
ax.add_patch(Rectangle((0, 8.2), 16, 0.8, fc="#E8EEF0", ec=BLACK))
ax.text(0.3, 8.6, "wokwi.com  -  your project", va="center", fontsize=11)
for k, tab in enumerate(["sketch.ino", "diagram.json", "Library Manager"]):
    ax.add_patch(Rectangle((0.1 + k * 2.3, 7.6), 2.2, 0.5, fc="white" if k == 0 else "#EEEEEE", ec=GREY))
    ax.text(0.2 + k * 2.3, 7.85, tab, va="center", fontsize=9.5)
for k, line in enumerate(["void setup() {", "  Serial.begin(9600);", "  pinMode(8, OUTPUT);", "}", "void loop() {",
                          "  digitalWrite(8, HIGH);", "  delay(500);", "  ..."]):
    ax.text(0.3, 7.2 - k * 0.42, line, fontsize=10, family="monospace", va="center")
ax.plot([7.2, 7.2], [0, 8.2], color=GREY, lw=1.5)
ax.add_patch(Circle((7.9, 7.6), 0.35, fc=GREEN, ec=BLACK)); ax.text(7.9, 7.6, ">", ha="center", va="center", color="white", weight="bold")
ax.text(8.4, 7.6, "start the simulation", va="center", fontsize=10)
ax.add_patch(Rectangle((11.5, 7.35), 0.5, 0.5, fc="white", ec=BLACK)); ax.text(11.75, 7.6, "+", ha="center", va="center", fontsize=14)
ax.text(12.15, 7.6, "add a part", va="center", fontsize=10)
ax.add_patch(FancyBboxPatch((8.0, 3.0), 5.0, 3.6, boxstyle="round,pad=0,rounding_size=0.2", fc=BOARD, ec=BLACK))
ax.text(10.5, 4.8, "Arduino Uno", color="white", ha="center", fontsize=11)
ax.add_patch(Circle((14.6, 5.7), 0.3, fc="#FF5252", ec=BLACK)); ax.text(14.6, 6.25, "LED", ha="center", fontsize=9.5)
ax.add_patch(Rectangle((13.95, 4.6), 0.3, 0.8, fc="#D7B98E", ec=BLACK)); ax.text(14.85, 4.75, "220\nohm", fontsize=9, ha="left")
ax.plot([12.6, 12.6, 14.1, 14.1], [6.6, 6.9, 6.9, 5.4], color=GREEN, lw=2)
ax.plot([14.1, 14.1], [4.6, 4.2], color=GREEN, lw=2); ax.plot([14.1, 14.6, 14.6], [4.2, 4.2, 5.4], color=GREEN, lw=2)
ax.plot([14.6, 14.6, 12.8], [5.4, 3.3, 3.3], color=BLACK, lw=2)
ax.add_patch(Rectangle((7.4, 0.2), 8.4, 2.3, fc="#263238", ec=BLACK))
ax.text(7.6, 2.2, "Serial Monitor (inside the simulator)", color="white", fontsize=9.5, va="center")
for k, line in enumerate(["Hello from Rover!", "seconds since power-on: 1", "seconds since power-on: 2"]):
    ax.text(7.6, 1.6 - k * 0.45, line, color="#C8E6C9", fontsize=9.5, family="monospace", va="center")
ax.set_xlim(-0.2, 16.2); ax.set_ylim(-0.2, 9.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig07-wokwi.png")

# Figure 7: hello_rover.ino on the PC test bench (times from pc_tests/test_hello_rover.cpp)
fig, ax = plt.subplots(figsize=(11, 4.2))
edges = [0.0001, 0.5001, 1.0002, 1.5002, 2.0004, 2.5004, 3.0005]
ts, vs = [0.0], [0]
level = 0
for e in edges:
    ts += [e, e]; vs += [level, 1 - level]; level = 1 - level
ts.append(3.2); vs.append(level)
ax.plot(ts, [v * 5 for v in vs], color=BLUE, lw=2.5, label="pin 13 (the L LED)")
for t, txt in [(0.0, "Hello from Rover!"), (1.0001, "seconds ...: 1"), (2.0003, "seconds ...: 2"), (3.0004, "seconds ...: 3")]:
    ax.axvline(t, color=GREEN, ls=":", lw=2)
    ax.text(t + 0.03, 6.0, txt, fontsize=10, color=GREEN)
ax.set_ylim(-0.5, 7.0); ax.set_xlim(-0.05, 3.25)
ax.set_xlabel("time since power-on (s)"); ax.set_ylabel("pin 13 (V)")
ax.legend(loc="center right", fontsize=10); ax.grid(alpha=0.3)
ax.set_title("hello_rover.ino: green dotted lines = a line printed on Serial", fontsize=12)
save(fig, "fig06-hello-timeline.png")

# Figure 8: Rover's pin plan (the fixed plan from Application 1)
fig, ax = plt.subplots(figsize=(13, 6.6))
pos = uno(ax)
groups = [(BLUE, "encoders", [("2", "left encoder A (interrupt)"), ("3", "right encoder A (interrupt)"),
                              ("4", "left encoder B"), ("7", "right encoder B")]),
          (ORANGE, "motor driver", [("5", "left motor speed (PWM)"), ("6", "right motor speed (PWM)"),
                                    ("11", "left motor IN1"), ("12", "left motor IN2"),
                                    ("9", "right motor IN1"), ("10", "right motor IN2")]),
          (GREEN, "sensors", [("8", "ultrasonic, one pin"), ("A0", "line sensor L"), ("A1", "line sensor M"),
                              ("A2", "line sensor R"), ("A3", "battery voltage")]),
          (L_RED, "I2C bus", [("A4", "SDA: IMU + I/O expander"), ("A5", "SCL: IMU + I/O expander")]),
          (GREY, "other", [("13", "status LED (the board's L)"), ("0", "USB serial: keep free"), ("1", "USB serial: keep free")])]
y = 52
for color, title, items in groups:
    ax.text(78, y, title, fontsize=12, weight="bold", color=color if color != L_RED else RED)
    y -= 3.6
    for pin, job in items:
        if not job:
            continue
        x, py = pos[pin]
        ax.add_patch(Rectangle((x - 1.1, py - 1.3), 2.2, 2.6, fc=color, ec="white", lw=0.8))
        ax.add_patch(Rectangle((78, y - 0.9), 2.2, 2.2, fc=color, ec=BLACK, lw=0.8))
        ax.text(82, y + 0.2, f"pin {pin}: {job}", fontsize=10.5, va="center")
        y -= 3.1
    y -= 1.2
ax.text(34, 27, "Rover's pin plan\n(bumpers and buzzer go on\nthe I2C expander, Chapter 108;\nevery Uno pin is now used)",
        ha="center", va="center", fontsize=10.5, color="white")
ax.set_xlim(-8, 128); ax.set_ylim(-36, 58); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig08-rover-pins.png")
print("figures saved in", os.path.abspath(OUT))
