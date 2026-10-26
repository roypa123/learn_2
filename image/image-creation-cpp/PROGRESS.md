# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 8, Chapter 55 — Value noise.**
File: `part-08-pictures-from-maths/ch55-value-noise.md`, code in `code/ch55/` and a new `common/noise.h` (include
`random.h`). Programs that save PNG also include `deflate.h`.
It should cover (promised by Ch 54 "Next chapter"): white noise is too wild (neighbours unrelated); random values only
at grid corners from `hashDouble(ix, iy, seed)`; the cell of a point (floor), the fraction inside the cell; bilinear
blend of the 4 corners (Ch 13 lerp, Ch 35 bilinear) → visible creases/diamonds; the "gentler curve" smoothstep
3t² − 2t³ (and maybe 6t⁵ − 15t⁴ + 10t³), with worked values and why the slope is 0 at 0 and 1; scale (cell size /
frequency); 1D value noise first as a graph (drawCurve-style), then 2D; worked numbers at a few points; noise → grey
picture and → colour with a gradient map (lerpColour); seeds. Ch 56 Perlin (gradients at corners), Ch 57 fractal noise.

## Chapters done

| Ch | File | Words | Code |
|---|---|---|---|
| 1 | part-01-what-is-an-image/ch01-how-to-use-this-book.md | 3,739 | code/ch01/check.cpp |
| 2 | part-01-what-is-an-image/ch02-light-eyes-and-pixels.md | 3,771 | code/ch02/number_picture.cpp |
| 3 | part-01-what-is-an-image/ch03-grids-and-coordinates.md | 4,809 | code/ch03/grid.cpp |
| 4 | part-01-what-is-an-image/ch04-bits-bytes-and-hex.md | 5,094 | code/ch04/bytes.cpp |
| 5 | part-01-what-is-an-image/ch05-how-colour-works-rgb.md | 4,606 | code/ch05/colours.cpp |
| 6 | part-01-what-is-an-image/ch06-an-image-inside-memory.md | 4,920 | code/ch06/buffer.cpp |
| 7 | part-02-first-image-files/ch07-writing-files-byte-by-byte.md | 5,123 | code/ch07/bytes_file.cpp |
| 8 | part-02-first-image-files/ch08-the-ppm-text-format-p3.md | 5,345 | code/ch08/ppm_p3.cpp |
| 9 | part-02-first-image-files/ch09-the-ppm-binary-format-p6.md | 4,758 | code/ch09/ppm_p6.cpp |
| 10 | part-02-first-image-files/ch10-grey-and-black-white-pgm-pbm.md | 5,399 | code/ch10/pgm_pbm.cpp |
| 11 | part-02-first-image-files/ch11-building-an-image-class.md | 5,029 | code/common/image.h (lines 1–89), code/ch11/use_image.cpp |
| 12 | part-02-first-image-files/ch12-reading-a-ppm-file.md | 6,544 | code/common/image.h (lines 91–213), code/ch12/read_ppm.cpp |
| 13 | part-03-mathematics-of-colour/ch13-gradients-and-linear-interpolation.md | 6,571 | code/common/image.h (lines 215–232), code/ch13/gradients.cpp |
| 14 | part-03-mathematics-of-colour/ch14-colours-as-vectors.md | 6,270 | code/common/colourf.h (new, 55 lines), code/ch14/colour_maths.cpp |
| 15 | part-03-mathematics-of-colour/ch15-turning-colour-into-grey-luminance.md | 5,186 | code/common/grey.h (new, 51 lines), code/ch15/to_grey.cpp |
| 16 | part-03-mathematics-of-colour/ch16-hue-saturation-value-hsv-hsl.md | 7,210 | code/common/hsv.h (new, 106 lines), code/ch16/hsv_hsl.cpp |
| 17 | part-03-mathematics-of-colour/ch17-gamma-and-srgb.md | 5,827 | code/common/srgb.h (new, 57 lines), code/ch17/gamma.cpp |
| 18 | part-03-mathematics-of-colour/ch18-transparency-alpha-and-blending.md | 5,802 | code/common/alpha.h (new, 60 lines), code/ch18/alpha.cpp |
| 19 | part-04-drawing-shapes/ch19-pixels-and-rectangles.md | 6,247 | code/common/draw.h (new, 80 lines), code/ch19/ |
| 20 | part-04-drawing-shapes/ch20-lines-part-1-slope-and-dda.md | 5,844 | code/common/lines.h (new, lines 1–41), code/ch20/ |
| 21 | part-04-drawing-shapes/ch21-lines-part-2-bresenham.md | 7,227 | code/common/lines.h (lines 43–130), code/ch21/ |
| 22 | part-04-drawing-shapes/ch22-circles-equation-and-midpoint.md | 6,443 | code/common/circles.h (new, 68 lines), code/ch22/circles.cpp |
| 23 | part-04-drawing-shapes/ch23-ellipses.md | 12,305 | code/common/ellipses.h (new, 79 lines), code/ch23/ellipses.cpp |
| 24 | part-04-drawing-shapes/ch24-triangles-and-edge-functions.md | 10,135 | code/common/triangles.h (new, 80 lines), code/ch24/triangles.cpp |
| 25 | part-04-drawing-shapes/ch25-filling-shapes-scanline-and-flood-fill.md | 9,791 | code/common/fill.h (new, 190 lines), code/ch25/fill.cpp |
| 26 | part-04-drawing-shapes/ch26-barycentric-coordinates.md | 7,564 | code/common/barycentric.h (new, 77 lines), code/ch26/barycentric.cpp |
| 27 | part-04-drawing-shapes/ch27-smooth-edges-part-1-supersampling.md | 9,124 | code/common/antialias.h (new, 204 lines), code/ch27/antialias.cpp |
| 28 | part-04-drawing-shapes/ch28-smooth-edges-part-2-wu-lines-and-coverage.md | 7,299 | code/common/wu.h (new, 106 lines), code/ch28/wu.cpp |
| 29 | part-05-moving-and-bending-shapes/ch29-2d-vectors.md | 7,916 | code/common/vec2.h (new, 149 lines), code/ch29/vectors.cpp |
| 30 | part-05-moving-and-bending-shapes/ch30-angles-radians-sine-and-cosine.md | 6,774 | code/common/angles.h (new, 66 lines), code/ch30/angles.cpp |
| 31 | part-05-moving-and-bending-shapes/ch31-move-scale-rotate.md | 9,863 | code/common/transform.h (new, 112 lines), code/ch31/transform.cpp |
| 32 | part-05-moving-and-bending-shapes/ch32-matrices-and-homogeneous-coordinates.md | 8,011 | code/common/matrix.h (new, 83 lines), code/ch32/matrices.cpp |
| 33 | part-05-moving-and-bending-shapes/ch33-combining-transforms.md | 7,629 | code/common/combine.h (new, 87 lines), code/ch33/combine.cpp |
| 34 | part-05-moving-and-bending-shapes/ch34-bezier-curves.md | 8,016 | code/common/bezier.h (new, 99 lines), code/ch34/bezier.cpp |
| 35 | part-05-moving-and-bending-shapes/ch35-resizing-images-nearest-and-bilinear.md | 7,057 | code/common/resize.h (new, 115 lines), code/ch35/resize.cpp |
| 36 | part-06-real-file-formats/ch36-the-bmp-format-headers-and-padding.md | 6,660 | code/common/bytes.h (new, 57 lines), code/ch36/bmp_layout.cpp |
| 37 | part-06-real-file-formats/ch37-writing-bmp-files.md | 5,616 | code/common/bmp.h (new, 81 lines), code/ch37/write_bmp.cpp |
| 38 | part-06-real-file-formats/ch38-reading-bmp-files.md | 6,059 | code/common/bmpload.h (new, 82 lines), code/ch38/read_bmp.cpp |
| 39 | part-06-real-file-formats/ch39-the-tga-format.md | 7,724 | code/common/tga.h (new, 202 lines), code/ch39/tga.cpp |
| 40 | part-06-real-file-formats/ch40-png-part-1-chunks-and-crc-32.md | 6,155 | code/common/png.h (new, 135 lines), code/ch40/png_chunks.cpp |
| 41 | part-06-real-file-formats/ch41-png-part-2-zlib-stored-blocks-and-adler-32.md | 5,874 | code/common/zlib.h (new, 93 lines), code/ch41/zlib_store.cpp |
| 42 | part-06-real-file-formats/ch42-png-part-3-writing-a-full-png.md | 5,898 | code/common/pngfile.h (new, 149 lines), code/ch42/write_png.cpp |
| 43 | part-06-real-file-formats/ch43-png-part-4-filters.md | 10,487 | code/common/pngfilter.h (new, 269 lines), code/ch43/filters.cpp |
| 44 | part-06-real-file-formats/ch44-compression-theory-huffman-coding.md | 9,567 | code/common/huffman.h (new, 280 lines), code/ch44/huffman.cpp |
| 45 | part-06-real-file-formats/ch45-deflate-with-lz77-and-fixed-huffman-codes.md | 11,658 | code/common/deflate.h (new, 408 lines), code/ch45/deflate.cpp |
| 46 | part-06-real-file-formats/ch46-drawing-text-with-a-bitmap-font.md | 8,275 | code/common/font.h (new, 239 lines), code/ch46/text.cpp |
| 47 | part-07-changing-images/ch47-point-operations-brightness-contrast-invert-threshold.md | 5,924 | code/common/pointops.h (new, 139 lines), code/ch47/pointops.cpp |
| 48 | part-07-changing-images/ch48-histograms-and-histogram-equalisation.md | 6,106 | code/common/histogram.h (new, 122 lines), code/ch48/histogram.cpp |
| 49 | part-07-changing-images/ch49-convolution-the-idea-and-the-maths.md | 6,616 | code/common/convolve.h (new, 96 lines), code/ch49/convolve.cpp |
| 50 | part-07-changing-images/ch50-blur-box-blur-and-gaussian-blur.md | 6,726 | code/common/blur.h (new, 151 lines), code/ch50/blur.cpp |
| 51 | part-07-changing-images/ch51-sharpen-and-edge-detection-sobel.md | 8,599 | code/common/edges.h (new, 139 lines), code/ch51/edges.cpp |
| 52 | part-07-changing-images/ch52-dithering-ordered-and-floyd-steinberg.md | 7,461 | code/common/dither.h (new, 129 lines), code/ch52/dither.cpp |
| 53 | part-07-changing-images/ch53-warping-and-distortion-effects.md | 5,689 | code/common/warp.h (new, 107 lines), code/ch53/warp.cpp |
| 54 | part-08-pictures-from-maths/ch54-making-our-own-random-numbers.md | 6,608 | code/common/random.h (new, 69 lines), code/ch54/random.cpp |

