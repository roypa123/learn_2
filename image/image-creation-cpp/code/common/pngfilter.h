#ifndef PNGFILTER_H
#define PNGFILTER_H

#include <cstdint>
#include <string>
#include <vector>
#include "pngfile.h"

const int kFilterNone = 0;
const int kFilterSub = 1;
const int kFilterUp = 2;
const int kFilterAverage = 3;
const int kFilterPaeth = 4;
const int kFilterBest = 5;

inline int absInt(int v) {
    return (v < 0) ? -v : v;
}

inline int paethPredictor(int a, int b, int c) {
    const int p = a + b - c;
    const int pa = absInt(p - a);
    const int pb = absInt(p - b);
    const int pc = absInt(p - c);
    if (pa <= pb && pa <= pc) {
        return a;
    }
    if (pb <= pc) {
        return b;
    }
    return c;
}

inline int predictByte(int filter, int a, int b, int c) {
    if (filter == kFilterSub) {
        return a;
    }
    if (filter == kFilterUp) {
        return b;
    }
    if (filter == kFilterAverage) {
        return (a + b) / 2;
    }
    if (filter == kFilterPaeth) {
        return paethPredictor(a, b, c);
    }
    return 0;
}

inline Bytes filterRow(int filter, const Bytes& row, const Bytes& above, int bpp) {
    Bytes out(row.size());
    for (int i = 0; i < static_cast<int>(row.size()); ++i) {
        const int a = (i >= bpp) ? row[i - bpp] : 0;
        const int b = above[i];
        const int c = (i >= bpp) ? above[i - bpp] : 0;
        out[i] = static_cast<std::uint8_t>(row[i] - predictByte(filter, a, b, c));
    }
    return out;
}

inline Bytes unfilterRow(int filter, const Bytes& filtered, const Bytes& above, int bpp) {
    Bytes row(filtered.size());
    for (int i = 0; i < static_cast<int>(filtered.size()); ++i) {
        const int a = (i >= bpp) ? row[i - bpp] : 0;
        const int b = above[i];
        const int c = (i >= bpp) ? above[i - bpp] : 0;
        row[i] = static_cast<std::uint8_t>(filtered[i] + predictByte(filter, a, b, c));
    }
    return row;
}

inline long long rowScore(const Bytes& filtered) {
    long long sum = 0;
    for (std::uint8_t v : filtered) {
        sum += (v < 128) ? v : 256 - v;
    }
    return sum;
}

inline int bestFilter(const Bytes& row, const Bytes& above, int bpp) {
    int best = kFilterNone;
    long long bestScore = rowScore(row);
    for (int f = kFilterSub; f <= kFilterPaeth; ++f) {
        const long long score = rowScore(filterRow(f, row, above, bpp));
        if (score < bestScore) {
            best = f;
            bestScore = score;
        }
    }
    return best;
}

inline Bytes filterScanlines(const Bytes& rows, int rowLength, int bpp, int mode) {
    Bytes out;
    Bytes above(rowLength, 0);
    const int height = static_cast<int>(rows.size()) / (1 + rowLength);
    for (int y = 0; y < height; ++y) {
        const int start = y * (1 + rowLength) + 1;
        const Bytes row(rows.begin() + start, rows.begin() + start + rowLength);
        const int filter = (mode == kFilterBest) ? bestFilter(row, above, bpp) : mode;
        const Bytes filtered = filterRow(filter, row, above, bpp);
        out.push_back(static_cast<std::uint8_t>(filter));
        out.insert(out.end(), filtered.begin(), filtered.end());
        above = row;
    }
    return out;
}

inline std::string unfilterScanlines(const Bytes& rows, int rowLength, int bpp, Bytes& out) {
    out.clear();
    Bytes above(rowLength, 0);
    const int height = static_cast<int>(rows.size()) / (1 + rowLength);
    for (int y = 0; y < height; ++y) {
        const int start = y * (1 + rowLength) + 1;
        const int filter = rows[start - 1];
        if (filter > kFilterPaeth) {
            return "unknown filter type " + std::to_string(filter);
        }
        const Bytes filtered(rows.begin() + start, rows.begin() + start + rowLength);
        const Bytes row = unfilterRow(filter, filtered, above, bpp);
        out.push_back(0);
        out.insert(out.end(), row.begin(), row.end());
        above = row;
    }
    return "";
}

inline Bytes makePngBytesFiltered(const Image& image, int mode,
                                  const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0 || mode < kFilterNone || mode > kFilterBest) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bpp = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bpp * static_cast<long long>(width)) * height > 1000000000LL) {
        return file;
    }
    const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, mode);
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibStore(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNGFiltered(const Image& image, const std::string& fileName, int mode,
                            const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytesFiltered(image, mode, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

struct PngInfo {
    int width = 0;
    int height = 0;
    int bytesPerPixel = 0;
};

inline std::string readPngStart(const Bytes& file, PngInfo& info, Bytes& zdata) {
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
    zdata.clear();
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
    info.width = static_cast<int>(width);
    info.height = static_cast<int>(height);
    info.bytesPerPixel = (colourType == 6) ? 4 : 3;
    return "";
}

inline std::string pngPixels(const PngInfo& info, const Bytes& rows, Image& image,
                             std::vector<std::uint8_t>* alpha) {
    const int w = info.width;
    const int h = info.height;
    const int bpp = info.bytesPerPixel;
    const long long rowBytes = 1 + static_cast<long long>(bpp) * w;
    if (static_cast<long long>(rows.size()) != rowBytes * h) {
        return "wrong amount of pixel data";
    }
    Bytes plain;
    const std::string problem = unfilterScanlines(rows, bpp * w, bpp, plain);
    if (!problem.empty()) {
        return problem;
    }
    Image result(w, h);
    std::vector<std::uint8_t> alphaResult(w * h, 255);
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            const int at = static_cast<int>(y * rowBytes) + 1 + x * bpp;
            result.setPixel(x, y, Colour{plain[at], plain[at + 1], plain[at + 2]});
            if (bpp == 4) {
                alphaResult[y * w + x] = plain[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline std::string decodePNGFiltered(const Bytes& file, Image& image,
                                     std::vector<std::uint8_t>* alpha = nullptr) {
    PngInfo info;
    Bytes zdata;
    std::string problem = readPngStart(file, info, zdata);
    if (!problem.empty()) {
        return problem;
    }
    Bytes rows;
    problem = zlibUnstore(zdata, rows);
    if (!problem.empty()) {
        return "IDAT: " + problem;
    }
    return pngPixels(info, rows, image, alpha);
}

inline bool loadPNGFiltered(const std::string& fileName, Image& image,
                            std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNGFiltered(file, image, alpha).empty();
}

#endif
