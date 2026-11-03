# Robotics From Scratch — Syllabus

A very beginner-friendly robotics course. It goes from "what is a robot?" to SLAM, robot arms, machine learning, ROS 2, drones and humanoid robots.
It has **33 parts and 749 chapters**, about **21,000 pages** in total (see `MASTER_PLAN.md` for the page budget).

- Rules for writing every chapter: `MASTER_PLAN.md`
- Which chapter is next: `PROGRESS.md`
- Every robot you build, part by part: `ROBOTS.md`
- Where every theory is used in real robots: `APPLICATIONS.md`
- The original request: `t.md`

**Order:** every chapter only uses ideas from earlier chapters.
Programming comes first (Part 2). The maths comes just before the robot topic that needs it.

**Languages:** **Python** is the main language (taught from zero in Part 2).
**C++ for Arduino** is taught in Part 6, for small boards.
Real-time systems and the buses robots use (UART, I2C, SPI, CAN) are covered in depth in Part 26.
**ROS 2** (Python, then C++) is taught in Parts 27 and 29. The simulators Gazebo, Webots, MuJoCo and Isaac Sim are taught in Part 28.

**Core robotics and control (Parts 12–20 and 23), drones (Part 30), legged robots (Part 31) and humanoids (Part 32)** are written as detailed lectures with many figures: at least 15 pictures per chapter.

**Theory, then real applications.** No theory stays an outline. Every theory chapter shows at least 5 real uses from different fields (factories, warehouses, cars, drones, humanoids, medicine, space, underwater, farms, homes, rescue), and 2 of them are worked in full with numbers, code and figures.

**Theory and practice together.** Every chapter has a 🔧 hands-on lab, and every part ends with at least one project. You build 28 robots and machines (see `ROBOTS.md`).

**Hardware is optional.** Every idea can be tried in a Python simulation.
Hardware chapters say what to buy (a cheap Arduino kit) and also show a free simulator (Wokwi).

---

## Part 1 — Welcome to Robots (Ch 1–10)

| Ch | Title |
|---|---|
| 1 | How to use this book |
| 2 | What is a robot? Sense, think, act |
| 3 | A short history of robots |
| 4 | Kinds of robots: arms, wheeled, legged, flying, underwater, soft, humanoid |
| 5 | The parts of a robot: body, sensors, brain, actuators, power |
| 6 | How a robot "thinks": the control loop (catching a ball as an example) |
| 7 | Safety first: electricity, moving parts, batteries, tools |
| 8 | Setting up your computer: Python, a code editor, folders |
| 9 | Simulation or real hardware: what you need (and what is optional) |
| 10 | Your first robot on paper: designing a tiny cleaning robot |

## Part 2 — Programming in Python From Zero (Ch 11–36)

| Ch | Title |
|---|---|
| 11 | What is a program? Instructions in order |
| 12 | Running Python: the shell and script files |
| 13 | Numbers and arithmetic |
| 14 | Variables: boxes with names |
| 15 | Text: strings |
| 16 | Output and input: `print` and `input` |
| 17 | True and false: booleans and comparisons |
| 18 | Making decisions: `if`, `elif`, `else` |
| 19 | Repeating part 1: `while` loops |
| 20 | Repeating part 2: `for` loops and `range` |
| 21 | Lists |
| 22 | Tuples and dictionaries |
| 23 | Functions part 1: making your own commands |
| 24 | Functions part 2: parameters, return values, scope |
| 25 | Errors and debugging: reading error messages |
| 26 | Modules and the `math` module |
| 27 | Files: saving and reading data |
| 28 | Classes and objects part 1: a `Robot` class |
| 29 | Classes and objects part 2: methods and inheritance |
| 30 | Time and loops that run forever: timing a control loop |
| 31 | Random numbers: simulating noisy sensors |
| 32 | Drawing with `turtle`: a robot on the screen |
| 33 | Plotting data with `matplotlib` |
| 34 | NumPy part 1: arrays |
| 35 | NumPy part 2: array maths and speed |
| 36 | Project: GridBot, a text robot simulator on a grid |

## Part 3 — The Maths You Need, From School Level (Ch 37–55)

| Ch | Title |
|---|---|
| 37 | Numbers: whole numbers, decimals, fractions, negative numbers |
| 38 | Powers, roots and scientific notation |
| 39 | Units and measurement: SI units, converting units |
| 40 | Algebra part 1: letters for numbers, equations |
| 41 | Algebra part 2: solving equations, rearranging formulas |
| 42 | Coordinates and the number plane |
| 43 | Straight lines: slope and y = mx + c |
| 44 | Functions and graphs |
| 45 | Quadratic equations and parabolas |
| 46 | Simultaneous equations |
| 47 | Angles: degrees and radians |
| 48 | Geometry: triangles, Pythagoras, circles |
| 49 | Trigonometry part 1: sin, cos, tan in right triangles |
| 50 | Trigonometry part 2: the unit circle, `atan2`, wrapping angles |
| 51 | Trigonometry part 3: the law of sines and the law of cosines |
| 52 | Exponentials and logarithms (battery discharge, filters) |
| 53 | Sequences, sums and sigma (Σ) notation |
| 54 | Error, accuracy, precision and rounding in computers |
| 55 | Project: measuring a room with a tape and trigonometry |

## Part 4 — Physics for Robots (Ch 56–72)