**Parts 1–7 complete**, Part 8 in progress (Ch 54 done). Total so far: ~371,000 words (`wc -w`, code included).

## The shared library: `code/common/image.h`

It grows over the book. Each chapter that adds to it says where to add the code, and gives the **real line
numbers** in the finished file. Before you add anything, run `cat -n code/common/image.h` so the new line
numbers are right. Free functions must be `inline`. Current contents:

- lines 1–89 (Ch 11): include guard, `struct Colour` (defaults 0), `namespace colours` (8 corner colours),
  `class Image` (width, height, isInside, setPixel, getPixel [black outside], clear, data, savePPM [P6], private index)
- lines 91–213 (Ch 12): `readFileBytes`, `isSpace`, `skipSpaceAndComments`, `readNumber`, `scaleToByte`, `loadPPM` (P3 + P6, maxval ≤ 255)
- lines 215–232 (Ch 13): `lerp`, `lerpByte` (clamps, rounds), `lerpColour`
- line 234: `#endif`

`code/common/colourf.h` (Ch 14, includes `image.h`): `struct ColourF` (doubles 0..1), operators `+ - * /`
(scalar both sides, and colour×colour), `toColourF`, `toByte` (std::clamp + round), `toColour`, `length`.
**Rule from Ch 14 on:** each new topic gets its own header that includes the previous ones, so existing
line numbers never move. Append to the end of a header only when the topic really belongs there.

