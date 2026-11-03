# Robotics From Scratch — Syllabus

A very beginner-friendly robotics course. It goes from "what is a robot?" to SLAM, robot arms, machine learning and ROS 2.
It has **30 parts and 607 chapters**, about **13,000 pages** in total (see `MASTER_PLAN.md` for the page budget).

- Rules for writing every chapter: `MASTER_PLAN.md`
- Which chapter is next: `PROGRESS.md`
- The original request: `t.md`

**Order:** every chapter only uses ideas from earlier chapters.
Programming comes first (Part 2). The maths comes just before the robot topic that needs it.

**Languages:** **Python** is the main language (taught from zero in Part 2).
**C++ for Arduino** is taught in Part 6, for small boards.
Real-time systems and the buses robots use (UART, I2C, SPI, CAN) are covered in depth in Part 26.
**ROS 2** (Python, then C++) is taught in Parts 27 and 29. The simulators Gazebo, Webots, MuJoCo and Isaac Sim are taught in Part 28.

**Core robotics and control (Parts 12–20 and 23)** are written as detailed lectures with many figures: at least 15 pictures per chapter.

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
| 36 | Project: a text robot simulator on a grid |

## Part 3 — The Maths You Need, From School Level (Ch 37–54)

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

## Part 4 — Physics for Robots (Ch 55–70)

