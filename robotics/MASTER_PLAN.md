# Master Plan — Robotics From Scratch

This file holds the **rules** for writing this course.
Read it before writing any new chapter. Every chapter must follow it.

---

## 1. The request (from `t.md`)

| # | Request | What it means for this course |
|---|---|---|
| 1 | Robotics from scratch | We assume no knowledge of robots, electronics, programming or higher maths. |
| 4 | Theories and mathematics, descriptively | Every topic starts with the idea, then the maths step by step with real numbers, then the code. |
| 5 | Very beginner friendly | School maths up to age 12 is enough. Everything above that is taught (Parts 3, 9, 10, 11). |
| 6 | Very descriptive, about 10,000 pages | 1 page ≈ 300 words. The core robotics and control parts were made bigger on request ("don't compromise anything"), so the course is now about 13,000 pages (see §2). |
| 7 | Small examples | Every section has at least one tiny example (one wheel, one sensor reading, a 2×2 matrix). |
| 8 | Everything in order | A chapter only uses ideas from earlier chapters. No forward references except "we will see this in Chapter N". |
| 9 | Every bit of code explained | Every code block is followed by a line-by-line table. No line is skipped. |
| 10 | Simple English, a 10-year-old can follow | Short sentences. One idea per sentence. No idioms. Many readers are not fluent in English. |
| 11 | Put it in this folder | Everything lives in `robotics/`. |
| 12 | Syllabus first | The syllabus is `README.md`. |
| 13 | Beginner to advanced | Parts 1–11 are beginner, Parts 12–20 are middle, Parts 21–30 are advanced. |
| 14 | Detailed lectures with many images for core robotics and control | Parts 12–20 and 23 follow the lecture rules in §6: at least 15 real figures per chapter, every derivation in full. |

---

## 2. Page budget

- 1 page ≈ 300 words (code and tables count).
- **Core robotics and control chapters (Parts 12–20 and 23, 227 chapters): 7,000–8,500 words** (about 25–28 pages), plus figures.
- **All other chapters (380 chapters): 5,500–6,500 words** (about 18–22 pages).
- Total ≈ 1,750,000 + 2,250,000 ≈ 4,000,000 words ≈ **13,000 pages**, plus the figures.
- Chapters are listed in `README.md`. Do not change the order without updating README and PROGRESS.

---

## 3. Tools and languages

| Tool | Where | Notes |
|---|---|---|
| Python 3 | From Part 2 | The main language. Taught from zero. |
| `matplotlib` | From Ch 33 | Plots and simple robot animations. Also draws every figure in the course (§6). |
| NumPy | From Ch 34 | First we write the maths by hand. Then we show the NumPy way. |
| Arduino C++ | Part 6 onwards | Taught from zero in Ch 93–94. Every sketch also runs in the free **Wokwi** simulator. |
| OpenCV | Part 24 | Only after we have written the basic filters by hand. |
| PyTorch | Ch 495 onwards | Only after the network from scratch (Ch 492). |
| FreeRTOS on ESP32 | Part 26 | Real-time tasks. CAN uses an MCP2515 board or the ESP32's built-in CAN (TWAI). |
| Linux, Docker, ROS 2 | Parts 27, 29 | Ubuntu (or WSL on Windows). Python (`rclpy`) first, then C++ (`rclcpp`). |
| Gazebo, Webots, MuJoCo | Part 28 | Free, run on most computers. |
| Isaac Sim, Isaac Lab | Part 28 | Needs an NVIDIA RTX graphics card. Readers without one read along; every result is shown. |

**Rule: build it by hand first, then use the library.** A reader must understand what a library does before using it.

---

## 4. Writing rules (simple English)

| Rule | Good example |
|---|---|
| Short sentences. One idea each. | "A motor turns. A sensor measures." |
| Explain a new word the first time. | 📖 **New word: actuator** — the part of a robot that moves something. |
| No idioms, no slang, no jokes that need culture. | Not "a piece of cake". Say "easy". |
| Use "we" and "you". | "Now we make the wheel turn." |
| One name for one thing, always. | Always "setpoint". Never "target" in one place and "goal" in another. |
| Maths step by step with real numbers. | "Wheel radius r = 3 cm. One turn = 2 × 3.14 × 3 = 18.84 cm." |
| Draw pictures with text (ASCII) where they help. | Robots from above, arms, number lines, grids, arrows. |
| Use everyday examples first. | A bicycle for gears. Riding a bike for balance. Closing your eyes and walking for odometry. |
| Remind the reader of earlier chapters. | "Remember from Chapter 49: sin = opposite ÷ hypotenuse." |
| Translate every formula into words. | "F = m × a" → "Force equals mass times acceleration." |

### Signs used in every chapter

| Sign | Meaning |
|---|---|
| 📖 **New word** | A new word, explained simply. |
| 🔢 **Maths** | A maths idea, worked step by step. |
| 🤖 **Robot link** | Where this idea is used in a real robot. |
| 💡 **Tip** | A helpful idea. |
| ⚠️ **Careful** | A common mistake, or a safety warning. |
| 🧠 **Remember** | The most important idea of the section. |
| 🏋️ **Practice** | A small task. Answers are at the end of the chapter. |
| 🖼️ **Figure** | A picture, followed by "How to read this picture". |
| 🧪 **Experiment** | Change one number, run again, and see what happens in the plot. |

---

## 5. Chapter template (every chapter, in this order)