`code/common/grey.h` (Ch 15, includes `colourf.h`): `luma` (Rec. 709 weights on gamma-encoded values —
deliberately called *luma*, true luminance comes in Ch 17), `plainAverage`, `greyByte`, `toGrey`,
`desaturate` (lerp toward own grey), `saveGreyPGM` (P5).

`code/common/hsv.h` (Ch 16, includes `colourf.h`): `struct HSV {h,s,v}`, `struct HSL {h,s,l}` (h in
degrees 0–360), `wrapHue`, `hueOf`, `rgbToHsv`, `rgbToHsl`, `hueToRgb`, `hsvToRgb`, `hslToRgb`, `shiftHue`.

`code/common/srgb.h` (Ch 17, includes `colourf.h`): `srgbToLinear`, `linearToSrgb` (clamps), `makeLinearTable`,
`linearTable` (static 256-entry table), `toLinear(Colour)`, `fromLinear(ColourF)`, `lerpLinear`, `luminance` (true, linear).

`code/common/alpha.h` (Ch 18, includes `srgb.h`): `struct ColourFA {r,g,b,a}`, `withAlpha`, `overStraight`,
`premultiply`, `unpremultiply`, `overPremultiplied`, `blendOver(dst, src, alpha)` (linear light, dst first!),
`blendPixel(Image&, x, y, src, alpha)`.

`code/common/draw.h` (Ch 19, includes `alpha.h`): `struct Rect {x0,y0,x1,y1}` (half-open), `fromCorners`,
`makeRect`, `rectWidth`, `rectHeight`, `isEmpty`, `contains`, `intersect`, `clipToImage`, `fillRect`,
`fillRectAlpha`, `strokeRect` (inside, corners once; overlaps if 2t > side — Ch 19 P7 fix).

`code/common/lines.h` (Ch 20, includes `draw.h`): `roundToInt` (floor(v+0.5)), `drawLineNaive`, `drawLineDDA`
(both endpoints included). Ch 21 appended (lines 43–130, `#endif` on 132): `#include <vector>`, `struct Point`,
`drawLineShallow` (teaching version, one octant), `drawLine(img, x0,y0,x1,y1, c, includeLast = true)` (general
Bresenham — the default line function from now on), `linePoints`, `drawThickLine` (square brush),
`drawDashedLine`.

`code/common/circles.h` (Ch 22, includes `lines.h`): `drawCircleNaive`, `plotEight`, `drawCircle` (midpoint,
integer centre, width 2r+1), `fillCircle(img, cx, cy, r, c, alpha = 1.0)` (pixel-centre test, clipped box).

`code/common/ellipses.h` (Ch 23, includes `circles.h`): `fillEllipse(img, cx, cy, a, b, c, alpha = 1.0)` (integer-form
test b²dx² + a²dy² ≤ a²b², clipped box), `plotFour`, `drawEllipse(img, cx, cy, a, b, c)` (midpoint, two regions,
×4 trick so all values are whole numbers, `long long`, extra loop that finishes row y = 0 for very flat ellipses;
identical pixels to `drawCircle` when a = b — tested r = 0…79).

`code/common/triangles.h` (Ch 24, includes `ellipses.h`): `struct PointF {x, y}` (doubles), `edgeFunction(a, b, p)`
(> 0 = right of a→b on screen, y down), `triangleArea`, `isTopLeft(from, to)` (ey == 0 && ex > 0, or ey < 0),
`edgeCovers`, `fillTriangle(img, a, b, c, col, alpha = 1.0)` (swaps b/c if counter-clockwise, w0 = E(b,c,p),
w1 = E(c,a,p), w2 = E(a,b,p), top-left rule), `drawTriangle(img, Point, Point, Point, col)` (three drawLine,
includeLast = false), `fillConvexPolygon(img, vector<PointF>, col, alpha = 1.0)` (fan from point 0).

`code/common/fill.h` (Ch 25, includes `triangles.h`): `enum class FillRule {EvenOdd, NonZero}`, `struct Crossing {x,
direction}`, `crossingIsLeft`, `findCrossings` (half-open top ≤ sy < bottom, skips horizontal edges, +1 = edge goes
down), `fillPaths(img, vector<vector<PointF>>, col, rule = NonZero, alpha = 1.0)` (holes = extra paths; with non-zero
the hole must be reversed), `fillPolygon` (one path), `struct Mask {width, height, vector<uint8_t> on}`, `makeMask`,
`maskGet` (false outside), `maskSet`, `maskCount`, `sameColour`, `floodMask(img, x, y, eightWay = false)` (explicit
std::vector<Point> stack), `paintMask(img, mask, c, alpha = 1.0)`, `floodFill(img, x, y, c, eightWay = false, alpha = 1.0)`
(returns count). Scanline fill == fillTriangle for triangles (tested 2000 random half-integer triangles).

`code/common/barycentric.h` (Ch 26, includes `fill.h`): `struct Barycentric {l0, l1, l2}`, `barycentric(a, b, c, p)`
(w / signed area; flat triangle → −1, −1, −1), `fromBarycentric`, `allPositive` (≥ 0), `mixThree(ColourF×3, w)`,
`fillTriangleColours(img, a, b, c, ca, cb, cc, linearLight = true)` (swaps colours with corners; top-left rule).

`code/common/antialias.h` (Ch 27, includes `barycentric.h`): `sampleOffset(i, n)` = (i + 0.5)/n, `paintCoverage(img, x, y,
c, coverage)` (≤ 0 skip, ≥ 1 set, else blendPixel), `circleCoverage`, `fillCircleAA(img, cx, cy, r, c, n = 4)` (half-
diagonal 0.70711 shortcut), `ellipseCoverage`, `fillEllipseAA`, `fillPathsAA(img, paths, col, rule = NonZero, n = 4)`
(n sub-rows, per-pixel sample counts — one call per shape avoids conflation seams), `fillPolygonAA`,
`fillThickLineAA(img, a, b, thickness, col, n = 4)` (band from (−dy, dx)/len × t/2), `shrinkAverage(big, factor)`
(linear-light average; identical to fillCircleAA for a 4× circle — tested).

