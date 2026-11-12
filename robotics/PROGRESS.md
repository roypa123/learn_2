# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 5, Chapter 91 — Digital and analog signals, logic levels.** Part 5 is Electricity and Electronics (Ch 73–93).
Part 4 (Ch 56–72) is complete: about 133,400 words, 97 figures, all programs run, all figures viewed. Pace (user, 2026-11-11): "one part completed then only show next" — write the whole of Part 5 straight through, then report and wait for "next".
Part 4 chapters run 7,100–8,950 words (above the 5,500–6,500 target; projects 6,500–8,000).
Open quality point: Ch 22–35 came out at 3,900–4,900 words, below the 5,500–6,500 target.
Rover's official numbers: encoder 540 ticks/turn, wheel 0.06589 m (Ch 47, 69); Ch 57's 360-tick, 65 mm example is now a generic small robot. Rover's gearbox is 30:1, motor stall 0.010 N m, free 12,000 rpm (Ch 68), effective mass 5.65 kg (Ch 66), track 0.15 m.

## Chapters done

| Ch | File | Words | Code / figures |
|---|---|---|---|
| 1 | part-01-welcome-to-robots/ch001-how-to-use-this-book.md | 8,570 | code/ch001/first_look.py, robot_trip.py, figures.py → images/ch001/fig01–fig06 |
| 2 | part-01-welcome-to-robots/ch002-what-is-a-robot.md | 10,580 | code/ch002/wall_stop.py, cliff_check.py, stop_distance.py, figures.py → images/ch002/fig01–fig06 |
| 3 | part-01-welcome-to-robots/ch003-a-short-history-of-robots.md | 11,380 | code/ch003/governor.py, tortoise.py, figures.py → images/ch003/fig01–fig06 |
| 4 | part-01-welcome-to-robots/ch004-kinds-of-robots.md | 10,590 | code/ch004/choose_robot.py, robot_range.py, figures.py → images/ch004/fig01–fig07 |
| 5 | part-01-welcome-to-robots/ch005-parts-of-a-robot.md | 9,150 | code/ch005/power_budget.py, centre_of_mass.py, figures.py → images/ch005/fig01–fig06 |
| 6 | part-01-welcome-to-robots/ch006-how-a-robot-thinks.md | 9,420 | code/ch006/catch.py, wall_proportional.py, follow.py, figures.py → images/ch006/fig01–fig07 |
| 7 | part-01-welcome-to-robots/ch007-safety-first.md | 13,650 | code/ch007/watchdog.py, e_stop_distance.py, prop_tip.py, figures.py → images/ch007/fig01–fig08 |
| 8 | part-01-welcome-to-robots/ch008-setting-up-your-computer.md | 9,230 | code/ch008/hello_robot.py, hello_error.py, hello_syntax.py, check_setup.py, plot_catch.py, figures.py → images/ch008/fig01–fig06 (fig05 = real output of plot_catch.py) |
| 9 | part-01-welcome-to-robots/ch009-simulation-or-real-hardware.md | 8,760 | code/ch009/sim_vs_real.py, robust_test.py, budget.py, figures.py → images/ch009/fig01–fig06 |
| 10 | part-01-welcome-to-robots/ch010-your-first-robot-on-paper.md | 11,450 | code/ch010/clean_sim.py, lawnmower.py, design_check.py, figures.py → images/ch010/fig01–fig08 |
| 11 | part-02-python-from-zero/ch011-what-is-a-program.md | 7,270 | code/ch011/order_matters.py, grid_trip.py, grid_trip_b.py, pick_place.py, pick_place_wrong.py, figures.py → images/ch011/fig01–fig05 |
| 12 | part-02-python-from-zero/ch012-running-python.md | 5,760 | code/ch012/quiet.py, robot_calc.py, wall_check.py, morning_check.py, figures.py → images/ch012/fig01–fig04 |
| 13 | part-02-python-from-zero/ch013-numbers-and-arithmetic.md | 6,200 | code/ch013/encoder.py, heading.py, trip_time.py, figures.py → images/ch013/fig01–fig05 |
| 14 | part-02-python-from-zero/ch014-variables.md | 10,030 | code/ch014/rover_state.py, swap_motors.py, deliveries.py, figures.py → images/ch014/fig01–fig06 |
| 15 | part-02-python-from-zero/ch015-strings.md | 6,200 | code/ch015/parse_command.py, gps_line.py, sensor_log.py, status_board.py, figures.py → images/ch015/fig01–fig06 |
| 16 | part-02-python-from-zero/ch016-print-and-input.md | 6,200 | code/ch016/keyboard_rover.py, preflight.py, calibrate_wheel.py, trip_ask.py, battery_bar.py, figures.py → images/ch016/fig01–fig06 |
| 17 | part-02-python-from-zero/ch017-booleans-and-comparisons.md | 6,300 | code/ch017/safe_to_drive.py, go_no_go.py, docking.py, truth_table.py, figures.py → images/ch017/fig01–fig06 |
| 18 | part-02-python-from-zero/ch018-if-elif-else.md | 5,200 | code/ch018/rover_commands.py, wall_controller.py, flight_decision.py, battery_bar_safe.py, figures.py → images/ch018/fig01–fig05 |
| 19 | part-02-python-from-zero/ch019-while-loops.md | 5,240 | code/ch019/wall_drive.py, rover_console.py, homing.py, figures.py → images/ch019/fig01–fig05 |
| 20 | part-02-python-from-zero/ch020-for-loops.md | 5,210 | code/ch020/route_runner.py, coverage_grid.py, gain_sweep.py, joint_path.py, figures.py → images/ch020/fig01–fig05 |
| 21 | part-02-python-from-zero/ch021-lists.md | 5,200 | code/ch021/sensor_clean.py, waypoints.py, moving_average.py, delivery_log.py, figures.py → images/ch021/fig01–fig06 |
| 22 | part-02-python-from-zero/ch022-tuples-and-dictionaries.md | 4,930 | code/ch022/rover_config.py, command_table.py, joint_limits.py, error_count.py, figures.py → images/ch022/fig01–fig05 |
| 23 | part-02-python-from-zero/ch023-functions-part-1.md | 4,400 | code/ch023/wall_drive_v2.py, units.py, function_table.py, route_function.py, figures.py → images/ch023/fig01–fig04 |
| 24 | part-02-python-from-zero/ch024-functions-part-2.md | 4,620 | code/ch024/trip_planner.py, summarise.py, fleet_move.py, figures.py → images/ch024/fig01–fig04 |
| 25 | part-02-python-from-zero/ch025-errors-and-debugging.md | 4,930 | code/ch025/crash_demo.py, safe_console.py, sensor_stream.py, motor_guard.py, test_tools.py, buggy_average.py, figures.py → images/ch025/fig01–fig04 |
| 26 | part-02-python-from-zero/ch026-modules-and-math.md | 4,600 | code/ch026/rover_math.py, drive_any_way.py, go_to_goal.py, gps_distance.py, figures.py → images/ch026/fig01–fig05 |
| 27 | part-02-python-from-zero/ch027-files.md | 4,640 | code/ch027/trip_logger.py, settings_file.py, analyse_log.py, drive_log.csv, figures.py → images/ch027/fig01–fig04 |
| 28 | part-02-python-from-zero/ch028-classes-part-1.md | 4,540 | code/ch028/robot.py, safe_rover.py, sensor_filter.py, figures.py → images/ch028/fig01–fig04 |
| 29 | part-02-python-from-zero/ch029-classes-part-2.md | 4,490 | code/ch029/robots.py, composed_rover.py, fake_sensor.py, figures.py → images/ch029/fig01–fig03 |
| 30 | part-02-python-from-zero/ch030-time-and-loops.md | 4,370 | code/ch030/naive_loop.py, steady_loop.py, multi_rate.py, watchdog.py, figures.py → images/ch030/fig01–fig04 |
| 31 | part-02-python-from-zero/ch031-random-numbers.md | 4,250 | code/ch031/noisy_sensor.py, average_helps.py, monte_carlo_wall.py, random_cleaner.py, figures.py → images/ch031/fig01–fig05 |
| 32 | part-02-python-from-zero/ch032-turtle.md | 4,120 | code/ch032/route_on_screen.py, lawnmower.py, two_link_arm.py, drive_with_keys.py, figures.py (matplotlib redraws) → images/ch032/fig01–fig05 |
| 33 | part-02-python-from-zero/ch033-matplotlib.md | 3,900 | code/ch033/first_plot.py, plot_drive_log.py, sensor_calibration.py, chart_kinds.py, figures.py → images/ch033/ |
| 34 | part-02-python-from-zero/ch034-numpy-part-1.md | 4,170 | code/ch034/sensor_array.py, lidar_scan.py, drive_log_stats.py, figures.py → images/ch034/fig01–fig05 |
| 35 | part-02-python-from-zero/ch035-numpy-part-2.md | 4,120 | code/ch035/speed_test.py, vector_monte_carlo.py, scan_to_world.py, wheel_mixer.py, figures.py → images/ch035/fig01–fig05 |
| 36 | part-02-python-from-zero/ch036-project-gridbot.md | 4,810 | code/ch036/gridbot.py, run_gridbot.py, test_gridbot.py, noisy_gridbot.py, worlds/maze.txt, figures.py → images/ch036/ |
| 37 | part-03-maths-you-need/ch037-numbers.md | 7,580 | code/ch037/fractions_by_hand.py, gear_train.py, signed_ticks.py, motor_command.py, figures.py → images/ch037/fig01–fig05 |
| 38 | part-03-maths-you-need/ch038-powers-roots-scientific-notation.md | 6,470 | code/ch038/bits_table.py, my_sqrt.py, sci_notation.py, encoder_resolution.py, hover_rpm.py, figures.py → images/ch038/fig01–fig05 |
| 39 | part-03-maths-you-need/ch039-units-and-measurement.md | 5,760 | code/ch039/convert.py, speed_and_temperature.py, orbiter_units.py, spec_sheet.py, figures.py → images/ch039/fig01–fig06 |
| 40 | part-03-maths-you-need/ch040-algebra-part-1.md | 6,470 | code/ch040/formula.py, check_rules.py, balance.py, mission_energy.py, cycle_time.py, figures.py → images/ch040/fig01–fig05 |
| 41 | part-03-maths-you-need/ch041-algebra-part-2.md | 5,910 | code/ch041/solve_linear.py, rearrange_check.py, intercept.py, drone_range.py, figures.py → images/ch041/fig01–fig04 |
| 42 | part-03-maths-you-need/ch042-coordinates.md | 6,700 | code/ch042/plane_basics.py, move_points.py, warehouse_route.py, world_and_cell.py, figures.py → images/ch042/fig01–fig06 |
| 43 | part-03-maths-you-need/ch043-straight-lines.md | 6,420 | code/ch043/slope_and_line.py, linear_map.py, load_cell.py, lane_centre.py, figures.py → images/ch043/fig01–fig06 |
| 44 | part-03-maths-you-need/ch044-functions-and-graphs.md | 6,420 | code/ch044/function_table.py, piecewise.py, ir_lookup.py, stopping_bisection.py, figures.py → images/ch044/fig01–fig06 |
| 45 | part-03-maths-you-need/ch045-quadratics-and-parabolas.md | 6,440 | code/ch045/quadratic.py, parabola_parts.py, stopping_exact.py, launcher.py, figures.py → images/ch045/fig01–fig06 |
| 46 | part-03-maths-you-need/ch046-simultaneous-equations.md | 6,600 | code/ch046/solve_2x2.py, solve_3x3.py, wheel_speeds.py, ball_fit.py, figures.py → images/ch046/fig01–fig05 |
| 47 | part-03-maths-you-need/ch047-angles-degrees-and-radians.md | 5,760 | code/ch047/convert_angles.py, wrap_angle.py, wheel_odometry.py, heading_hold.py, figures.py → images/ch047/fig01–fig06 |
| 48 | part-03-maths-you-need/ch048-triangles-pythagoras-circles.md | 5,940 | code/ch048/distance.py, estimate_pi.py, arm_reach.py, flower_bed.py, figures.py → images/ch048/fig01–fig07 |
| 49 | part-03-maths-you-need/ch049-trigonometry-part-1.md | 6,010 | code/ch049/trig_ratios.py, find_angle.py, rotate_points.py, scan_to_xy.py, ramp_force.py, figures.py → images/ch049/fig01–fig07 |
| 50 | part-03-maths-you-need/ch050-trigonometry-part-2.md | 5,930 | code/ch050/unit_circle.py, atan_vs_atan2.py, wrap_radians.py, go_to_goal.py, average_heading.py, figures.py → images/ch050/fig01–fig07 |
| 51 | part-03-maths-you-need/ch051-trigonometry-part-3.md | 5,710 | code/ch051/solve_triangle.py, two_link_ik.py, stereo_range.py, figures.py → images/ch051/fig01–fig06 |
| 52 | part-03-maths-you-need/ch052-exponentials-and-logarithms.md | 5,600 | code/ch052/growth_and_decay.py, find_e.py, motor_cooling.py, ema_filter.py, figures.py → images/ch052/fig01–fig06 |
| 53 | part-03-maths-you-need/ch053-sequences-and-sums.md | 5,620 | code/ch053/sequences.py, sigma.py, odometry_sum.py, repeatability.py, figures.py → images/ch053/fig01–fig07 |
| 54 | part-03-maths-you-need/ch054-error-and-rounding-in-computers.md | 6,610 | code/ch054/float_surprises.py, clock_drift.py, encoder_overflow.py, cancellation.py, figures.py → images/ch054/fig01–fig05 |
| 55 | part-03-maths-you-need/ch055-project-measuring-a-room.md | 8,890 | code/ch055/survey_data.py, room_survey.py, heights.py, survey_errors.py, room_map.py, figures.py → images/ch055/fig01–fig07. Ends with the Part 3 review and quiz R1–R10 |
| 56 | part-04-physics-for-robots/ch056-position-distance-and-displacement.md | 8,790 | code/ch056/corridor_trip.py, path_2d.py, encoder_trip.py, drone_home.py, figures.py → images/ch056/fig01–fig06 |
| 57 | part-04-physics-for-robots/ch057-speed-and-velocity.md | 8,030 | code/ch057/speed_basics.py, encoder_speed.py, route_time.py, figures.py → images/ch057/fig01–fig06 |
| 58 | part-04-physics-for-robots/ch058-acceleration.md | 8,150 | code/ch058/accel_basics.py, ramp_limiter.py, lift_ride.py, figures.py → images/ch058/fig01–fig06 |
| 59 | part-04-physics-for-robots/ch059-equations-of-motion.md | 8,170 | code/ch059/suvat.py, stopping.py, move_time.py, figures.py → images/ch059/fig01–fig06. Derives v^2/(2a) promised in Ch 2, 7, 38, 44, 45; ruler table of Ch 6; arm cycle of Ch 40 |
| 60 | part-04-physics-for-robots/ch060-motion-in-two-directions.md | 8,230 | code/ch060/vectors.py, projectile.py, aim_throw.py, drone_drop.py, figures.py → images/ch060/fig01–fig06. Keeps the Ch 45 promise (independent parts of a throw) |
| 61 | part-04-physics-for-robots/ch061-forces-and-newtons-laws.md | 7,580 | code/ch061/newton2.py, hover.py, ramp_accel.py, figures.py → images/ch061/fig01–fig06. Keeps the Ch 49 promise (m g sin angle) and Ch 58 landing force |
| 62 | part-04-physics-for-robots/ch062-mass-weight-and-gravity.md | 7,320 | code/ch062/weight_and_g.py, lift_scale.py, tilt.py, figures.py → images/ch062/fig01–fig05. Explains the still accelerometer reading (Ch 58 promise) |
| 63 | part-04-physics-for-robots/ch063-friction-and-grip.md | 7,600 | code/ch063/friction_basics.py, gripper.py, grip_limits.py, figures.py → images/ch063/fig01–fig06. Keeps Ch 1 promise (load slides at a > mu g) and Ch 9 stiction |
| 64 | part-04-physics-for-robots/ch064-turning.md | 7,090 | code/ch064/spin.py, turn_radius.py, cornering.py, figures.py → images/ch064/fig01–fig05 |
| 65 | part-04-physics-for-robots/ch065-torque-and-levers.md | 7,580 | code/ch065/torque_basics.py, arm_torque.py, rug_edge.py, figures.py → images/ch065/fig01–fig06. Keeps Ch 5 (moment), Ch 37 (gear torque), Ch 49/61 (F = torque / r) promises |
| 66 | part-04-physics-for-robots/ch066-moment-of-inertia.md | 7,290 | code/ch066/inertia.py, arm_swing.py, reaction_wheel.py, figures.py → images/ch066/fig01–fig05 |
| 67 | part-04-physics-for-robots/ch067-work-energy-and-power.md | 7,460 | code/ch067/energy_basics.py, drone_flight_time.py, shift_battery.py, figures.py → images/ch067/fig01–fig06. Keeps Ch 4 (Wh), Ch 7 (crash energy), Ch 40 (E = P t, hills), Ch 41 (1/2 m v^2) promises |
| 68 | part-04-physics-for-robots/ch068-gears-pulleys-and-belts.md | 7,320 | code/ch068/gearbox.py, choose_ratio.py, belt_axis.py, figures.py → images/ch068/fig01–fig06. Keeps Ch 7, Ch 37 (gears, strain wave) and Ch 66 (N^2) promises |
| 69 | part-04-physics-for-robots/ch069-wheels-and-rolling.md | 7,750 | code/ch069/rolling.py, roll_race.py, slip_check.py, lawn_wheel.py, figures.py → images/ch069/fig01–fig05. Answers the Ch 66 rolling challenge |
| 70 | part-04-physics-for-robots/ch070-centre-of-mass-and-balance.md | 8,100 | code/ch070/com.py, tip_limits.py, forklift.py, figures.py → images/ch070/fig01–fig06. Keeps Ch 4/5 centre-of-mass and Ch 62/63/64/69 tipping promises |
| 71 | part-04-physics-for-robots/ch071-simulating-physics-euler.md | 7,980 | code/ch071/euler_fall.py, drag_fall.py, spring_euler.py, rover_speedup.py, figures.py → images/ch071/fig01–fig05. Answers the Ch 59 dt challenge; drag for Ch 60/62 |
| 72 | part-04-physics-for-robots/ch072-project-rolling-cart.md | 8,950 | code/ch072/ramp_data.py, analyse_ramp.py, coast_down.py, models.py, figures.py → images/ch072/fig01–fig06. Example measurement set (replace with your own). Ends with the Part 4 review and quiz R1–R10 |
| 73 | part-05-electricity-and-electronics/ch073-what-is-electricity.md | 9,040 | code/ch073/charge_count.py, drift_speed.py, esd.py, drone_charge.py, figures.py → images/ch073/fig01–fig06. Coulomb, ampere = C/s, conventional current, drift speed, closed loop, ESD |
| 74 | part-05-electricity-and-electronics/ch074-voltage-current-and-resistance.md | 8,450 | code/ch074/volts_and_joules.py, wire_resistance.py, drone_energy.py, thermistor.py, figures.py → images/ch074/fig01–fig06. V = J/C (proves Ch 5's Wh = V × Ah), ground, series cells (NiMH 1.4/1.2/1.0, Li 4.2/3.7/3.3), R = ρ L / A (Rover wire 10 mΩ), NTC thermistor 10 kΩ B 3950 |
| 75 | part-05-electricity-and-electronics/ch075-ohms-law.md | 8,310 | code/ch075/ohm.py, wire_drop.py, short_circuit.py, shunt.py, drone_wire.py, figures.py → images/ch075/fig01–fig06. V = I R three ways, voltage drop, Rover motor stall 4.8 Ω / 1.5 A, battery internal resistance 0.15 Ω (short 48 A, fuse 4 A), non-ohmic parts, 0.1 Ω shunt, 4 mm² drone wire |
| 76 | part-05-electricity-and-electronics/ch076-power-and-heat.md | 8,900 | code/ch076/power_forms.py, wire_heat.py, temperature_rise.py, driver_heat.py, motor_heating.py, figures.py → images/ch076/fig01–fig06. P = V I = I² R = V² / R (keeps Ch 7's I = P / V), wire heat I² ρ / A, thermal resistance θ (driver 60 / 25 °C/W, 2.25 W stall → 150 °C after 234 s), time constant C θ, leg motor 120 W → 100 °C in 6.6 min |
| 77 | part-05-electricity-and-electronics/ch077-series-and-parallel.md | 8,720 | code/ch077/series_parallel.py, reduce_circuit.py, current_split.py, rail_load.py, pack_builder.py, figures.py → images/ch077/fig01–fig06. Series/parallel rules, shrink-then-expand (100 + 200||300 + 50 = 270 Ω, 44.4 mA), Rover's 5 V rail 187 mA (Pi → 987 mA, needs own regulator Ch 90), xSyP packs, current hogging |
| 78 | part-05-electricity-and-electronics/ch078-kirchhoffs-laws.md | 9,000 | code/ch078/check_laws.py, nodal.py (solve(n, resistors, sources), reused later), dock.py, bridge.py, ground_offset.py, figures.py → images/ch078/fig01–fig06. KCL, KVL with sign rule, nodal analysis with NumPy, dock (rail 7.414 V, 1.427 A charging, stops at 8.10 V), Wheatstone bridge 1.25 mV at 500 µε, ground offset 60 mV / star ground |
| 79 | part-05-electricity-and-electronics/ch079-voltage-dividers.md | 7,790 | code/ch079/divider.py, battery_monitor.py, light_sensor.py, thermistor_reader.py, figures.py → images/ch079/fig01–fig06. Vout = Vin R2/(R1+R2), output resistance R1||R2 (rule of ten), pot, R_fixed = √(Rlow Rhigh) (LDR 4.7 kΩ for Moth), 4S monitor 22k/4.7k (453 mAh/month drain), Rover thermistor counts 153 (70 °C) / 100 (85 °C) with 10 kΩ |
| 80 | part-05-electricity-and-electronics/ch080-breadboards-and-diagrams.md | 8,340 | code/ch080/breadboard.py (net finder + checker using nodal.py), wire_gauge.py (AWG, 5 W/m inside a robot: AWG 20 = 12.4 A), breadboard_current.py (0.26 Ω path, 1 A rating), figures.py → images/ch080/fig01–fig06. Symbols chart, dot = joined, same name = same net, strips a–e/f–j, check-before-power routine |
| 81 | part-05-electricity-and-electronics/ch081-the-multimeter.md | 8,910 | code/ch081/meter_loading.py, accuracy.py, burden.py, voltage_walk.py (uses nodal.py), internal_resistance.py, figures.py → images/ch081/fig01–fig06. V across / I in series / R power off, rule of a hundred, ±(0.5% + 2 digits), burden (1 Ω mA, 0.01 Ω 10A), voltage walk (corroded connector 2.4 V), Rover pack internal resistance 0.146 Ω (example data) |
| 82 | part-05-electricity-and-electronics/ch082-leds-and-resistors.md | 8,800 | code/ch082/led_resistor.py (next_standard E12), led_model.py (exponential LED, bisection), colour_code.py, pin_budget.py (Rover 7 status LEDs = 60 mA, 30% of Uno), ir_emitter.py (220 Ω, 14.9–19.9 mA worst case), figures.py → images/ch082/fig01–fig06. Vf by colour, R = (Vs − Vf)/I, E12, colour code, pin limits 20 mA/200 mA |
| 83 | part-05-electricity-and-electronics/ch083-switches-and-pull-ups.md | 8,100 | code/ch083/floating.py, pullup_choice.py (10 k; 4.7 k–100 k band), bounce.py (12 false edges, 5 ms debounce), fail_safe.py (NC bumpers with pull-up), figures.py → images/ch083/fig01–fig06. SPST/SPDT/NO/NC, floating pin, active low, bounce, NC for safety inputs. Rover bumpers = NC contact + built-in pull-up |
| 84 | part-05-electricity-and-electronics/ch084-capacitors.md | 8,400 | code/ch084/rc_charge.py, cap_energy.py, brownout.py (servo start 1.49 A vs 1 A regulator: 4,700 µF needed), rc_filter.py (10 k/1 µF: noise 257 → 22 mV, 23 ms delay), figures.py → images/ch084/fig01–fig06. Q = CV, τ = RC (keeps Ch 52's 10 k/10 µF reset promise), I = C dV/dt, E = ½CV², decoupling 100 nF, bulk, RC filter/debounce, supercaps |
| 85 | part-05-electricity-and-electronics/ch085-inductors-and-coils.md | 7,800 | code/ch085/rl_rise.py (relay 70 Ω/0.15 H, τ 2.14 ms, pulls in 2.6 ms), spike.py (10,714 V with no path; diode 5.7 V), back_emf.py (Rover motor K = 5.35 mV/(rad/s) = 0.56 mV/rpm; pushed 1.5 m/s → 7.3 V), figures.py → images/ch085/fig01–fig06. V = L dI/dt, τ = L/R, ½LI², back EMF, generator. Rover motor winding ~1.5 mH (τ 0.31 ms) |
| 86 | part-05-electricity-and-electronics/ch086-diodes-and-flyback.md | 7,000 | code/ch086/diode_iv.py, flyback.py (24 V valve: diode 6.8 ms, +24 V Zener 1.4 ms at 48.7 V), reverse_protection.py (Rover: Si 11%, Schottky 5.3%, P-MOSFET 0.15%), solar_bypass.py (90 → 18 → 58 W), figures.py → images/ch086/fig01–fig06. p–n junction, Vf 0.7 / Schottky 0.3–0.45, flyback cathode to +, Zener, OR-ing, rectifier, TVS. Rover plan: Schottky now, P-MOSFET after Ch 88 |
| 87 | part-05-electricity-and-electronics/ch087-transistors-bjt.md | 7,200 | code/ch087/bjt_model.py (12 V lamp: half on 800 mW vs saturated 59 mW), base_resistor.py (forced β 20: relay 1 k, fan 470, lamp 220; 0.5 A strip needs 26.7 mA → MOSFET), light_switch.py (one transistor starts at 1,067 lux; Darlington at 7 lux → Moth compares two sensors), figures.py → images/ch087/fig01–fig06. NPN, β, active/saturated, low-side switch with base pull-down and flyback, phototransistor, optocoupler |
| 88 | part-05-electricity-and-electronics/ch088-mosfets.md | 6,940 | code/ch088/mosfet_model.py (logic-level vs standard at 5 V: 0.62 vs 3.85 W at 5 A), choose_mosfet.py (2N7000/AO3400/IRLZ44N/3 mΩ FET for 0.5–30 A), switching_loss.py (ESC 30 A 22.2 V: 0.9 W conduction + 0.8 W switching at 24 kHz), figures.py → images/ch088/fig01–fig06. Gate = capacitor, Vth vs R_DS(on) at 4.5 V, gate 100 Ω + 10 k pull-down, body diode, P-MOSFET reverse protection |
| 89 | part-05-electricity-and-electronics/ch089-batteries.md | 9,700 | code/ch089/lipo_model.py (OCV table, np.interp; imported by others), chemistries.py, c_rating.py (5,000 mAh 25C: 125 A; 120 A → 2.4 V sag, 288 W), cc_cv_charge.py (1C, 0.04 Ω path: CC 42 min, full 74 min), coulomb_count.py (3,900 mAh → land), figures.py → images/ch089/fig01–fig06. Keeps Ch 5 (Wh = V×Ah), Ch 7 (thermal runaway, 3.8 V storage), Ch 16/52/73/75/81 promises; 80% rule; balancing; BMS |
| 90 | part-05-electricity-and-electronics/ch090-regulators-and-power-supplies.md | 7,300 | code/ch090/linear_reg.py (Rover 5 V rail 0.19 A: 0.65 W at 8.4 V; 7805 drops out below 7 V, LDO fine), pi_power.py (Pi: linear 72 min vs buck 84 min), buck_sim.py (8.4→5 V, 200 kHz, 22 µH/100 µF: 3 mV ripple), figures.py → images/ch090/fig01–fig06. Keeps Ch 76/77 Pi promise: LDO for Arduino rail + 5 V 3 A buck for Pi; power tree |

## Notes for writers

- Ch 1 set these reader expectations: 📖 word list at the back of the notebook; folders `robotics/my-code/chNNN/`;
  5 safety rules (simulation first, a way to stop, start slow, no propellers on the table, respect batteries);
  colour meanings (setpoint black dashed, output blue, error red, control green, robot orange, obstacles grey).
- Ch 1 forward references to keep true: Ch 54 (float rounding, `0.4 * 3 = 1.2000000000000002`), Ch 63 (a ≤ μ·g, load
  sliding on a warehouse robot), Ch 7 and Ch 89 (battery safety).
- Ch 2 defined: the **robot test** (4 questions: senses? thinks by itself? acts by moving? loops?); tool / automatic
  machine / robot; a thermostat is a *controller*, not a robot; open loop vs closed loop (feedback); setpoint;
  autonomy vs teleoperation; "blind distance" between loops = speed × loop time; loop-rate figure (thermostat 0.2/s,
  vacuum ~50, warehouse ~100, arm ~1,000, drone ~2,000). Room model used: new T = T + heat − 0.05 × (T − outside).
  Forward refs to keep: Ch 59 (braking distance grows with speed², warehouse table 0.50/1.13/2.00 m), Ch 52 (log scale),
  Ch 208 (on-off zigzag), Ch 250 (loop rate maths), Ch 641–643 (drone tilt loop), Ch 744 (safety fields).
- Ch 3 used: S/T/A tags for milestones; governor model `speed += 10 × (2.0 × valve − load × speed / 100)` with
  valve = 0.5 + 0.02 × (100 − speed) → settles at 90.9 (open loop 66.7) — Ch 211 must explain this steady-state error,
  Ch 212 removes it. Tortoise model: brightness = 1/(1 + d²), sensors ±30° at 0.2 m, turn = 400 × (left − right);
  start C (facing away) gets lost; gain 50 → passes the lamp and leaves (4.4 m away after 100 steps); gain −400 → flees
  (11 m). Lab 3.3 left an open challenge: `turn_gain = 4000` (test it once Python is installed, Ch 8+).
  Forward refs: Ch 93 Moth, Ch 292–295 line/wall following, Ch 454 A*, Ch 744 safety, Ch 745 ethics.
- Ch 4 introduced: DOF (6 free in space, 3 on a floor, 1 per simple joint; arm ≈ 7 for a human arm); link, joint,
  end effector, cobot, multirotor, tether, centre of mass, support polygon (static stability rule); differential drive
  forward speed = (left + right) ÷ 2; W and Wh with time = energy ÷ power (example values 1 kg robots: wheeled 10 W
  1 m/s, legged 40 W 1 m/s, flying 150 W 10 m/s, 50 Wh → 300/75/20 min, 18/4.5/12 km); weighted score table
  (decision matrix) with the "forgot 'sees from above'" lesson; drone survey 50 Wh, 75% usable, 150 W, 8 m/s, 40 m strip
  → 28.8 ha. No dedicated underwater part: underwater ideas live in 🌊 applications.
  Forward refs: Ch 70, 67, 122, 146, 150, 270 (MPC), 284, 285, 301–309, 334, 344, 348–349, 368, 370, 390, 476,
  594, 615, 624, 630, 668, 671, 687–690, 740–743, 749.
- Ch 5 fixed Rover's design (stage 3): 6 × AA NiMH 7.2 V 2.0 Ah = 14.4 Wh (80% usable = 11.52 Wh), switch + fuse,
  5 V regulator (brain + sensors), TB6612 driver fed 7.2 V direct, Arduino, bumpers, line sensor, distance sensor,
  2 gearmotors with encoders, caster at −9 cm behind the axle. Typical watts: Arduino 0.25, driver 0.3, motors 3.0,
  line 0.15, distance 0.08 → 3.78 W → 3.05 h; stage 7 adds Pi 4.0 + camera 1.0 → 8.78 W → 79 min.
  Masses: chassis 150 g (−3), motors+wheels 160 (0), Arduino+driver 35 (−4), sensors 30 (+7), battery 165 (−5 back)
  → CoM −2.23 cm (battery front +5 → +0.82, tips). Rover loop 50 Hz = 20 ms (sense 2, think 1, send 0.5 ms).
  Taught: signal vs power wires, common ground, digital/analog/PWM, two-level brains, Wh = V × Ah (trust until Ch 89),
  CoM = Σ m·x ÷ Σ m (Ch 70 full), "moment" word (Ch 65). Diagram colours here: power = thick black, signal = blue,
  motor power = green.
- Ch 6 defined the control-loop vocabulary (setpoint, measurement, error = setpoint − measurement, controller,
  command, actuator, system/plant, output, disturbance, gain, overshoot, delay, steady-state error) and proportional
  control (command = gain × error) as a PREVIEW of Ch 210. Key rule taught: for x += gain·(sp − x)·dt the "fraction per
  loop" gain·dt should be well below 1 and must be < 2. Results to stay consistent with: catch gain 4, dt 0.05 → 1.186 m
  at 1 s; gains 1/30/45 → 0.77 / settles / unstable (2.7, −0.675, 3.544); 0.2 s delay with gain 4 → peak 1.68, dip 1.02;
  gain 8 + delay unstable; follower error = v ÷ gain (gain 2 → 1.5 m, gain 5 → 1.2 m); feedforward removes the gap
  (Ch 227); chase vs aim: 0.90 vs 1.19 m. Rover wall with P (gain 1, dt 0.5, limit 0.25) → 0.301 m, no overshoot.
  Ruler-drop table (Ch 59 formula): 5/10/15/20/25/30 cm → 0.10/0.14/0.18/0.20/0.23/0.25 s.
  Forward refs: 103, 210–216, 212, 218–219, 227, 228, 270, 298, 306, 310–312, 385, 416, 637.
- Ch 7 defined hazard, risk = how likely × how bad (1–3 each; 1–2 low, 3–4 medium, 6–9 high), mains vs low voltage
  (water picture: voltage = how hard the pump pushes, current = how much flows; dry skin = narrow pipe), short circuit,
  fuse rules (near battery on +, above peak and below wire limit, never replace with bigger/wire), lithium types table,
  thermal runaway as a GROWING loop (×1.5 per round picture), LiPo 4.2 V full / 3.8 V storage per cell, coin-cell
  swallowing danger, pinch points, fail-safe brakes, propeller rules, tools table, e-stop 6 properties (red on yellow,
  reachable, mushroom, latching, cuts MOTOR power with a real switch while brain stays on, release does not restart),
  two stop kinds (cut at once / brake then cut = stop cat. 0 / 1, Ch 744), drone arm/disarm + failsafe + kill switch,
  "safe state depends on the robot", watchdog/heartbeat ("if I hear nothing, I stop"), 5 safety layers (design,
  software, sensors, hardware, people), 8-item pre-power checklist incl. "wheels up". Rover now has an e-stop in the
  MOTOR power path (after the regulator split; 2nd contact to an Arduino pin) and a 4 A slow fuse (normal 0.53 A,
  start peak 3.1 A = 2 × 1.5 A + 0.1, wires ~5 A, current = power ÷ voltage preview of Ch 76).
  Results: watchdog (0.5 m/s, dt 0.1, link lost step 20, 3 silent loops) → STOP at 2.2 s, 0.1 m vs 1.55 m without;
  e-stop totals at 1.5 m/s: 1.535 / 2.66 / 5.66 m (human 0.25/1.0/3.0 s, circuit 0.02 s) vs own sensor 1.355 m;
  prop tips: toy 62.8, racing 199.5 (500 turns/s), camera 88.0, farm 119.4 m/s; saw ~55, motorway 33 m/s;
  cobot zone 1.6 m/s × 0.6 s + 0.2 + 0.1 ≈ 1.3 m (simplified; real rule Ch 744); battery room 40 × 100 Wh, 6S
  25.2 / 22.8 V. Introduced π = 3.14159 and circumference = π × d (Ch 48 full), rpm ÷ 60, m/s × 3.6 = km/h.
  Forward refs: 26, 48, 59, 67, 68, 73–93, 76, 80, 81, 87–88, 89, 92, 129, 151, 385, 523, 544, 615, 618, 621, 640,
  718, 729, 743, 744. Ch 7 ran long (~13,650 words): Part 1 chapters keep growing; aim shorter for Ch 8–12.
- Ch 8 set up: Python ≥ 3.12 (tested 3.14), Thonny (beginners) or VS Code + Python extension; `python` on Windows
  (`py` also), `python3` on macOS/Linux; `python -m pip install numpy matplotlib`; Linux "externally-managed-
  environment" → venv `~/robotics-venv` (source …/activate each terminal). Terminal commands taught: pwd, dir/ls, cd,
  cd .., mkdir (mkdir -p), python file.py, Tab, ↑, Ctrl+C ("software e-stop", not enough on a real robot). Rules for
  file names (lowercase, _, no spaces, not a library name, start with a letter). Four steps to read an error (last
  line, line number, ^^^, fix/save/run); error table (SyntaxError, NameError, IndentationError, TypeError,
  ModuleNotFoundError, ZeroDivisionError). Introduced (lightly): comment, print, variable, import, `as plt`, list
  `.append`, indexing from 0, `str()`, `**`, plt.plot/axhline/xlabel/ylabel/title/legend/savefig/show.
  Results: plot_catch gains 1/4/30 at 1.0 s → 0.77 / 1.186 / 1.2 m (Ch 6 table fixed from 0.79 to 0.77);
  gain 20 → 1.2 in one loop; 39 swings (0.77 at 1 s); 45 unstable (−102.9 at 1 s); watchdog max_silent 10 → STOP
  2.9 s, 0.45 m; max_silent 1 → 2.0 s, 0.0 m. Application 1: requirements.txt, version comparison (3.10 > 3.9).
  Forward refs: 11, 12, 13, 14, 15, 18, 21, 25, 26, 27, 33, 34–35, 96, 111, 112, 214, 549, 554, 639, Part 27/28.
- Ch 9 defined simulation, model ("all models are wrong, some are useful"), reality gap (table of effects), noise,
  friction/stiction (Ch 63), robust, Monte Carlo, domain randomization (Ch 687), BOM, datasheet, compatible boards.
  Taught `random.seed`, `random.uniform`, `==`, nested if, `len()`, running total, `abs()`. Key formula: friction
  stuck error ≤ smallest moving command ÷ gain; bigger gain shrinks it but amplifies noise.
  Results: sim_vs_real (gain 2, dt 0.1, 0.85 motors, stiction 0.05, noise ±1 cm, seed 1) → perfect 0.300, real 0.315 m;
  robust_test (seed 2; strength 0.6–1.2, stiction 0–0.08, 2 cm test) → gain 2: 78/100, gain 4: 100, gain 8: 100 (all
  slightly past the setpoint: noise). Rover stage 3 BOM $83–153 (avg $118); full hardware track ≈ $870 (midpoints,
  bought when needed); core (steps 1–5, to Ch ~446) ≈ $160; nothing needed before Ch 81. Paths A ($0) / B ($100–200) /
  C (full). Club example: 6 Rovers, shared chargers, compatible boards ≈ $605. Tools table: Python, Wokwi, Tinkercad,
  Webots, Gazebo, MuJoCo, Isaac Sim/Lab. Forward refs: 17, 31, 63, 81, 91, 92, 93, 141, 151, 212, 423–424, 548, 615,
  687, 747–749, Part 28, Part 30.
- Ch 10 (end of Part 1) taught the design loop (requirements → ideas → choose → details → check → improve; "a
  control loop for designs"), checkable requirements, must / nice to have, constraint, trade-off, coverage,
  behaviour + priority (cliff > bump > battery low > clean; subsumption / Rodney Brooks; Ch 104), verification, BOM,
  prototype. Tiny cleaner: round 20 cm × 8 cm, 0.6 kg, 0.2 m/s, differential drive, caster front, battery in front of
  the axis, 2 bumpers, 4 cliff sensors 4 cm ahead, 2 encoders, Arduino Nano, TB6612 + MOSFET (brush), 4 × AA NiMH
  4.8 V 2.0 Ah, 3 A slow fuse, buck-boost 5 V regulator, STOP button in motor power. Power 4.35 W → 106 min; cliff
  stop 0.2 × 0.02 + 0.02 = 0.024 m; BOM $96. Sims (4 × 3 m room, 5 cm cells, brush r 0.08, robot r 0.10):
  clean_sim seed 3 → 0.2/49.4/75.8/84.1/88.7/92.3/93.8% at 0–30 min (90% at ~21 min); lawnmower row gap 0.15 →
  19 rows, 96.1% in 6.3 min (missing top row bug) → fixed 20 rows 99.5% in 6.6 min; reachable max 99.9%. App 1: +6 W
  fan → 10.35 W → 44.5 min FAIL, $104 FAIL; fixes (a) 2.5 Ah 55.7 min, (b) drop brush 52.1 min $98, (c) question the
  45-min requirement. Lab 10.2 results: brush 0.10 → 98.2%, speed 0.3 → 95.5%, turn 180 → 6.0%, gap 0.20 → 92.6% in
  4.7 min. Previewed math.cos/sin/radians, Pythagoras, `//`, `**`, `not`, `or`, while, tuples, sum, x-if-else.
  Part 1 review checklist + quiz R1–R8 at the end. Forward refs: 18, 19, 21, 22, 26, 47–50, 48, 88, 90, 94, 104, 122,
  130, 151, 288, 454, 747, Part 23, Part 30.
- Ch 11 (start of Part 2) defined instruction, program, programming language, algorithm, sequence, statement, state,
  trace table, flowchart (oval start/end, rectangle instruction, arrows; diamond comes in Ch 18, back-arrows Ch 19),
  bug (Harvard Mark II moth, 9 Sep 1947, Grace Hopper), debugging; three kinds of bugs (syntax, runtime, logic: "no
  error message ≠ no bug"). Ada Lovelace 1843. Results: order_matters 80→+20→/2 = 50.0 vs /2→+20 = 60.0;
  grid_trip (3E,2N,1E,1N) corners (0,0)(3,0)(3,2)(4,2)(4,3) avoids TABLE at (1,2),(2,2); grid_trip_b (2N,3E,1N,1E)
  passes through the table; 16 of the 24 orders of those moves are safe. pick_place state z / gripper / holding with
  `holding = z == 0`: right order → True; close-before-down → False. Drone start-up order C→B→D→E→A→F (never arm
  before the propeller check); "topological sorting" named. Previewed `==` (Ch 17), text values (Ch 15), True/False.
  Forward refs: 13, 14, 15, 17, 18, 19, 36, 149, 643, 748, Part 23.
- Ch 12 taught the shell (REPL = read, evaluate, print, loop; prompt >>>; exit()/exit/Ctrl+Z Enter/Ctrl+D; echo of
  expressions, no echo for assignments; session-only variables; `<python-input-0>` in tracebacks), `_` last answer
  (shell only; NameError in scripts), ↑ history, help() (q to leave), type() → float/int/str (preview), `...` for
  multi-line, scripts only show what is printed (quiet.py → only 0.01), shell-or-script flowchart (diamond = question,
  preview of Ch 18), `python -i` (wall_check.py: distance 0.5, step 3, 0.125), working habits list (folder per chapter,
  header comment, names with units like power_w / usable_wh, save, small steps, predict, scratch.py), `import this`.
  Results: robot_calc → 0.01 m, 183 min, 199.5 m/s; 0.8 × 14.4 = 11.520000000000001 (Ch 54); with Pi+camera 8.78 W →
  79 min; drone field: 15 min flight, 980 m, ≈2.04 min. Forward refs: 13, 15, 17, 18, 20, 27, 54, 111, 112, 651, 664,
  Part 25, Part 27.
- Ch 13 taught int (counting) vs float (measuring), type(), int+float → float, 1e3 / 2.5e-3 / 1_000_000, the
  operators + - * / // % ** (/ always float; ** 0.5 = sqrt; ** -1), // and % with check (a//b)*b + a%b = a, negative
  // rounds down (-7//2 = -4, -7%2 = 1), order of operations (brackets → ** (right to left) → * / // % → + -; -2**2 =
  -4; average bug a + b / 2), round(x), round(x, n), round(x, -2), round half to even (0.5→0, 1.5→2, 2.5→2, 3.5→4),
  round(2.675, 2) = 2.67, 0.1 + 0.2 = 0.30000000000000004, never == with floats (Ch 17), int() cuts, unit
  conversions (÷100, ÷60, ×3.6, //60 %60), Mars Climate Orbiter units story. Results: encoder.py 2000 ticks, 540/turn,
  65 mm wheel → 3 full turns, 380 leftover, 3.704 turns, 0.2042 m circumference, 0.756 m; heading.py 350+30 → 20,
  −50 → 330, +725 → 335; trip_time.py 120 rpm, 0.2 m wheel, 900 m → 1.257 m/s = 4.52 km/h, 716 s = 11 min 56 s;
  field 10 ha in 6 h 10 min; Mars delay 750 s = 12 min 30 s; 0.02 added 50 times = 1.0000000000000004.
  Forward refs: 17, 21, 26, 47, 48, 54, 59, 122, 126, 288, 298, Part 23.
- Ch 14 taught variable = name + value (box picture, then labels in 14.8), = means store (right side first),
  NameError before assignment, replace vs update, += -= *= /= //= %= **=, the =+ trap, computing without storing,
  trace tables, naming rules (letters/digits/_, no digit first, 35 keywords in Python 3.14 via keyword.kwlist,
  case-sensitive, don't shadow round/max/print: TypeError 'int' object is not callable), snake_case, units in names
  (x_cm + x_m = 12.3 bug), state = group of variables, multiple assignment and unpack ValueError, a = b = 0.0, swap
  (wrong 8 8, temp, a, b = b, a), CAPITALS constants (not locked), b = a + 3 is one-time. Results: rover_state.py
  (POWER_W 3.78, SPEED_MS 0.25, 11.52 Wh) → (2.0, 0.0) 11.5116 Wh, (2.0, 1.5) heading 0 11.5053 Wh, odometer 3.5 m,
  used 0.0147 Wh = 0.13 %; lab leg 3 west 0.5 m → x 1.5, heading 270, 11.5032 Wh, 4.0 m, 0.15 %; swap_motors pins 5/6;
  deliveries 120 + 85.5 + 240 = 445.5 m, average 148.5 m, 354 s = 5 min 54 s; float swap trick → b =
  0.10000000000000003. Forward refs: 15, 17, 18, 19, 20, 21, 22, 23, 26, 27, 28, 49–50, 96, 141, 288, 563, 569, 646,
  Part 32.
- Ch 15 taught str, the digits trap ("5" + "1" = '51', "5" + 1 TypeError), escapes (newline, tab, quote, backslash; Windows
  path trap; r"" raw), triple quotes, repr() to see hidden characters, + * len, index from 0 and negative, IndexError,
  slices as cuts between characters (forgiving past the end, [::2], [::-1]), immutable (TypeError on item assignment),
  methods strip lower upper split split(sep) replace startswith endswith find count, `in`, first look at lists from
  split (unpack into names, or pick by index; lists are Ch 21), chaining left to right, "parse" = clean, cut, convert,
  float/int/str, ValueError (int("0.25"), float("abc"), float("")), "10" < "9" is True, f-strings (.2f, width, < > ^,
  03d, .0%, comma, x=). From Ch 15 on, shell error examples show only the last line of the traceback. Results:
  parse_command "  FORWARD 0.25" → 0.25 m/s, 73.5 rpm; gps_line (standard GGA example) → 12:35:19, 48.11730 N,
  11.51667 E, 8 sats, 545.4 m; sensor_log → cell 1.188 V and 1.163 V; status_board widths 10 + 8 + 10 = 28.
  Forward refs: 16, 17, 18, 20, 21, 25, 27, 33, 111, 130, 426, 533, 559, 630, Part 32.
- Ch 16 taught argument, keyword argument, print with several values, sep, end, print(), print returns None (Ch 24),
  staying on a line, carriage return and leftover characters (fixed width), buffer and flush=True, input pauses and
  always returns str, prompts with units and a trailing space, inside-out float(input(...)), strip/lower on input,
  input removes the newline but keeps spaces, Enter as a go button, Ctrl+C KeyboardInterrupt, EOFError with no keyboard,
  rule: never input in a robot's control loop, input-process-output = sense-think-act, ZeroDivisionError (lab),
  f-string +.2f, fill-and-centre (=^21), CSV with sep=",". Sessions in the text came from running the real programs
  with typed answers echoed. Results: keyboard_rover "0.25 8" and "-0.1 5" → 1.50 m, 11.5063 Wh; trip_ask 900, 1.257 →
  11 min 56 s; preflight 4S 16.2 V → 4.05 V/cell, 79%, 11.8 min (3.5–4.2 V linear, 15 min full); calibrate_wheel 2640
  ticks, 1.012 m → believed 0.998, -1.35 %, true D 0.06589 m; battery_bar 87% → 17 of 20.
  Forward refs: 17, 18, 19, 24, 25, 27, 30, 33, 89, 112, 289, 643.
- Ch 17 taught bool, flag, six comparisons, = vs ==, > vs >= at the edge, storing conditions, chained 0 < x < 1,
  and/or/not with truth tables and series/parallel switches, order arithmetic → comparisons → not → and → or, the
  x == 1 or 2 bug, short-circuit guard (speed != 0 and ...), De Morgan, text comparison (clean first, "Z" < "a",
  "10" < "9"), floats with tolerance abs(a - b) <= tol (math.isclose in Ch 26), True = 1 / False = 0, truthy/falsy,
  bool("False") trap, f-string !s for bools with a width, fail-safe rules (flags name the good state, unknown means
  unsafe, edge on the safe side), heading error (a - b + 180) % 360 - 180 in −180..179. Results: safe_to_drive 0.25 m/s
  or 0.0; go_no_go (3.7 V/cell, 6 sats, 10 m/s) 16.2/8/6/y GO, 14.4/5/6/yes 3 failed; docking 0.015 m, −1 deg, docked.
  Forward refs: 18, 26, 50, 119, 208, 299, 643, 664.
- Ch 18 taught if, block, indentation rules and real error messages, pass, else, one-line conditional, elif (first True
  wins), order, elif vs separate ifs, nesting vs and, truthy in if, guard / clamp / deadband. In wall_controller the
  error is distance − setpoint (flipped vs Ch 6, explained). Results: wall_controller (0.30, gain 1, ±0.25, ±0.01) at
  1.0/0.5/0.305/0.25/0.0 → +.25/+.20/0/−.05/−.25; rover_commands; flight_decision prints each problem; battery tiers
  3.7 normal, 3.5 return home, else land. Forward refs: 19, 23, 25, 208, 210, 212, 640, 664, 718.
- Ch 19 taught while, iteration, trace, start/condition/update, Ctrl+C, while True, floats and loop conditions (t != 1.0
  never ends; t < 1.0 takes 11 passes), break, continue trap, sentinel, retry until valid, max-steps guard. Results:
  wall_drive (1.0 m, gain 1, clamp .25, deadband .01, dt .5) → 9 steps, 0.306 m; gains .5/3/4/6 → 16 steps .308,
  8 steps .291, 50 steps .25 (bounces), 50 steps .25; homing 74 steps, broken switch FAULT after 400. Refs: 20, 30, 115.
- Ch 20 taught for, loop variable, iterable, range forms, stop never included, count with int and calculate floats,
  off-by-one, for vs while, _ variable, nested loops, four patterns (count, total, largest so far, search). Results:
  route_runner FFRFFLFRFF → (4,3), 7 m, 5.0 m; coverage 6x4 → 24 cells, 23 moves; gain_sweep best 2.0 in 6 steps
  (.5:16, 1:9, 1.5:7, 2:6, 2.5:7, 3:8, 3.5:12, 4:60); joint_path 20→80 in 6 steps.
- Ch 21 taught list, mutable, append/insert/pop/remove/del/clear, methods return None, queue/stack, enumerate, zip, no
  removing while looping, sum/min/max/sorted/sort/in/index/count, join, comprehensions, alias/copy, is, x = y = [],
  [[0]*3]*2 trap, nested lists, waypoints, mean/median/outlier. Results: sensor_clean mean 1.082, median 0.520;
  waypoints 6.00 m, 24 s, 0.0252 Wh; moving average window 3 (spike 30 → 16.7/17.0/17.3); delivery_log 510 m, 127.5 avg.
- Ch 22 taught tuple, unpacking, (5,), dict, key, KeyError, in/get, pop/del, items/values, unhashable list keys, tuple keys,
  nested dict, set, list of dicts, lookup table. Results: rover_config one tick 0.383 mm, 3.05 h; command_table
  forward/back/left/right/stop as (left, right) fractions, SPEED 0.2; joint_limits left_knee 140→135, right_ankle 31→25.
- Ch 23 taught def, call, parameters/arguments, return vs print, None, flow, docstrings, help, one job, DRY, refactor,
  functions as values, dispatch table. Results: wall_drive_v2 same as Ch 19 (9 steps, 0.306); units 2640 ticks = 1.012 m,
  1 m = 2609 ticks, 72.5 rpm, round trip 1.0001 m; run_route returns (x, y, heading). Ch 26 must import units.py as a module.
- Ch 30–36 results to stay consistent with: steady loop 50 Hz average 20.01 ms vs naive 26 ms; watchdog 0.25 s; Monte Carlo wall (noise 3 cm, near miss < 0.25 m) gains 1/2/3 → 1.2/46/88% of 500 runs and 1.8/49.3/88.9% of 100,000; averaging N divides noise by sqrt(N); random cleaner 20x20: 11/32/74/99% at 100/400/1600/6400 steps; sensor fit 1.0439 x + 0.0137; scan_to_world first point (2.866, 1.5); wheel mixer track 0.15 m; GridBot right-hand 55 moves, left-hand 29, BFS shortest 29, 43 free cells; sensor error 0/1/5/10/20% → 100/100/84/55/23% reach goal.
- Part 2 now provides: rover_math-style modules, Robot and SafeRover classes, MovingAverage with update(), Watchdog, Every timer, NoisySensor, FakeSensor, GridBot. Later chapters can refer back to them.
- Chapter length: theory chapters with the full 🏭 applications section come out at ~10,000 words (Ch 2: 10,580).
  That matches MASTER_PLAN §2 (base + 2,000–3,000 for applications) only loosely; it is on the long side, not short.
- Figures: the matplotlib default font has no emoji, so do not put emoji inside figures (only in the Markdown text).
- Ch 1 is 8,570 words, above the 5,500–6,500 target for normal chapters. That is fine for an introduction chapter, but
  keep later Part 1 chapters nearer the target.

## Status

- 2026-11-10: Chapters 34, 35, 36 written. Part 2 complete (Ch 11–36, about 135,700 words). Next: Part 3.
- 2026-11-10: Chapter 33 written (matplotlib fig/ax, chart kinds, graph rules, best-fit line; 5 figures, 4 programs).
- 2026-11-10: Chapter 32 written (turtle, logo mode, scale, callbacks, event loop; 5 figures, 4 programs).
- 2026-11-10: Chapter 31 written (random, seed, distributions, noise, sqrt N, Monte Carlo: gain 2 near misses 231/500; 5 figures, 4 programs).
- 2026-11-10: Chapter 30 written (clocks, sleep, drift, steady loop, jitter, overruns, multi-rate timers, watchdog; 4 figures, 4 programs).
- 2026-11-10: Chapter 29 written (inheritance, super, polymorphism, composition, properties, dunders, dataclass, fakes; 3 figures, 3 programs).
- 2026-11-10: Chapter 28 written (classes, __init__, self, methods, class attributes, __str__, encapsulation, filter objects; 4 figures, 3 programs).
- 2026-11-10: Chapter 27 written (files, modes, with, paths, CSV, JSON, atomic save; 4 figures, 3 programs + data).
- 2026-11-10: Chapter 26 written (modules, math, radians, sin/cos heading, atan2, own modules, __name__, pip/venv; 5 figures, 4 programs).
- 2026-11-10: Chapter 25 written (traceback, try/except/finally, raise, assert, debugging loop; 4 figures, 6 programs).
- 2026-11-10: Chapter 24 written (defaults, keywords, several returns, scope, mutable default, key functions; 4 figures, 3 programs).
- 2026-11-10: Chapter 23 written (functions part 1; 4 figures, 4 programs).
- 2026-11-10: Chapter 22 written (tuples, dictionaries, sets, list of records; 5 figures, 4 programs).
- 2026-11-10: Chapters 20 and 21 written (for and range; lists). 5 and 6 figures, 4 and 4 programs.
- 2026-11-10: Chapter 19 written (while, break, continue, max-steps guard, a real control loop; 5 figures, 3 programs).
- 2026-11-10: Chapter 18 written (if, elif, else, indentation, guard, clamp, deadband; 5 figures, 4 programs).
- 2026-11-10: Chapter 17 written (booleans, comparisons, and/or/not, tolerance, fail-safe; 6 figures, 4 programs). On word target.
- 2026-11-10: Chapter 16 written (print sep/end, carriage return, flush, input, input-process-output; 6 figures, 5 programs). On word target.
- 2026-11-10: Chapter 15 written (strings, index and slice, methods, parsing, conversions, f-strings; 6 figures, 4 programs). On word target.
- 2026-11-03: Chapter 14 written (variables, updates, names, state, swap, constants; 6 figures, 3 programs). Long: ~10,000 words.
- 2026-11-03: Chapter 13 written (int/float, operators, // %, order of operations, rounding, units; 5 figures, 3 programs).
- 2026-11-03: Chapter 12 written (shell vs scripts, echo, _, help, python -i, habits; 4 figures, 4 programs). On word target.
- 2026-11-03: Chapter 11 written (programs, order, trace tables, flowcharts, bugs; 5 figures, 5 programs). Part 2 started.
- 2026-11-03: Chapter 10 written (paper design of a tiny cleaner, coverage sims, requirements checker; 8 figures, 3 programs). Part 1 complete.
- 2026-11-03: Chapter 9 written (simulation vs hardware, reality gap, Monte Carlo test, budgets; 6 figures, 3 programs).
- 2026-11-03: Chapter 8 written (setup, terminal, errors, first plot; 6 figures, 5 programs). Ch 6 gain-1 value corrected 0.79 → 0.77.
- 2026-11-03: Chapter 7 written (safety, e-stop, watchdog; 8 figures, 3 programs).
- 2026-11-03: Chapter 1 written. `matplotlib` 3.11 and `numpy` 2.5 installed (Python 3.14).
- 2026-11-03: Every theory chapter gets a 🏭 Real robot applications section (MASTER_PLAN §5.2): at least 5 applications from at least 3 fields, 2 worked in full. Catalogue in `APPLICATIONS.md`. Estimate now about 21,000 pages.
- 2026-11-03: Full tutorials added: Part 30 Drones (53 ch), Part 31 Legged robots (24 ch), Part 32 Humanoids (48 ch), all under the lecture and figure rules. Robots Hero and Buddy added to `ROBOTS.md`. The course now has 33 parts, 749 chapters, about 16,500 pages.
- 2026-11-03: More practice: 24 project chapters added (now 631 chapters, about 13,500 pages), `ROBOTS.md` lists the 26 robots, and every chapter gets a 🔧 hands-on lab (MASTER_PLAN §5.1).
- 2026-11-03: Control split into 3 parts (PID; classical analysis; state-space, LQR, MPC, nonlinear). Mobile robots, frames, arms, IK, dynamics, trajectories and planning expanded. Lecture and figure rules added (MASTER_PLAN §6). The course had 30 parts, 607 chapters.
- 2026-11-03: Parts 24–28 added (real-time and protocols with CAN, ROS 2, four simulators, ROS 2 in practice).
- 2026-11-03: Syllabus (`README.md`), rules (`MASTER_PLAN.md`) and this file were written.
