# Applications — Where Every Theory Is Used in Real Robots

This course never stops at "here is the theory". Every theory chapter has a **🏭 Real robot applications** section (rules: `MASTER_PLAN.md` §5.2):
- **at least 5 applications**, from **at least 3 different fields** of robotics;
- **at least 2 of them worked in full**: the real problem, the numbers, the maths, the code, the figure and the result;
- the others explained in 1–3 paragraphs, with real numbers.

This file lists the main applications for each theory. Chapter writers start from this list and add more.

## The fields of robotics we take examples from

| Sign | Field | Examples of robots |
|---|---|---|
| 🏭 | Factory and industrial | welding, painting and pick-and-place arms, CNC, conveyors, delta robots |
| 📦 | Warehouse and logistics | shelf-moving robots, picking arms, sorting, delivery robots |
| 🚗 | Self-driving vehicles | cars, trucks, tractors, autonomous racing |
| 🚁 | Drones | camera drones, inspection, spraying, delivery, mapping, racing |
| 🦿 | Legged and humanoid | four-legged inspection robots, humanoids, exoskeletons |
| 🏥 | Medical | surgical robots, rehabilitation robots, prosthetic hands, hospital delivery |
| 🚀 | Space | planetary rovers, robot arms on space stations, satellites |
| 🌊 | Underwater and marine | underwater vehicles (ROV/AUV), boats |
| 🌾 | Agriculture | autosteer tractors, weeding robots, fruit pickers, milking robots |
| 🏠 | Home and service | robot vacuums, lawn mowers, hotel and restaurant robots, toys |
| 🔥 | Search, rescue and inspection | rubble robots, pipe crawlers, power-line and bridge inspection |

---

## Part 3 — School maths

| Theory | Applications |
|---|---|
| Units and conversion | 🚀 A space probe was lost in 1999 because one team used pound-force and another used newtons: we redo the mistake with numbers. 🏭 Motor datasheets in oz·in vs N·m. 🚁 Propeller sizes in inches, thrust in grams. |
| Pythagoras, distance | 📦 Distance from a robot to a shelf. 🚁 Straight-line distance to a drone flying at a height. 🏠 Vacuum coverage of a room. |
| Trigonometry (sin, cos, tan) | 🚁 A tilted drone: how much thrust pushes forward (T·sin θ) and how much holds it up (T·cos θ). 🚀 Can a rover climb a 25° slope? 🌾 How wide a strip of field a camera sees from 30 m (field of view). 🏭 Height reached by an arm link at 40°. |
| `atan2`, wrapping angles | 🚗 The heading error of a car that crosses ±180°. 🏠 A vacuum turning the short way round. |
| Law of cosines | 🏭 The elbow angle of a two-link arm (first taste of IK). 🦿 Knee angle needed for a given hip-to-ankle distance. |
| Exponentials and logarithms | 🏠 Battery voltage dropping. 🏭 Motor speed rising with a time constant. 🌊 Sound getting weaker with distance underwater, in dB. 📦 Wi-Fi signal strength. |
| Floating-point error | 📦 Odometry slowly drifting because of rounding. 🚀 A clock error that grows over a long mission. |

## Part 4 — Physics

| Theory | Applications |
|---|---|
| Newton's laws, F = m·a | 🚁 Hover thrust = m·g for a 1.2 kg drone. 📦 The fastest acceleration before a box slides off a robot (a ≤ μ·g). 🦿 Ground force on a robot foot when it lands from a jump. |
| Friction | 🏭 Gripper squeeze force needed so a part does not slip (F ≥ m·g / 2μ). 🚗 Braking distance on wet and dry roads. 🚀 Wheels slipping in sand. |
| Torque and levers | 🏭 Motor torque to hold an arm straight out (τ = m·g·L). 🦿 Knee torque in an exoskeleton when standing up. 🏠 Wheel torque for a vacuum to climb a carpet edge. |
| Moment of inertia | 🚀 Satellites turning with reaction wheels. 🚁 Why a drone yaws slowly. 🦿 How humanoids swing their arms to keep balance. |
| Work, energy, power | 🚁 The flight time of a delivery drone. 📦 Battery size for an 8-hour warehouse shift. 🚗 Energy got back with regenerative braking. |
| Gears, pulleys, belts | 🦿 Harmonic drives in humanoid joints. 🚀 A rover gearbox for steep slopes. 🏭 A belt-driven 3D printer axis. |
| Centre of mass | 📦 A forklift tipping with a high load. 🦿 A humanoid keeping its CoM over its feet. 🚀 A rover on a side slope. |
| Euler simulation | All fields: every simulator in the course starts here. A falling ball, a rolling cart, then a whole drone. |

