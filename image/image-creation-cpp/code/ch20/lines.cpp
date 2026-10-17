#include <iostream>
#include <vector>
#include "hsv.h"
#include "lines.h"

void printGrid(const Image& img) {
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

int main() {
    Image shallow(6, 3);
    drawLineDDA(shallow, 0, 0, 5, 2, colours::white);
    std::cout << "DDA from (0, 0) to (5, 2):\n";
    printGrid(shallow);

    Image steepNaive(3, 7);
    drawLineNaive(steepNaive, 0, 0, 2, 6, colours::white);
    std::cout << "naive from (0, 0) to (2, 6):\n";
    printGrid(steepNaive);

    Image steepDDA(3, 7);
    drawLineDDA(steepDDA, 0, 0, 2, 6, colours::white);
    std::cout << "DDA from (0, 0) to (2, 6):\n";
    printGrid(steepDDA);

    Image fan(200, 200, colours::white);
    for (int i = 0; i < 200; i += 10) {
        Colour c = toColour(hsvToRgb(HSV{i * 1.8, 0.9, 0.8}));
        drawLineDDA(fan, 100, 100, i, 0, c);
        drawLineDDA(fan, 100, 100, 199, i, c);
        drawLineDDA(fan, 100, 100, 199 - i, 199, c);
        drawLineDDA(fan, 100, 100, 0, 199 - i, c);
    }

    Image compare(200, 120, colours::white);
    for (int k = 0; k < 5; ++k) {
        int top = 10;
        int bottom = 110;
        drawLineNaive(compare, 10 + k * 8, top, 20 + k * 8, bottom, colours::red);
        drawLineDDA(compare, 110 + k * 8, top, 120 + k * 8, bottom, colours::blue);
    }

    Image graph(201, 201, colours::white);
    drawLineDDA(graph, 0, 100, 200, 100, Colour{200, 200, 200});
    drawLineDDA(graph, 100, 0, 100, 200, Colour{200, 200, 200});
    std::vector<int> rows;
    for (int px = 0; px < graph.width(); ++px) {
        double mathsX = -1.0 + 2.0 * px / (graph.width() - 1);
        double mathsY = mathsX * mathsX;
        double row = (mathsY + 1.0) / 2.0 * (graph.height() - 1);
        rows.push_back((graph.height() - 1) - roundToInt(row));
    }
    for (int px = 0; px + 1 < graph.width(); ++px) {
        drawLineDDA(graph, px, rows[px], px + 1, rows[px + 1], colours::red);
    }

    bool ok = fan.savePPM("fan.ppm");
    ok = ok && compare.savePPM("naive_vs_dda.ppm");
    ok = ok && graph.savePPM("graph_lines.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
