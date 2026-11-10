# scan_to_world.py - move laser points from the robot's view to the map's view
import numpy as np

# where the robot is on the map (maths angle: 0 = along +x, counter-clockwise)
robot_x, robot_y, robot_deg = 2.0, 1.0, 30.0

# three points the robot sees, as (forward, left) in its OWN frame
points_robot = np.array([[1.0, 0.0],
                         [1.0, 1.0],
                         [0.0, 2.0]])

th = np.radians(robot_deg)
R = np.array([[np.cos(th), -np.sin(th)],      # the rotation matrix
              [np.sin(th),  np.cos(th)]])

# R @ each point, then shift by where the robot is
points_world = (R @ points_robot.T).T + np.array([robot_x, robot_y])

print("rotation matrix:")
print(R.round(3))
print("points on the map:")
print(points_world.round(3))
print("distances are unchanged:",
      np.allclose(np.linalg.norm(points_robot, axis=1),
                  np.linalg.norm(points_world - [robot_x, robot_y], axis=1)))
