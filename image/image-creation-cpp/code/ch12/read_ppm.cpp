#include <iostream>
#include <fstream>
#include "image.h"

void printImage(const Image& img) {
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            std::cout << "(" << static_cast<int>(c.r) << "," << static_cast<int>(c.g)
                      << "," << static_cast<int>(c.b) << ") ";
        }
        std::cout << "\n";
    }
}

int main() {
    {
        std::ofstream text("hand.ppm", std::ios::binary);
        text << "P3\n"
             << "# a 2 x 2 test image with maxval 15\n"
             << "2 2\n"
             << "15\n"
             << "15 0 0    0 15 0\n"
             << "0 0 15    5 5 5\n";
    }

    Image hand(1, 1);
    if (!loadPPM("hand.ppm", hand)) {
        std::cout << "could not load hand.ppm\n";
        return 1;
    }
    std::cout << "hand.ppm is " << hand.width() << " x " << hand.height() << ":\n";
    printImage(hand);

    Image first(3, 2);
    first.setPixel(0, 0, colours::red);
    first.setPixel(1, 0, colours::green);
    first.setPixel(2, 0, colours::blue);
    first.setPixel(0, 1, colours::yellow);
    first.setPixel(1, 1, colours::white);
    first.setPixel(2, 1, colours::black);
    first.savePPM("first_binary.ppm");

    Image back(1, 1);
    if (!loadPPM("first_binary.ppm", back)) {
        std::cout << "could not load first_binary.ppm\n";
        return 1;
    }
    std::cout << "\nfirst_binary.ppm is " << back.width() << " x " << back.height() << ":\n";
    printImage(back);

    for (int y = 0; y < back.height(); ++y) {
        for (int x = 0; x < back.width(); ++x) {
            Colour c = back.getPixel(x, y);
            Colour negative{static_cast<std::uint8_t>(255 - c.r),
                            static_cast<std::uint8_t>(255 - c.g),
                            static_cast<std::uint8_t>(255 - c.b)};
            back.setPixel(x, y, negative);
        }
    }
    back.savePPM("first_negative.ppm");
    std::cout << "\nnegative:\n";
    printImage(back);

    Image missing(1, 1);
    bool loaded = loadPPM("no_such_file.ppm", missing);
    std::cout << "\nloading a missing file: " << (loaded ? "worked?!" : "failed, as expected") << "\n";
    return 0;
}