```
# Chapter N — Title

> **Part X · Chapter N of 607**
> **You need:** Chapters … · **You will make:** <program / circuit / robot>

## What you will learn            (3–6 bullet points)
## New words in this chapter      (table: word | simple meaning)
## N.1 … N.k  Theory sections     (everyday example → idea → ASCII picture → 🔢 maths with numbers → small example)
## Code                           (full program, then a line-by-line table)
## Small examples                 (at least 5, each tiny, each explained)
## Common mistakes                (⚠️ list)
## Practice                       (🏋️ 6–10 tasks, easy → hard)
## Answers                        (full answers, explained step by step)
## Experiments                    (core and control parts only: 🧪 "what if?" runs, see §6)
## Summary                        (🧠 5–8 short points)
## Next chapter                   (one or two sentences)
```

### Code explanation format

After every code block, give a table that covers **every line**:

| Line | Code | What it does (simple English) |
|---|---|---|
| 1 | `import math` | Gives us the maths tools, such as `math.sin`. |

Then show the **exact output** when the program runs, and explain it.

---

## 6. Detailed lectures and figures (core robotics and control)

These rules apply to **Parts 12–20 and 23**: control (12–14), mobile robots, frames, forward and inverse kinematics, dynamics, trajectories, and path planning.
Do not cut anything in these parts. Each one is taught like a full university lecture, but in simple English.

### 6.1 Lecture rules

| Rule | What it means |
|---|---|
| Every derivation in full | Never write "it can be shown" or "after some algebra". Show every line, and say in words what changed from the line before. |
| Picture first, formula second | Every new formula comes after a figure that shows what it means. |
| Three views of every idea | 1) an everyday example, 2) a picture, 3) the maths with real numbers. |
| Worked numbers | At least 2 complete worked examples per main formula, every number shown. |
| Code makes the figure | The program in the chapter also produces the result plot. The reader sees the theory and the plot agree. |
| Experiments | At least 4 🧪 experiments per chapter: change one gain, length, mass or step size, show the new plot, explain why it changed. |
| Compare methods | When a chapter has two methods (P vs PI, DH vs PoE, A* vs Dijkstra), add a figure with both side by side. |
| Look back and ahead | End each lecture with a figure that shows where this idea sits in the whole robot (sense → think → act). |

### 6.2 Figure rules

- **How many:** at least **15 figures** in each core and control chapter. Other chapters: at least **4**.
- **Real images**, not only ASCII. Each figure is drawn by a Python script `code/chNNN/figures.py` with `matplotlib`, so it can be re-made and checked.
  Saved as `images/chNNN/figNN-short-name.png` (150 dpi) or `.svg` for line drawings.
- **In the chapter:**
  ```
  ![Figure 205.3 — P control with three gains](../images/ch205/fig03-p-three-gains.png)

  *Figure 205.3 — P control with three different gains Kp.*

  **How to read this picture:** 2–5 short sentences. What is on each axis. What each line or colour means. What to notice.
  ```
- **Kinds of figures to use:**

| Topic | Figures |
|---|---|
| Control | Block diagrams. Step responses with rise time, overshoot and settling time marked. The same system with 3 gains on one plot. Error, P, I and D terms each plotted over time. Pole–zero maps, root loci, Bode and Nyquist plots. Phase portraits. Cart-pole snapshot strips. MPC prediction windows. |
| Mobile robots | Top views with the robot frame, wheel speeds and ICR (turning centre). Path plots: planned vs driven. Odometry drift growing over time. Line and wall following, frame by frame. |
| Frames | Two or three frames drawn with arrows. Before/after rotation. Chains of transforms as arrows from frame to frame. |
| Arms | The arm drawn with every length and angle labelled. Workspace shading. Elbow-up and elbow-down answers. DH frames on each joint. Jacobian velocity arrows. Manipulability ellipses. Singular poses. |
| Dynamics | Free-body diagrams with every force and torque. Energy over time. Torque plots for each joint. Controlled vs uncontrolled motion. |
| Trajectories | Position, velocity, acceleration and jerk plots stacked under each other. Paths in 2D and 3D. |
| Planning | Search frame by frame (open/closed cells coloured). Trees growing (RRT). Final paths compared. C-space pictures next to the real workspace. |

- **Style:** large labels (12 pt or more). Colour-blind safe colours, and lines also differ by style (solid, dashed, dotted). The same thing always has the same colour across the whole course: **setpoint = black dashed, output = blue, error = red, control signal = green, robot = orange, obstacles = grey.**
- **Sequences:** for anything that moves, show a strip of 4–8 snapshots (time 0, 1, 2 …) instead of one picture.
- ASCII pictures are still used for small quick sketches inside the text.

---

## 7. File layout

```
robotics/
  t.md                 the original request
  README.md            syllabus (all 607 chapters)
  MASTER_PLAN.md       this file
  PROGRESS.md          what is done, what is next
  part-01-welcome-to-robots/
    ch001-how-to-use-this-book.md
  part-02-python-from-zero/
  ...
  code/
    ch013/             code for Chapter 13 (programs and figures.py)
    common/            helper files that later chapters reuse
  images/
    ch205/             figures for Chapter 205
```

Part folder names: `part-NN-short-name`. Chapter files: `chNNN-short-name.md` (three digits).

---

## 8. Checking

- Run every Python program before saving it, and paste the real output.
- Check every worked number with a quick Python calculation.
- Arduino sketches: check them in Wokwi if possible. Otherwise check them carefully by hand and say so in PROGRESS.
- Run `figures.py` and look at every figure before saving the chapter. Check that the numbers in the text match the plot.
- After writing a chapter, update `PROGRESS.md` (word count, code files, and the promises made in "Next chapter").
