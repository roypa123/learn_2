# Make Images From Scratch With C++

Welcome! 👋

In this book you will learn how to **make pictures with a computer program**.
You write the program yourself in **C++**.
You do **not** use any extra packages or libraries.
You build **everything** yourself: the pixels, the colours, the shapes, and even the image files.

You do **not** need to know anything before you start.
We go **slowly**, **step by step**, with **many small examples**.

---

## Who is this book for?

- People who have **never written code** before.
- People who want to know **how pictures really work inside a computer**.
- People whose **English is not perfect**. We use short and simple sentences.
- Children and adults. If you are 10 years old and can add and multiply, you can follow this book.

---

## What will you be able to make?

By the end of the book you will be able to make, **with your own code**:

- Coloured pictures, colour gradients, and patterns.
- Lines, circles, triangles, stars, and other shapes.
- Smooth edges and see-through colours.
- Spirals, curves, clouds, marble, and wood patterns.
- Fractals like the **Mandelbrot set**.
- Blurred, sharpened, and resized photos.
- Text drawn with your own font.
- **3D pictures**: a spinning cube and a ray-traced scene with shiny balls and shadows.

---

## What do the signs mean?

| Sign | Meaning |
|---|---|
| 📖 **New word** | A new word, explained simply. |
| 💡 **Tip** | A helpful idea. |
| ⚠️ **Careful** | A common mistake. Read this! |
| 🧠 **Remember** | The most important thing in this section. |
| 🏋️ **Practice** | A small task for you to try. |
| 🔢 **Maths** | A maths explanation, worked step by step with real numbers. |

---

## How to use this book

1. Read the chapters **in order**. Every chapter uses ideas from the chapters before it.
2. **Type** every program yourself. Do not copy and paste. Typing helps your brain remember.
3. **Run** every program and look at the result.
4. Do every 🏋️ **Practice** task. The answers are at the end of each chapter.
5. If something is hard, read it again slowly. That is normal. Everyone does this.
6. All complete programs are also in the [code/](code/) folder, so you can check your typing.

---

## Table of Contents

Status: ✅ Ready · ⏳ Planned

### Part 0 — Getting Ready

| # | Chapter | Status |
|---|---|---|
| 01 | [How to Use This Book](part-00-getting-ready/ch01-how-to-use-this-book.md) | ✅ |
| 02 | [Computers, Files, Folders and the Terminal](part-00-getting-ready/ch02-computers-files-terminal.md) | ✅ |
| 03 | [Installing a C++ Compiler](part-00-getting-ready/ch03-installing-a-compiler.md) | ✅ |
| 04 | [Your First C++ Program](part-00-getting-ready/ch04-your-first-program.md) | ✅ |

### Part 1 — C++ From Zero

| # | Chapter | Status |
|---|---|---|
| 05 | [Output, Statements and Comments](part-01-cpp-from-zero/ch05-output-statements-comments.md) | ⏳ |
| 06 | [Variables and Types](part-01-cpp-from-zero/ch06-variables-and-types.md) | ⏳ |
| 07 | [Doing Maths in C++](part-01-cpp-from-zero/ch07-maths-in-cpp.md) | ⏳ |
| 08 | [Making Decisions: if and else](part-01-cpp-from-zero/ch08-if-and-else.md) | ⏳ |
| 09 | [Loops and Nested Loops](part-01-cpp-from-zero/ch09-loops.md) | ⏳ |
| 10 | [Functions](part-01-cpp-from-zero/ch10-functions.md) | ⏳ |
| 11 | [Arrays and std::vector](part-01-cpp-from-zero/ch11-arrays-and-vectors.md) | ⏳ |
| 12 | [Strings](part-01-cpp-from-zero/ch12-strings.md) | ⏳ |
| 13 | [Structs: Grouping Values Together](part-01-cpp-from-zero/ch13-structs.md) | ⏳ |
| 14 | [References and const](part-01-cpp-from-zero/ch14-references-and-const.md) | ⏳ |
| 15 | [Writing and Reading Files](part-01-cpp-from-zero/ch15-files.md) | ⏳ |
| 16 | [Classes and Header Files](part-01-cpp-from-zero/ch16-classes-and-headers.md) | ⏳ |

### Part 2 — What Is an Image?

| # | Chapter | Status |
|---|---|---|
| 17 | [Pixels and the Grid](part-02-what-is-an-image/ch17-pixels-and-the-grid.md) | ⏳ |
| 18 | [Coordinates: Where Is Each Pixel?](part-02-what-is-an-image/ch18-coordinates.md) | ⏳ |
| 19 | [Light and Colour: Red, Green, Blue](part-02-what-is-an-image/ch19-light-and-colour-rgb.md) | ⏳ |
| 20 | [Bits, Bytes and the Numbers 0 to 255](part-02-what-is-an-image/ch20-bits-and-bytes.md) | ⏳ |
| 21 | [Hexadecimal and Colour Codes](part-02-what-is-an-image/ch21-hexadecimal.md) | ⏳ |
| 22 | [How an Image Lives in Memory](part-02-what-is-an-image/ch22-image-in-memory.md) | ⏳ |