## Part 5 — Electronics

| Theory | Applications |
|---|---|
| Ohm's law, power | 🏭 Choosing a current-sense resistor to find a motor stall. 🏠 Heat in a motor driver. 🚁 Wire thickness for 40 A drone motors. |
| Voltage divider | Battery-level monitor on every mobile robot. 🌾 A soil moisture sensor. |
| Capacitors | 📦 A controller that restarts when motors start (brown-out), and how capacitors stop it. 🏭 RC filters on noisy sensor wires. |
| Diodes, flyback | 🏭 Relays and solenoid valves in a factory cell. 📦 An electromagnet gripper. |
| Transistors, MOSFETs | 🚁 Inside an ESC: six MOSFETs switching a brushless motor. 🏠 Switching a vacuum fan. |
| Batteries | 🚁 LiPo choice and safety for drones. 🏥 Hospital robots that must run all day. 🚀 Batteries kept warm on cold planets. |

## Part 6 — Microcontrollers

| Theory | Applications |
|---|---|
| PWM | Servo angles, motor speeds, drone ESC signals, LED brightness on robot "faces". |
| Interrupts | 🏭 Counting 10,000 encoder pulses per second. All fields: the emergency stop button. |
| `millis()` timing, state machines | 🏠 Vacuum modes (clean, return, dock, charge). 🚁 Drone arming and disarming rules. 🏭 A pick-and-place cell sequence. 🌾 A milking robot's steps. |
| UART, I2C, SPI | GPS (UART), IMU (I2C/SPI), LiDAR (UART), displays (SPI) on the same robot. |

## Part 7 — Sensors

| Theory | Applications |
|---|---|
| Encoders | 📦 Odometry. 🏭 Arm joint angles. 🏭 CNC axis position. |
| IMU (accelerometer, gyroscope, magnetometer) | 🚁 Drone attitude. 🦿 Humanoid fall detection. 🏠 Camera gimbals. 🌊 Heading under water, where GPS does not work. |
| Ultrasonic, time-of-flight | 🚗 Parking sensors. 🏠 Cliff sensors that stop a vacuum falling down stairs. 🚁 Drone height above the ground when landing. |
| LiDAR | 🚗 Self-driving cars. 📦 Safety zones around warehouse robots. 🌾 Measuring trees in a forest. |
| GPS, RTK GPS | 🌾 Tractors steering to 2 cm accuracy. 🚁 Drone missions. 🌊 Boats returning home. |
| Force and pressure sensors | 🏥 Feeling tissue force in surgery. 🦿 Foot sensors that measure the ZMP. 🏭 Cobots stopping when they touch a person. |
| Calibration | 🚗 Camera–LiDAR calibration on a car. 🚁 IMU bias at power-up. 🏭 Tool-centre-point calibration on a welding arm. |

## Part 8 — Actuators

| Theory | Applications |
|---|---|
| DC motor equations | Sizing the wheel motors of a delivery robot. Choosing a fuse from the stall current. |
| Servos | Hobby arms, RC car steering, Buddy's 18 joints. |
| Steppers | 🏭 3D printers and CNC. 🏥 Lab robots moving liquid samples. Camera sliders. |
| Brushless motors | 🚁 Drones. 🦿 Quasi-direct-drive legs in four-legged robots. Electric bikes. |
| Hydraulics, pneumatics | 🏭 Excavators and presses. 🏭 Suction cups and soft grippers. 🦿 Strong hydraulic legged robots. |
| Grippers | 📦 Suction picking of parcels. 🌾 Soft grippers that pick fruit without bruising it. 🏥 Prosthetic hands. |

## Part 9 — Linear algebra

| Theory | Applications |
|---|---|
| Vectors | 🚁 Adding wind to drone velocity. 🦿 Adding up all the foot forces on a four-legged robot. |
| Dot product | 🚗 Is the obstacle in front of us or behind? 📦 The angle between the heading and the goal. 🌾 Sun angle on a solar-powered robot. |
| Cross product | 🏭 Torque from a force at the end of a lever. 📦 Surface normals for suction picking. 🚗 Is the goal to the left or to the right? |
| Rotation matrices | 🚗 Turning LiDAR points into the car frame. 🚁 Turning the camera image to point north. |
| Solving linear systems | 📦 Indoor positioning from radio beacons (UWB). 🦿 Sharing weight between the feet. |
| Least squares | 🏭 Sensor calibration curves. 🏠 Fitting a wall line to LiDAR points. 🏭 Hand–eye calibration. |
| Eigenvalues and eigenvectors | Uncertainty ellipses. 📦 The main axis of an object, to grasp it (PCA). 🏭 Vibration modes of a long arm. |
| SVD | Point-cloud alignment (ICP). Pseudoinverse IK. Manipulability of an arm. |

