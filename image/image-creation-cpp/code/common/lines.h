#ifndef LINES_H
#define LINES_H

#include <algorithm>
#include <cmath>
#include "draw.h"

inline int roundToInt(double v) {
    return static_cast<int>(std::floor(v + 0.5));
}

inline void drawLineNaive(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    if (x0 == x1) {
        for (int y = std::min(y0, y1); y <= std::max(y0, y1); ++y) {
            image.setPixel(x0, y, c);
        }
        return;
    }
    double slope = static_cast<double>(y1 - y0) / (x1 - x0);
    for (int x = std::min(x0, x1); x <= std::max(x0, x1); ++x) {
        double y = y0 + slope * (x - x0);
        image.setPixel(x, roundToInt(y), c);
    }
}

inline void drawLineDDA(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    int steps = std::max(std::abs(dx), std::abs(dy));
    if (steps == 0) {
        image.setPixel(x0, y0, c);
        return;
    }
    double xStep = static_cast<double>(dx) / steps;
    double yStep = static_cast<double>(dy) / steps;
    for (int i = 0; i <= steps; ++i) {
        double x = x0 + xStep * i;
        double y = y0 + yStep * i;
        image.setPixel(roundToInt(x), roundToInt(y), c);
    }
}

#include <vector>

struct Point {
    int x = 0;
    int y = 0;
};

inline void drawLineShallow(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    int d = -dx;
    int y = y0;
    for (int x = x0; x <= x1; ++x) {
        image.setPixel(x, y, c);
        d += 2 * dy;
        if (d > 0) {
            y += 1;
            d -= 2 * dx;
        }
    }
}

inline void drawLine(Image& image, int x0, int y0, int x1, int y1, Colour c,
                     bool includeLast = true) {
    int dx = std::abs(x1 - x0);
    int dy = -std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy;
    while (x0 != x1 || y0 != y1) {
        image.setPixel(x0, y0, c);
        int e2 = 2 * err;
        if (e2 >= dy) {
            err += dy;
            x0 += sx;
        }
        if (e2 <= dx) {
            err += dx;
            y0 += sy;
        }
    }
    if (includeLast) {
        image.setPixel(x1, y1, c);
    }
}

inline std::vector<Point> linePoints(int x0, int y0, int x1, int y1) {
    std::vector<Point> points;
    int dx = std::abs(x1 - x0);
    int dy = -std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy;
    while (x0 != x1 || y0 != y1) {
        points.push_back(Point{x0, y0});
        int e2 = 2 * err;
        if (e2 >= dy) {
            err += dy;
            x0 += sx;
        }
        if (e2 <= dx) {
            err += dx;
            y0 += sy;
        }
    }
    points.push_back(Point{x1, y1});
    return points;
}

inline void drawThickLine(Image& image, int x0, int y0, int x1, int y1, int width, Colour c) {
    int r = width / 2;
    for (const Point& p : linePoints(x0, y0, x1, y1)) {
        fillRect(image, makeRect(p.x - r, p.y - r, width, width), c);
    }
}

inline void drawDashedLine(Image& image, int x0, int y0, int x1, int y1,
                           int dash, int gap, Colour c) {
    if (dash <= 0 || gap < 0) {
        return;
    }
    std::vector<Point> points = linePoints(x0, y0, x1, y1);
    for (int i = 0; i < static_cast<int>(points.size()); ++i) {
        if (i % (dash + gap) < dash) {
            image.setPixel(points[i].x, points[i].y, c);
        }
    }
}

#endif
