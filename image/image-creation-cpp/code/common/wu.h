#ifndef WU_H
#define WU_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "antialias.h"

struct CoveragePixel {
    int x = 0;
    int y = 0;
    double coverage = 0.0;
};

inline std::vector<CoveragePixel> wuLinePixels(PointF a, PointF b) {
    std::vector<CoveragePixel> pixels;
    bool steep = std::fabs(b.y - a.y) > std::fabs(b.x - a.x);
    if (steep) {
        std::swap(a.x, a.y);
        std::swap(b.x, b.y);
    }
    if (a.x > b.x) {
        std::swap(a, b);
    }
    double dx = b.x - a.x;
    if (dx == 0.0) {
        return pixels;
    }
    double gradient = (b.y - a.y) / dx;
    int xStart = static_cast<int>(std::ceil(a.x - 0.5));
    int xEnd = static_cast<int>(std::ceil(b.x - 0.5));
    for (int x = xStart; x < xEnd; ++x) {
        double yc = a.y + gradient * ((x + 0.5) - a.x);
        double t = yc - 0.5;
        int row = static_cast<int>(std::floor(t));
        double f = t - row;
        if (steep) {
            pixels.push_back(CoveragePixel{row, x, 1.0 - f});
            pixels.push_back(CoveragePixel{row + 1, x, f});
        } else {
            pixels.push_back(CoveragePixel{x, row, 1.0 - f});
            pixels.push_back(CoveragePixel{x, row + 1, f});
        }
    }
    return pixels;
}

inline void drawLineWu(Image& image, PointF a, PointF b, Colour c) {
    for (const CoveragePixel& p : wuLinePixels(a, b)) {
        paintCoverage(image, p.x, p.y, c, p.coverage);
    }
}

inline void drawPolylineWu(Image& image, const std::vector<PointF>& points, Colour c) {
    const int n = static_cast<int>(points.size());
    for (int i = 0; i + 1 < n; ++i) {
        drawLineWu(image, points[i], points[i + 1], c);
    }
}

inline void plotSplitRow(Image& image, int x, double yc, Colour c) {
    double t = yc - 0.5;
    int row = static_cast<int>(std::floor(t));
    double f = t - row;
    paintCoverage(image, x, row, c, 1.0 - f);
    paintCoverage(image, x, row + 1, c, f);
}

inline void plotSplitColumn(Image& image, double xc, int y, Colour c) {
    double t = xc - 0.5;
    int column = static_cast<int>(std::floor(t));
    double f = t - column;
    paintCoverage(image, column, y, c, 1.0 - f);
    paintCoverage(image, column + 1, y, c, f);
}

inline void drawCircleWu(Image& image, double cx, double cy, double r, Colour c) {
    if (r <= 0.0) {
        return;
    }
    const double limit = r / std::sqrt(2.0);
    int first = static_cast<int>(std::floor(cx - limit - 0.5));
    int last = static_cast<int>(std::ceil(cx + limit));
    for (int x = first; x <= last; ++x) {
        double dx = (x + 0.5) - cx;
        if (std::fabs(dx) > limit) {
            continue;
        }
        double h = std::sqrt(r * r - dx * dx);
        plotSplitRow(image, x, cy - h, c);
        plotSplitRow(image, x, cy + h, c);
    }
    first = static_cast<int>(std::floor(cy - limit - 0.5));
    last = static_cast<int>(std::ceil(cy + limit));
    for (int y = first; y <= last; ++y) {
        double dy = (y + 0.5) - cy;
        if (std::fabs(dy) >= limit) {
            continue;
        }
        double w = std::sqrt(r * r - dy * dy);
        plotSplitColumn(image, cx - w, y, c);
        plotSplitColumn(image, cx + w, y, c);
    }
}

#endif
