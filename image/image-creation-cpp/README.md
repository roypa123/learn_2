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
| 15 | [Turning colour into grey: luminance](part-03-mathematics-of-colour/ch15-turning-colour-into-grey-luminance.md) |
| 16 | [Hue, saturation, value (HSV and HSL)](part-03-mathematics-of-colour/ch16-hue-saturation-value-hsv-hsl.md) |
| 17 | [Gamma and sRGB: why 128 is not half bright](part-03-mathematics-of-colour/ch17-gamma-and-srgb.md) |
| 18 | [Transparency: alpha and blending](part-03-mathematics-of-colour/ch18-transparency-alpha-and-blending.md) |

## Part 4 — Drawing Shapes

| Ch | Title |
|---|---|
| 19 | [Pixels and rectangles](part-04-drawing-shapes/ch19-pixels-and-rectangles.md) |
| 20 | [Lines, part 1: the slope and the DDA method](part-04-drawing-shapes/ch20-lines-part-1-slope-and-dda.md) |
| 21 | [Lines, part 2: Bresenham's algorithm](part-04-drawing-shapes/ch21-lines-part-2-bresenham.md) |
| 22 | [Circles: the equation and the midpoint method](part-04-drawing-shapes/ch22-circles-equation-and-midpoint.md) |
| 23 | [Ellipses](part-04-drawing-shapes/ch23-ellipses.md) |
| 24 | [Triangles and edge functions](part-04-drawing-shapes/ch24-triangles-and-edge-functions.md) |
| 25 | [Filling shapes: scanline fill and flood fill](part-04-drawing-shapes/ch25-filling-shapes-scanline-and-flood-fill.md) |
| 26 | [Barycentric coordinates: colouring inside a triangle](part-04-drawing-shapes/ch26-barycentric-coordinates.md) |
| 27 | [Smooth edges, part 1: supersampling](part-04-drawing-shapes/ch27-smooth-edges-part-1-supersampling.md) |
| 28 | [Smooth edges, part 2: Wu's lines and coverage](part-04-drawing-shapes/ch28-smooth-edges-part-2-wu-lines-and-coverage.md) |

## Part 5 — Moving and Bending Shapes

| Ch | Title |
|---|---|
| 29 | [2D vectors](part-05-moving-and-bending-shapes/ch29-2d-vectors.md) |
| 30 | [Angles, radians, sine and cosine](part-05-moving-and-bending-shapes/ch30-angles-radians-sine-and-cosine.md) |
| 31 | [Move, scale, rotate](part-05-moving-and-bending-shapes/ch31-move-scale-rotate.md) |
| 32 | [Matrices and homogeneous coordinates](part-05-moving-and-bending-shapes/ch32-matrices-and-homogeneous-coordinates.md) |
| 33 | [Combining transforms](part-05-moving-and-bending-shapes/ch33-combining-transforms.md) |
| 34 | [Bézier curves](part-05-moving-and-bending-shapes/ch34-bezier-curves.md) |
| 35 | [Resizing images: nearest and bilinear](part-05-moving-and-bending-shapes/ch35-resizing-images-nearest-and-bilinear.md) |

## Part 6 — Real File Formats

| Ch | Title |
|---|---|
| 36 | [The BMP format: headers and padding](part-06-real-file-formats/ch36-the-bmp-format-headers-and-padding.md) |
| 37 | [Writing BMP files](part-06-real-file-formats/ch37-writing-bmp-files.md) |
| 38 | [Reading BMP files](part-06-real-file-formats/ch38-reading-bmp-files.md) |
| 39 | [The TGA format](part-06-real-file-formats/ch39-the-tga-format.md) |
| 40 | [PNG, part 1: chunks and CRC-32](part-06-real-file-formats/ch40-png-part-1-chunks-and-crc-32.md) |
| 41 | [PNG, part 2: zlib, stored blocks and Adler-32](part-06-real-file-formats/ch41-png-part-2-zlib-stored-blocks-and-adler-32.md) |
| 42 | [PNG, part 3: writing a full PNG](part-06-real-file-formats/ch42-png-part-3-writing-a-full-png.md) |
| 43 | [PNG, part 4: filters](part-06-real-file-formats/ch43-png-part-4-filters.md) |
| 44 | [Compression theory: Huffman coding](part-06-real-file-formats/ch44-compression-theory-huffman-coding.md) |
| 45 | [Deflate with LZ77 and fixed Huffman codes](part-06-real-file-formats/ch45-deflate-with-lz77-and-fixed-huffman-codes.md) |
| 46 | [Drawing text with a bitmap font](part-06-real-file-formats/ch46-drawing-text-with-a-bitmap-font.md) |

## Part 7 — Changing Images (Image Processing)

| Ch | Title |
|---|---|
| 47 | [Point operations: brightness, contrast, invert, threshold](part-07-changing-images/ch47-point-operations-brightness-contrast-invert-threshold.md) |
| 48 | [Histograms and histogram equalisation](part-07-changing-images/ch48-histograms-and-histogram-equalisation.md) |
| 49 | [Convolution: the idea and the maths](part-07-changing-images/ch49-convolution-the-idea-and-the-maths.md) |
| 50 | [Blur: box blur and Gaussian blur](part-07-changing-images/ch50-blur-box-blur-and-gaussian-blur.md) |
| 51 | [Sharpen and edge detection (Sobel)](part-07-changing-images/ch51-sharpen-and-edge-detection-sobel.md) |
| 52 | [Dithering: ordered and Floyd–Steinberg](part-07-changing-images/ch52-dithering-ordered-and-floyd-steinberg.md) |
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
