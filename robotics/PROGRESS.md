# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 1, Chapter 2 — What is a robot? Sense, think, act.**
File: `part-01-welcome-to-robots/ch002-what-is-a-robot.md`, code and `figures.py` in `code/ch002/`, figures in `images/ch002/`.
Promised by Ch 1 "Next chapter": the three things every robot does (sense, think, act); why a washing machine is (almost)
a robot but a hammer is not; play the human robot game (Lab 1.3) again, this time **with** sensors (the robot may say
"I see the cup is 2 steps away" and the programmer may use IF rules). Ch 1 also told the reader that Chapter 2 explains
the definition of a robot fully, and that robots use sensors to correct themselves.

## Chapters done

| Ch | File | Words | Code / figures |
|---|---|---|---|
| 1 | part-01-welcome-to-robots/ch001-how-to-use-this-book.md | 8,570 | code/ch001/first_look.py, robot_trip.py, figures.py → images/ch001/fig01–fig06 |

## Notes for writers

- Ch 1 set these reader expectations: 📖 word list at the back of the notebook; folders `robotics/my-code/chNNN/`;
  5 safety rules (simulation first, a way to stop, start slow, no propellers on the table, respect batteries);
  colour meanings (setpoint black dashed, output blue, error red, control green, robot orange, obstacles grey).
- Ch 1 forward references to keep true: Ch 54 (float rounding, `0.4 * 3 = 1.2000000000000002`), Ch 63 (a ≤ μ·g, load
  sliding on a warehouse robot), Ch 7 and Ch 89 (battery safety).
- Figures: the matplotlib default font has no emoji, so do not put emoji inside figures (only in the Markdown text).
- Ch 1 is 8,570 words, above the 5,500–6,500 target for normal chapters. That is fine for an introduction chapter, but
  keep later Part 1 chapters nearer the target.

## Status

- 2026-11-03: Chapter 1 written. `matplotlib` 3.11 and `numpy` 2.5 installed (Python 3.14).
- 2026-11-03: Every theory chapter gets a 🏭 Real robot applications section (MASTER_PLAN §5.2): at least 5 applications from at least 3 fields, 2 worked in full. Catalogue in `APPLICATIONS.md`. Estimate now about 21,000 pages.
- 2026-11-03: Full tutorials added: Part 30 Drones (53 ch), Part 31 Legged robots (24 ch), Part 32 Humanoids (48 ch), all under the lecture and figure rules. Robots Hero and Buddy added to `ROBOTS.md`. The course now has 33 parts, 749 chapters, about 16,500 pages.
- 2026-11-03: More practice: 24 project chapters added (now 631 chapters, about 13,500 pages), `ROBOTS.md` lists the 26 robots, and every chapter gets a 🔧 hands-on lab (MASTER_PLAN §5.1).
- 2026-11-03: Control split into 3 parts (PID; classical analysis; state-space, LQR, MPC, nonlinear). Mobile robots, frames, arms, IK, dynamics, trajectories and planning expanded. Lecture and figure rules added (MASTER_PLAN §6). The course had 30 parts, 607 chapters.
- 2026-11-03: Parts 24–28 added (real-time and protocols with CAN, ROS 2, four simulators, ROS 2 in practice).
- 2026-11-03: Syllabus (`README.md`), rules (`MASTER_PLAN.md`) and this file were written.