| Ch | Title |
|---|---|
| 55 | Position, distance and displacement |
| 56 | Speed and velocity |
| 57 | Acceleration |
| 58 | Equations of motion with constant acceleration |
| 59 | Motion in two directions (first look at vectors) |
| 60 | Forces and Newton's three laws |
| 61 | Mass, weight and gravity |
| 62 | Friction and grip (traction) |
| 63 | Turning: angle, angular speed, angular acceleration |
| 64 | Torque and levers |
| 65 | Moment of inertia: how hard it is to spin something |
| 66 | Work, energy and power |
| 67 | Gears, pulleys and belts: trading speed for torque |
| 68 | Wheels and rolling |
| 69 | Centre of mass and balance: why robots fall over |
| 70 | Simulating physics in Python: small time steps (Euler's method) |

## Part 5 — Electricity and Electronics (Ch 71–90)

| Ch | Title |
|---|---|
| 71 | What is electricity? Charge and electrons |
| 72 | Voltage, current and resistance |
| 73 | Ohm's law with many worked examples |
| 74 | Power in circuits (P = V × I) and heat |
| 75 | Series and parallel circuits |
| 76 | Kirchhoff's laws |
| 77 | Voltage dividers |
| 78 | Breadboards, wires and reading circuit diagrams |
| 79 | The multimeter: measuring safely |
| 80 | LEDs and resistors |
| 81 | Switches and buttons, pull-up and pull-down resistors |
| 82 | Capacitors |
| 83 | Inductors and coils (why motors make voltage spikes) |
| 84 | Diodes and flyback protection |
| 85 | Transistors as switches (BJT) |
| 86 | MOSFETs |
| 87 | Batteries: types, capacity, C rating, safety |
| 88 | Voltage regulators and power supplies |
| 89 | Digital and analog signals, logic levels |
| 90 | Soldering and building a small circuit |

## Part 6 — Microcontrollers and Arduino (Ch 91–110)

| Ch | Title |
|---|---|
| 91 | What is a microcontroller? |
| 92 | The Arduino board, the Arduino IDE and the Wokwi simulator |
| 93 | C++ for Arduino part 1: `setup`, `loop`, variables, types |
| 94 | C++ for Arduino part 2: `if`, loops, functions, arrays |
| 95 | Blink: digital output |
| 96 | Reading buttons: digital input and debouncing |
| 97 | The serial monitor: talking to the computer |
| 98 | Analog input: the ADC |
| 99 | PWM: "fake" analog output |
| 100 | Timing without `delay`: `millis()` |
| 101 | State machines |
| 102 | Interrupts |
| 103 | Hardware timers |
| 104 | Communication part 1: UART |
| 105 | Communication part 2: I2C |
| 106 | Communication part 3: SPI |
| 107 | Libraries and how they work inside |
| 108 | Arduino talking to Python (`pyserial`) |
| 109 | Raspberry Pi: a small computer, GPIO with Python |
| 110 | Project: a traffic light and a reaction-time game |

## Part 7 — Sensors (Ch 111–132)

| Ch | Title |
|---|---|
| 111 | What is a sensor? Range, resolution, accuracy, noise |
| 112 | Buttons, limit switches and bumpers |
| 113 | Potentiometers: measuring an angle |
| 114 | Light sensors (LDR, photodiode) |
| 115 | Infrared sensors and line sensors |
| 116 | The ultrasonic distance sensor |
| 117 | Time-of-flight laser distance sensors |
| 118 | Temperature and humidity |
| 119 | Encoders part 1: how they count |
| 120 | Encoders part 2: quadrature and measuring speed |
| 121 | Accelerometers |
| 122 | Gyroscopes |
| 123 | Magnetometers and compasses |
| 124 | IMUs: putting the three together |
| 125 | Force and pressure sensors, load cells |
| 126 | Measuring current and voltage |
| 127 | GPS |
| 128 | Cameras as sensors (first look) |
| 129 | LiDAR |
| 130 | Calibration: making sensors honest |
| 131 | Noise and simple filters: average and median |
| 132 | Project: an obstacle-detecting distance meter |

## Part 8 — Actuators and Motors (Ch 133–150)

| Ch | Title |
|---|---|
| 133 | What is an actuator? |
| 134 | How a DC motor works: magnets and coils |
| 135 | Motor equations: back EMF, torque constant, speed–torque curve |
| 136 | Driving a motor both ways: the H-bridge |
| 137 | Speed control with PWM |
| 138 | Motor driver boards (L298N, TB6612) |
| 139 | Gearmotors and choosing a gearbox |
| 140 | Hobby servos |
| 141 | Stepper motors part 1: how they step |
| 142 | Stepper motors part 2: drivers and microstepping |
| 143 | Brushless motors and ESCs |
| 144 | Linear actuators and solenoids |
| 145 | Pneumatics and hydraulics (first look) |
| 146 | Grippers and end effectors |
| 147 | Choosing a motor: worked sizing examples |
| 148 | The power budget of a robot |
| 149 | A motor with encoder feedback (a preview of control) |
| 150 | Project: a pan-tilt camera head with two servos |

## Part 9 — Linear Algebra for Robots (Ch 151–170)

| Ch | Title |
|---|---|
| 151 | Vectors: arrows made of numbers |
| 152 | Adding, subtracting and scaling vectors |
| 153 | Length and unit vectors |
| 154 | The dot product: angles and projections |
| 155 | The cross product (3D) and torque again |
| 156 | Matrices: tables of numbers |
| 157 | Matrix times vector |
| 158 | Matrix times matrix |
| 159 | The identity matrix and the transpose |
| 160 | The determinant |
| 161 | The inverse of a matrix |
| 162 | Solving systems of equations (Gaussian elimination) |
| 163 | Linear transformations: matrices that move points |
| 164 | Rotation matrices in 2D |
| 165 | Orthogonal matrices |
| 166 | Rank and null space (gently) |
| 167 | Eigenvalues and eigenvectors |
| 168 | Least squares: fitting a line to sensor data |
| 169 | The SVD (gently) |
| 170 | Building a tiny linear algebra library, then using NumPy |

## Part 10 — Calculus for Robots (Ch 171–186)

| Ch | Title |
|---|---|
| 171 | Change and rates of change |
| 172 | Limits (gently) |
| 173 | Derivatives: the slope at one point |
| 174 | Derivative rules |
| 175 | Derivatives of sin, cos and exp |
| 176 | The chain rule |
| 177 | Numerical derivatives in Python: speed from position |
| 178 | Integrals: area and adding up |
| 179 | Numerical integration: position from speed |
| 180 | Differential equations: what they are |
| 181 | Solving them with a computer: Euler and Runge–Kutta |
| 182 | Partial derivatives |
| 183 | The gradient and gradient descent |
| 184 | The Jacobian matrix |
| 185 | Taylor series and linearisation |
| 186 | Optimisation basics: minimums and constraints |

## Part 11 — Probability and Statistics (Ch 187–200)

| Ch | Title |
|---|---|
| 187 | Chance and probability |
| 188 | The rules of probability |
| 189 | Conditional probability |
| 190 | Bayes' rule (a robot looking for a door) |
| 191 | Random variables |
| 192 | Mean, variance and standard deviation |
| 193 | The normal (Gaussian) distribution |
| 194 | Combining Gaussians |
| 195 | Covariance and correlation |
| 196 | Multivariate Gaussians and uncertainty ellipses |
| 197 | Sampling and Monte Carlo |
| 198 | Histograms and probability on a grid |
| 199 | Noise models for sensors and motion |
| 200 | Project: a simulated noisy sensor and its statistics |

## Part 12 — Control Systems 1: Feedback and PID (Ch 201–225)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 201 | What is control? Open loop and closed loop |
| 202 | Block diagrams: drawing a control system |
| 203 | On-off (bang-bang) control and hysteresis |
| 204 | The setpoint, the error and the feedback signal |
| 205 | P control part 1: the idea |
| 206 | P control part 2: steady-state error |
| 207 | I control part 1: removing steady-state error |
| 208 | I control part 2: overshoot and integral windup |
| 209 | D control part 1: damping |
| 210 | D control part 2: noise and derivative filtering |
| 211 | PID together: how the three terms work as a team |
| 212 | Reading response graphs: rise time, overshoot, settling time, steady-state error |
| 213 | Tuning PID part 1: by hand, step by step |
| 214 | Tuning PID part 2: Ziegler–Nichols and Cohen–Coon |
| 215 | PID in code part 1: time steps and sample rate |
| 216 | PID in code part 2: anti-windup, derivative kick, output limits, bumpless transfer |
| 217 | Modelling systems part 1: mass–spring–damper |
| 218 | Modelling systems part 2: the DC motor (electrical and mechanical) |
| 219 | Modelling systems part 3: the pendulum, heat and liquid tanks |
| 220 | First-order systems and the time constant |
| 221 | Second-order systems: natural frequency and damping ratio |
| 222 | Feedforward control |
| 223 | Cascade control: current, speed and position loops |
| 224 | Project: motor speed control with PID |
| 225 | Project: motor position control with cascade PID |

## Part 13 — Control Systems 2: Classical Analysis and Design (Ch 226–246)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 226 | Complex numbers for control |
| 227 | The Laplace transform part 1: the idea and the table |
| 228 | The Laplace transform part 2: solving differential equations, partial fractions |
| 229 | Transfer functions |
| 230 | Block diagram algebra |
| 231 | Poles and zeros |
| 232 | Stability and the s-plane |
| 233 | The Routh–Hurwitz test |
| 234 | Steady-state error and system type |
| 235 | The root locus part 1: the idea and drawing it |
| 236 | The root locus part 2: designing with it |
| 237 | Frequency response: sine in, sine out |
| 238 | Bode plots part 1: drawing them by hand |
| 239 | Bode plots part 2: reading them |
| 240 | Gain margin and phase margin |
| 241 | The Nyquist plot (gently) |
| 242 | Lead and lag compensators |
| 243 | Designing PID with the root locus and Bode plots |
| 244 | Digital control part 1: sampling, aliasing and the z-transform |
| 245 | Digital control part 2: discrete transfer functions, turning controllers into code |
| 246 | Project: designing a DC motor controller with frequency methods |

## Part 14 — Control Systems 3: State-Space, LQR, MPC and Nonlinear Control (Ch 247–273)

Control part: every chapter has many figures — block diagrams, response graphs, plots (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 247 | State-space models part 1: states, inputs and outputs |
| 248 | State-space models part 2: from differential equations and transfer functions |
| 249 | Solving state equations: the matrix exponential |
| 250 | Linearisation around an operating point |
| 251 | Stability in state space: eigenvalues |
| 252 | Discrete-time state space |
| 253 | Controllability |
| 254 | Observability |
| 255 | State feedback and pole placement part 1 |
| 256 | Pole placement part 2: Ackermann's formula |
| 257 | Integral action in state feedback |
| 258 | State observers (the Luenberger observer) |
| 259 | The separation principle |
| 260 | LQR part 1: the cost function, Q and R |
| 261 | LQR part 2: the Riccati equation and how to solve it |
| 262 | LQR part 3: worked example on a cart-pole |
| 263 | MPC part 1: predicting ahead (the receding horizon) |
| 264 | MPC part 2: the prediction model and the cost, MPC without limits |
| 265 | MPC part 3: limits (constraints) and quadratic programming |
| 266 | MPC part 4: nonlinear MPC (a swinging pendulum) |
| 267 | Nonlinear control part 1: the phase plane |
| 268 | Nonlinear control part 2: Lyapunov stability |
| 269 | Nonlinear control part 3: feedback linearisation |
| 270 | Sliding mode control |
| 271 | Adaptive control (first look) |
| 272 | Robust control (first look): uncertainty and the H∞ idea |
| 273 | Project: balancing a cart-pole with LQR and MPC |

## Part 15 — Mobile Robots (Ch 274–302)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 274 | Building your first wheeled robot: chassis, motors, battery, controller |
| 275 | Driving straight and turning |
| 276 | Wheel geometry: rolling without slipping |
| 277 | Holonomic and nonholonomic robots: motion constraints |
| 278 | Differential-drive kinematics part 1: forward |
| 279 | Differential-drive kinematics part 2: inverse (wheel speeds from the motion we want) |
| 280 | The unicycle model |
| 281 | Odometry from encoders |
| 282 | Odometry errors, drift and calibration |
| 283 | Simulating a differential-drive robot in Python |
| 284 | Bump-and-turn behaviour |
| 285 | Line following part 1: on-off |
| 286 | Line following part 2: PID |
| 287 | Wall following |
| 288 | Obstacle avoidance with distance sensors |
| 289 | Behaviour-based robots (subsumption) |
| 290 | Go to a goal point |
| 291 | Go to a pose: position and heading |
| 292 | Pure pursuit path following |
| 293 | Car-like robots: Ackermann steering and the bicycle model |
| 294 | Kinematic and dynamic bicycle models, tyre slip |
| 295 | The Stanley controller |
| 296 | MPC path tracking for a car-like robot |
| 297 | Trajectory tracking for mobile robots (nonlinear tracking controller) |
| 298 | Omni wheels and mecanum wheels |
| 299 | Tracked and skid-steer robots |
| 300 | The balancing robot part 1: modelling the inverted pendulum |
| 301 | The balancing robot part 2: PID and LQR control |
| 302 | Project: a maze-solving robot |

## Part 16 — Frames and Transformations (Ch 303–320)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 303 | Why frames? The world, the robot, the sensor |
| 304 | Moving a point in 2D: translation |
| 305 | Turning a point in 2D: rotation |
| 306 | 2D homogeneous transforms |
| 307 | Chaining transforms |
| 308 | Inverse transforms |
| 309 | 3D coordinates and the right-hand rule |
| 310 | 3D rotation matrices about x, y and z |
| 311 | Euler angles and roll–pitch–yaw |
| 312 | Gimbal lock |
| 313 | Axis–angle and Rodrigues' formula |
| 314 | Quaternions part 1: what they are |
| 315 | Quaternions part 2: rotating and interpolating (slerp) |
| 316 | 3D homogeneous transforms |
| 317 | Angular velocity in 3D and skew-symmetric matrices |
| 318 | Choosing a rotation representation |
| 319 | Frame trees |
| 320 | Project: moving a sensor reading into the world frame |

## Part 17 — Robot Arms: Forward Kinematics (Ch 321–338)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 321 | Parts of a robot arm: links, joints, end effector |
| 322 | Joint types and degrees of freedom |
| 323 | Grübler's formula: counting degrees of freedom |
| 324 | Configuration space and workspace |
| 325 | Forward kinematics of a one-link arm |
| 326 | The two-link planar arm |
| 327 | The three-link planar arm |
| 328 | Drawing and animating arms in Python |
| 329 | DH parameters part 1: the four numbers |
| 330 | DH parameters part 2: worked examples |
| 331 | DH parameters part 3: a full six-axis arm |
| 332 | Modified DH parameters |
| 333 | Arms in 3D: SCARA, six-axis arms and the spherical wrist |
| 334 | Screw theory part 1: twists |
| 335 | Screw theory part 2: the product of exponentials |
| 336 | Comparing DH and the product of exponentials |
| 337 | Building a small servo arm |
| 338 | Project: an arm that draws |

## Part 18 — Inverse Kinematics and Velocity (Ch 339–358)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 339 | The inverse problem: we know where, we need the angles |
| 340 | IK for a two-link arm with geometry |
| 341 | IK for a two-link arm with algebra |
| 342 | Elbow up, elbow down: many answers |
| 343 | IK for three links and a wrist |
| 344 | Kinematic decoupling: IK of a six-axis arm with a spherical wrist |
| 345 | Velocity kinematics |
| 346 | The Jacobian part 1: by differentiating |
| 347 | The Jacobian part 2: the geometric Jacobian of any arm |
| 348 | Singularities part 1: what they are |
| 349 | Singularities part 2: manipulability ellipsoids |
| 350 | Numerical IK: Newton–Raphson with the Jacobian inverse |
| 351 | Pseudoinverse and damped least squares |
| 352 | The Jacobian transpose and gradient methods |
| 353 | IK for position and orientation together |
| 354 | Redundant arms and null-space motion |
| 355 | Static forces and the Jacobian |
| 356 | Joint limits and collisions in IK |
| 357 | Mobile manipulators: an arm on a moving base |
| 358 | Project: an arm that follows the mouse |

## Part 19 — Dynamics (Ch 359–380)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 359 | Why dynamics? From motion to forces |
| 360 | Pendulum dynamics |
| 361 | Rigid bodies: mass, centre of mass and the inertia tensor |
| 362 | Newton–Euler for one link |
| 363 | Recursive Newton–Euler for a whole arm |
| 364 | Lagrangian mechanics part 1: energy |
| 365 | Lagrangian mechanics part 2: equations of motion |
| 366 | Dynamics of a two-link arm part 1: deriving the equations |
| 367 | Dynamics of a two-link arm part 2: checking them in simulation |
| 368 | The mass matrix, Coriolis terms and gravity terms, and their properties |
| 369 | Simulating arm dynamics |
| 370 | Joint friction and motor models |
| 371 | Finding the dynamic parameters of a real arm (identification) |
| 372 | Joint PD control |
| 373 | Gravity compensation |
| 374 | Computed-torque control |
| 375 | Robust and adaptive arm control (first look) |
| 376 | Force control |
| 377 | Hybrid position and force control |
| 378 | Impedance and admittance control |
| 379 | Contact and collision |
| 380 | Project: simulate and control a two-link arm |

## Part 20 — Trajectories (Ch 381–398)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 381 | Path or trajectory? |
| 382 | Straight-line interpolation in joint space |
| 383 | Cubic polynomials |
| 384 | Quintic polynomials |
| 385 | Trapezoidal velocity profiles |
| 386 | S-curve profiles |
| 387 | Via points and blending |
| 388 | Splines part 1: cubic splines |
| 389 | Splines part 2: Bézier curves and B-splines |
| 390 | Cartesian trajectories and orientation interpolation |
| 391 | Time scaling and limits |
| 392 | Minimum-jerk trajectories |
| 393 | Time-optimal trajectories (first look) |
| 394 | Trajectory optimisation part 1: the idea and the cost |
| 395 | Trajectory optimisation part 2: CHOMP and TrajOpt (first look) |
| 396 | Smooth paths for mobile robots: curvature |
| 397 | Tracking a trajectory |
| 398 | Project: a pick-and-place trajectory |

## Part 21 — Estimation and Sensor Fusion (Ch 399–415)

| Ch | Title |
|---|---|
| 399 | Why estimate? State and belief |
| 400 | Moving-average and exponential filters |
| 401 | The complementary filter for tilt |
| 402 | The Bayes filter |
| 403 | The histogram (grid) filter |
| 404 | The Kalman filter in 1D |
| 405 | The Kalman filter with matrices |
| 406 | Tuning Q and R |
| 407 | A Kalman filter for a moving robot |
| 408 | LQG: LQR together with a Kalman filter |
| 409 | The extended Kalman filter (EKF) |
| 410 | The unscented Kalman filter (UKF) |
| 411 | The particle filter part 1 |
| 412 | The particle filter part 2: resampling |
| 413 | Orientation estimation (Madgwick and Mahony filters) |
| 414 | Fusing GPS, IMU and odometry |
| 415 | Project: tracking a robot with noisy sensors |

## Part 22 — Maps, Localization and SLAM (Ch 416–433)

| Ch | Title |
|---|---|
| 416 | What is a map? Kinds of maps |
| 417 | Occupancy grids |
| 418 | Sensor models for range sensors |
| 419 | Building a map when we know where we are |
| 420 | Ray casting |
| 421 | Markov localization |
| 422 | Monte Carlo localization |
| 423 | Landmarks and feature maps |
| 424 | Scan matching and ICP part 1 |
| 425 | ICP part 2 |
| 426 | The SLAM problem |
| 427 | EKF SLAM |
| 428 | FastSLAM |
| 429 | Graph SLAM part 1: poses and constraints |
| 430 | Graph SLAM part 2: optimisation |
| 431 | Loop closure |
| 432 | Visual SLAM (first look) |
| 433 | Project: SLAM in a simulated world |

## Part 23 — Path Planning (Ch 434–461)

Core robotics part: every chapter has many figures (see `MASTER_PLAN.md` §6).

| Ch | Title |
|---|---|
| 434 | What is planning? |
| 435 | Graphs: nodes and edges |
| 436 | Grids as graphs |
| 437 | Breadth-first search |
| 438 | Depth-first search |
| 439 | Dijkstra's algorithm |
| 440 | A* search |
| 441 | Heuristics |
| 442 | Weighted A* and anytime search |
| 443 | Replanning when the map changes: D* Lite |
| 444 | Configuration space and obstacles |
| 445 | Visibility graphs |
| 446 | Cell decomposition |
| 447 | Potential fields |
| 448 | Sampling-based planning: PRM |
| 449 | RRT |
| 450 | RRT* |
| 451 | RRT-Connect and other RRT variants |
| 452 | Path smoothing |
| 453 | Planning for car-like robots part 1: Dubins paths |
| 454 | Planning for car-like robots part 2: Reeds–Shepp paths |
| 455 | Hybrid A* |
| 456 | State lattice planners |
| 457 | Local planning part 1: the dynamic window approach |
| 458 | Local planning part 2: elastic bands and timed elastic bands |
| 459 | Planning for robot arms |
| 460 | Task and motion planning (first look) |
| 461 | Project: a planner and a controller for a mobile robot |

## Part 24 — Computer Vision (Ch 462–483)

| Ch | Title |
|---|---|
| 462 | How cameras work: light, lens, sensor |
| 463 | Images as arrays of numbers |
| 464 | Colour spaces |
| 465 | Thresholding and colour detection |
| 466 | Convolution and filters (blur) |
| 467 | Finding edges |
| 468 | Morphology: growing and shrinking shapes |
| 469 | Contours and blobs |
| 470 | The Hough transform |
| 471 | Features part 1: corners |
| 472 | Features part 2: descriptors and matching |
| 473 | The pinhole camera model |
| 474 | Camera calibration |
| 475 | Lens distortion |
| 476 | Marker tracking (ArUco and AprilTag) |
| 477 | Finding pose from a camera (PnP) |
| 478 | Stereo vision and depth |
| 479 | Depth cameras and point clouds part 1 |
| 480 | Point clouds part 2: filtering, normals and finding planes (RANSAC) |
| 481 | Point clouds part 3: grouping points into objects |
| 482 | Optical flow and visual odometry |
| 483 | Project: follow a coloured ball |

## Part 25 — Machine Learning for Robots (Ch 484–503)

| Ch | Title |
|---|---|
| 484 | What is machine learning? |
| 485 | Data, features and labels |
| 486 | Linear regression from scratch |
| 487 | Logistic regression and classification |
| 488 | Overfitting, training data and test data |
| 489 | Neurons and neural networks |
| 490 | The forward pass |
| 491 | Backpropagation by hand |
| 492 | A neural network from scratch in NumPy |
| 493 | Training tricks |
| 494 | Convolutional neural networks |
| 495 | Using PyTorch (first look) |
| 496 | Object detection for robots |
| 497 | Reinforcement learning: agent, action, reward |
| 498 | Markov decision processes |
| 499 | Value iteration |
| 500 | Q-learning |
| 501 | Deep reinforcement learning and policy gradients |
| 502 | Imitation learning |
| 503 | Sim-to-real and large robot models (first look) |

## Part 26 — Real-Time Systems and Communication Protocols (Ch 504–530)

Part 6 gave a first look at UART, I2C and SPI. This part goes deep: real-time timing, RTOS, every bus bit by bit, and CAN.

| Ch | Title |
|---|---|
| 504 | What is a real-time system? Hard, firm and soft deadlines |
| 505 | Measuring time: latency, jitter and deadlines |
| 506 | The super loop and simple schedulers |
| 507 | Interrupts in depth: priorities, ISR rules, shared data |
| 508 | What is an RTOS? Tasks, the scheduler, context switches |
| 509 | FreeRTOS part 1: tasks and delays (on an ESP32) |
| 510 | FreeRTOS part 2: queues, semaphores and mutexes |
| 511 | Scheduling and priority inversion |
| 512 | Real-time Linux: PREEMPT_RT and measuring latency |
| 513 | Digital communication basics: bits, baud rate, clocks, serial and parallel |
| 514 | UART in depth: frames, baud errors, RS-232 and RS-485 |
| 515 | Designing a packet: header, length, checksum and CRC |
| 516 | I2C in depth: addresses, ACK, pull-ups, clock stretching |
| 517 | I2C in practice: reading an IMU's registers by hand |
| 518 | SPI in depth: the four modes, chip select, speed |
| 519 | SPI in practice: reading an encoder and an ADC by hand |
| 520 | CAN bus part 1: two wires, differential signals, frames |
| 521 | CAN bus part 2: IDs, arbitration and filters |
| 522 | CAN bus part 3: bit timing and error handling |
| 523 | CAN bus part 4: CAN on Arduino/ESP32 and SocketCAN on Linux |
| 524 | CAN FD and CANopen: controlling smart motors |
| 525 | Other robot buses: Modbus, EtherCAT, USB, Dynamixel |
| 526 | Wireless: Wi-Fi, Bluetooth and radio |
| 527 | Networks for robots: IP, TCP, UDP and sockets in Python |
| 528 | Sending data: binary packing, JSON and MQTT |
| 529 | Debugging buses: logic analysers and oscilloscopes |
| 530 | Project: a two-motor robot base controlled over CAN |

## Part 27 — Linux and ROS 2 (Ch 531–560)

ROS 2 is the standard software framework for robots. We learn it from the first node to real-time ROS 2.

| Ch | Title |
|---|---|
| 531 | Linux terminal basics |
| 532 | Files, permissions and processes |
| 533 | Shell scripts and environment variables |
| 534 | Git for robot projects |
| 535 | Docker for robotics |
| 536 | How robot software is organised |
| 537 | What is ROS 2? ROS 1 and ROS 2 |
| 538 | Installing ROS 2 (Ubuntu, WSL, Docker) |
| 539 | Workspaces, packages and `colcon` |
| 540 | Nodes in Python (`rclpy`) |
| 541 | Topics: publish and subscribe |
| 542 | Messages and custom interfaces |
| 543 | Services |
| 544 | Actions |
| 545 | Parameters |
| 546 | Launch files |
| 547 | Nodes in C++ (`rclcpp`) |
| 548 | DDS and Quality of Service (QoS) |
| 549 | Executors, callbacks and timers |
| 550 | Recording and replaying data: `ros2 bag` |
| 551 | Debugging tools: logging, `rqt`, `ros2 doctor` |
| 552 | tf2: frames in ROS |
| 553 | URDF and Xacro: describing a robot in a file |
| 554 | RViz: seeing what the robot sees |
| 555 | Managed (lifecycle) nodes |
| 556 | Components and zero-copy messages |
| 557 | Many machines: domain IDs, networking and security |
| 558 | Testing ROS 2 code |
| 559 | Real-time ROS 2 |
| 560 | micro-ROS: ROS 2 on a microcontroller |

## Part 28 — Robot Simulators: Gazebo, Webots, MuJoCo, Isaac Sim (Ch 561–582)

Four simulators, each from installing to a full project. Isaac Sim needs an NVIDIA RTX graphics card; the other three run on most computers.

| Ch | Title |
|---|---|
| 561 | What is a robot simulator? Why we simulate |
| 562 | Inside a physics engine: time steps, collisions and contacts |
| 563 | Robot model files: URDF, SDF, MJCF and USD |
| 564 | Gazebo part 1: installing, worlds and models |
| 565 | Gazebo part 2: sensors and plugins |
| 566 | Gazebo part 3: connecting to ROS 2 (`ros_gz`) |
| 567 | Gazebo project: a mobile robot with a LiDAR |
| 568 | Webots part 1: installing, worlds and a first robot |
| 569 | Webots part 2: Python controllers and sensors |
| 570 | Webots part 3: connecting to ROS 2 |
| 571 | Webots project: a line follower and a robot arm |
| 572 | MuJoCo part 1: installing and MJCF models |
| 573 | MuJoCo part 2: the Python simulation loop, actuators and sensors |
| 574 | MuJoCo part 3: contacts, controlling an arm, balancing |
| 575 | MuJoCo part 4: reinforcement learning with Gymnasium |
| 576 | Isaac Sim part 1: what it needs, installing, USD scenes |
| 577 | Isaac Sim part 2: importing robots, sensors and Python scripts |
| 578 | Isaac Sim part 3: the ROS 2 bridge and synthetic data |
| 579 | Isaac Lab: training robots in thousands of worlds at once |
| 580 | Choosing a simulator: a comparison |
| 581 | The sim-to-real gap and domain randomisation |
| 582 | Project: one robot in four simulators |

## Part 29 — ROS 2 in Practice (Ch 583–593)

Now ROS 2 drives complete robots, first in Gazebo, then on real hardware.

| Ch | Title |
|---|---|
| 583 | Sensor drivers in ROS 2: LiDAR, camera, IMU |
| 584 | `ros2_control` part 1: controllers and hardware interfaces |
| 585 | `ros2_control` part 2: writing our own hardware interface (CAN motors) |
| 586 | `robot_localization`: fusing sensors in ROS 2 |
| 587 | SLAM Toolbox: making maps in ROS 2 |
| 588 | Nav2 part 1: setting up navigation |
| 589 | Nav2 part 2: costmaps, planners and controllers |
| 590 | Nav2 part 3: behaviour trees |
| 591 | MoveIt 2 part 1: planning arm motion |
| 592 | MoveIt 2 part 2: pick and place |
| 593 | Project: a ROS 2 robot that drives around a house |

## Part 30 — Advanced Robots and Final Projects (Ch 594–607)

| Ch | Title |
|---|---|
| 594 | Drones part 1: how a quadcopter flies |
| 595 | Drones part 2: dynamics and control |
| 596 | Legged robots: static and dynamic walking |
| 597 | ZMP and balance |
| 598 | Humanoid robots (first look) |
| 599 | Grasping and manipulation |
| 600 | Soft robots |
| 601 | Many robots together: multi-robot systems and swarms |
| 602 | Humans and robots working together |
| 603 | Robot safety standards |
| 604 | Ethics: robots in society |
| 605 | Testing and debugging robots |
| 606 | Final project 1: an autonomous delivery robot |
| 607 | Final project 2: a pick-and-place arm with vision |

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
