# survey_data.py - the measurements taken in one example room (replace them with your own)

# tape measurements in metres, read to the nearest 0.5 cm
SIDES = {"AB": 4.200, "BC": 3.105, "CD": 3.155, "DE": 1.695, "EA": 2.100}
DIAGONALS = {"AC": 5.340, "AD": 3.510}
CHECKS = {"BE": 4.695, "BD": 4.460}          # extra lengths, used only to check the result

# ceiling: phone held 1.20 m above the floor, 3.00 m from the wall, angle up to the ceiling line
EYE_M = 1.20
WALL_DISTANCE_M = 3.00
CEILING_ANGLE_DEG = 30.3

# a high shelf behind a table: two angles to its top edge, 1.50 m apart
SHELF_ANGLES_DEG = (25.0, 38.0)
SHELF_STEP_M = 1.50

# how good our tools are (one standard deviation)
TAPE_ERROR_M = 0.005
ANGLE_ERROR_DEG = 0.5