`code/common/wu.h` (Ch 28, includes `antialias.h`): `struct CoveragePixel {x, y, coverage}`, `wuLinePixels(a, b)`
(steep swap, left-to-right, half-open columns ceil(x0 − 0.5)…ceil(x1 − 0.5), t = yc − 0.5, split 1 − f / f),
`drawLineWu`, `drawPolylineWu`, `plotSplitRow`, `plotSplitColumn`, `drawCircleWu(img, cx, cy, r, c)` (two loops,
limit r/√2; 0 or 4 pixels near 45° get paint twice — noted in the chapter).

`code/common/vec2.h` (Ch 29, includes `wu.h`): `using Vec2 = PointF;` (one type for points and vectors — PointF was
NOT changed), operators `+ - (unary -) * (both sides) /`, `dot`, `cross` (= edgeFunction(a,b,p) with b−a, p−a),
`length(Vec2)` (overloads Ch 14's length(ColourF)), `distance`, `normalize` (zero-safe), `perpendicular` = (−y, x)
(clockwise quarter turn on screen), `project`, `reflect(v, normal)` (normalises the normal), `distanceToLine`,
`closestPointOnSegment` (clamped t), `distanceToSegment`, `capsuleCoverage`, `fillCapsuleAA(img, a, b, radius, c,
n = 4)` (round-ended smooth lines), `drawArrowAA(img, from, to, thickness, c)` (shaft + head in ONE fillPathsAA call).

`code/common/angles.h` (Ch 30, includes `vec2.h`): `const double kPi`, `degreesToRadians`, `radiansToDegrees`,
`fromAngle` (cos, sin), `pointOnCircle(centre, r, rad)`, `pointOnEllipse(centre, a, b, rad)` (parametric),
`angleOf` (atan2(y, x)), `angleBetween` (acos of clamped dot/(|a||b|)), `regularPolygon(centre, r, sides, start)`,
`starPoints(centre, outer, inner, tips, start)` (2n points, no crossings). Screen angles turn CLOCKWISE; −90° = up.

`code/common/transform.h` (Ch 31, includes `angles.h`): `translate(p, offset)`, `scaleAbout(p, centre, sx, sy)` (−1 =
mirror), `rotate(p, radians)` (about the origin; positive = clockwise on screen), `rotateAbout(p, centre, radians)`,
`translatePoints`, `scalePoints`, `rotatePoints` (return NEW lists), `tiltedEllipsePoints(centre, a, b, radians,
count)`, `insideTiltedEllipse(p, centre, a, b, radians)` (turn back by −θ, level test), `tiltedEllipseCoverage`,
`tiltedEllipseBox` (half sizes √(a²c² + b²s²), √(a²s² + b²c²), derived with a dot product), `fillTiltedEllipseAA(img,
centre, a, b, radians, c, n = 4)`.

`code/common/matrix.h` (Ch 32, includes `transform.h`): `struct Mat3 { double m[3][3] }` (m[row][col], defaults to the
identity), `identity()`, `translation(tx, ty)`, `scaling(sx, sy)`, `rotation(radians)`, `skew(kx, ky)`, `operator*`
(A × B: B acts first — read right to left), `applyToPoint` (w = 1, skips the third row), `applyToDirection` (w = 0),
`applyToPoints`, `determinant` (ad − bc = area factor; < 0 mirror). NOTE: chapter programs define their own small
`closed(points)` helper (Ch 31, Ch 32) — it is not in a header.

`code/common/combine.h` (Ch 33, includes `matrix.h`): `rotationAbout(c, radians)`, `scalingAbout(c, sx, sy)` (T(c)·X·T(−c)),
`bool inverse(const Mat3& t, Mat3& result)` (|det| < 1e-12 → false, result untouched; (1/det)[d −b; −c a], move = −A⁻¹t),
`transformedBox(t, width, height)` (4 picture CORNERS (0,0)…(w,h), floor/ceil), `drawImageForward` (the wrong way —
holes), `drawImageTransformed(dest, source, t)` (inverse mapping, nearest neighbour, only inside the box and inside the
source; other dest pixels untouched). Ch 33 program has `clean()` for printing −0 as 0.

`code/common/bezier.h` (Ch 34, includes `combine.h`): `lerpPoint`, `quadraticPoint`, `cubicPoint` (de Casteljau),
`cubicPointFormula` (u³, 3u²t, 3ut², t³), `cubicTangent`, `segmentsFor(controlLength)` = max(1, ceil(len/4)),
`appendQuadratic(path, …)` / `appendCubic(path, …)` (add the start point only if the path is empty), `drawCubic`,
`smoothPath(points)` (Catmull–Rom, handles ± (next − prev)/6, ends use the end stop), `bezierCircle(centre, r)`
(k = 0.5522847498, 177 points for r = 100, max error 0.0272 px).

`code/common/resize.h` (Ch 35, includes `bezier.h`): `resizeNearest(src, w, h)` (source = (x + 0.5) × W/w, floor),
`getPixelClamped` (clamp to edge), `pixelAsF(img, x, y, linearLight)`, `sampleBilinear(img, PointF, linearLight = true)`
(−0.5 shift, 4 centres, lerp across then down), `resizeBilinear(src, w, h, linearLight = true)`, `firstCentreAtOrAfter(edge)`
= ceil(edge − 0.5), `resizeBox(src, w, h)` (average of all source centres in the half-open cell, linear light, at least
one pixel), `drawImageTransformedSmooth(dest, src, t)` (Ch 33 with bilinear; outer edge still hard — Ch 35 P7).

`code/common/bytes.h` (Ch 36, includes ONLY `image.h` — the start of the file-format branch): `using Bytes =
std::vector<std::uint8_t>`, `putU16`, `putU32`, `putS32` (little-endian), `getU16`, `getU32`, `getS32` (int pos; casts to
uint32 before shifting), `hasBytes(in, pos, count)`, `hexByte(b)` (two hex digits), `bmpRowSize(width)` = (3w + 3)/4×4.
Big-endian versions are Ch 36 Practice 5 (needed for PNG, Ch 40 — put them in a header then).

`code/common/bmp.h` (Ch 37, includes `bytes.h`): `const int kBmpHeaderSize = 54`, `writeBytes(fileName, bytes)` (binary),
`bmpSizeIsOk(w, h)` (w, h > 0; 54 + rowSize·h ≤ 2³¹ − 1 in long long), `makeBmpBytes(image)` (empty Bytes = failure),
`saveBMP(image, fileName)` (picture FIRST). Image has NO default constructor — use `Image x(0, 0)` as a placeholder.

`code/common/bmpload.h` (Ch 38, includes `bmp.h`): `std::string bmpProblem(const Bytes&)` ("" = OK; 10 checks: size ≤
2³¹−1, ≥ 54, "BM", header ≥ 40, planes 1, bpp 24/32, compression 0, width > 0 & height ≠ 0 & height ≥ −1e8, w·rows ≤ 1e8,
offset ≥ 54 & offset + rowSize·rows ≤ size — all in long long), `decodeBMP(bytes, image)` (top-down if height < 0;
32-bit ignores the 4th byte), `loadBMP(fileName, image)`.

`code/common/tga.h` (Ch 39, includes `bmpload.h`): `kTgaHeaderSize = 18`, `samePixel`, `appendPixelBytes`, `encodeRleRow(out,
row, bpp)` (run packet if ≥ 2 equal, else raw packet stopping before a run; ≤ 128; packets never cross rows),
`makeTgaBytes(image, const vector<uint8_t>* alpha, bool rle)` (writes TOP-DOWN, descriptor 0x20 / 0x28, type 2/10),
`saveTGA(image, name, rle = false, alpha = nullptr)`, `std::string decodeTGA(bytes, image, alpha* = nullptr)` ("" = OK;
checks + per-packet bounds), `loadTGA(name, image, alpha* = nullptr)`. Alpha is a separate vector (index y·w + x).

`code/common/png.h` (Ch 40, includes `tga.h`): `putU32BE`, `getU32BE`, `crc32Bitwise(data, from, count)`, `makeCrcTable`,
`crcTable()` (static), `crc32(data, from, count)` (table), `appendPngSignature`, `appendChunk(out, type, data)` (CRC over
type + data), `makeIhdr(w, h, withAlpha)` (8-bit, colour type 2/6), `struct PngChunk {type, dataStart, length, crcOk}`,
`std::string listChunks(file, chunks)` (signature, bounds in long long, CRC check, stops after IEND).

`code/common/zlib.h` (Ch 41, includes `png.h`): `kAdlerModulus = 65521`, `kMaxStoredBlock = 65535`, `adler32(data, from,
count)`, `zlibStore(data)` (78 01, stored blocks 0x00/0x01 + LEN/NLEN little-endian, Adler-32 big-endian; do-while so
empty data → one empty final block), `std::string zlibUnstore(z, out)` (method 8, %31, no FDICT, BTYPE must be 0 →
"compressed blocks are not supported yet", NLEN, bounds, Adler). Verified with Python's zlib.decompress.

`code/common/pngfile.h` (Ch 42, includes `zlib.h`): `makePngRows(image, alpha*)` (filter byte 0 + R G B (A)),
`makePngBytes(image, alpha* = nullptr)` (wrong-sized alpha → RGB), `savePNG(image, name, alpha* = nullptr)`,
`isKnownChunk`, `std::string decodePNG(bytes, image, alpha* = nullptr)` (11 checks; joins IDATs; skips ancillary;
refuses filter ≠ 0 with "row filters are not supported yet"), `loadPNG`. tiny 3×2 PNG = 88 bytes; heart 300² PNG
270,388 vs BMP 270,054.

`code/common/pngfilter.h` (Ch 43, includes `pngfile.h`): `kFilterNone/Sub/Up/Average/Paeth` = 0–4, `kFilterBest` = 5
(our "adaptive" mode, never written to a file), `absInt`, `paethPredictor(a, b, c)` (ties a, b, c), `predictByte(filter,
a, b, c)`, `filterRow(filter, row, above, bpp)` / `unfilterRow(filter, filtered, above, bpp)` (rows WITHOUT filter byte;
above = zeros for the top row; a from the rebuilt row), `rowScore` (signed sizes), `bestFilter` (strictly smaller wins,
ties keep the earlier filter), `filterScanlines(rows, rowLength, bpp, mode)` (input = Ch 42 rows with filter byte 0),
`std::string unfilterScanlines(rows, rowLength, bpp, out)` (output has filter byte 0 again; type > 4 → "unknown filter
type N"), `makePngBytesFiltered(image, mode, alpha*)`, `savePNGFiltered`, `struct PngInfo {width, height,
bytesPerPixel}`, `readPngStart(file, info, zdata)` (Ch 42 checks 1–8), `pngPixels(info, rows, image, alpha*)` (checks
10–11 with unfiltering), `decodePNGFiltered` (= readPngStart + zlibUnstore + pngPixels — Ch 45 swaps the middle),
`loadPNGFiltered`. Ch 42's pngfile.h is UNCHANGED (its loadPNG still refuses filters). Five test pictures 300×200:
flag, sky, sunset (horizontal lerp), blend (x·255/299, y·255/199, (x+y)·255/498), noise. Filtered PNG = 180,278 bytes
(same as unfiltered: stored blocks).

`code/common/huffman.h` (Ch 44, includes `pngfilter.h`): `kMaxCodeLength = 30`, `countBytes` (256 long long),
`struct HuffmanNode {weight, symbol, left, right}`, `takeSmallest` (ties → lower index: leaves in symbol order, then
joined nodes), `huffmanLengths(counts)` (any alphabet size; 1 symbol → length 1; depths by walking the node list
backwards), `canonicalCodes(lengths)` (RFC 1951 rule; −1 = no code / does not fit), `codedBits`, `entropyBits`
(std::log2), `struct BitWriter {bytes, used}`, `putBit` (fills from bit 0), `putBits` (value, lowest bit first),
`putCode` (code, top bit first), `struct BitReader {const Bytes* bytes; long long bit}`, `getBit` (−1 at end),
`getBits`, `struct DecodeNode {child[2], symbol}`, `buildDecoder(lengths, tree)` ("a code length is out of range",
"too many codes for their lengths"), `decodeSymbol` (−1 = bad/missing), our OWN format `huffmanCompress` (4-byte BE
count + 256 lengths + bits) / `huffmanDecompress`. Results: ABRACADABRA A 0, B 100, C 101, D 110, R 111, 23 bits,
bytes 72 35 39; filtered sky 22,910 bytes (unfiltered 166,298), flag 22,815, blend 26,739, noise 180,460; 1-bit floor
180,200 bits = 22,525 bytes.

`code/common/deflate.h` (Ch 45, includes `huffman.h`): `kMinMatch 3`, `kMaxMatch 258`, `kWindowSize 32768`, `kEndOfBlock
256`, `kMaxInflated 1e9`, tables `kLengthBase/kLengthExtra` (29), `kDistanceBase/kDistanceExtra` (30), `kCodeLengthOrder`
(19), `struct Lz77Token {literal, length, distance}` (length 0 = literal), `hash3`, `findMatches(data, maxTries)` (hash
chains head/previous, greedy, nearest wins ties, stop at max length), `lengthIndex`/`distanceIndex` (search from top),
`fixedLiteralLengths()` (288: 8/9/7/8), `fixedDistanceLengths()` (30 × 5), `writeFixedBlock(w, tokens, last)`,
`deflateFixed(data)` (one block, 64 tries), `zlibCompress(data)` (78 01; falls back to zlibStore if not smaller),
`inflateCodes`, `readDynamicTrees`, `std::string zlibDecompress(z, out)` (BTYPE 0/1/2, all checks), `makePngBytesCompressed
(image, alpha*)` (Best filters + zlibCompress; ≤ 1e8 row bytes), `savePNGCompressed`, `decodePNGFull` (readPngStart +
zlibDecompress + pngPixels), `loadPNGFull`. Verified: Python zlib.decompress accepts our output; the Python port of
inflate decodes zlib levels 0–9 (dynamic blocks). Sizes (300×200): flag 1,683, sky 1,746, sunset 1,769, blend 3,132,
noise 131,616 (BMP 180,054); disk RGBA 3,278. ch45/deflate.cpp embeds a 174-byte PNG made by Python zlib level 9
(8×8, dynamic block, HLIT 258, HDIST 12, HCLEN 18); ours = 100 bytes.

`code/common/font.h` (Ch 46, includes `resize.h` — DRAWING chain): `kGlyphWidth 5`, `kGlyphHeight 8` (row 7 =
descender), `kCharAdvance 6`, `kLineAdvance 10`, `kFirstChar 32`, `kLastChar 126`, `kFont` (95 × 8 bytes, bit 4 = left
column; the table in font.h is the only copy of the design — edit its bytes directly), `glyphIndex(char)`
(unsigned char; outside → '?'), `glyphPixel(c, x, y)` (false outside the grid), `lineCount`, `longestLine`, `textWidth(text,
scale)` = (chars·6 − 1)·scale, `textHeight` = (lines·10 − 2)·scale, `drawText(img, x, y, text, c, scale = 1)` (top-left,
fillRect squares, '\n' supported), `drawTextCentred(img, centreX, y, …)`, `textBox(x, y, text, scale, padding)` → Rect,
`overlapLength`, `glyphCoverage(ch, left, top, size, px, py)` (exact area), `drawTextSmooth(img, x, y, text, c, size)`
(double size of one font pixel; paintCoverage).

`code/common/pointops.h` (Ch 47, includes `font.h` AND `grey.h`): `using LookupTable = std::array<uint8_t, 256>`,
`clampByte(double)` (clamp 0..255, +0.5 round), `identityTable`, `brightnessTable(amount)`, `contrastTable(factor, centre =
128)`, `invertTable`, `thresholdTable(level)` (≥ level → 255), `gammaTable(g)`, `exposureTable(factor)` (linear light),
`levelsTable(low, high)` (high ≤ low → low + 1), `combineTables(first, second)` (= second[first[v]]), `applyTables(img, r,
g, b)`, `applyTable(img, t)`, `makeGrey(img)`, `tableAverage`, `drawCurve(img, x, y, size, t, c)` (frame + identity
diagonal + curve). Ch 47 program has `makeScene()` (160×110 sky/sun/hills/house) and `paste()` — not in a header.

`code/common/histogram.h` (Ch 48, includes `pointops.h`): `using Histogram = std::array<long long, 256>`, `greyHistogram`
(greyByte), `channelHistogram(img, 0/1/2)`, `cumulative`, `histogramTotal`, `lowestValue`, `highestValue` (0 if empty),
`usedValues`, `histogramMean`, `percentile(h, fraction)` (first v with c[v] ≥ f·total and c[v] > 0), `autoLevelsTable(h,
clip)`, `equaliseTable(h)` ((c − c_min)·255/(total − c_min); one value → identity), `drawHistogram(img, x, y, height, h, c)`
(frame 258 × height+2, labels "0"/"255"). Ch 48 program: `makeDull()` 256×160 grey 81..151, `printStats`, `printBars`.

`code/common/convolve.h` (Ch 49, includes `histogram.h`): `struct Kernel {size, std::vector<double> weights}` (row by row),
`enum class EdgeMode {Zero, Clamp, Mirror, Wrap}`, `kernelSum`, `identityKernel`, `boxKernel(size)`, `edgeIndex(i, n,
mode)` (−1 = Zero/black; Mirror repeats the edge pixel: −1 → 0, −2 → 1), `readPixel(src, x, y, mode, linearLight)` →
ColourF 0..1, `writePixel(ColourF, linearLight)` (clamps), `convolvePixel`, `convolve(src, k, mode = Clamp, linearLight =
false)` (CORRELATION, no flip — explained §49.5; new picture). Weights 1 → brightness kept, 0 → only changes.

`code/common/blur.h` (Ch 50, includes `convolve.h`): `struct PixelsF {width, height, vector<ColourF> data}`, `toPixelsF(img,
linear)`, `fromPixelsF(p, linear)`, `gaussianWeights(sigma)` (r = ceil(3σ), normalised), `boxWeights(r)`,
`kernelFromWeights(w)` (2D = w[j]·w[i]), `blurRows`, `blurColumns` (PixelsF, any EdgeMode), `separableBlur(img, w, mode =
Clamp, linearLight = TRUE)`, `gaussianBlur(img, sigma, mode = Clamp, linearLight = true)` (σ ≤ 0 → copy), `boxRowsFast`
(running sum, clamp), `transposed`, `boxBlurFast(img, r, linearLight = true)`. Results: σ 1 weights .0044 .0540 .2420
.3991; 2D vs separable and running sum identical on the test; 3 boxes r=1 ≈ Gaussian σ √2; red/green blur sRGB 170 85 0
vs linear 213 156 0; stripes period 4 shrunk ×3 alias to 255 255 0 0…; blurred first ≈ 182–193 (≈ 188 = linear 0.5).
Ch 49/50 programs copy Ch 47's `makeScene()`.

`code/common/edges.h` (Ch 51, includes `blur.h` and `hsv.h`): `struct GreyF {width, height, vector<double> data}` (grey
in 0..255 sRGB-value units, may be negative), `makeGreyF`, `greyAt` (clamp), `toGreyF` (255·luma), `convolveGrey(src,
Kernel)` (no rounding/clamping), `sharpenKernel` (0 −1 0/−1 5 −1/0 −1 0), `laplacianKernel`, `sobelX`, `sobelY`,
`magnitudeOf(gx, gy)`, `sobelMagnitude(g)`, `directionDegrees(gx, gy)` (0..360, y down, points dark→bright),
`largestValue` (abs), `greyFToImage(g, scale, offset = 0)` (clampByte), `edgeMap(mag, level)`, `directionColours(gx,
gy, largest)` (hue = direction), `unsharpMask(img, sigma, amount, linearLight = FALSE)` (sRGB default: balanced halos).
Results: row 100→160 sharpen 100 100 40 220 160 160; unsharp σ1 a1 100 96 82 178 164 160 (linear 100 95 69 173 163 160);
Sobel edge grid 0 360 360 0 0; diagonal 270/270 → 381.8 at 45°; noisy edge ≥100: 920 vs 192 after blur σ1.

`code/common/dither.h` (Ch 52, includes `edges.h`): `kBayer4[16]`, `bayerThreshold(x, y)` ((n + 0.5)/16),
`nearestLevel(v, levels)`, `posterise(img, levels)` (sRGB nearest), `orderedChannel(v, t, levels, linear)`,
`orderedDither(img, levels, linearLight = true)` (fraction between two sRGB levels measured in light), `cubePalette(levels)`
(r outer, b inner), `distanceSquared(ColourF, ColourF)`, `nearestIndex(c, vector<ColourF>)` (tie → earlier),
`addError`, `floydSteinberg(img, vector<Colour> palette, linearLight = true)` (7/3/5/1 sixteenths), `averageColour(img)`
(average light as a Colour). Results: grey 128 16×16: ordered sRGB 128 white (looks 188), linear 48 (120); FS sRGB 128
(188), linear 52 (124); orange 200 100 50 → red, 124.6; ramp avg 131 131 146, posterised 179 195 195, ordered 132 131
146, FS 129 131 145. Ch 51/52 programs copy Ch 47's `makeScene()`.

`code/common/warp.h` (Ch 53, includes `dither.h`): `enum class WarpKind {None, Wave, Ripple, Swirl, Bulge}`, `struct Warp
{kind, centre, amount, size}` (amount = A px / angle rad / k; size = wavelength L / radius R), `waveSource`,
`rippleSource`, `swirlSource` (angle·(1 − r/R)), `bulgeSource` (scale (r/R)^(k−1); k < 1 = pinch), `warpSource(p, w)`,
`insideImage`, `warpImage(src, w, Colour outside, linearLight = true)` (backwards, pixel centres, sampleBilinear),
`warpForward(src, w, background, int& holes)`. Results: wave (50,10) ← (56,10); ripple (85,55) ← (88,55); swirl
(105,55) ← (97.68,72.68); bulge ← (92.5,55); pinch ← (115.36,55); forward swirl 1472 of 17600 holes.

`code/common/random.h` (Ch 54, includes `warp.h`): `lcgNext(uint32&)` (Ch 39's), `xorshiftNext(uint32&)` (13, 17, 5),
`struct Random {state = 2463534242u}`, `makeRandom(seed)` (0 → default), `nextNumber`, `randomDouble` (top 24 bits /
2^24, < 1), `randomRange`, `randomInt(r, low, high)` (inclusive), `hash2(x, y, seed)` (×374761393, ×668265263, mix
×1274126177), `hashDouble(x, y, seed)`, `jitteredOffset(i, n, r)`, `whiteNoise(w, h, r)`. Results: LCG low bit
alternates; pair test 128 / 41308 / 41420 (ideal ≈ 41427); hashDouble(3, 7, 1) = 0.7641, (4, 7, 1) = 0.4679;
nearly-flat edge: grid 5 values, jittered 15, error 1.0 vs 0.6.

Header include chain so far: image.h ← colourf.h ← {grey.h, hsv.h, srgb.h ← alpha.h ← draw.h ← lines.h ← circles.h
← ellipses.h ← triangles.h ← fill.h ← barycentric.h ← antialias.h ← wu.h ← vec2.h ← angles.h ← transform.h ← matrix.h
← combine.h ← bezier.h ← resize.h ← font.h ← pointops.h (+ grey.h) ← histogram.h ← convolve.h ← blur.h ← edges.h (+ hsv.h) ← dither.h ← warp.h ← random.h}; and the file-format branch image.h ← bytes.h ← bmp.h ← bmpload.h ← tga.h ← png.h ← zlib.h ← pngfile.h ← pngfilter.h ← huffman.h ← deflate.h.
Note: programs that need HSV colours include `hsv.h` as well (it is not in the draw chain).

Chapter programs from Ch 11 on use `#include "image.h"` and are built with `g++ -std=c++17 -Wall -Wextra -O2 -I ../common`.

## Ideas and promises already made to the reader (keep them!)

Earlier chapters point forward to these. The later chapters must deliver them:

- (Ch 13 and 14 delivered: rounding with floor, graphs, any-width gradients, clamping, overflow.)
- Ch 20: line drawing fills the gaps in the Ch 13 graph of y = x².
- Ch 27 / 35 / 50: averages of many colours (Ch 14 §14.9) — do them in **linear light** (Ch 17 Ex 1) and with premultiplied alpha (Ch 18 §18.6); alpha = coverage (Ch 18 §18.2).
- Ch 42: PNG with RGBA to really store transparency (Ch 18 §18.8). Ch 67: painter's algorithm (Ch 18 §18.4). Ch 80: fades (Ch 18 Ex 3).
- Ch 68/73: lighting = colour × colour (Ch 14 §14.5).
- Ch 15: turning colour into grey (PGM output).
- Ch 17: why (128,128,128) is only ~22 % of white's light (gamma).
- Ch 19+: drawing. Ch 22: circles using √(dx² + dy²) and pixel centres (Ch 10 already drew a disk with them).
- Ch 25: flood fill with 4/8 neighbours; masks.
- Ch 27: many small masks for smooth edges.
- Ch 35: "nearest neighbour" (viewers that blur when zooming).
- Ch 36: BMP bottom-up rows, **BGR** order (Ch 12 P5 swaps R and B), rows padded to a multiple of 4,
  little-endian (Ch 4 P8 `78 56 34 12`, Ch 9 §9.8).
- (Ch 25 and 26 delivered: any polygon, flood fill 4/8, masks, barycentric weights, colour per corner.)
- (Ch 27 and 28 delivered: coverage = alpha, linear-light edge blending, small sample masks, Wu lines.)
- (Ch 29 and 30 delivered: dot/cross, perpendicular proof, edge function = cross, sin/cos, star constants of Ch 25,
  parametric orbits of Ch 23, hexagon √3/2 = sin 60°.)
- (Ch 31 and 32 delivered: rotation formula, tilted ellipse of Ch 23, matrices, homogeneous coordinates, determinant.)
- (Ch 33 and 34 delivered: pivot matrices, hierarchies, inverse, transforming whole images, Bézier curves.)
- (Ch 35 and 36 delivered: nearest/bilinear/box resizing, linear-light blending, BMP layout, little-endian, padding.)
- (Ch 37 and 38 delivered: saveBMP, loadBMP, viewer, sizes, top-down, 32-bit, broken-file tests.)
- (Ch 39 and 40 delivered: TGA, alpha = coverage, RLE, PNG signature/chunks/IHDR/IEND, CRC-32.)
- (Ch 41 and 42 delivered: zlib stored blocks, Adler-32, full PNG with alpha in browsers, decodePNG for our files.)
- (Ch 43 and 44 delivered: the five filters, unfiltering, adaptive choice, decodePNGFiltered; Huffman, entropy,
  canonical codes, bit writer/reader in Deflate order, filters + Huffman size win.)
- (Ch 45 and 46 delivered: LZ77, fixed + dynamic Deflate, real PNG sizes, loadPNGFull for other programs' PNGs, the
  ≤ 15-bit explanation; bitmap font, blocky and smooth text, shadows and caption boxes. Part 6 complete.)
- (Ch 47 and 48 delivered: point operations as curves and tables, invert/remap backwards (Ch 13 Ex 4), clamping vs
  wrap-around, gamma/exposure in linear light; histograms, percentiles, auto levels, equalisation.)
- (Ch 49 and 50 delivered: convolution, kernels, edge modes, in-place bug, cost; Gaussian, separable, running sum, linear
  light blur, blur-before-shrink (Ch 35 §35.7), clamp-to-edge for blurring (Ch 35 §35.4).)
- (Ch 51 and 52 delivered: negative edge values kept (Ch 49 §49.8), Laplacian (Ch 49 P3), Sobel strength/direction,
  unsharp mask; dithering keeps shading (Ch 47 §47.7), colour distance in the RGB cube (Ch 5).)
- (Ch 53 and 54 delivered: backwards warps with bilinear sampling, wave/ripple/swirl/bulge/pinch, forward holes
  counted; our own random numbers (Ch 1), the LCG of Ch 39 explained, jittered samples (Ch 27 §27.4).)
- Ch 55: value noise from `hashDouble` at grid corners, blended with "a gentler curve" than lerp (Ch 54 "Next").
- Ch 56/57: Perlin noise, then fractal noise for clouds, marble, wood (Ch 54 "Next chapter").
- Ch 80: the windmill animation (Ch 31 P6) can now be saved as BMP frames.
- Ch 35: resizing with the same inverse idea (Ch 31 §31.10); bilinear sampling for transformed images.
- Part 9: normals need a special matrix rule under non-uniform scale (Ch 32 §32.8); 4 × 4 matrices whose bottom row is
  not (0, 0, 0, 1) give perspective (Ch 32 §32.7). Ray tracing also uses "undo the transformation" (Ch 31 §31.10).
- Ch 80: a spinning windmill, frame by frame (Ch 31 P6).
- Ch 68: "is the lamp in front of the wall?" with (L − W)·n > 0 (Ch 29 Example 2).
- Exponential curves (Ch 30 P6 says "we do not use yet") — a later chapter may use std::exp (it is in <cmath>).
- Ch 35: nearest-neighbour enlarging was used in Ch 27 (`pasteEnlarged`) — Ch 35 explains it properly.
- Ch 35: bilinear blending again for resizing (Ch 26 §26.9).
- Ch 68: lighting computed at the corners and blended (Ch 26 Example 4). Ch 70: texture mapping with barycentric
  coordinates (Ch 26 §26.10).
- Ch 29: the edge function is the 2D **cross product** (Ch 24 §24.4). Relate `PointF` (Ch 24) to the new vector type.
- Ch 30: sine/cosine — orbits/planets via x = a·cos t, y = b·sin t (Ch 23 used y = b√(1 − (x/a)²) instead);
  hexagon/star corners with sin/cos (Ch 24 used √3/2).
- Ch 31: rotated (tilted) ellipses (Ch 23 §23.1). Kepler/foci were shown in Ch 23 §23.13 and P8.
- Ch 67: painter's order is already used informally (Ch 24 mountains).
- The allowed header list is in Ch 1 §1.2 (`<climits>` was also used in Ch 1).

## Notes

- No compiler was installed on the authoring machine (as of Ch 12), so the code was checked by hand, not compiled.
  The code blocks inside the chapters were diffed against the files in `code/`. Compile everything in `code/`
  with `g++ -std=c++17 -Wall -Wextra` when a compiler is available.
- Watch for line-number drift in the tables: write the code file first, run `cat -n`, then write the table.
