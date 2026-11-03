# The Robots You Will Build

In this course you build **28 robots and machines**. Many of them grow with you. **Rover** is your main robot. It starts as two wheels and an Arduino. It ends as a ROS 2 robot with a camera, a LiDAR and an arm.

Every robot has a **simulation track**: it runs in Python or in a free simulator, so you can do all of it on a computer.
Most robots also have a **hardware track**: you build the real robot with cheap parts. The hardware is optional.

Prices are rough ranges in US dollars (2026). They are different in each country.

---

## Overview

| # | Robot | What it is | Main chapters | Simulation | Real hardware | Rough cost |
|---|---|---|---|---|---|---|
| 1 | **GridBot** | A robot that moves on a grid on the screen | 36 | ✅ Python | — | free |
| 2 | **Moth** | A small robot that drives towards light, made only with transistors, no code | 93 | — | ✅ | $10–15 |
| 3 | **Reaction box** | A traffic light and a reaction-time game (first Arduino gadget) | 113 | ✅ Wokwi | ✅ | starter kit |
| 4 | **Sonar meter** | Measures distance and warns about obstacles | 135 | ✅ Wokwi | ✅ | starter kit |
| 5 | **Pan-tilt head** | A camera head that turns left–right and up–down with two servos | 153 | ✅ Wokwi | ✅ | $10 |
| 6 | **MotorLab** | A test bench: one DC motor with an encoder, used for all control experiments | 152, 229–230, 252 | ✅ Python model | ✅ | $15–25 |
| 7 | **Beam** | A ball rolling on a beam; the robot tilts the beam to keep the ball in place | 231, 253 | ✅ Python | ✅ | $15–20 |
| 8 | **Cart-pole** | A cart that balances a standing stick | 269, 280, 520 | ✅ Python | optional | — |
| 9 | **Rover** | **The main robot.** Two-wheel differential drive. Grows in stages (see below) | 281–313 and many later parts | ✅ Python, Gazebo, Webots | ✅ | $40–60 (base) |
| 10 | **Balancer** | A two-wheel robot that balances standing up, like a person on a bicycle wheel | 310–312 | ✅ Python | ✅ | $30–45 |
| 11 | **Racer** | A small car with real steering (Ackermann). Follows a track, then parks itself | 301–305, 476 | ✅ Python | ✅ optional | $40–70 |
| 12 | **Glide** | A robot with mecanum wheels that can drive sideways | 307–308 | ✅ Python | optional | $50–80 |
| 13 | **Scribe** | A small three-servo arm that draws pictures with a pen | 348–349, 369 | ✅ Python | ✅ | $15–25 |
| 14 | **Six** | A six-axis robot arm, like a factory arm | 370, 392, 410, 613 | ✅ Python, MoveIt 2 | optional | $80–150 |
| 15 | **Tilt display** | An IMU board that shows its tilt, made smooth with a Kalman filter | 428 | ✅ Python | ✅ | $5–10 |
| 16 | **Colour sorter** | Scribe plus a camera: picks up blocks and sorts them by colour | 499 | ✅ Python | ✅ | +$20 (camera) |
| 17 | **Learner** | A line follower that learns to drive by copying you | 521 | ✅ Python | ✅ (Rover) | — |
| 18 | **CAN base** | A two-motor robot base where the motors talk over CAN bus | 548 | — | ✅ | $25–40 |
| 19 | **Walker** | A legged robot that learns to walk by itself (reinforcement learning) | 594, 687 | ✅ MuJoCo | — | free |
| 20 | **HomeBot** | Rover as a full ROS 2 robot: makes a map of a house and drives to any room | 586, 606–612 | ✅ Gazebo | ✅ (Rover) | — |
| 21 | **Hover** | A quadcopter drone. First our own flight controller on a test stand, then a full drone with PX4 that flies GPS missions by itself | 614–666 | ✅ Python, PX4 + Gazebo | ✅ | $150–300 |
| 22 | **Quad** | A four-legged walking robot with 12 servos: static walking, trotting, then a learned walking policy | 667–690 | ✅ Python, MuJoCo | ✅ | $60–120 |
| 23 | **Swarm** | Many small simulated robots that work together | 741–742 | ✅ Python | — | free |
| 24 | **Courier** | Final project 1: an autonomous delivery robot | 747 | ✅ Gazebo | ✅ (Rover) | — |
| 25 | **Sorter** | Final project 2: a pick-and-place arm that sees with a camera | 748 | ✅ | ✅ (Scribe or Six) | — |
| 26 | **Fetch** | Final project 3: a mobile manipulator (Rover with an arm) that brings you objects | 368, 749 | ✅ Gazebo | ✅ (Rover + Scribe) | — |
| 27 | **Hero** | A full-size humanoid robot in simulation: stands, balances, walks with ZMP control and with reinforcement learning | 691–734 | ✅ MuJoCo, Isaac Lab | — | free |
| 28 | **Buddy** | A real small humanoid (about 40 cm, 18 servos): poses, balance, walking, arm tasks, getting up after a fall | 691–738 | ✅ Python, MuJoCo | ✅ | $120–250 |

