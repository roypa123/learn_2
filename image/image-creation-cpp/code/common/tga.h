#ifndef TGA_H
#define TGA_H

#include <cstdint>
#include <string>
#include <vector>
#include "bmpload.h"

const int kTgaHeaderSize = 18;

inline bool samePixel(const Bytes& row, int a, int b, int bytesPerPixel) {
    for (int i = 0; i < bytesPerPixel; ++i) {
        if (row[a * bytesPerPixel + i] != row[b * bytesPerPixel + i]) {
            return false;
        }
    }
    return true;
}

inline void appendPixelBytes(Bytes& out, const Bytes& row, int index, int bytesPerPixel) {
    for (int i = 0; i < bytesPerPixel; ++i) {
        out.push_back(row[index * bytesPerPixel + i]);
    }
}

inline void encodeRleRow(Bytes& out, const Bytes& row, int bytesPerPixel) {
    const int count = static_cast<int>(row.size()) / bytesPerPixel;
    int i = 0;
    while (i < count) {
        int run = 1;
        while (i + run < count && run < 128 && samePixel(row, i, i + run, bytesPerPixel)) {
            ++run;
        }
        if (run >= 2) {
            out.push_back(static_cast<std::uint8_t>(0x80 | (run - 1)));
            appendPixelBytes(out, row, i, bytesPerPixel);
            i += run;
        } else {
            int raw = 1;
            while (i + raw < count && raw < 128 &&
                   !(i + raw + 1 < count && samePixel(row, i + raw, i + raw + 1, bytesPerPixel))) {
                ++raw;
            }
            out.push_back(static_cast<std::uint8_t>(raw - 1));
            for (int k = 0; k < raw; ++k) {
                appendPixelBytes(out, row, i + k, bytesPerPixel);
            }
            i += raw;
        }
    }
}

inline Bytes makeTgaBytes(const Image& image, const std::vector<std::uint8_t>* alpha, bool rle) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0 || width > 65535 || height > 65535) {
        return file;
    }
    const bool withAlpha =
        alpha != nullptr && static_cast<int>(alpha->size()) == width * height;
    const int bytesPerPixel = withAlpha ? 4 : 3;

    file.push_back(0);
    file.push_back(0);
    file.push_back(rle ? 10 : 2);
    for (int i = 0; i < 5; ++i) {
        file.push_back(0);
    }
    putU16(file, 0);
    putU16(file, 0);
    putU16(file, static_cast<std::uint16_t>(width));
    putU16(file, static_cast<std::uint16_t>(height));
    file.push_back(static_cast<std::uint8_t>(bytesPerPixel * 8));
    file.push_back(withAlpha ? 0x28 : 0x20);

    for (int y = 0; y < height; ++y) {
        Bytes row;
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            row.push_back(c.b);
            row.push_back(c.g);
            row.push_back(c.r);
            if (withAlpha) {
                row.push_back((*alpha)[y * width + x]);
            }
        }
        if (rle) {
            encodeRleRow(file, row, bytesPerPixel);
        } else {
            file.insert(file.end(), row.begin(), row.end());
        }
    }
    return file;
}

inline bool saveTGA(const Image& image, const std::string& fileName, bool rle = false,
                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makeTgaBytes(image, alpha, rle);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline std::string decodeTGA(const Bytes& file, Image& image,
                             std::vector<std::uint8_t>* alpha = nullptr) {
    if (file.size() > 2147483647u) {
        return "file too big";
    }
    if (!hasBytes(file, 0, kTgaHeaderSize)) {
        return "too short for the header";
    }
    const int idLength = file[0];
    const int type = file[2];
    const int width = getU16(file, 12);
    const int height = getU16(file, 14);
    const int depth = file[16];
    const bool topDown = (file[17] & 0x20) != 0;
    if (file[1] != 0) {
        return "colour-mapped TGA files are not supported";
    }
    if (type != 2 && type != 10) {
        return "only true-colour TGA files (type 2 or 10) are supported";
    }
    if (depth != 24 && depth != 32) {
        return "only 24 and 32 bits per pixel are supported";
    }
    if (width == 0 || height == 0) {
        return "bad width or height";
    }
    if (static_cast<long long>(width) * height > 100000000LL) {
        return "picture too big";
    }
    const int bytesPerPixel = depth / 8;
    const int pixelCount = width * height;
    int pos = kTgaHeaderSize + idLength;

    Bytes pixels;
    pixels.reserve(pixelCount * bytesPerPixel);
    if (type == 2) {
        if (!hasBytes(file, pos, pixelCount * bytesPerPixel)) {
            return "the pixels are not inside the file";
        }
        pixels.assign(file.begin() + pos, file.begin() + pos + pixelCount * bytesPerPixel);
    } else {
        int done = 0;
        while (done < pixelCount) {
            if (!hasBytes(file, pos, 1)) {
                return "the file ends in the middle of the pixels";
            }
            const int header = file[pos];
            ++pos;
            const int count = (header & 0x7F) + 1;
            if (done + count > pixelCount) {
                return "a packet goes past the last pixel";
            }
            const bool isRun = (header & 0x80) != 0;
            const int dataBytes = isRun ? bytesPerPixel : count * bytesPerPixel;
            if (!hasBytes(file, pos, dataBytes)) {
                return "the file ends in the middle of a packet";
            }
            for (int k = 0; k < count; ++k) {
                const int from = isRun ? pos : pos + k * bytesPerPixel;
                for (int i = 0; i < bytesPerPixel; ++i) {
                    pixels.push_back(file[from + i]);
                }
            }
            pos += dataBytes;
            done += count;
        }
    }

    Image result(width, height);
    std::vector<std::uint8_t> alphaResult(pixelCount, 255);
    for (int row = 0; row < height; ++row) {
        const int y = topDown ? row : height - 1 - row;
        for (int x = 0; x < width; ++x) {
            const int at = (row * width + x) * bytesPerPixel;
            result.setPixel(x, y, Colour{pixels[at + 2], pixels[at + 1], pixels[at]});
            if (bytesPerPixel == 4) {
                alphaResult[y * width + x] = pixels[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline bool loadTGA(const std::string& fileName, Image& image,
                    std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodeTGA(file, image, alpha).empty();
}

#endif
