# rug_edge.py - can a robot vacuum push its front wheel up onto a rug?
import math

G = 9.81
WHEEL_RADIUS_M = 0.025          # the small front wheel
FRONT_LOAD_N = 0.30 * 3.5 * G   # 30% of a 3.5 kg robot rests on the front wheel
MAX_PUSH_N = 0.6 * 0.70 * 3.5 * G   # drive wheels: mu 0.6 x the 70% of the weight they carry


def push_needed(step_m):
    """Horizontal push at the axle to roll the wheel over a step: turn about the step's edge."""
    if step_m >= WHEEL_RADIUS_M:
        return float("inf")                       # the step is as high as the axle: impossible
    lever_weight = math.sqrt(WHEEL_RADIUS_M ** 2 - (WHEEL_RADIUS_M - step_m) ** 2)
    lever_push = WHEEL_RADIUS_M - step_m
    return FRONT_LOAD_N * lever_weight / lever_push   # push x lever_push = load x lever_weight


print(f"front wheel load {FRONT_LOAD_N:.2f} N, drive wheels can push {MAX_PUSH_N:.2f} N")
for step_mm in [2, 5, 10, 15, 20]:
    need = push_needed(step_mm / 1000)
    print(f"rug edge {step_mm:2d} mm: push needed {need:6.2f} N  ->  {'climbs' if need <= MAX_PUSH_N else 'stuck'}")
