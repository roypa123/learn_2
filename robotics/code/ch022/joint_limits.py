# joint_limits.py - check a humanoid's pose against each joint's safe range
LIMITS_DEG = {                # joint name: (lowest, highest) allowed angle
    "left_hip":    (-30, 90),
    "left_knee":   (0, 135),
    "left_ankle":  (-40, 25),
    "right_hip":   (-30, 90),
    "right_knee":  (0, 135),
    "right_ankle": (-40, 25),
}

pose_deg = {                  # the pose a planner has asked for
    "left_hip": 45,
    "left_knee": 140,
    "left_ankle": -10,
    "right_hip": 20,
    "right_knee": 30,
    "right_ankle": 31,
}

safe_pose = {}                # the pose we will really send
problems = 0

for joint, angle in pose_deg.items():
    low, high = LIMITS_DEG[joint]
    safe = angle
    if angle < low:
        safe = low
    elif angle > high:
        safe = high
    if safe != angle:
        problems += 1
        print(f"{joint}: {angle} is outside ({low}, {high}) -> using {safe}")
    safe_pose[joint] = safe

print("problems:", problems)
print("left_knee will go to", safe_pose["left_knee"])
