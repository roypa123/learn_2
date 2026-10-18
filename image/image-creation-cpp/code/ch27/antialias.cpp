#include <iostream>
#include <string>
#include <vector>
#include "antialias.h"

void printSampleMask(double cx, double cy, double r, int x, int y, int n) {
    std::cout << "samples in pixel (" << x << ", " << y << "):\n";
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        std::cout << "  ";
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            bool in = dx * dx + dy * dy <= r * r;
            if (in) {
                ++inside;
            }
            std::cout << (in ? '#' : '.');
        }
        std::cout << "\n";
    }
    std::cout << "  coverage " << inside << " / " << n * n << "\n";
}

void printCoverageMap(double cx, double cy, double r, int width, int height, int n) {
    std::cout << "coverage of each pixel, from 0 to 9:\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            double coverage = circleCoverage(cx, cy, r, x, y, n);
            int digit = static_cast<int>(coverage * 9.0 + 0.5);
            if (digit == 0) {
                std::cout << '.';
            } else {
                std::cout << digit;
            }
        }
        std::cout << "\n";
    }
}

int channelDifference(int a, int b) {
    return (a > b) ? a - b : b - a;
}

int largestDifference(const Image& p, const Image& q) {
    int largest = 0;
    for (int y = 0; y < p.height(); ++y) {
        for (int x = 0; x < p.width(); ++x) {
            Colour s = p.getPixel(x, y);
            Colour t = q.getPixel(x, y);
            largest = std::max(largest, channelDifference(s.r, t.r));
            largest = std::max(largest, channelDifference(s.g, t.g));
            largest = std::max(largest, channelDifference(s.b, t.b));
        }
    }
    return largest;
}

int countNotWhite(const Image& img) {
    int count = 0;
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            if (!sameColour(img.getPixel(x, y), colours::white)) {
                ++count;
            }
        }
    }
    return count;
}

void pasteEnlarged(Image& dst, const Image& src, int ox, int oy, int factor) {
    for (int y = 0; y < src.height() * factor; ++y) {
        for (int x = 0; x < src.width() * factor; ++x) {
            dst.setPixel(ox + x, oy + y, src.getPixel(x / factor, y / factor));
        }
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

int main() {
    printSampleMask(5.5, 5.5, 5.0, 9, 2, 4);
    printCoverageMap(5.5, 5.5, 5.0, 11, 11, 4);

    Image smooth(50, 50);
    fillCircleAA(smooth, 25.0, 25.0, 17.3, colours::white);
    Image big(200, 200);
    fillCircle(big, 100.0, 100.0, 4 * 17.3, colours::white);
    Image shrunk = shrinkAverage(big, 4);
    std::cout << "largest difference, fillCircleAA vs draw big and shrink: "
              << largestDifference(smooth, shrunk) << "\n";

    Image twoTriangles(8, 8);
    fillPolygonAA(twoTriangles, {PointF{0.0, 0.0}, PointF{8.0, 0.0}, PointF{8.0, 8.0}},
                  colours::white);
    fillPolygonAA(twoTriangles, {PointF{0.0, 0.0}, PointF{8.0, 8.0}, PointF{0.0, 8.0}},
                  colours::white);
    Image onePolygon(8, 8);
    fillPolygonAA(onePolygon,
                  {PointF{0.0, 0.0}, PointF{8.0, 0.0}, PointF{8.0, 8.0}, PointF{0.0, 8.0}},
                  colours::white);
    std::cout << "pixel (3, 3): two triangles " << static_cast<int>(twoTriangles.getPixel(3, 3).r)
              << ", one polygon " << static_cast<int>(onePolygon.getPixel(3, 3).r) << "\n";
    std::cout << "pixels that are not white: two triangles " << countNotWhite(twoTriangles)
              << ", one polygon " << countNotWhite(onePolygon) << "\n";

    Image jagged(40, 40, colours::white);
    fillCircle(jagged, 20.0, 20.0, 15.0, Colour{30, 60, 160});
    Image soft(40, 40, colours::white);
    fillCircleAA(soft, 20.0, 20.0, 15.0, Colour{30, 60, 160});
    Image zoom(490, 240, colours::white);
    pasteEnlarged(zoom, jagged, 0, 0, 6);
    pasteEnlarged(zoom, soft, 250, 0, 6);

    Image stars(420, 220, Colour{20, 30, 70});
    Colour gold{255, 200, 40};
    fillPolygon(stars, star(110.5, 115.5, 100.0), gold);
    fillPolygonAA(stars, star(310.5, 115.5, 100.0), gold);

    Image spokes(400, 200, colours::white);
    for (int k = 0; k < 10; ++k) {
        int ex = 10 + 20 * k;
        drawLine(spokes, 100, 100, ex, 10, colours::black);
        drawLine(spokes, 100, 100, ex, 190, colours::black);
        PointF centre{300.0, 100.0};
        fillThickLineAA(spokes, centre, PointF{ex + 200.0, 10.0}, 1.0, colours::black);
        fillThickLineAA(spokes, centre, PointF{ex + 200.0, 190.0}, 1.0, colours::black);
    }

    bool ok = zoom.savePPM("zoom.ppm");
    ok = ok && stars.savePPM("stars_aa.ppm");
    ok = ok && spokes.savePPM("spokes.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