### Part 3 — Your First Image Files

| # | Chapter | Status |
|---|---|---|
| 23 | [The PPM Format Explained](part-03-first-image-files/ch23-ppm-format.md) | ⏳ |
| 24 | [Writing Your First Image: A Red Square](part-03-first-image-files/ch24-first-image.md) | ⏳ |
| 25 | [Binary PPM (P6)](part-03-first-image-files/ch25-binary-ppm.md) | ⏳ |
| 26 | [Writing Raw Bytes and Little-Endian](part-03-first-image-files/ch26-raw-bytes-little-endian.md) | ⏳ |
| 27 | [The BMP Format Explained](part-03-first-image-files/ch27-bmp-format.md) | ⏳ |
| 28 | [Writing a BMP File](part-03-first-image-files/ch28-writing-bmp.md) | ⏳ |

### Part 4 — Building an Image Toolkit

| # | Chapter | Status |
|---|---|---|
| 29 | [The Color Struct](part-04-image-toolkit/ch29-color-struct.md) | ⏳ |
| 30 | [The Image Class](part-04-image-toolkit/ch30-image-class.md) | ⏳ |
| 31 | [Saving From the Image Class](part-04-image-toolkit/ch31-saving.md) | ⏳ |
| 32 | [Clamping and Testing Your Code](part-04-image-toolkit/ch32-clamping-and-testing.md) | ⏳ |

### Part 5 — Colour Mathematics

| # | Chapter | Status |
|---|---|---|
| 33 | [Mixing Colours](part-05-colour-maths/ch33-mixing-colours.md) | ⏳ |
| 34 | [Linear Interpolation and Gradients](part-05-colour-maths/ch34-lerp-and-gradients.md) | ⏳ |
| 35 | [2D and Round Gradients, and Distance](part-05-colour-maths/ch35-2d-and-radial-gradients.md) | ⏳ |
| 36 | [Brightness and Grayscale](part-05-colour-maths/ch36-brightness-and-grayscale.md) | ⏳ |
| 37 | [Negative, Threshold and Posterize](part-05-colour-maths/ch37-negative-threshold-posterize.md) | ⏳ |
| 38 | [The HSV Colour Model](part-05-colour-maths/ch38-hsv.md) | ⏳ |
| 39 | [Gamma: Why 128 Is Not Half as Bright](part-05-colour-maths/ch39-gamma.md) | ⏳ |

### Part 6 — Drawing Shapes