## Part 10 — Calculus

| Theory | Applications |
|---|---|
| Derivatives | Speed from encoder counts. 🏭 Jerk limits for comfortable lifts and smooth arms. The D term of PID. |
| Integrals | Odometry (position from speed). The I term of PID. 🚁 Energy used on a flight. |
| Differential equations | Every robot simulator. A battery model. 🌊 Water drag on an underwater vehicle. |
| Gradient descent | Training neural networks. Numerical IK. Potential-field planning. |
| Jacobian | Arm velocity. Linearising the EKF. |
| Taylor series, linearisation | The EKF. LQR around the upright balance point. |
| Optimisation | Trajectory optimisation, MPC, path smoothing, fitting parameters. |

## Part 11 — Probability

| Theory | Applications |
|---|---|
| Bayes' rule | 🏠 "Am I in front of a door?" localization. 📦 Occupancy grids (is this cell blocked?). 🏭 Machine fault diagnosis. |
| Gaussians | Sensor noise models. The heart of the Kalman filter. |
| Covariance | 🚁 GPS uncertainty ellipses. 🚗 Trusting the better sensor more when fusing. |
| Monte Carlo | 📦 Particle-filter localization in a warehouse. 🚁 "Will the battery last?" risk for a drone mission. |

## Parts 12–14 — Control

| Theory | Applications |
|---|---|
| On-off control, hysteresis | 🚀 Battery heaters on a rover on a cold planet. 🌾 Greenhouse heating and watering. 🏠 Docking-station charging. |
| P, PI, PID | 🚁 Drone rate loops. 🚗 Cruise control. 🏭 3D-printer nozzle temperature. 🏭 Joint position of an arm. 📦 Line following. 🏠 Camera gimbals. |
| Feedforward | 🏭 Gravity feedforward on an arm. 🚁 Hover throttle feedforward. 🏭 Velocity feedforward on CNC axes. |
| Cascade control | 🏭 Industrial servo drives (current → speed → position). 🚁 Drones (position → velocity → attitude → rate). |
| Modelling (mass–spring–damper, motor, tank) | 🚗 Car suspension. 🏭 Conveyor motor. 🌾 Irrigation tank level. |
| Laplace, transfer functions, poles | Predicting overshoot before building. 🚀 Telescope and antenna pointing. |
| Root locus | 🏭 Choosing a gain for a ball-on-beam. 🚀 Satellite pointing. |
| Bode, margins, notch filters | 🚁 Removing frame vibration from drone gyros. 🏭 A long, flexible arm that shakes. 🏭 Bandwidth of a fast pick-and-place axis. |
| Digital control, sampling | 🚁 Drone loops at 1–8 kHz. 📦 A rover loop at 50 Hz. Aliasing in a vibrating machine. |
| State space, pole placement | 🏠 Self-balancing personal transporters. 🏭 Overhead cranes that stop the load swinging. |
| Observers | 🏭 Sensorless brushless motor control. Estimating the speed of a pendulum when we only measure its angle. |
| LQR | 🏠 Balancing robots. 🚀 Satellite attitude. 🚁 Drone hover. 🦿 Humanoid balance. |
| MPC | 🚗 Lane keeping in self-driving cars. 🦿 Four-legged walking (convex MPC). 🚁 Drone racing. 🏭 Chemical plants and building heating. |
| Lyapunov, nonlinear control | Proving a robot-arm PD controller is stable. 🚗 Tracking controllers for wheeled robots. |
| Sliding mode | 🌊 Underwater vehicles in unknown currents. 🏭 Motor control with changing loads. |
| Adaptive control | 🏭 An arm picking up loads it does not know. 🚁 A drone carrying different parcels. |

## Part 15 — Mobile robots

