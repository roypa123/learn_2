# Image Creation From Scratch in C++

A very beginner-friendly book. We make pictures **with our own code only**.
No image libraries, no extra packages. Just C++ and the standard library.

- You already know basic C++. This book does **not** teach loops, functions or classes.
- You do **not** need to know graphics or advanced maths. We teach all of it, step by step.
- The English is simple. Sentences are short. Every new word is explained.
- About **800 pages** in 11 parts and 82 chapters, plus appendices.

Start with [Chapter 1](part-01-what-is-an-image/ch01-how-to-use-this-book.md).
See [PROGRESS.md](PROGRESS.md) for which chapters are written.

---

## Part 1 — What Is an Image?

| Ch | Title | You will make |
|---|---|---|
| 1 | [How to use this book](part-01-what-is-an-image/ch01-how-to-use-this-book.md) | a folder and a test program |
| 2 | [Light, eyes and pixels](part-01-what-is-an-image/ch02-light-eyes-and-pixels.md) | a picture on paper made of numbers |
| 3 | [Grids and coordinates](part-01-what-is-an-image/ch03-grids-and-coordinates.md) | a program that prints a grid |
| 4 | [Bits, bytes and hexadecimal](part-01-what-is-an-image/ch04-bits-bytes-and-hex.md) | a program that prints bytes |
| 5 | [How colour works: the RGB model](part-01-what-is-an-image/ch05-how-colour-works-rgb.md) | a colour table in the terminal |
| 6 | [An image inside memory](part-01-what-is-an-image/ch06-an-image-inside-memory.md) | a pixel buffer |

## Part 2 — Our First Image Files

| Ch | Title | You will make |
|---|---|---|
| 7 | [Writing files byte by byte](part-02-first-image-files/ch07-writing-files-byte-by-byte.md) | `bytes.bin` |
| 8 | [The PPM text format (P3)](part-02-first-image-files/ch08-the-ppm-text-format-p3.md) | `first.ppm` |
| 9 | [The PPM binary format (P6)](part-02-first-image-files/ch09-the-ppm-binary-format-p6.md) | `first_binary.ppm` |
| 10 | [Grey and black-and-white images (PGM, PBM)](part-02-first-image-files/ch10-grey-and-black-white-pgm-pbm.md) | `grey.pgm`, `checker.pbm`, `disk.pbm` |
| 11 | [Building an `Image` class](part-02-first-image-files/ch11-building-an-image-class.md) | `image.h` |
| 12 | [Reading a PPM file back](part-02-first-image-files/ch12-reading-a-ppm-file.md) | a PPM reader |

## Part 3 — The Mathematics of Colour

| Ch | Title |
|---|---|
| 13 | [Gradients and linear interpolation](part-03-mathematics-of-colour/ch13-gradients-and-linear-interpolation.md) |
| 14 | [Colours as vectors: add, scale, clamp](part-03-mathematics-of-colour/ch14-colours-as-vectors.md) |
| 15 | Turning colour into grey: luminance |
| 16 | Hue, saturation, value (HSV and HSL) |
| 17 | Gamma and sRGB: why 128 is not half bright |
| 18 | Transparency: alpha and blending |

## Part 4 — Drawing Shapes

| Ch | Title |
|---|---|
| 19 | Pixels and rectangles |
| 20 | Lines, part 1: the slope and the DDA method |
| 21 | Lines, part 2: Bresenham's algorithm |
| 22 | Circles: the equation and the midpoint method |
| 23 | Ellipses |
| 24 | Triangles and edge functions |
| 25 | Filling shapes: scanline fill and flood fill |
| 26 | Barycentric coordinates: colouring inside a triangle |
| 27 | Smooth edges, part 1: supersampling |
| 28 | Smooth edges, part 2: Wu's lines and coverage |

## Part 5 — Moving and Bending Shapes

| Ch | Title |
|---|---|
| 29 | 2D vectors |
| 30 | Angles, radians, sine and cosine |
| 31 | Move, scale, rotate |
| 32 | Matrices and homogeneous coordinates |
| 33 | Combining transforms |
| 34 | Bézier curves |
| 35 | Resizing images: nearest and bilinear |

## Part 6 — Real File Formats

| Ch | Title |
|---|---|
| 36 | The BMP format: headers and padding |
| 37 | Writing BMP files |
| 38 | Reading BMP files |
| 39 | The TGA format |
| 40 | PNG, part 1: chunks and CRC-32 |
| 41 | PNG, part 2: zlib, stored blocks and Adler-32 |
| 42 | PNG, part 3: writing a full PNG |
| 43 | PNG, part 4: filters |
| 44 | Compression theory: Huffman coding |
| 45 | Deflate with LZ77 and fixed Huffman codes |
| 46 | Drawing text with a bitmap font |

## Part 7 — Changing Images (Image Processing)

| Ch | Title |
|---|---|
| 47 | Point operations: brightness, contrast, invert, threshold |
| 48 | Histograms and histogram equalisation |
| 49 | Convolution: the idea and the maths |
| 50 | Blur: box blur and Gaussian blur |
| 51 | Sharpen and edge detection (Sobel) |
| 52 | Dithering: ordered and Floyd–Steinberg |
| 53 | Warping and distortion effects |

## Part 8 — Pictures From Maths (Procedural Images)

| Ch | Title |
|---|---|
| 54 | Making our own random numbers |
| 55 | Value noise |
| 56 | Perlin noise |
| 57 | Fractal noise: clouds, marble, wood |
| 58 | Patterns: checkers, stripes, rings |
| 59 | Signed distance functions in 2D |
| 60 | Complex numbers and the Mandelbrot set |
| 61 | Julia sets and smooth colouring |
| 62 | Voronoi diagrams |
| 63 | Turtle graphics and L-systems |

## Part 9 — 3D Pictures by Rasterisation

| Ch | Title |
|---|---|
| 64 | 3D vectors: dot product and cross product |
| 65 | The camera and perspective projection |
| 66 | Wireframe drawing of a cube |
| 67 | Filled triangles in 3D and the depth buffer |
| 68 | Light, part 1: Lambert shading |
| 69 | Light, part 2: Phong highlights |
| 70 | Texture mapping |

## Part 10 — Ray Tracing

| Ch | Title |
|---|---|
| 71 | Rays and the ray tracing idea |
| 72 | Hitting a sphere: solving a quadratic |
| 73 | Normals and shading in a ray tracer |
| 74 | Shadows |
| 75 | Mirrors: reflection |
| 76 | Glass: refraction and Snell's law |
| 77 | Planes and triangles |
| 78 | Many samples per pixel |
| 79 | A first path tracer |

## Part 11 — Moving Pictures and Final Project

| Ch | Title |
|---|---|
| 80 | Animation: a sequence of frames |
| 81 | The GIF format and LZW compression |
| 82 | Final project: a small picture-making program |

## Appendices

| | Title |
|---|---|
| A | Maths reference sheet |
| B | File format reference sheet |
| C | All code, in one place |
| D | Glossary of all new words |
| E | How to view your images on Windows, macOS and Linux |