(Fetch, Courier, Sorter and HomeBot reuse Rover, Scribe and Six, so they cost little extra.)

---

## Rover grows with you

| Stage | Chapters | What Rover can do |
|---|---|---|
| 1. Rover drives | 281–282 | Arduino, two motors, a battery. Drives straight and turns. |
| 2. Rover counts | 288–290 | Wheel encoders. Knows how far it has driven (odometry). |
| 3. Rover feels | 291–297 | Bumpers, line sensors and distance sensors. Bump-and-turn, line following, wall following, obstacle avoidance. |
| 4. Rover races | 294 | A line-following race with a PID controller. |
| 5. Rover navigates | 298–300 | Drives to a goal point and follows a path (pure pursuit). |
| 6. Rover solves a maze | 313 | Finds its way out of a maze. |
| 7. Rover sees | 498 | Raspberry Pi and a camera. Follows a coloured ball. |
| 8. Rover maps | 447 | A LiDAR. Makes a map and finds itself on it (SLAM). |
| 9. Rover speaks ROS 2 | 579 | ROS 2 nodes for motors, sensors and camera. |
| 10. Rover becomes HomeBot | 612 | Full navigation with Nav2: "go to the kitchen". |
| 11. Rover delivers | 747 | Courier: picks up a parcel point and drives it to a place. |
| 12. Rover gets an arm | 749 | Fetch: Rover carries Scribe and brings small objects. |

---

## Shopping list (only if you want real hardware)

| Kit | Used for | Rough cost |
|---|---|---|
| Arduino starter kit (Arduino Uno or compatible board, breadboard, wires, LEDs, resistors, buttons, a servo, an ultrasonic sensor) | Parts 5–8 | $30–50 |
| Multimeter and a small soldering iron | Parts 5 onward | $20–40 |
| Rover base: 2WD chassis, 2 gearmotors with encoders, motor driver (TB6612), battery pack | Rover, MotorLab | $40–60 |
| Sensors: line sensor array, IMU (accelerometer and gyroscope), time-of-flight distance sensor | Rover, Tilt display, Beam | $15–25 |
| 3–4 hobby servos | Scribe, Pan-tilt head | $15–25 |
| Raspberry Pi and a camera | Rover stages 7–12, Colour sorter | $80–130 |
| Low-cost 2D LiDAR | Rover stage 8, HomeBot | $70–100 |
| ESP32 board and two CAN transceiver modules | CAN base, FreeRTOS | $15–25 |
| Drone kit: frame, 4 brushless motors, 4 ESCs, propellers, flight controller, GPS, radio, LiPo batteries and a safe charger | Hover | $150–300 |
| 12 servos and a leg frame | Quad | $60–120 |
| 18 servos, a humanoid frame kit, a servo controller and an IMU | Buddy | $120–250 |
| Optional: 6-axis arm kit, mecanum chassis | Six, Glide | $50–150 each |

**No money? No problem.** Every robot except Moth and CAN base can be done fully in simulation. Those two chapters show every result with photos and plots, so you can read along.
