# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 5, Chapter 35 — Resizing images: nearest and bilinear** (the LAST chapter of Part 5).
File: `part-05-moving-and-bending-shapes/ch35-resizing-images-nearest-and-bilinear.md`, code in `code/ch35/` and a new
`common/resize.h` (include `bezier.h`).
It should cover: resizing = inverse mapping with a scale (Ch 33 §33.5): destination pixel centre (x + 0.5) maps to
source position (x + 0.5) × srcW / dstW (and the same for y) — derive it, show why NOT x × srcW / dstW (half-pixel
shift); NEAREST neighbour (floor of the source position) — explain properly, as promised by Ch 27 (`pasteEnlarged`)
and Ch 33 ("blocky"); the pixel-centre view of a picture: colours live at centres (k + 0.5); BILINEAR: subtract 0.5,
floor → the 4 neighbours, fx/fy fractions, lerp across twice then down once (Ch 26 §26.9 / Ch 13 lerp; mention it
equals the weights (1−fx)(1−fy) etc.), clamp at the edges (repeat the edge pixel — better than Ch 11's black outside,
promised for Ch 50 but give the clamp idea here); blend in LINEAR light (Ch 17, toLinear/fromLinear) — show the dark
fringe when blending sRGB bytes directly; worked numbers for a 2×2 picture enlarged to 4×4; SHRINKING: nearest and
bilinear skip pixels → aliasing/shimmer (checkerboard shrunk to 1/3 shows moiré); the fix = average all source pixels
under each destination pixel (box filter; generalises Ch 27's shrinkAverage to any factor — at least integer-friendly
version, or area-weighted); mention better filters later (Ch 50 blur). Also a `sampleBilinear(image, PointF)` helper
and a smooth version of Ch 33's drawImageTransformed (drawImageTransformedSmooth) — rotate the Ch 33 test picture
again and compare edges. Pictures: an 8×8 pixel-art sprite enlarged ×16 by nearest vs bilinear; a gradient strip
sRGB vs linear blend; a fine checkerboard shrunk by nearest vs box average; the rotated test picture nearest vs bilinear.
Then Part 6 (Ch 36 BMP) — the Ch 36 promises list (BGR, bottom-up, padding, little-endian) is below.

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

**Parts 1–4 complete**, Part 5 in progress (Ch 29–34 done). Total so far: ~226,200 words (`wc -w`, code included).

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

Header include chain so far: image.h ← colourf.h ← {grey.h, hsv.h, srgb.h ← alpha.h ← draw.h ← lines.h ← circles.h
← ellipses.h ← triangles.h ← fill.h ← barycentric.h ← antialias.h ← wu.h ← vec2.h ← angles.h ← transform.h ← matrix.h
← combine.h ← bezier.h}.
Note: programs that need HSV colours include `hsv.h` as well (it is not in the draw chain).

Chapter programs from Ch 11 on use `#include "image.h"` and are built with `g++ -std=c++17 -Wall -Wextra -O2 -I ../common`.

## Ideas and promises already made to the reader (keep them!)

Earlier chapters point forward to these. The later chapters must deliver them:

- (Ch 13 and 14 delivered: rounding with floor, graphs, any-width gradients, clamping, overflow.)
- Ch 20: line drawing fills the gaps in the Ch 13 graph of y = x².
- Ch 27 / 35 / 50: averages of many colours (Ch 14 §14.9) — do them in **linear light** (Ch 17 Ex 1) and with premultiplied alpha (Ch 18 §18.6); alpha = coverage (Ch 18 §18.2).
- Ch 42: PNG with RGBA to really store transparency (Ch 18 §18.8). Ch 67: painter's algorithm (Ch 18 §18.4). Ch 80: fades (Ch 18 Ex 3).
- Ch 47: invert via remap backwards (Ch 13 Ex 4); Ch 68/73: lighting = colour × colour (Ch 14 §14.5).
- Ch 15: turning colour into grey (PGM output).
- Ch 17: why (128,128,128) is only ~22 % of white's light (gamma).
- Ch 19+: drawing. Ch 22: circles using √(dx² + dy²) and pixel centres (Ch 10 already drew a disk with them).
- Ch 25: flood fill with 4/8 neighbours; masks.
- Ch 27: many small masks for smooth edges.
- Ch 35: "nearest neighbour" (viewers that blur when zooming).
- Ch 36: BMP bottom-up rows, **BGR** order (Ch 12 P5 swaps R and B), rows padded to a multiple of 4,
  little-endian (Ch 4 P8 `78 56 34 12`, Ch 9 §9.8).
- Ch 47: invert (`255 − v`); Ch 12 already does a negative.
- Ch 50: better choices than black for pixels outside the edge (getPixel returns black).
- Ch 52: colour distance in the RGB cube for dithering.
- Ch 54: our own random numbers (we never use `<random>`).
- (Ch 25 and 26 delivered: any polygon, flood fill 4/8, masks, barycentric weights, colour per corner.)
- (Ch 27 and 28 delivered: coverage = alpha, linear-light edge blending, small sample masks, Wu lines.)
- (Ch 29 and 30 delivered: dot/cross, perpendicular proof, edge function = cross, sin/cos, star constants of Ch 25,
  parametric orbits of Ch 23, hexagon √3/2 = sin 60°.)
- (Ch 31 and 32 delivered: rotation formula, tilted ellipse of Ch 23, matrices, homogeneous coordinates, determinant.)
- (Ch 33 and 34 delivered: pivot matrices, hierarchies, inverse, transforming whole images, Bézier curves.)
- Ch 35: bilinear sampling to make Ch 33's turned/enlarged pictures smooth (Ch 33 §33.5 says "In Chapter 35 we will
  blend the four nearest source pixels").
- Ch 46 (text): fonts are Bézier outlines (Ch 34 §34.10) — our bitmap font is simpler, but may mention it.
- Ch 35: resizing with the same inverse idea (Ch 31 §31.10); bilinear sampling for transformed images.
- Part 9: normals need a special matrix rule under non-uniform scale (Ch 32 §32.8); 4 × 4 matrices whose bottom row is
  not (0, 0, 0, 1) give perspective (Ch 32 §32.7). Ray tracing also uses "undo the transformation" (Ch 31 §31.10).
- Ch 80: a spinning windmill, frame by frame (Ch 31 P6).
- Ch 68: "is the lamp in front of the wall?" with (L − W)·n > 0 (Ch 29 Example 2).
- Exponential curves (Ch 30 P6 says "we do not use yet") — a later chapter may use std::exp (it is in <cmath>).
- Ch 54: random / jittered sample positions for supersampling (Ch 27 §27.4).
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
