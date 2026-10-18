#ifndef ANTIALIAS_H
#define ANTIALIAS_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "barycentric.h"

inline double sampleOffset(int i, int n) {
    return (i + 0.5) / n;
}

inline void paintCoverage(Image& image, int x, int y, Colour c, double coverage) {
    if (coverage <= 0.0) {
        return;
    }
    if (coverage >= 1.0) {
        image.setPixel(x, y, c);
        return;
    }
    blendPixel(image, x, y, c, coverage);
}

inline double circleCoverage(double cx, double cy, double r, int x, int y, int n) {
    double r2 = r * r;
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            if (dx * dx + dy * dy <= r2) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillCircleAA(Image& image, double cx, double cy, double r, Colour c, int n = 4) {
    if (r <= 0.0 || n < 1) {
        return;
    }
    const double halfDiagonal = 0.70711;
    int x0 = static_cast<int>(std::floor(cx - r));
    int y0 = static_cast<int>(std::floor(cy - r));
    int x1 = static_cast<int>(std::ceil(cx + r));
    int y1 = static_cast<int>(std::ceil(cy + r));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            double d = std::sqrt(dx * dx + dy * dy);
            if (d <= r - halfDiagonal) {
                image.setPixel(x, y, c);
            } else if (d < r + halfDiagonal) {
                paintCoverage(image, x, y, c, circleCoverage(cx, cy, r, x, y, n));
            }
        }
    }
}

inline double ellipseCoverage(double cx, double cy, double a, double b, int x, int y, int n) {
    double a2 = a * a;
    double b2 = b * b;
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            if (b2 * dx * dx + a2 * dy * dy <= a2 * b2) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillEllipseAA(Image& image, double cx, double cy, double a, double b, Colour c,
                          int n = 4) {
    if (a <= 0.0 || b <= 0.0 || n < 1) {
        return;
    }
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - b));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + b));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            paintCoverage(image, x, y, c, ellipseCoverage(cx, cy, a, b, x, y, n));
        }
    }
}

inline void fillPathsAA(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col,
                        FillRule rule = FillRule::NonZero, int n = 4) {
    if (n < 1) {
        return;
    }
    bool any = false;
    double minY = 0.0;
    double maxY = 0.0;
    for (const std::vector<PointF>& path : paths) {
        for (PointF p : path) {
            if (!any) {
                minY = p.y;
                maxY = p.y;
                any = true;
            } else {
                minY = std::min(minY, p.y);
                maxY = std::max(maxY, p.y);
            }
        }
    }
    if (!any) {
        return;
    }
    const int width = image.width();
    int y0 = std::max(0, static_cast<int>(std::floor(minY)));
    int y1 = std::min(image.height(), static_cast<int>(std::ceil(maxY)));
    std::vector<int> counts(width, 0);
    std::vector<Crossing> crossings;
    for (int y = y0; y < y1; ++y) {
        std::fill(counts.begin(), counts.end(), 0);
        for (int j = 0; j < n; ++j) {
            double sy = y + sampleOffset(j, n);
            crossings.clear();
            for (const std::vector<PointF>& path : paths) {
                findCrossings(path, sy, crossings);
            }
            std::sort(crossings.begin(), crossings.end(), crossingIsLeft);
            int winding = 0;
            const int count = static_cast<int>(crossings.size());
            for (int k = 0; k + 1 < count; ++k) {
                winding += crossings[k].direction;
                bool inside = (rule == FillRule::EvenOdd) ? (k % 2 == 0) : (winding != 0);
                if (!inside) {
                    continue;
                }
                double xa = crossings[k].x;
                double xb = crossings[k + 1].x;
                int first = std::max(0, static_cast<int>(std::floor(xa)));
                int last = std::min(width - 1, static_cast<int>(std::floor(xb)));
                for (int x = first; x <= last; ++x) {
                    for (int i = 0; i < n; ++i) {
                        double sx = x + sampleOffset(i, n);
                        if (sx >= xa && sx < xb) {
                            ++counts[x];
                        }
                    }
                }
            }
        }
        for (int x = 0; x < width; ++x) {
            if (counts[x] > 0) {
                paintCoverage(image, x, y, col, static_cast<double>(counts[x]) / (n * n));
            }
        }
    }
}

inline void fillPolygonAA(Image& image, const std::vector<PointF>& points, Colour col,
                          FillRule rule = FillRule::NonZero, int n = 4) {
    std::vector<std::vector<PointF>> paths;
    paths.push_back(points);
    fillPathsAA(image, paths, col, rule, n);
}

inline void fillThickLineAA(Image& image, PointF a, PointF b, double thickness, Colour col,
                            int n = 4) {
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double length = std::sqrt(dx * dx + dy * dy);
    if (length == 0.0) {
        return;
    }
    double half = thickness / 2.0;
    double nx = -dy / length * half;
    double ny = dx / length * half;
    std::vector<PointF> band = {PointF{a.x + nx, a.y + ny}, PointF{b.x + nx, b.y + ny},
                                PointF{b.x - nx, b.y - ny}, PointF{a.x - nx, a.y - ny}};
    fillPolygonAA(image, band, col, FillRule::NonZero, n);
}

inline Image shrinkAverage(const Image& big, int factor) {
    const int w = big.width() / factor;
    const int h = big.height() / factor;
    Image small(w, h);
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int j = 0; j < factor; ++j) {
                for (int i = 0; i < factor; ++i) {
                    sum = sum + toLinear(big.getPixel(x * factor + i, y * factor + j));
                }
            }
            small.setPixel(x, y, fromLinear(sum / (factor * factor)));
        }
    }
    return small;
}

#endif
