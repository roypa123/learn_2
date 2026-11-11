# heights.py - heights we cannot reach, from angles
import math

from survey_data import CEILING_ANGLE_DEG, EYE_M, SHELF_ANGLES_DEG, SHELF_STEP_M, WALL_DISTANCE_M


def height_from_one_angle(eye_m, distance_m, angle_deg):
    return eye_m + distance_m * math.tan(math.radians(angle_deg))


def height_from_two_angles(eye_m, step_m, far_deg, near_deg):
    t_far = math.tan(math.radians(far_deg))
    t_near = math.tan(math.radians(near_deg))
    near_distance = step_m * t_far / (t_near - t_far)
    return eye_m + near_distance * t_near, near_distance


if __name__ == "__main__":
    ceiling = height_from_one_angle(EYE_M, WALL_DISTANCE_M, CEILING_ANGLE_DEG)
    print(f"ceiling height: {ceiling:.3f} m")

    shelf, distance = height_from_two_angles(EYE_M, SHELF_STEP_M, *SHELF_ANGLES_DEG)
    print(f"shelf top     : {shelf:.3f} m, found {distance:.3f} m in front of the second spot")
