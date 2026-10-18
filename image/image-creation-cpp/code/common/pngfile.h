#ifndef PNGFILE_H
#define PNGFILE_H

#include <cstdint>
#include <string>
#include <vector>
#include "zlib.h"

inline Bytes makePngRows(const Image& image, const std::vector<std::uint8_t>* alpha) {
    Bytes rows;
    const int width = image.width();
    const bool withAlpha = alpha != nullptr;
    for (int y = 0; y < image.height(); ++y) {
        rows.push_back(0);
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            rows.push_back(c.r);
            rows.push_back(c.g);
            rows.push_back(c.b);
            if (withAlpha) {
                rows.push_back((*alpha)[y * width + x]);
            }
        }
    }
    return rows;
}

inline Bytes makePngBytes(const Image& image, const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bytesPerPixel = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bytesPerPixel * static_cast<long long>(width)) * height > 1000000000LL) {
        return file;
    }
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibStore(makePngRows(image, alpha)));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNG(const Image& image, const std::string& fileName,
                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytes(image, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline bool isKnownChunk(const std::string& type) {
    return type == "IHDR" || type == "IDAT" || type == "IEND" || type == "PLTE";
}

inline std::string decodePNG(const Bytes& file, Image& image,
                             std::vector<std::uint8_t>* alpha = nullptr) {
    std::vector<PngChunk> chunks;
    const std::string problem = listChunks(file, chunks);
    if (!problem.empty()) {
        return problem;
    }
    if (chunks.empty() || chunks[0].type != "IHDR" || chunks[0].length != 13) {
        return "the first chunk must be a 13-byte IHDR";
    }
    if (chunks.back().type != "IEND") {
        return "there is no IEND chunk";
    }
    Bytes zdata;
    for (const PngChunk& c : chunks) {
        if (!c.crcOk) {
            return "the " + c.type + " chunk has a wrong CRC";
        }
        const bool critical = c.type[0] >= 'A' && c.type[0] <= 'Z';
        if (critical && !isKnownChunk(c.type)) {
            return "unknown critical chunk " + c.type;
        }
        if (c.type == "IDAT") {
            zdata.insert(zdata.end(), file.begin() + c.dataStart,
                         file.begin() + c.dataStart + c.length);
        }
    }

    const int d = chunks[0].dataStart;
    const std::uint32_t width = getU32BE(file, d);
    const std::uint32_t height = getU32BE(file, d + 4);
    const int bitDepth = file[d + 8];
    const int colourType = file[d + 9];
    if (width == 0 || height == 0 || static_cast<long long>(width) * height > 100000000LL) {
        return "bad width or height";
    }
    if (bitDepth != 8 || (colourType != 2 && colourType != 6)) {
        return "only 8-bit RGB and RGBA pictures are supported";
    }
    if (file[d + 10] != 0 || file[d + 11] != 0 || file[d + 12] != 0) {
        return "unknown compression, filter or interlace method";
    }

    Bytes rows;
    const std::string zproblem = zlibUnstore(zdata, rows);
    if (!zproblem.empty()) {
        return "IDAT: " + zproblem;
    }
    const int w = static_cast<int>(width);
    const int h = static_cast<int>(height);
    const int bytesPerPixel = (colourType == 6) ? 4 : 3;
    const long long rowBytes = 1 + static_cast<long long>(bytesPerPixel) * w;
    if (static_cast<long long>(rows.size()) != rowBytes * h) {
        return "wrong amount of pixel data";
    }

    Image result(w, h);
    std::vector<std::uint8_t> alphaResult(w * h, 255);
    for (int y = 0; y < h; ++y) {
        const int start = static_cast<int>(y * rowBytes);
        if (rows[start] != 0) {
            return "row filters are not supported yet";
        }
        for (int x = 0; x < w; ++x) {
            const int at = start + 1 + x * bytesPerPixel;
            result.setPixel(x, y, Colour{rows[at], rows[at + 1], rows[at + 2]});
            if (bytesPerPixel == 4) {
                alphaResult[y * w + x] = rows[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline bool loadPNG(const std::string& fileName, Image& image,
                    std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNG(file, image, alpha).empty();
}

#endif
