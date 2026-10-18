#include <iostream>
#include <string>
#include <vector>
#include "wu.h"

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

void printCoverageGrid(const std::string& title, const std::vector<CoveragePixel>& pixels,
                       int width, int height) {
    std::vector<double> grid(width * height, 0.0);
    for (const CoveragePixel& p : pixels) {
        if (p.x >= 0 && p.x < width && p.y >= 0 && p.y < height) {
            grid[p.y * width + p.x] += p.coverage;
        }
    }
    std::cout << title << ":\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            int digit = static_cast<int>(grid[y * width + x] * 9.0 + 0.5);
            if (digit == 0) {
                std::cout << '.';
            } else {
                std::cout << digit;
            }
        }
        std::cout << "\n";
    }
}

double columnLight(const Image& img, int x) {
    double sum = 0.0;
    for (int y = 0; y < img.height(); ++y) {
        sum += toLinear(img.getPixel(x, y)).r;
    }
    return sum;
}

int main() {
    std::vector<CoveragePixel> wu = wuLinePixels(PointF{0.5, 0.5}, PointF{8.5, 3.5});
    std::cout << "Wu line from (0.5, 0.5) to (8.5, 3.5):\n";
    for (const CoveragePixel& p : wu) {
        if (p.coverage > 0.0) {
            std::cout << "  (" << p.x << ", " << p.y << ") " << p.coverage << "\n";
        }
    }
    printCoverageGrid("the same, as digits (9 = full)", wu, 9, 5);
    Image bresenham(9, 5);
    drawLine(bresenham, 0, 0, 8, 3, colours::white, false);
    printGrid("Bresenham from (0, 0) to (8, 3), last pixel left out", bresenham);

    Image wuDiagonal(30, 30);
    drawLineWu(wuDiagonal, PointF{2.0, 2.0}, PointF{28.0, 28.0}, colours::white);
    Image bandDiagonal(30, 30);
    fillThickLineAA(bandDiagonal, PointF{2.0, 2.0}, PointF{28.0, 28.0}, 1.0, colours::white);
    std::cout << "light in column 15 of a 45-degree line: Wu " << columnLight(wuDiagonal, 15)
              << ", supersampled band " << columnLight(bandDiagonal, 15) << "\n";

    Image spokes(600, 200, colours::white);
    for (int k = 0; k < 10; ++k) {
        int ex = 10 + 20 * k;
        drawLine(spokes, 100, 100, ex, 10, colours::black);
        drawLine(spokes, 100, 100, ex, 190, colours::black);
        drawLineWu(spokes, PointF{300.5, 100.5}, PointF{ex + 200.5, 10.5}, colours::black);
        drawLineWu(spokes, PointF{300.5, 100.5}, PointF{ex + 200.5, 190.5}, colours::black);
        fillThickLineAA(spokes, PointF{500.5, 100.5}, PointF{ex + 400.5, 10.5}, 1.0,
                        colours::black);
        fillThickLineAA(spokes, PointF{500.5, 100.5}, PointF{ex + 400.5, 190.5}, 1.0,
                        colours::black);
    }

    Image rings(400, 200, colours::white);
    for (int r = 10; r <= 90; r += 16) {
        drawCircle(rings, 100, 100, r, Colour{30, 60, 160});
        drawCircleWu(rings, 300.5, 100.5, r, Colour{30, 60, 160});
    }

    Image graph(400, 300, colours::white);
    drawLine(graph, 20, 150, 380, 150, Colour{180, 180, 180});
    drawLine(graph, 200, 10, 200, 290, Colour{180, 180, 180});
    std::vector<PointF> parabola;
    std::vector<PointF> cubic;
    for (int x = 20; x <= 380; x += 5) {
        double u = x - 200.0;
        parabola.push_back(PointF{x + 0.5, 280.0 - u * u / 150.0});
        cubic.push_back(PointF{x + 0.5, 150.0 + u * u * u / 40000.0});
    }
    drawPolylineWu(graph, parabola, Colour{30, 60, 200});
    drawPolylineWu(graph, cubic, Colour{200, 40, 40});

    bool ok = spokes.savePPM("wu_spokes.ppm");
    ok = ok && rings.savePPM("wu_rings.ppm");
    ok = ok && graph.savePPM("graph.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
