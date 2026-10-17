#include <iostream>
#include <string>
#include <vector>
#include "fill.h"

void printGrid(const std::string& title, const Image& img) {
    std::cout << title << ":\n";
    for (int y = 0; y < img.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            bool on = c.r != 0 || c.g != 0 || c.b != 0;
            std::cout << (on ? '#' : '.');
        }
        std::cout << "\n";
    }
}

int countLit(const Image& img) {
    int count = 0;
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            if (c.r != 0 || c.g != 0 || c.b != 0) {
                ++count;
            }
        }
    }
    return count;
}

bool samePixels(const Image& p, const Image& q) {
    if (p.width() != q.width() || p.height() != q.height()) {
        return false;
    }
    for (int y = 0; y < p.height(); ++y) {
        for (int x = 0; x < p.width(); ++x) {
            if (!sameColour(p.getPixel(x, y), q.getPixel(x, y))) {
                return false;
            }
        }
    }
    return true;
}

void printColours(const std::string& title, const Image& img) {
    std::cout << title << ":\n";
    for (int y = 0; y < img.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            char ch = '?';
            if (sameColour(c, colours::black)) {
                ch = '.';
            } else if (sameColour(c, colours::white)) {
                ch = '#';
            } else if (sameColour(c, colours::red)) {
                ch = 'o';
            }
            std::cout << ch;
        }
        std::cout << "\n";
    }
}

std::vector<PointF> star(double cx, double cy, double r) {
    const double ux[5] = {0.0, 0.9511, 0.5878, -0.5878, -0.9511};
    const double uy[5] = {-1.0, -0.3090, 0.8090, 0.8090, -0.3090};
    const int order[5] = {0, 2, 4, 1, 3};
    std::vector<PointF> points;
    for (int i = 0; i < 5; ++i) {
        int k = order[i];
        points.push_back(PointF{cx + r * ux[k], cy + r * uy[k]});
    }
    return points;
}

std::vector<PointF> square(double x0, double y0, double x1, double y1) {
    return {PointF{x0, y0}, PointF{x1, y0}, PointF{x1, y1}, PointF{x0, y1}};
}

std::vector<PointF> reversed(const std::vector<PointF>& points) {
    return std::vector<PointF>(points.rbegin(), points.rend());
}

int main() {
    Image evenOdd(21, 20);
    fillPolygon(evenOdd, star(10.5, 10.5, 10.0), colours::white, FillRule::EvenOdd);
    printGrid("star, even-odd rule", evenOdd);
    Image nonZero(21, 20);
    fillPolygon(nonZero, star(10.5, 10.5, 10.0), colours::white, FillRule::NonZero);
    printGrid("star, non-zero rule", nonZero);
    std::cout << "pixels: even-odd " << countLit(evenOdd) << ", non-zero " << countLit(nonZero)
              << "\n";

    std::vector<PointF> arrowHead = {PointF{0.0, 0.0}, PointF{10.0, 5.0}, PointF{0.0, 10.0},
                                     PointF{3.0, 5.0}};
    Image arrow(11, 11);
    fillPolygon(arrow, arrowHead, colours::white);
    printGrid("arrow-head (a shape with a dent)", arrow);

    std::vector<PointF> tri = {PointF{1.0, 1.0}, PointF{12.0, 4.0}, PointF{4.0, 10.0}};
    Image byScan(14, 12);
    Image byEdges(14, 12);
    fillPolygon(byScan, tri, colours::white);
    fillTriangle(byEdges, tri[0], tri[1], tri[2], colours::white);
    std::cout << "scanline fill and fillTriangle give the same pixels: "
              << (samePixels(byScan, byEdges) ? "yes" : "no") << "\n";

    std::vector<PointF> outer = square(1.0, 1.0, 11.0, 11.0);
    std::vector<PointF> inner = square(4.0, 4.0, 8.0, 8.0);
    Image sameWay(12, 12);
    Image otherWay(12, 12);
    Image evenOddFrame(12, 12);
    fillPaths(sameWay, {outer, inner}, colours::white, FillRule::NonZero);
    fillPaths(otherWay, {outer, reversed(inner)}, colours::white, FillRule::NonZero);
    fillPaths(evenOddFrame, {outer, inner}, colours::white, FillRule::EvenOdd);
    printGrid("frame, non-zero rule, inner square reversed", otherWay);
    std::cout << "pixels: non-zero same way " << countLit(sameWay) << ", non-zero reversed "
              << countLit(otherWay) << ", even-odd " << countLit(evenOddFrame) << "\n";

    Image diamond(13, 13);
    drawLine(diamond, 6, 0, 12, 6, colours::white);
    drawLine(diamond, 12, 6, 6, 12, colours::white);
    drawLine(diamond, 6, 12, 0, 6, colours::white);
    drawLine(diamond, 0, 6, 6, 0, colours::white);
    Image four = diamond;
    int filled4 = floodFill(four, 6, 6, colours::red);
    printColours("4-way flood fill from (6, 6)", four);
    Image eight = diamond;
    int filled8 = floodFill(eight, 6, 6, colours::red, true);
    printColours("8-way flood fill from (6, 6)", eight);
    std::cout << "filled pixels: 4-way " << filled4 << ", 8-way " << filled8 << "\n";

    Image stars(420, 220, Colour{20, 30, 70});
    Colour gold{255, 200, 40};
    fillPolygon(stars, star(110.5, 115.5, 100.0), gold, FillRule::EvenOdd);
    fillPolygon(stars, star(310.5, 115.5, 100.0), gold, FillRule::NonZero);

    Image holes(320, 180, colours::white);
    for (int x = 0; x < 320; x += 20) {
        fillRect(holes, Rect{x, 0, x + 10, 180}, Colour{190, 210, 230});
    }
    std::vector<PointF> letterC = {PointF{40.0, 20.0}, PointF{140.0, 20.0}, PointF{140.0, 50.0},
                                   PointF{70.0, 50.0}, PointF{70.0, 130.0}, PointF{140.0, 130.0},
                                   PointF{140.0, 160.0}, PointF{40.0, 160.0}};
    fillPolygon(holes, letterC, Colour{200, 40, 60});
    fillPaths(holes,
              {square(170.0, 20.0, 290.0, 160.0), reversed(square(200.0, 50.0, 260.0, 130.0))},
              Colour{40, 120, 60});

    Image venn(300, 200, colours::white);
    drawCircle(venn, 110, 100, 70, colours::black);
    drawCircle(venn, 190, 100, 70, colours::black);
    floodFill(venn, 5, 5, Colour{255, 250, 210});
    floodFill(venn, 70, 100, Colour{250, 120, 120});
    floodFill(venn, 150, 100, Colour{180, 110, 200});
    floodFill(venn, 230, 100, Colour{110, 150, 250});

    bool ok = stars.savePPM("stars.ppm");
    ok = ok && holes.savePPM("holes.ppm");
    ok = ok && venn.savePPM("venn.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