| Theory | Applications |
|---|---|
| Differential-drive kinematics | 🏠 Robot vacuums. 📦 Shelf-moving warehouse robots. 🏥 Hospital delivery robots. |
| Odometry and drift | 🚀 Planetary rovers checking wheel odometry with cameras. 🏠 Vacuums that re-find their dock. |
| Nonholonomic constraints | 🚗 Why a car cannot park sideways. 📦 Pallet trucks. |
| Ackermann, bicycle model | 🚗 Self-driving cars. 🌾 Tractor autosteer. 📦 Airport baggage tugs. |
| Pure pursuit, Stanley, MPC tracking | 🚗 Autonomous racing. 🚗 The 2005 desert robot-car race won with the Stanley method. 🌾 Following crop rows. |
| Mecanum, omni wheels | 🏭 Platforms that move aircraft wings and large parts. 🏥 Hospital beds that move sideways. |
| Skid-steer, tracks | 🔥 Bomb-disposal and rubble robots. 🏠 Lawn mowers. 🚀 Tracked lunar test vehicles. |
| Balancing robots | 🏠 Personal transporters. 📦 Two-wheeled delivery robots. |

## Part 16 — Frames and transformations

| Theory | Applications |
|---|---|
| Homogeneous transforms | 🚗 LiDAR on the roof → car → map. 🏭 Camera on the wrist (hand–eye). 🚁 Gimbal camera → drone → world. |
| Quaternions | 🚁 Every modern flight controller. VR headsets. 🚀 Spacecraft attitude. |
| Gimbal lock | 🚀 Apollo-era spacecraft guidance had to avoid gimbal lock: we rebuild why. |
| Frame trees | 🦿 A humanoid with 30+ frames. 📦 Mobile manipulators. |

## Parts 17–18 — Arm kinematics

| Theory | Applications |
|---|---|
| Forward kinematics | 🏭 Checking a welding path. 🏥 Where the surgical tool tip is. 🏭 Excavator bucket position. |
| Inverse kinematics | 🏭 Welding and painting robots reaching a seam. 🦿 Humanoid foot placement. Game and film animation. |
| Jacobian | 🏥 Teleoperation (hand motion → tool motion). 🏭 Cobot collision detection from joint torques. |
| Singularities, manipulability | 🏭 Painting robots that avoid wrist flips. 🚀 Space arm planning. |
| Redundancy, null space | 🚀 Seven-joint space station arms. 🏥 Surgical arms that pivot about the cut in the skin. |
| Mobile manipulators | 📦 Warehouse picking robots. 🏠 Home helpers. 🌾 Fruit-picking platforms. |

## Part 19 — Dynamics

| Theory | Applications |
|---|---|
| Gravity compensation | 🏭 Cobots you can guide by hand. 🦿 Exoskeletons that carry their own weight. |
| Computed torque | 🏭 Very fast delta robots packing food. |
| Force control, hybrid control | 🏭 Polishing, grinding and sanding. 🏭 Peg-in-hole assembly. |
| Impedance, admittance | 🏭 Cobots working beside people. 🏥 Rehabilitation robots. 🏥 Gentle touch in surgery. |
| Identification | 🏭 Estimating an unknown payload. Better models for better control. |

## Part 20 — Trajectories

| Theory | Applications |
|---|---|
| Trapezoidal, S-curve | 🏭 CNC machines and 3D printers. Lifts. 📦 Conveyor transfers. |
| Quintic, minimum jerk | Film camera cranes. Human-like arm motion. 🏥 Smooth rehabilitation exercises. |
| Splines | 🚗 Smooth car paths. 🚁 Racing through gates. |
| Time-optimal | 🏭 Shorter cycle times in packaging. |
| Trajectory optimisation | 🦿 Jumps and flips. 🚁 Minimum-snap drone paths. 🏭 Arm motion around obstacles. |

## Part 21 — Estimation

| Theory | Applications |
|---|---|
| Complementary filter | 🚁 Cheap flight controllers. Phone orientation. 🏠 Balancing robots. |
| Kalman filter | 🚀 The Apollo navigation computer. 🚗 GPS + IMU in cars. 🚗 Tracking pedestrians. |
| EKF | 🚁 The EKF inside real flight stacks. 📦 Fusing wheels, IMU and GPS on mobile robots. |
| UKF | 🚀 Spacecraft. Strongly curved (nonlinear) systems. |
| Particle filter | 📦 Warehouse localization on a known map. 🚗 Tracking in crowded scenes. |
| LQG | 🏠 Balancing with noisy sensors. 🚀 Pointing with noisy star trackers. |

## Part 22 — Maps and SLAM

