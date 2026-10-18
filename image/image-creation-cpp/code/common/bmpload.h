#ifndef BMPLOAD_H
#define BMPLOAD_H

#include <cstdint>
#include <string>
#include "bmp.h"

inline std::string bmpProblem(const Bytes& file) {
    if (file.size() > 2147483647u) {
        return "file too big";
    }
    if (!hasBytes(file, 0, kBmpHeaderSize)) {
        return "too short for the two headers";
    }
    if (file[0] != 'B' || file[1] != 'M') {
        return "no BM signature";
    }
    const std::uint32_t headerSize = getU32(file, 14);
    const std::int32_t width = getS32(file, 18);
    const std::int32_t height = getS32(file, 22);
    const std::uint16_t bits = getU16(file, 28);
    if (headerSize < 40) {
        return "unknown (old) info header";
    }
    if (getU16(file, 26) != 1) {
        return "planes is not 1";
    }
    if (bits != 24 && bits != 32) {
        return "only 24 and 32 bits per pixel are supported";
    }
    if (getU32(file, 30) != 0) {
        return "compressed BMP files are not supported";
    }
    if (width <= 0 || height == 0 || height < -100000000) {
        return "bad width or height";
    }
    const long long rows = (height < 0) ? -static_cast<long long>(height) : height;
    if (static_cast<long long>(width) * rows > 100000000LL) {
        return "picture too big";
    }
    const long long rowSize = (static_cast<long long>(width) * (bits / 8) + 3) / 4 * 4;
    const long long offset = getU32(file, 10);
    if (offset < kBmpHeaderSize || offset + rowSize * rows > static_cast<long long>(file.size())) {
        return "the pixels are not inside the file";
    }
    return "";
}

inline bool decodeBMP(const Bytes& file, Image& image) {
    if (!bmpProblem(file).empty()) {
        return false;
    }
    const int width = getS32(file, 18);
    const int rawHeight = getS32(file, 22);
    const bool topDown = rawHeight < 0;
    const int height = topDown ? -rawHeight : rawHeight;
    const int bytesPerPixel = getU16(file, 28) / 8;
    const int rowSize = (width * bytesPerPixel + 3) / 4 * 4;
    const int offset = static_cast<int>(getU32(file, 10));

    Image result(width, height);
    for (int row = 0; row < height; ++row) {
        const int y = topDown ? row : height - 1 - row;
        const int rowStart = offset + row * rowSize;
        for (int x = 0; x < width; ++x) {
            const int at = rowStart + x * bytesPerPixel;
            result.setPixel(x, y, Colour{file[at + 2], file[at + 1], file[at]});
        }
    }
    image = result;
    return true;
}

inline bool loadBMP(const std::string& fileName, Image& image) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodeBMP(file, image);
}

#endif
