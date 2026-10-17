#ifndef DRAW_H
#define DRAW_H

#include <algorithm>
#include "alpha.h"

struct Rect {
    int x0 = 0;
    int y0 = 0;
    int x1 = 0;
    int y1 = 0;
};

inline Rect fromCorners(int ax, int ay, int bx, int by) {
    return Rect{std::min(ax, bx), std::min(ay, by), std::max(ax, bx), std::max(ay, by)};
}

inline Rect makeRect(int x, int y, int width, int height) {
    return fromCorners(x, y, x + width, y + height);
}

inline int rectWidth(Rect r) {
    return r.x1 - r.x0;
}

inline int rectHeight(Rect r) {
    return r.y1 - r.y0;
}

inline bool isEmpty(Rect r) {
    return r.x1 <= r.x0 || r.y1 <= r.y0;
}

inline bool contains(Rect r, int x, int y) {
    return x >= r.x0 && x < r.x1 && y >= r.y0 && y < r.y1;
}

inline Rect intersect(Rect a, Rect b) {
    Rect r{std::max(a.x0, b.x0), std::max(a.y0, b.y0),
           std::min(a.x1, b.x1), std::min(a.y1, b.y1)};
    if (isEmpty(r)) {
        return Rect{};
    }
    return r;
}

inline Rect clipToImage(Rect r, const Image& image) {
    return intersect(r, Rect{0, 0, image.width(), image.height()});
}

inline void fillRect(Image& image, Rect r, Colour c) {
    Rect clipped = clipToImage(r, image);
    for (int y = clipped.y0; y < clipped.y1; ++y) {
        for (int x = clipped.x0; x < clipped.x1; ++x) {
            image.setPixel(x, y, c);
        }
    }
}

inline void fillRectAlpha(Image& image, Rect r, Colour c, double alpha) {
    Rect clipped = clipToImage(r, image);
    for (int y = clipped.y0; y < clipped.y1; ++y) {
        for (int x = clipped.x0; x < clipped.x1; ++x) {
            blendPixel(image, x, y, c, alpha);
        }
    }
}

inline void strokeRect(Image& image, Rect r, int thickness, Colour c) {
    if (isEmpty(r) || thickness <= 0) {
        return;
    }
    int t = std::min(thickness, std::min(rectWidth(r), rectHeight(r)));
    fillRect(image, Rect{r.x0, r.y0, r.x1, r.y0 + t}, c);
    fillRect(image, Rect{r.x0, r.y1 - t, r.x1, r.y1}, c);
    fillRect(image, Rect{r.x0, r.y0 + t, r.x0 + t, r.y1 - t}, c);
    fillRect(image, Rect{r.x1 - t, r.y0 + t, r.x1, r.y1 - t}, c);
}

#endif