| Theory | Applications |
|---|---|
| Occupancy grids | 🏠 Vacuum maps. 📦 Warehouse maps. |
| Monte Carlo localization | 🏥 Hospital and hotel robots on a known map. |
| ICP | 🏭 Aligning 3D scans to inspect buildings. 🚗 LiDAR odometry. |
| Graph SLAM, loop closure | 🔥 Mapping mines and caves. 🚗 HD maps for cars. AR headsets. |
| Visual SLAM | Phone AR. 🚁 Drones flying indoors. |

## Part 23 — Path planning

| Theory | Applications |
|---|---|
| BFS, Dijkstra, A* | 📦 Routing hundreds of warehouse robots on a grid. Car navigation. Game characters. |
| D* Lite (replanning) | 🚀 Mars rovers replanning on unknown ground (a D* variant flew on them). 🔥 Rescue robots in changing rubble. |
| PRM, RRT, RRT* | 🏭 Arms in cluttered cells (MoveIt). 🏥 Steering surgical needles. |
| Dubins, Reeds–Shepp, Hybrid A* | 🚗 Automatic parking. 🚁 Fixed-wing paths (Dubins). |
| DWA, elastic bands | 🏥 Service robots moving through crowds. |
| State lattices | 🚗 Self-driving car planners. |
| Task and motion planning | 🏠 A home robot that makes tea: what to do, and how to move. |

## Part 24 — Computer vision

| Theory | Applications |
|---|---|
| Colour thresholding | 🌾 Sorting fruit by ripeness. 🏠 Following a ball. |
| Edges, Hough transform | 🚗 Lane detection. 🏭 Reading dial gauges. |
| Features, matching | Visual odometry. Place recognition. Panoramas. |
| Calibration, PnP, markers | 🏠 Docking to a charger with a tag. 🏭 Bin picking. AR. |
| Stereo, depth | 🚗 Obstacle detection. 🌾 Measuring crop height. |
| Point clouds, RANSAC | 🏭 Finding the table plane to pick objects. 📦 Measuring boxes. |
| Optical flow | 🚁 Holding position without GPS. Insect-like flying robots. |

## Part 25 — Machine learning

| Theory | Applications |
|---|---|
| Regression | Sensor calibration curves. 🏠 Remaining battery time. |
| Classification | 🚀 Terrain type from wheel vibration. 🏭 Spotting faulty parts. |
| CNNs, detection | 🌾 Finding weeds for precise spraying. 🚗 Pedestrian detection. 📦 Parcel detection. |
| Reinforcement learning | 🦿 Legged walking. 🏭 A robot hand turning a Rubik's cube (2019). 🚁 A learned drone racer that beat human champions (2023). |
| Imitation learning | 🏠 Folding laundry from human demonstrations. 🚗 Driving by copying a driver. |

## Part 26 — Real-time and communication

| Theory | Applications |
|---|---|
| Real-time deadlines, RTOS | 🚁 1 kHz drone loops. 🏭 Safety stops within milliseconds. |
| CAN bus | 🚗 Every modern car. 🦿 Motor drivers in legged robots and cobots. 🌾 Tractors and implements (ISOBUS is built on CAN). |
| EtherCAT | 🏭 Industrial arms. 🦿 Humanoids with many joints. |
| UART, I2C, SPI | GPS, IMU, LiDAR and displays on one robot. |
| TCP, UDP, MQTT | 📦 Monitoring a fleet of delivery robots. 🚁 Video from a drone. |

## Parts 27–29 — ROS 2 and simulators

| Theory | Applications |
|---|---|
| ROS 2 nodes, topics, tf2 | 📦 Warehouse fleets. 🦿 Research humanoids. 🌾 Field robots. |
| Nav2 | 🏥 Hospital, hotel and office robots. |
| MoveIt 2 | 🏭 Pick-and-place and machine tending. |
| Gazebo, Webots | Testing a field robot before it goes outside. |
| MuJoCo, Isaac Sim | 🦿 Training legged and humanoid walking. Synthetic images for training vision. |

## Parts 30–32 — Drones, legged robots, humanoids

| Theory | Applications |
|---|---|
| Drone dynamics and control | 🚁 Aerial filming. Bridge and power-line inspection. 🌾 Crop spraying. 📦 Parcel delivery. 🔥 Search and rescue. Mapping and photogrammetry. |
| Legged locomotion | 🔥 Industrial plant inspection. Climbing stairs. 🔥 Search and rescue on rubble. |
| Humanoid balance and walking | 🏭 Moving boxes in factories and warehouses. 🏠 Home help. 🚀 Space humanoids. 🏥 Exoskeletons that use the same balance maths. |
