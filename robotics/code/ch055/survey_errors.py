# survey_errors.py - how sure are we? Repeat the survey 10,000 times with small random errors
import math
import random

from heights import height_from_one_angle
from room_survey import place_corners, shoelace_area
from survey_data import (ANGLE_ERROR_DEG, CEILING_ANGLE_DEG, DIAGONALS, EYE_M, SIDES,
                         TAPE_ERROR_M, WALL_DISTANCE_M)

random.seed(55)
RUNS = 10_000


def jitter(lengths):
    return {k: v + random.gauss(0, TAPE_ERROR_M) for k, v in lengths.items()}


areas = []
ceilings = []
for _ in range(RUNS):
    corners = place_corners(jitter(SIDES), jitter(DIAGONALS))
    areas.append(shoelace_area([corners[k] for k in "ABCDE"]))
    ceilings.append(height_from_one_angle(EYE_M + random.gauss(0, TAPE_ERROR_M),
                                          WALL_DISTANCE_M + random.gauss(0, TAPE_ERROR_M),
                                          CEILING_ANGLE_DEG + random.gauss(0, ANGLE_ERROR_DEG)))


def mean_and_spread(values):
    m = sum(values) / len(values)
    s = math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))
    return m, s


area_m, area_s = mean_and_spread(areas)
ceil_m, ceil_s = mean_and_spread(ceilings)
print(f"area   : {area_m:.3f} m^2, spread {area_s:.3f} m^2 ({100 * area_s / area_m:.2f}%)")
print(f"ceiling: {ceil_m:.3f} m,   spread {ceil_s:.3f} m   ({100 * ceil_s / ceil_m:.2f}%)")
print(f"so we report: area {area_m:.2f} +/- {2 * area_s:.2f} m^2, ceiling {ceil_m:.2f} +/- {2 * ceil_s:.2f} m")
