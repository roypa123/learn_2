#include <iostream>
#include <string>
#include "bytes.h"

void printBytes(const char* label, const Bytes& b) {
    std::cout << label;
    for (std::uint8_t v : b) {
        std::cout << " " << hexByte(v);
    }
    std::cout << "\n";
}

void putPixelBGR(Bytes& out, Colour c) {
    out.push_back(c.b);
    out.push_back(c.g);
    out.push_back(c.r);
}

int main() {
    Bytes number;
    putU32(number, 0x12345678);
    printBytes("0x12345678 as 4 little-endian bytes:", number);
    Bytes small;
    putU32(small, 54);
    printBytes("54 as 4 little-endian bytes:", small);
    Bytes negative;
    putS32(negative, -2);
    printBytes("-2 as 4 little-endian bytes:", negative);
    std::cout << "read back: " << getU32(number, 0) << " = 0x12345678? "
              << (getU32(number, 0) == 0x12345678 ? "yes" : "no") << ", and " << getS32(negative, 0)
              << "\n";

    std::cout << "width, pixel bytes, row size, padding:\n";
    for (int w = 1; w <= 8; ++w) {
        std::cout << "  " << w << ", " << w * 3 << ", " << bmpRowSize(w) << ", "
                  << bmpRowSize(w) - w * 3 << "\n";
    }

    Image picture(3, 2);
    picture.setPixel(0, 0, colours::red);
    picture.setPixel(1, 0, colours::green);
    picture.setPixel(2, 0, colours::blue);
    picture.setPixel(0, 1, colours::white);
    picture.setPixel(1, 1, colours::black);
    picture.setPixel(2, 1, colours::yellow);

    int rowSize = bmpRowSize(picture.width());
    int pixelBytes = rowSize * picture.height();
    int fileSize = 14 + 40 + pixelBytes;
    Bytes file;
    file.push_back('B');
    file.push_back('M');
    putU32(file, fileSize);
    putU16(file, 0);
    putU16(file, 0);
    putU32(file, 14 + 40);
    putU32(file, 40);
    putS32(file, picture.width());
    putS32(file, picture.height());
    putU16(file, 1);
    putU16(file, 24);
    putU32(file, 0);
    putU32(file, pixelBytes);
    putS32(file, 2835);
    putS32(file, 2835);
    putU32(file, 0);
    putU32(file, 0);
    for (int y = picture.height() - 1; y >= 0; --y) {
        for (int x = 0; x < picture.width(); ++x) {
            putPixelBGR(file, picture.getPixel(x, y));
        }
        for (int p = picture.width() * 3; p < rowSize; ++p) {
            file.push_back(0);
        }
    }

    std::cout << "the whole file, " << file.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(file.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(file.size()); ++j) {
            std::cout << " " << hexByte(file[j]);
        }
        std::cout << "\n";
    }

    std::cout << "reading it back: signature " << file[0] << file[1] << ", file size "
              << getU32(file, 2) << ", pixels start at " << getU32(file, 10) << ", width "
              << getS32(file, 18) << ", height " << getS32(file, 22) << ", bits per pixel "
              << getU16(file, 28) << "\n";
    int offset = static_cast<int>(getU32(file, 10));
    int height = getS32(file, 22);
    const int wanted[2][2] = {{2, 0}, {0, 1}};
    for (const auto& xy : wanted) {
        int x = xy[0];
        int y = xy[1];
        int at = offset + (height - 1 - y) * rowSize + x * 3;
        if (hasBytes(file, at, 3)) {
            std::cout << "pixel (" << x << ", " << y << ") is at byte " << at << ": R "
                      << static_cast<int>(file[at + 2]) << ", G " << static_cast<int>(file[at + 1])
                      << ", B " << static_cast<int>(file[at]) << "\n";
        }
    }
    return 0;
}