| Ch | Title |
|---|---|
| 56 | Position, distance and displacement |
| 57 | Speed and velocity |
| 58 | Acceleration |
| 59 | Equations of motion with constant acceleration |
| 60 | Motion in two directions (first look at vectors) |
| 61 | Forces and Newton's three laws |
| 62 | Mass, weight and gravity |
| 63 | Friction and grip (traction) |
| 64 | Turning: angle, angular speed, angular acceleration |
| 65 | Torque and levers |
| 66 | Moment of inertia: how hard it is to spin something |
| 67 | Work, energy and power |
| 68 | Gears, pulleys and belts: trading speed for torque |
| 69 | Wheels and rolling |
| 70 | Centre of mass and balance: why robots fall over |
| 71 | Simulating physics in Python: small time steps (Euler's method) |
| 72 | Project: a rolling cart on a ramp, measured and simulated |

## Part 5 — Electricity and Electronics (Ch 73–93)

| Ch | Title |
|---|---|
| 73 | What is electricity? Charge and electrons |
| 74 | Voltage, current and resistance |
| 75 | Ohm's law with many worked examples |
| 76 | Power in circuits (P = V × I) and heat |
| 77 | Series and parallel circuits |
| 78 | Kirchhoff's laws |
| 79 | Voltage dividers |
| 80 | Breadboards, wires and reading circuit diagrams |
| 81 | The multimeter: measuring safely |
| 82 | LEDs and resistors |
| 83 | Switches and buttons, pull-up and pull-down resistors |
| 84 | Capacitors |
| 85 | Inductors and coils (why motors make voltage spikes) |
| 86 | Diodes and flyback protection |
| 87 | Transistors as switches (BJT) |
| 88 | MOSFETs |
| 89 | Batteries: types, capacity, C rating, safety |
| 90 | Voltage regulators and power supplies |
| 91 | Digital and analog signals, logic levels |
| 92 | Soldering and building a small circuit |
| 93 | Project: Moth — a light-seeking robot made only with transistors (no code) |

## Part 6 — Microcontrollers and Arduino (Ch 94–113)

| Ch | Title |
|---|---|
| 94 | What is a microcontroller? |
| 95 | The Arduino board, the Arduino IDE and the Wokwi simulator |
| 96 | C++ for Arduino part 1: `setup`, `loop`, variables, types |
| 97 | C++ for Arduino part 2: `if`, loops, functions, arrays |
| 98 | Blink: digital output |
| 99 | Reading buttons: digital input and debouncing |
| 100 | The serial monitor: talking to the computer |
| 101 | Analog input: the ADC |
| 102 | PWM: "fake" analog output |
| 103 | Timing without `delay`: `millis()` |
| 104 | State machines |
| 105 | Interrupts |
| 106 | Hardware timers |
| 107 | Communication part 1: UART |
| 108 | Communication part 2: I2C |
| 109 | Communication part 3: SPI |
| 110 | Libraries and how they work inside |
| 111 | Arduino talking to Python (`pyserial`) |
| 112 | Raspberry Pi: a small computer, GPIO with Python |
| 113 | Project: a traffic light and a reaction-time game |

## Part 7 — Sensors (Ch 114–135)

| Ch | Title |
|---|---|
| 114 | What is a sensor? Range, resolution, accuracy, noise |
| 115 | Buttons, limit switches and bumpers |
| 116 | Potentiometers: measuring an angle |
| 117 | Light sensors (LDR, photodiode) |
| 118 | Infrared sensors and line sensors |
| 119 | The ultrasonic distance sensor |
| 120 | Time-of-flight laser distance sensors |
| 121 | Temperature and humidity |
| 122 | Encoders part 1: how they count |
| 123 | Encoders part 2: quadrature and measuring speed |
| 124 | Accelerometers |
| 125 | Gyroscopes |
| 126 | Magnetometers and compasses |
| 127 | IMUs: putting the three together |
| 128 | Force and pressure sensors, load cells |
| 129 | Measuring current and voltage |
| 130 | GPS |
| 131 | Cameras as sensors (first look) |
| 132 | LiDAR |
| 133 | Calibration: making sensors honest |
| 134 | Noise and simple filters: average and median |
| 135 | Project: an obstacle-detecting distance meter |

## Part 8 — Actuators and Motors (Ch 136–153)

| Ch | Title |
|---|---|
| 136 | What is an actuator? |
| 137 | How a DC motor works: magnets and coils |
| 138 | Motor equations: back EMF, torque constant, speed–torque curve |
| 139 | Driving a motor both ways: the H-bridge |
| 140 | Speed control with PWM |
| 141 | Motor driver boards (L298N, TB6612) |
| 142 | Gearmotors and choosing a gearbox |
| 143 | Hobby servos |
| 144 | Stepper motors part 1: how they step |
| 145 | Stepper motors part 2: drivers and microstepping |
| 146 | Brushless motors and ESCs |
| 147 | Linear actuators and solenoids |
| 148 | Pneumatics and hydraulics (first look) |
| 149 | Grippers and end effectors |
| 150 | Choosing a motor: worked sizing examples |
| 151 | The power budget of a robot |
| 152 | A motor with encoder feedback (a preview of control) |
| 153 | Project: a pan-tilt camera head with two servos |

## Part 9 — Linear Algebra for Robots (Ch 154–174)

| Ch | Title |
|---|---|
| 154 | Vectors: arrows made of numbers |
| 155 | Adding, subtracting and scaling vectors |
| 156 | Length and unit vectors |
| 157 | The dot product: angles and projections |
| 158 | The cross product (3D) and torque again |
| 159 | Matrices: tables of numbers |
| 160 | Matrix times vector |
| 161 | Matrix times matrix |
| 162 | The identity matrix and the transpose |
| 163 | The determinant |
| 164 | The inverse of a matrix |
| 165 | Solving systems of equations (Gaussian elimination) |
| 166 | Linear transformations: matrices that move points |
| 167 | Rotation matrices in 2D |
| 168 | Orthogonal matrices |
| 169 | Rank and null space (gently) |
| 170 | Eigenvalues and eigenvectors |
| 171 | Least squares: fitting a line to sensor data |
| 172 | The SVD (gently) |
| 173 | Building a tiny linear algebra library, then using NumPy |
| 174 | Project: moving and turning a robot drawing with matrices |

## Part 10 — Calculus for Robots (Ch 175–191)

| Ch | Title |
|---|---|
| 175 | Change and rates of change |
| 176 | Limits (gently) |
| 177 | Derivatives: the slope at one point |
| 178 | Derivative rules |
| 179 | Derivatives of sin, cos and exp |
| 180 | The chain rule |
| 181 | Numerical derivatives in Python: speed from position |
| 182 | Integrals: area and adding up |
| 183 | Numerical integration: position from speed |
| 184 | Differential equations: what they are |
| 185 | Solving them with a computer: Euler and Runge–Kutta |
| 186 | Partial derivatives |
| 187 | The gradient and gradient descent |
| 188 | The Jacobian matrix |
| 189 | Taylor series and linearisation |
| 190 | Optimisation basics: minimums and constraints |
| 191 | Project: speed and distance from a real encoder log |

## Part 11 — Probability and Statistics (Ch 192–205)

| Ch | Title |
|---|---|
| 192 | Chance and probability |
| 193 | The rules of probability |
| 194 | Conditional probability |
| 195 | Bayes' rule (a robot looking for a door) |
| 196 | Random variables |
| 197 | Mean, variance and standard deviation |
| 198 | The normal (Gaussian) distribution |
| 199 | Combining Gaussians |
| 200 | Covariance and correlation |
| 201 | Multivariate Gaussians and uncertainty ellipses |
| 202 | Sampling and Monte Carlo |
| 203 | Histograms and probability on a grid |
| 204 | Noise models for sensors and motion |
| 205 | Project: a simulated noisy sensor and its statistics |

## Part 12 — Control Systems 1: Feedback and PID (Ch 206–231)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 206 | What is control? Open loop and closed loop |
| 207 | Block diagrams: drawing a control system |
| 208 | On-off (bang-bang) control and hysteresis |
| 209 | The setpoint, the error and the feedback signal |
| 210 | P control part 1: the idea |
| 211 | P control part 2: steady-state error |
| 212 | I control part 1: removing steady-state error |
| 213 | I control part 2: overshoot and integral windup |
| 214 | D control part 1: damping |
| 215 | D control part 2: noise and derivative filtering |
| 216 | PID together: how the three terms work as a team |
| 217 | Reading response graphs: rise time, overshoot, settling time, steady-state error |
| 218 | Tuning PID part 1: by hand, step by step |
| 219 | Tuning PID part 2: Ziegler–Nichols and Cohen–Coon |
| 220 | PID in code part 1: time steps and sample rate |
| 221 | PID in code part 2: anti-windup, derivative kick, output limits, bumpless transfer |
| 222 | Modelling systems part 1: mass–spring–damper |
| 223 | Modelling systems part 2: the DC motor (electrical and mechanical) |
| 224 | Modelling systems part 3: the pendulum, heat and liquid tanks |
| 225 | First-order systems and the time constant |
| 226 | Second-order systems: natural frequency and damping ratio |
| 227 | Feedforward control |
| 228 | Cascade control: current, speed and position loops |
| 229 | Project: motor speed control with PID |
| 230 | Project: motor position control with cascade PID |
| 231 | Project: Beam — balancing a ball on a beam with PID |

## Part 13 — Control Systems 2: Classical Analysis and Design (Ch 232–253)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 232 | Complex numbers for control |
| 233 | The Laplace transform part 1: the idea and the table |
| 234 | The Laplace transform part 2: solving differential equations, partial fractions |
| 235 | Transfer functions |
| 236 | Block diagram algebra |
| 237 | Poles and zeros |
| 238 | Stability and the s-plane |
| 239 | The Routh–Hurwitz test |
| 240 | Steady-state error and system type |
| 241 | The root locus part 1: the idea and drawing it |
| 242 | The root locus part 2: designing with it |
| 243 | Frequency response: sine in, sine out |
| 244 | Bode plots part 1: drawing them by hand |
| 245 | Bode plots part 2: reading them |
| 246 | Gain margin and phase margin |
| 247 | The Nyquist plot (gently) |
| 248 | Lead and lag compensators |
| 249 | Designing PID with the root locus and Bode plots |
| 250 | Digital control part 1: sampling, aliasing and the z-transform |
| 251 | Digital control part 2: discrete transfer functions, turning controllers into code |
| 252 | Project: designing a DC motor controller with frequency methods |
| 253 | Project: Beam again — a controller designed with the root locus |

## Part 14 — Control Systems 3: State-Space, LQR, MPC and Nonlinear Control (Ch 254–280)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 254 | State-space models part 1: states, inputs and outputs |
| 255 | State-space models part 2: from differential equations and transfer functions |
| 256 | Solving state equations: the matrix exponential |
| 257 | Linearisation around an operating point |
| 258 | Stability in state space: eigenvalues |
| 259 | Discrete-time state space |
| 260 | Controllability |
| 261 | Observability |
| 262 | State feedback and pole placement part 1 |
| 263 | Pole placement part 2: Ackermann's formula |
| 264 | Integral action in state feedback |
| 265 | State observers (the Luenberger observer) |
| 266 | The separation principle |
| 267 | LQR part 1: the cost function, Q and R |
| 268 | LQR part 2: the Riccati equation and how to solve it |
| 269 | LQR part 3: worked example on a cart-pole |
| 270 | MPC part 1: predicting ahead (the receding horizon) |
| 271 | MPC part 2: the prediction model and the cost, MPC without limits |
| 272 | MPC part 3: limits (constraints) and quadratic programming |
| 273 | MPC part 4: nonlinear MPC (a swinging pendulum) |
| 274 | Nonlinear control part 1: the phase plane |
| 275 | Nonlinear control part 2: Lyapunov stability |
| 276 | Nonlinear control part 3: feedback linearisation |
| 277 | Sliding mode control |
| 278 | Adaptive control (first look) |
| 279 | Robust control (first look): uncertainty and the H∞ idea |
| 280 | Project: balancing a cart-pole with LQR and MPC |

## Part 15 — Mobile Robots (Ch 281–313)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 281 | Building your first wheeled robot: chassis, motors, battery, controller |
| 282 | Driving straight and turning |
| 283 | Wheel geometry: rolling without slipping |
| 284 | Holonomic and nonholonomic robots: motion constraints |
| 285 | Differential-drive kinematics part 1: forward |
| 286 | Differential-drive kinematics part 2: inverse (wheel speeds from the motion we want) |
| 287 | The unicycle model |
| 288 | Odometry from encoders |
| 289 | Odometry errors, drift and calibration |
| 290 | Simulating a differential-drive robot in Python |
| 291 | Bump-and-turn behaviour |
| 292 | Line following part 1: on-off |
| 293 | Line following part 2: PID |
| 294 | Project: a line-following race |
| 295 | Wall following |
| 296 | Obstacle avoidance with distance sensors |
| 297 | Behaviour-based robots (subsumption) |
| 298 | Go to a goal point |
| 299 | Go to a pose: position and heading |
| 300 | Pure pursuit path following |
| 301 | Car-like robots: Ackermann steering and the bicycle model |
| 302 | Kinematic and dynamic bicycle models, tyre slip |
| 303 | The Stanley controller |
| 304 | MPC path tracking for a car-like robot |
| 305 | Project: Racer, the car robot, follows a track |
| 306 | Trajectory tracking for mobile robots (nonlinear tracking controller) |
| 307 | Omni wheels and mecanum wheels |
| 308 | Project: Glide, a mecanum robot in simulation |
| 309 | Tracked and skid-steer robots |
| 310 | The balancing robot part 1: modelling the inverted pendulum |
| 311 | The balancing robot part 2: PID and LQR control |
| 312 | Project: building Balancer, the self-balancing robot |
| 313 | Project: Rover solves a maze |

## Part 16 — Frames and Transformations (Ch 314–331)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 314 | Why frames? The world, the robot, the sensor |
| 315 | Moving a point in 2D: translation |
| 316 | Turning a point in 2D: rotation |
| 317 | 2D homogeneous transforms |
| 318 | Chaining transforms |
| 319 | Inverse transforms |
| 320 | 3D coordinates and the right-hand rule |
| 321 | 3D rotation matrices about x, y and z |
| 322 | Euler angles and roll–pitch–yaw |
| 323 | Gimbal lock |
| 324 | Axis–angle and Rodrigues' formula |
| 325 | Quaternions part 1: what they are |
| 326 | Quaternions part 2: rotating and interpolating (slerp) |
| 327 | 3D homogeneous transforms |
| 328 | Angular velocity in 3D and skew-symmetric matrices |
| 329 | Choosing a rotation representation |
| 330 | Frame trees |
| 331 | Project: moving a sensor reading into the world frame |

## Part 17 — Robot Arms: Forward Kinematics (Ch 332–349)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 332 | Parts of a robot arm: links, joints, end effector |
| 333 | Joint types and degrees of freedom |
| 334 | Grübler's formula: counting degrees of freedom |
| 335 | Configuration space and workspace |
| 336 | Forward kinematics of a one-link arm |
| 337 | The two-link planar arm |
| 338 | The three-link planar arm |
| 339 | Drawing and animating arms in Python |
| 340 | DH parameters part 1: the four numbers |
| 341 | DH parameters part 2: worked examples |
| 342 | DH parameters part 3: a full six-axis arm |
| 343 | Modified DH parameters |
| 344 | Arms in 3D: SCARA, six-axis arms and the spherical wrist |
| 345 | Screw theory part 1: twists |
| 346 | Screw theory part 2: the product of exponentials |
| 347 | Comparing DH and the product of exponentials |
| 348 | Building a small servo arm |
| 349 | Project: Scribe, the arm that draws |

## Part 18 — Inverse Kinematics and Velocity (Ch 350–370)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 350 | The inverse problem: we know where, we need the angles |
| 351 | IK for a two-link arm with geometry |
| 352 | IK for a two-link arm with algebra |
| 353 | Elbow up, elbow down: many answers |
| 354 | IK for three links and a wrist |
| 355 | Kinematic decoupling: IK of a six-axis arm with a spherical wrist |
| 356 | Velocity kinematics |
| 357 | The Jacobian part 1: by differentiating |
| 358 | The Jacobian part 2: the geometric Jacobian of any arm |
| 359 | Singularities part 1: what they are |
| 360 | Singularities part 2: manipulability ellipsoids |
| 361 | Numerical IK: Newton–Raphson with the Jacobian inverse |
| 362 | Pseudoinverse and damped least squares |
| 363 | The Jacobian transpose and gradient methods |
| 364 | IK for position and orientation together |
| 365 | Redundant arms and null-space motion |
| 366 | Static forces and the Jacobian |
| 367 | Joint limits and collisions in IK |
| 368 | Mobile manipulators: an arm on a moving base |
| 369 | Project: an arm that follows the mouse |
| 370 | Project: Six, a six-axis arm in simulation |

## Part 19 — Dynamics (Ch 371–392)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 371 | Why dynamics? From motion to forces |
| 372 | Pendulum dynamics |
| 373 | Rigid bodies: mass, centre of mass and the inertia tensor |
| 374 | Newton–Euler for one link |
| 375 | Recursive Newton–Euler for a whole arm |
| 376 | Lagrangian mechanics part 1: energy |
| 377 | Lagrangian mechanics part 2: equations of motion |
| 378 | Dynamics of a two-link arm part 1: deriving the equations |
| 379 | Dynamics of a two-link arm part 2: checking them in simulation |
| 380 | The mass matrix, Coriolis terms and gravity terms, and their properties |
| 381 | Simulating arm dynamics |
| 382 | Joint friction and motor models |
| 383 | Finding the dynamic parameters of a real arm (identification) |
| 384 | Joint PD control |
| 385 | Gravity compensation |
| 386 | Computed-torque control |
| 387 | Robust and adaptive arm control (first look) |
| 388 | Force control |
| 389 | Hybrid position and force control |
| 390 | Impedance and admittance control |
| 391 | Contact and collision |
| 392 | Project: simulate and control a two-link arm |

## Part 20 — Trajectories (Ch 393–410)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 393 | Path or trajectory? |
| 394 | Straight-line interpolation in joint space |
| 395 | Cubic polynomials |
| 396 | Quintic polynomials |
| 397 | Trapezoidal velocity profiles |
| 398 | S-curve profiles |
| 399 | Via points and blending |
| 400 | Splines part 1: cubic splines |
| 401 | Splines part 2: Bézier curves and B-splines |
| 402 | Cartesian trajectories and orientation interpolation |
| 403 | Time scaling and limits |
| 404 | Minimum-jerk trajectories |
| 405 | Time-optimal trajectories (first look) |
| 406 | Trajectory optimisation part 1: the idea and the cost |
| 407 | Trajectory optimisation part 2: CHOMP and TrajOpt (first look) |
| 408 | Smooth paths for mobile robots: curvature |
| 409 | Tracking a trajectory |
| 410 | Project: a pick-and-place trajectory |

## Part 21 — Estimation and Sensor Fusion (Ch 411–428)

| Ch | Title |
|---|---|
| 411 | Why estimate? State and belief |
| 412 | Moving-average and exponential filters |
| 413 | The complementary filter for tilt |
| 414 | The Bayes filter |
| 415 | The histogram (grid) filter |
| 416 | The Kalman filter in 1D |
| 417 | The Kalman filter with matrices |
| 418 | Tuning Q and R |
| 419 | A Kalman filter for a moving robot |
| 420 | LQG: LQR together with a Kalman filter |
| 421 | The extended Kalman filter (EKF) |
| 422 | The unscented Kalman filter (UKF) |
| 423 | The particle filter part 1 |
| 424 | The particle filter part 2: resampling |
| 425 | Orientation estimation (Madgwick and Mahony filters) |
| 426 | Fusing GPS, IMU and odometry |
| 427 | Project: tracking a robot with noisy sensors |
| 428 | Project: a tilt display with a Kalman filter on a real IMU |

## Part 22 — Maps, Localization and SLAM (Ch 429–447)

| Ch | Title |
|---|---|
| 429 | What is a map? Kinds of maps |
| 430 | Occupancy grids |
| 431 | Sensor models for range sensors |
| 432 | Building a map when we know where we are |
| 433 | Ray casting |
| 434 | Markov localization |
| 435 | Monte Carlo localization |
| 436 | Landmarks and feature maps |
| 437 | Scan matching and ICP part 1 |
| 438 | ICP part 2 |
| 439 | The SLAM problem |
| 440 | EKF SLAM |
| 441 | FastSLAM |
| 442 | Graph SLAM part 1: poses and constraints |
| 443 | Graph SLAM part 2: optimisation |
| 444 | Loop closure |
| 445 | Visual SLAM (first look) |
| 446 | Project: SLAM in a simulated world |
| 447 | Project: SLAM on the real Rover with a LiDAR |

## Part 23 — Path Planning (Ch 448–476)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 448 | What is planning? |
| 449 | Graphs: nodes and edges |
| 450 | Grids as graphs |
| 451 | Breadth-first search |
| 452 | Depth-first search |
| 453 | Dijkstra's algorithm |
| 454 | A* search |
| 455 | Heuristics |
| 456 | Weighted A* and anytime search |
| 457 | Replanning when the map changes: D* Lite |
| 458 | Configuration space and obstacles |
| 459 | Visibility graphs |
| 460 | Cell decomposition |
| 461 | Potential fields |
| 462 | Sampling-based planning: PRM |
| 463 | RRT |
| 464 | RRT* |
| 465 | RRT-Connect and other RRT variants |
| 466 | Path smoothing |
| 467 | Planning for car-like robots part 1: Dubins paths |
| 468 | Planning for car-like robots part 2: Reeds–Shepp paths |
| 469 | Hybrid A* |
| 470 | State lattice planners |
| 471 | Local planning part 1: the dynamic window approach |
| 472 | Local planning part 2: elastic bands and timed elastic bands |
| 473 | Planning for robot arms |
| 474 | Task and motion planning (first look) |
| 475 | Project: a planner and a controller for a mobile robot |
| 476 | Project: parking Racer with Hybrid A* |

## Part 24 — Computer Vision (Ch 477–499)

| Ch | Title |
|---|---|
| 477 | How cameras work: light, lens, sensor |
| 478 | Images as arrays of numbers |
| 479 | Colour spaces |
| 480 | Thresholding and colour detection |
| 481 | Convolution and filters (blur) |
| 482 | Finding edges |
| 483 | Morphology: growing and shrinking shapes |
| 484 | Contours and blobs |
| 485 | The Hough transform |
| 486 | Features part 1: corners |
| 487 | Features part 2: descriptors and matching |
| 488 | The pinhole camera model |
| 489 | Camera calibration |
| 490 | Lens distortion |
| 491 | Marker tracking (ArUco and AprilTag) |
| 492 | Finding pose from a camera (PnP) |
| 493 | Stereo vision and depth |
| 494 | Depth cameras and point clouds part 1 |
| 495 | Point clouds part 2: filtering, normals and finding planes (RANSAC) |
| 496 | Point clouds part 3: grouping points into objects |
| 497 | Optical flow and visual odometry |
| 498 | Project: follow a coloured ball |
| 499 | Project: a colour-sorting arm with a camera |

## Part 25 — Machine Learning for Robots (Ch 500–521)

| Ch | Title |
|---|---|
| 500 | What is machine learning? |
| 501 | Data, features and labels |
| 502 | Linear regression from scratch |
| 503 | Logistic regression and classification |
| 504 | Overfitting, training data and test data |
| 505 | Neurons and neural networks |
| 506 | The forward pass |
| 507 | Backpropagation by hand |
| 508 | A neural network from scratch in NumPy |
| 509 | Training tricks |
| 510 | Convolutional neural networks |
| 511 | Using PyTorch (first look) |
| 512 | Object detection for robots |
| 513 | Reinforcement learning: agent, action, reward |
| 514 | Markov decision processes |
| 515 | Value iteration |
| 516 | Q-learning |
| 517 | Deep reinforcement learning and policy gradients |
| 518 | Imitation learning |
| 519 | Sim-to-real and large robot models (first look) |
| 520 | Project: teach a robot to balance a pole with reinforcement learning |
| 521 | Project: a line follower that learns from your driving |

## Part 26 — Real-Time Systems and Communication Protocols (Ch 522–548)

Part 6 gave a first look at UART, I2C and SPI. This part goes deep: real-time timing, RTOS, every bus bit by bit, and CAN.

| Ch | Title |
|---|---|
| 522 | What is a real-time system? Hard, firm and soft deadlines |
| 523 | Measuring time: latency, jitter and deadlines |
| 524 | The super loop and simple schedulers |
| 525 | Interrupts in depth: priorities, ISR rules, shared data |
| 526 | What is an RTOS? Tasks, the scheduler, context switches |
| 527 | FreeRTOS part 1: tasks and delays (on an ESP32) |
| 528 | FreeRTOS part 2: queues, semaphores and mutexes |
| 529 | Scheduling and priority inversion |
| 530 | Real-time Linux: PREEMPT_RT and measuring latency |
| 531 | Digital communication basics: bits, baud rate, clocks, serial and parallel |
| 532 | UART in depth: frames, baud errors, RS-232 and RS-485 |
| 533 | Designing a packet: header, length, checksum and CRC |
| 534 | I2C in depth: addresses, ACK, pull-ups, clock stretching |
| 535 | I2C in practice: reading an IMU's registers by hand |
| 536 | SPI in depth: the four modes, chip select, speed |
| 537 | SPI in practice: reading an encoder and an ADC by hand |
| 538 | CAN bus part 1: two wires, differential signals, frames |
| 539 | CAN bus part 2: IDs, arbitration and filters |
| 540 | CAN bus part 3: bit timing and error handling |
| 541 | CAN bus part 4: CAN on Arduino/ESP32 and SocketCAN on Linux |
| 542 | CAN FD and CANopen: controlling smart motors |
| 543 | Other robot buses: Modbus, EtherCAT, USB, Dynamixel |
| 544 | Wireless: Wi-Fi, Bluetooth and radio |
| 545 | Networks for robots: IP, TCP, UDP and sockets in Python |
| 546 | Sending data: binary packing, JSON and MQTT |
| 547 | Debugging buses: logic analysers and oscilloscopes |
| 548 | Project: a two-motor robot base controlled over CAN |

## Part 27 — Linux and ROS 2 (Ch 549–579)

ROS 2 is the standard software framework for robots. We learn it from the first node to real-time ROS 2.

| Ch | Title |
|---|---|
| 549 | Linux terminal basics |
| 550 | Files, permissions and processes |
| 551 | Shell scripts and environment variables |
| 552 | Git for robot projects |
| 553 | Docker for robotics |
| 554 | How robot software is organised |
| 555 | What is ROS 2? ROS 1 and ROS 2 |
| 556 | Installing ROS 2 (Ubuntu, WSL, Docker) |
| 557 | Workspaces, packages and `colcon` |
| 558 | Nodes in Python (`rclpy`) |
| 559 | Topics: publish and subscribe |
| 560 | Messages and custom interfaces |
| 561 | Services |
| 562 | Actions |
| 563 | Parameters |
| 564 | Launch files |
| 565 | Nodes in C++ (`rclcpp`) |
| 566 | DDS and Quality of Service (QoS) |
| 567 | Executors, callbacks and timers |
| 568 | Recording and replaying data: `ros2 bag` |
| 569 | Debugging tools: logging, `rqt`, `ros2 doctor` |
| 570 | tf2: frames in ROS |
| 571 | URDF and Xacro: describing a robot in a file |
| 572 | RViz: seeing what the robot sees |
| 573 | Managed (lifecycle) nodes |
| 574 | Components and zero-copy messages |
| 575 | Many machines: domain IDs, networking and security |
| 576 | Testing ROS 2 code |
| 577 | Real-time ROS 2 |
| 578 | micro-ROS: ROS 2 on a microcontroller |
| 579 | Project: ROS 2 nodes for the real Rover |

## Part 28 — Robot Simulators: Gazebo, Webots, MuJoCo, Isaac Sim (Ch 580–601)

Four simulators, each from installing to a full project. Isaac Sim needs an NVIDIA RTX graphics card; the other three run on most computers.

| Ch | Title |
|---|---|
| 580 | What is a robot simulator? Why we simulate |
| 581 | Inside a physics engine: time steps, collisions and contacts |
| 582 | Robot model files: URDF, SDF, MJCF and USD |
| 583 | Gazebo part 1: installing, worlds and models |
| 584 | Gazebo part 2: sensors and plugins |
| 585 | Gazebo part 3: connecting to ROS 2 (`ros_gz`) |
| 586 | Gazebo project: a mobile robot with a LiDAR |
| 587 | Webots part 1: installing, worlds and a first robot |
| 588 | Webots part 2: Python controllers and sensors |
| 589 | Webots part 3: connecting to ROS 2 |
| 590 | Webots project: a line follower and a robot arm |
| 591 | MuJoCo part 1: installing and MJCF models |
| 592 | MuJoCo part 2: the Python simulation loop, actuators and sensors |
| 593 | MuJoCo part 3: contacts, controlling an arm, balancing |
| 594 | MuJoCo part 4: teaching Walker to walk with reinforcement learning |
| 595 | Isaac Sim part 1: what it needs, installing, USD scenes |
| 596 | Isaac Sim part 2: importing robots, sensors and Python scripts |
| 597 | Isaac Sim part 3: the ROS 2 bridge and synthetic data |
| 598 | Isaac Lab: training robots in thousands of worlds at once |
| 599 | Choosing a simulator: a comparison |
| 600 | The sim-to-real gap and domain randomisation |
| 601 | Project: one robot in four simulators |

## Part 29 — ROS 2 in Practice (Ch 602–613)

Now ROS 2 drives complete robots, first in Gazebo, then on real hardware.

| Ch | Title |
|---|---|
| 602 | Sensor drivers in ROS 2: LiDAR, camera, IMU |
| 603 | `ros2_control` part 1: controllers and hardware interfaces |
| 604 | `ros2_control` part 2: writing our own hardware interface (CAN motors) |
| 605 | `robot_localization`: fusing sensors in ROS 2 |
| 606 | SLAM Toolbox: making maps in ROS 2 |
| 607 | Nav2 part 1: setting up navigation |
| 608 | Nav2 part 2: costmaps, planners and controllers |
| 609 | Nav2 part 3: behaviour trees |
| 610 | MoveIt 2 part 1: planning arm motion |
| 611 | MoveIt 2 part 2: pick and place |
| 612 | Project: HomeBot, a ROS 2 robot that drives around a house |
| 613 | Project: ROS 2 arm pick-and-place with MoveIt 2 |

## Part 30 — Drones: From Zero to Autonomous Flight (Ch 614–666)

Full tutorial from zero, written with the lecture and figure rules (`MASTER_PLAN.md` §6) and a hands-on lab in every chapter. You build **Hover** (`ROBOTS.md`).

| Ch | Title |
|---|---|
| 614 | What is a drone? Multirotors, fixed-wing, VTOL and helicopters |
| 615 | Drone safety and the law: where and how you may fly |
| 616 | Parts of a quadcopter: frame, motors, propellers, ESCs, flight controller, battery, radio |
| 617 | How a propeller makes lift: air, pressure and thrust |
| 618 | Propeller maths: thrust, RPM, diameter and pitch |
| 619 | Brushless motors for drones: KV rating and thrust tables |
| 620 | ESCs and motor signals: PWM, OneShot and DShot |
| 621 | LiPo batteries for drones: cells, C rating, flight time, safe charging |
| 622 | Weight and thrust-to-weight ratio: designing a drone on paper |
| 623 | How a quadcopter moves: throttle, roll, pitch and yaw |
| 624 | Motor mixing: from four commands to four motor speeds |
| 625 | Frames for flying: body frame, NED and ENU |
| 626 | Attitude: roll–pitch–yaw and quaternions on a drone |
| 627 | Quadcopter dynamics part 1: forces and moments |
| 628 | Quadcopter dynamics part 2: the full six-degree-of-freedom equations |
| 629 | Simulating a quadcopter in Python |
| 630 | Drone sensors: IMU, barometer, magnetometer, GPS, optical flow, rangefinder |
| 631 | Sensor calibration and vibration on a drone |
| 632 | Attitude estimation part 1: complementary and Mahony filters |
| 633 | Attitude estimation part 2: the EKF used in real flight controllers |
| 634 | The control cascade: rate, attitude, velocity and position loops |
| 635 | Rate control with PID |
| 636 | Attitude control |
| 637 | Altitude hold |
| 638 | Velocity and position control |
| 639 | Tuning a drone: step responses, flight logs and notch filters |
| 640 | Radio control: transmitters, receivers, SBUS and CRSF, failsafe |
| 641 | Our own flight controller part 1: reading the IMU and mixing (ESP32) |
| 642 | Our own flight controller part 2: rate PID and first hover on a test stand |
| 643 | Our own flight controller part 3: angle mode and safe arming |
| 644 | Flight stacks: PX4, ArduPilot and Betaflight |
| 645 | Building a drone part 1: frame, motors, ESCs, wiring and soldering |
| 646 | Building a drone part 2: flight controller, receiver, setup and first flight |
| 647 | PX4 in simulation (SITL with Gazebo) |
| 648 | MAVLink: how computers talk to drones |
| 649 | Flight modes: manual, stabilise, altitude hold, position hold, mission, return home |
| 650 | GPS missions and waypoints |
| 651 | Programming drones from Python: MAVSDK and offboard control |
| 652 | Drones with ROS 2: the PX4–ROS 2 bridge |
| 653 | Flying without GPS: optical flow and visual-inertial odometry |
| 654 | Trajectories for drones: minimum-snap paths |
| 655 | Differential flatness and geometric control |
| 656 | MPC for drones |
| 657 | 3D maps for drones: octomaps |
| 658 | Path planning and obstacle avoidance in 3D |
| 659 | Precision landing on a marker with a camera |
| 660 | Fixed-wing aircraft: lift, drag and control surfaces |
| 661 | VTOL and hybrid drones |
| 662 | Many drones together: formation and swarm flight |
| 663 | Fast and agile flight, learned flight controllers (first look) |
| 664 | Failsafes, fault detection and reliability |
| 665 | Project: Hover part 1 — a full autonomous mission in simulation |
| 666 | Project: Hover part 2 — build the real drone and fly a mission |

## Part 31 — Legged Robots and Walking (Ch 667–690)

Full tutorial from zero, written with the lecture and figure rules (`MASTER_PLAN.md` §6) and a hands-on lab in every chapter. You build **Quad** and train **Walker**.

| Ch | Title |
|---|---|
| 667 | Why legs? Kinds of legged robots |
| 668 | Leg design and actuators for legs: servos and quasi-direct-drive motors |
| 669 | Leg forward kinematics: a three-joint leg |
| 670 | Leg inverse kinematics |
| 671 | Support polygon and static stability |
| 672 | Gaits part 1: slow walking gaits |
| 673 | Gaits part 2: trot, pace, bound and gallop |
| 674 | Foot trajectories: swing phase and stance phase |
| 675 | Body kinematics: moving the body with the feet on the ground |
| 676 | Static walking for a four-legged robot |
| 677 | Contact forces and friction cones |
| 678 | Dynamic legs: the spring-loaded inverted pendulum (SLIP) |
| 679 | The Raibert hopping controller |
| 680 | The linear inverted pendulum model (LIPM) |
| 681 | The capture point |
| 682 | Quadruped dynamics: the single rigid body model |
| 683 | Convex MPC for four-legged walking |
| 684 | Whole-body control for legged robots (first look) |
| 685 | State estimation for legged robots: leg odometry and the IMU |
| 686 | Walking on stairs, slopes and rough ground |
| 687 | Learning to walk with reinforcement learning (MuJoCo and Isaac Lab) |
| 688 | Project: Quad part 1 — building a 12-servo four-legged robot |
| 689 | Project: Quad part 2 — trot gait, turning and balance |
| 690 | Project: Quad part 3 — a learned walking policy, from simulation to the real robot |

## Part 32 — Humanoid Robots: From Zero to Walking, Balancing and Working (Ch 691–738)

Full tutorial from zero, written with the lecture and figure rules (`MASTER_PLAN.md` §6) and a hands-on lab in every chapter. You build **Buddy** (a real small humanoid) and **Hero** (a full-size humanoid in simulation).

| Ch | Title |
|---|---|
| 691 | What is a humanoid robot? History and today's humanoids |
| 692 | The human body as a guide: joints, degrees of freedom, how people walk |
| 693 | Designing a humanoid: body layout and degrees of freedom |
| 694 | Actuators for humanoids: servos, harmonic drives, series elastic actuators |
| 695 | Sensors in a humanoid: IMU, joint encoders, foot force sensors, cameras |
| 696 | Electronics and power in a humanoid: battery, power, CAN and EtherCAT |
| 697 | The kinematic tree of a humanoid and its URDF |
| 698 | Forward kinematics of the whole body |
| 699 | Inverse kinematics of a six-joint leg |
| 700 | Inverse kinematics of a seven-joint arm (redundancy) |
| 701 | The centre of mass of the whole robot |
| 702 | Balance part 1: standing still and the support polygon |
| 703 | Balance part 2: the ZMP in detail |
| 704 | Balance part 3: ankle, hip and stepping strategies |
| 705 | Walking part 1: the phases of a human step |
| 706 | Walking part 2: walking patterns from the LIPM |
| 707 | Walking part 3: ZMP preview control |
| 708 | Walking part 4: footstep planning |
| 709 | Walking part 5: capture point and DCM walking |
| 710 | Walking part 6: turning, slopes and stairs |
| 711 | Floating-base dynamics of a humanoid |
| 712 | Centroidal dynamics |
| 713 | Whole-body control part 1: tasks and priorities |
| 714 | Whole-body control part 2: whole-body control with quadratic programming |
| 715 | Contacts and torque control |
| 716 | Model predictive control for humanoids |
| 717 | State estimation for humanoids |
| 718 | Falling: detecting a fall, falling safely and getting up |
| 719 | Upper body: reaching and two-arm manipulation |
| 720 | Robot hands: dexterous hands and grasping |
| 721 | Loco-manipulation: walking while carrying things |
| 722 | Humanoid perception: head cameras, depth, finding people |
| 723 | Reinforcement learning for humanoid walking part 1: setting up in Isaac Lab and MuJoCo |
| 724 | Reinforcement learning for humanoid walking part 2: rewards, randomisation and sim-to-real |
| 725 | Learning from human motion: motion capture and retargeting |
| 726 | Teleoperation: controlling a humanoid with VR |
| 727 | Vision-language-action models for humanoids (first look) |
| 728 | Talking with people: speech, faces and gestures |
| 729 | Humanoid safety |
| 730 | Humanoid software architecture with ROS 2 |
| 731 | Project: Hero part 1 — modelling a full-size humanoid (URDF and MJCF) |
| 732 | Project: Hero part 2 — standing and balancing |
| 733 | Project: Hero part 3 — walking with ZMP preview control |
| 734 | Project: Hero part 4 — walking with reinforcement learning |
| 735 | Project: Buddy part 1 — mechanics and wiring of an 18-servo humanoid |
| 736 | Project: Buddy part 2 — poses and balance with an IMU |
| 737 | Project: Buddy part 3 — a walking gait |
| 738 | Project: Buddy part 4 — arm tasks and getting up after a fall |

## Part 33 — Advanced Robots and Final Projects (Ch 739–749)

| Ch | Title |
|---|---|
| 739 | Grasping and manipulation |
| 740 | Soft robots |
| 741 | Many robots together: multi-robot systems and swarms |
| 742 | Project: a swarm of simulated robots |
| 743 | Humans and robots working together |
| 744 | Robot safety standards |
| 745 | Ethics: robots in society |
| 746 | Testing and debugging robots |
| 747 | Final project 1: Courier, an autonomous delivery robot |
| 748 | Final project 2: Sorter, a pick-and-place arm with vision |
| 749 | Final project 3: Fetch, a mobile manipulator that brings objects |

## Appendices

| | Title |
|---|---|
| A | All maths formulas in one place |
| B | Glossary (every 📖 new word, A–Z) |
| C | Parts list and where to buy |
| D | Python cheat sheet |
| E | Arduino C++ cheat sheet |
| G | ROS 2 command cheat sheet |
| F | Index of all projects |
