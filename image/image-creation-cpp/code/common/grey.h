#ifndef GREY_H
#define GREY_H

#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include "colourf.h"

inline double luma(ColourF c) {
    return 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b;
}

inline double plainAverage(ColourF c) {
    return (c.r + c.g + c.b) / 3.0;
}

inline std::uint8_t greyByte(Colour c) {
    return toByte(luma(toColourF(c)));
}

inline Colour toGrey(Colour c) {
    std::uint8_t v = greyByte(c);
    return Colour{v, v, v};
}

inline Colour desaturate(Colour c, double amount) {
    ColourF f = toColourF(c);
    double y = luma(f);
    ColourF grey{y, y, y};
    return toColour(f + (grey - f) * amount);
}

inline bool saveGreyPGM(const Image& image, const std::string& fileName) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    std::vector<std::uint8_t> grey(image.width() * image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            grey[y * image.width() + x] = greyByte(image.getPixel(x, y));
        }
    }
    file << "P5\n" << image.width() << " " << image.height() << "\n255\n";
    file.write(reinterpret_cast<const char*>(grey.data()),
               static_cast<std::streamsize>(grey.size()));
    return static_cast<bool>(file);
}

#endif
