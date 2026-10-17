#ifndef FILL_H
#define FILL_H

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <vector>
#include "triangles.h"

enum class FillRule { EvenOdd, NonZero };

struct Crossing {
    double x = 0.0;
    int direction = 0;
};

inline bool crossingIsLeft(const Crossing& p, const Crossing& q) {
    return p.x < q.x;
}

inline void findCrossings(const std::vector<PointF>& path, double sy,
                          std::vector<Crossing>& crossings) {
    const int n = static_cast<int>(path.size());
    for (int i = 0; i < n; ++i) {
        PointF a = path[i];
        PointF b = path[(i + 1) % n];
        if (a.y == b.y) {
            continue;
        }
        double top = std::min(a.y, b.y);
        double bottom = std::max(a.y, b.y);
        if (sy >= top && sy < bottom) {
            double t = (sy - a.y) / (b.y - a.y);
            int direction = (b.y > a.y) ? 1 : -1;
            crossings.push_back(Crossing{a.x + t * (b.x - a.x), direction});
        }
    }
}

inline void fillPaths(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col,
                      FillRule rule = FillRule::NonZero, double alpha = 1.0) {
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
    int y0 = std::max(0, static_cast<int>(std::floor(minY)));
    int y1 = std::min(image.height(), static_cast<int>(std::ceil(maxY)));
    std::vector<Crossing> crossings;
    for (int y = y0; y < y1; ++y) {
        double sy = y + 0.5;
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
            int xa = std::max(0, static_cast<int>(std::ceil(crossings[k].x - 0.5)));
            int xb = std::min(image.width(), static_cast<int>(std::ceil(crossings[k + 1].x - 0.5)));
            for (int x = xa; x < xb; ++x) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

inline void fillPolygon(Image& image, const std::vector<PointF>& points, Colour col,
                        FillRule rule = FillRule::NonZero, double alpha = 1.0) {
    std::vector<std::vector<PointF>> paths;
    paths.push_back(points);
    fillPaths(image, paths, col, rule, alpha);
}

struct Mask {
    int width = 0;
    int height = 0;
    std::vector<std::uint8_t> on;
};

inline Mask makeMask(int width, int height) {
    Mask mask;
    mask.width = width;
    mask.height = height;
    mask.on.assign(width * height, 0);
    return mask;
}

inline bool maskGet(const Mask& mask, int x, int y) {
    if (x < 0 || y < 0 || x >= mask.width || y >= mask.height) {
        return false;
    }
    return mask.on[y * mask.width + x] != 0;
}

inline void maskSet(Mask& mask, int x, int y, bool value) {
    if (x < 0 || y < 0 || x >= mask.width || y >= mask.height) {
        return;
    }
    mask.on[y * mask.width + x] = value ? 1 : 0;
}

inline int maskCount(const Mask& mask) {
    int count = 0;
    for (std::uint8_t v : mask.on) {
        if (v != 0) {
            ++count;
        }
    }
    return count;
}

inline bool sameColour(Colour p, Colour q) {
    return p.r == q.r && p.g == q.g && p.b == q.b;
}

inline Mask floodMask(const Image& image, int x, int y, bool eightWay = false) {
    Mask mask = makeMask(image.width(), image.height());
    if (!image.isInside(x, y)) {
        return mask;
    }
    const Colour target = image.getPixel(x, y);
    const int stepX[8] = {1, -1, 0, 0, 1, 1, -1, -1};
    const int stepY[8] = {0, 0, 1, -1, 1, -1, 1, -1};
    const int steps = eightWay ? 8 : 4;
    std::vector<Point> stack;
    stack.push_back(Point{x, y});
    while (!stack.empty()) {
        Point p = stack.back();
        stack.pop_back();
        if (!image.isInside(p.x, p.y) || maskGet(mask, p.x, p.y)) {
            continue;
        }
        if (!sameColour(image.getPixel(p.x, p.y), target)) {
            continue;
        }
        maskSet(mask, p.x, p.y, true);
        for (int i = 0; i < steps; ++i) {
            stack.push_back(Point{p.x + stepX[i], p.y + stepY[i]});
        }
    }
    return mask;
}

inline void paintMask(Image& image, const Mask& mask, Colour c, double alpha = 1.0) {
    for (int y = 0; y < mask.height; ++y) {
        for (int x = 0; x < mask.width; ++x) {
            if (!maskGet(mask, x, y)) {
                continue;
            }
            if (alpha >= 1.0) {
                image.setPixel(x, y, c);
            } else {
                blendPixel(image, x, y, c, alpha);
            }
        }
    }
}

inline int floodFill(Image& image, int x, int y, Colour c, bool eightWay = false,
                     double alpha = 1.0) {
    Mask mask = floodMask(image, x, y, eightWay);
    paintMask(image, mask, c, alpha);
    return maskCount(mask);
}

#endif
