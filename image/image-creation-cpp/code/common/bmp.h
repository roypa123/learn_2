#ifndef BMP_H
#define BMP_H

#include <cstdint>
#include <fstream>
#include <string>
#include "bytes.h"

const int kBmpHeaderSize = 14 + 40;

inline bool writeBytes(const std::string& fileName, const Bytes& bytes) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file.write(reinterpret_cast<const char*>(bytes.data()),
               static_cast<std::streamsize>(bytes.size()));
    return static_cast<bool>(file);
}

inline bool bmpSizeIsOk(int width, int height) {
    if (width <= 0 || height <= 0) {
        return false;
    }
    long long rowSize = (3LL * width + 3) / 4 * 4;
    return kBmpHeaderSize + rowSize * height <= 2147483647LL;
}

inline Bytes makeBmpBytes(const Image& image) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (!bmpSizeIsOk(width, height)) {
        return file;
    }
    const int rowSize = bmpRowSize(width);
    const int pixelBytes = rowSize * height;
    file.reserve(kBmpHeaderSize + pixelBytes);

    file.push_back('B');
    file.push_back('M');
    putU32(file, kBmpHeaderSize + pixelBytes);
    putU16(file, 0);
    putU16(file, 0);
    putU32(file, kBmpHeaderSize);

    putU32(file, 40);
    putS32(file, width);
    putS32(file, height);
    putU16(file, 1);
    putU16(file, 24);
    putU32(file, 0);
    putU32(file, pixelBytes);
    putS32(file, 2835);
    putS32(file, 2835);
    putU32(file, 0);
    putU32(file, 0);

    for (int y = height - 1; y >= 0; --y) {
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            file.push_back(c.b);
            file.push_back(c.g);
            file.push_back(c.r);
        }
        for (int p = width * 3; p < rowSize; ++p) {
            file.push_back(0);
        }
    }
    return file;
}

inline bool saveBMP(const Image& image, const std::string& fileName) {
    Bytes file = makeBmpBytes(image);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

#endif