| # | Chapter | Status |
|---|---|---|
| 40 | [Points, Straight Lines and Rectangles](part-06-drawing-shapes/ch40-points-and-rectangles.md) | ⏳ |
| 41 | [Slope and the Line Equation](part-06-drawing-shapes/ch41-slope-and-line-equation.md) | ⏳ |
| 42 | [The DDA Line Algorithm](part-06-drawing-shapes/ch42-dda-lines.md) | ⏳ |
| 43 | [Bresenham's Line Algorithm](part-06-drawing-shapes/ch43-bresenham-lines.md) | ⏳ |
| 44 | [Thick Lines](part-06-drawing-shapes/ch44-thick-lines.md) | ⏳ |
| 45 | [Circles](part-06-drawing-shapes/ch45-circles.md) | ⏳ |
| 46 | [The Midpoint Circle Algorithm](part-06-drawing-shapes/ch46-midpoint-circle.md) | ⏳ |
| 47 | [Ellipses](part-06-drawing-shapes/ch47-ellipses.md) | ⏳ |
| 48 | [Triangles and Edge Functions](part-06-drawing-shapes/ch48-triangles.md) | ⏳ |
| 49 | [Polygons and Flood Fill](part-06-drawing-shapes/ch49-polygons-and-flood-fill.md) | ⏳ |

### Part 7 — Smooth Edges and See-Through Colours

| # | Chapter | Status |
|---|---|---|
| 50 | [Why Edges Look Like Stairs](part-07-smooth-edges/ch50-aliasing.md) | ⏳ |
| 51 | [Supersampling](part-07-smooth-edges/ch51-supersampling.md) | ⏳ |
| 52 | [Alpha and Blending](part-07-smooth-edges/ch52-alpha-blending.md) | ⏳ |
| 53 | [Smooth Lines and Soft Circles](part-07-smooth-edges/ch53-smooth-lines-and-circles.md) | ⏳ |

### Part 8 — Geometry and Transforms

| # | Chapter | Status |
|---|---|---|
| 54 | [Vectors](part-08-geometry/ch54-vectors.md) | ⏳ |
| 55 | [Angles, Radians, Sine and Cosine](part-08-geometry/ch55-angles-sin-cos.md) | ⏳ |
| 56 | [Rotating Points](part-08-geometry/ch56-rotation.md) | ⏳ |
| 57 | [Moving, Scaling and Shearing](part-08-geometry/ch57-translate-scale-shear.md) | ⏳ |
| 58 | [Matrices: Joining Transforms Together](part-08-geometry/ch58-matrices.md) | ⏳ |
| 59 | [Drawing With Transforms: Stars and Clocks](part-08-geometry/ch59-stars-and-clocks.md) | ⏳ |

### Part 9 — Curves

| # | Chapter | Status |
|---|---|---|
| 60 | [Parametric Curves and Spirals](part-09-curves/ch60-parametric-curves.md) | ⏳ |
| 61 | [Bezier Curves](part-09-curves/ch61-bezier-curves.md) | ⏳ |
| 62 | [Smooth Paths Through Points](part-09-curves/ch62-splines.md) | ⏳ |

### Part 10 — Patterns, Randomness and Fractals

| # | Chapter | Status |
|---|---|---|
| 63 | [Patterns With Remainders](part-10-patterns-and-fractals/ch63-patterns.md) | ⏳ |
| 64 | [Making Our Own Random Numbers](part-10-patterns-and-fractals/ch64-random-numbers.md) | ⏳ |
| 65 | [Value Noise](part-10-patterns-and-fractals/ch65-value-noise.md) | ⏳ |
| 66 | [Perlin Noise: Clouds, Marble and Wood](part-10-patterns-and-fractals/ch66-perlin-noise.md) | ⏳ |
| 67 | [Complex Numbers](part-10-patterns-and-fractals/ch67-complex-numbers.md) | ⏳ |
| 68 | [The Mandelbrot and Julia Sets](part-10-patterns-and-fractals/ch68-mandelbrot-julia.md) | ⏳ |
| 69 | [Recursive Fractals: Triangles, Trees and Snowflakes](part-10-patterns-and-fractals/ch69-recursive-fractals.md) | ⏳ |

### Part 11 — Changing Existing Images

| # | Chapter | Status |
|---|---|---|
| 70 | [Reading Image Files](part-11-image-processing/ch70-reading-images.md) | ⏳ |
| 71 | [Copy, Crop, Flip and Turn](part-11-image-processing/ch71-crop-flip-turn.md) | ⏳ |
| 72 | [Resizing Images](part-11-image-processing/ch72-resizing.md) | ⏳ |
| 73 | [Convolution and Kernels](part-11-image-processing/ch73-convolution.md) | ⏳ |
| 74 | [Blur](part-11-image-processing/ch74-blur.md) | ⏳ |
| 75 | [Sharpen and Find Edges](part-11-image-processing/ch75-sharpen-and-edges.md) | ⏳ |
| 76 | [Histograms and Contrast](part-11-image-processing/ch76-histograms.md) | ⏳ |
| 77 | [Dithering](part-11-image-processing/ch77-dithering.md) | ⏳ |

### Part 12 — Text

| # | Chapter | Status |
|---|---|---|
| 78 | [Making a Font From Bits](part-12-text/ch78-bitmap-font.md) | ⏳ |
| 79 | [Drawing and Scaling Text](part-12-text/ch79-drawing-text.md) | ⏳ |

### Part 13 — 3D Pictures

| # | Chapter | Status |
|---|---|---|
| 80 | [3D Points and Perspective](part-13-3d/ch80-perspective.md) | ⏳ |
| 81 | [A Wireframe Cube](part-13-3d/ch81-wireframe-cube.md) | ⏳ |
| 82 | [Solid 3D Shapes and the Z-Buffer](part-13-3d/ch82-z-buffer.md) | ⏳ |
| 83 | [Light and Shading](part-13-3d/ch83-shading.md) | ⏳ |
| 84 | [Ray Tracing: Rays and Spheres](part-13-3d/ch84-ray-tracing-spheres.md) | ⏳ |
| 85 | [Ray Tracing: Lights and Shadows](part-13-3d/ch85-ray-tracing-shadows.md) | ⏳ |
| 86 | [Ray Tracing: Mirrors and a Final Scene](part-13-3d/ch86-ray-tracing-reflections.md) | ⏳ |

### Part 14 — Projects

| # | Chapter | Status |
|---|---|---|
| 87 | [Project: A Poster Maker](part-14-projects/ch87-poster-maker.md) | ⏳ |
| 88 | [Project: Animation Frames](part-14-projects/ch88-animation-frames.md) | ⏳ |
| 89 | [Project: Your Own Drawing Library](part-14-projects/ch89-drawing-library.md) | ⏳ |
| 90 | [Where to Go Next](part-14-projects/ch90-where-next.md) | ⏳ |

### Appendices

| | Appendix | Status |
|---|---|---|
| A | [Maths Reference](appendices/a-maths-reference.md) | ⏳ |
| B | [C++ Reference](appendices/b-cpp-reference.md) | ⏳ |
| C | [Glossary: Every New Word](appendices/c-glossary.md) | ⏳ |
| D | [When Things Go Wrong](appendices/d-troubleshooting.md) | ⏳ |
| E | [Colour Table](appendices/e-colour-table.md) | ⏳ |
