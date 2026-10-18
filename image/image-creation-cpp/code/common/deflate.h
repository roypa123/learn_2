#ifndef DEFLATE_H
#define DEFLATE_H

#include <algorithm>
#include <array>
#include <cstdint>
#include <string>
#include <vector>
#include "huffman.h"

const int kMinMatch = 3;
const int kMaxMatch = 258;
const int kWindowSize = 32768;
const int kEndOfBlock = 256;
const int kMaxInflated = 1000000000;

const std::array<int, 29> kLengthBase = {3,  4,  5,  6,  7,  8,  9,  10, 11, 13,  15,  17,  19,  23, 27,
                                         31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258};
const std::array<int, 29> kLengthExtra = {0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2,
                                          2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0};
const std::array<int, 30> kDistanceBase = {1, 2, 3, 4, 5, 7, 9, 13, 17, 25,
                                           33, 49, 65, 97, 129, 193, 257, 385, 513, 769,
                                           1025, 1537, 2049, 3073, 4097,
                                           6145, 8193, 12289, 16385, 24577};
const std::array<int, 30> kDistanceExtra = {0, 0, 0, 0, 1, 1, 2, 2,  3,  3,  4,  4,  5,  5,  6,
                                            6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13};
const std::array<int, 19> kCodeLengthOrder = {16, 17, 18, 0, 8, 7, 9, 6, 10, 5,
                                              11, 4,  12, 3, 13, 2, 14, 1, 15};

struct Lz77Token {
    int literal = 0;
    int length = 0;
    int distance = 0;
};

inline int hash3(const Bytes& data, int i) {
    return ((data[i] << 10) ^ (data[i + 1] << 5) ^ data[i + 2]) & (kWindowSize - 1);
}

inline std::vector<Lz77Token> findMatches(const Bytes& data, int maxTries) {
    std::vector<Lz77Token> tokens;
    const int n = static_cast<int>(data.size());
    std::vector<int> head(kWindowSize, -1);
    std::vector<int> previous(n, -1);
    int i = 0;
    while (i < n) {
        int bestLength = 0;
        int bestDistance = 0;
        if (i + kMinMatch <= n) {
            const int maxLength = std::min(kMaxMatch, n - i);
            int candidate = head[hash3(data, i)];
            int tries = 0;
            while (candidate >= 0 && i - candidate <= kWindowSize && tries < maxTries) {
                int length = 0;
                while (length < maxLength && data[candidate + length] == data[i + length]) {
                    ++length;
                }
                if (length > bestLength) {
                    bestLength = length;
                    bestDistance = i - candidate;
                }
                if (bestLength == maxLength) {
                    break;
                }
                candidate = previous[candidate];
                ++tries;
            }
        }
        int step = 1;
        if (bestLength >= kMinMatch) {
            tokens.push_back(Lz77Token{0, bestLength, bestDistance});
            step = bestLength;
        } else {
            tokens.push_back(Lz77Token{data[i], 0, 0});
        }
        for (int k = i; k < i + step; ++k) {
            if (k + kMinMatch <= n) {
                const int h = hash3(data, k);
                previous[k] = head[h];
                head[h] = k;
            }
        }
        i += step;
    }
    return tokens;
}

inline int lengthIndex(int length) {
    int k = 28;
    while (kLengthBase[k] > length) {
        --k;
    }
    return k;
}

inline int distanceIndex(int distance) {
    int k = 29;
    while (kDistanceBase[k] > distance) {
        --k;
    }
    return k;
}

inline std::vector<int> fixedLiteralLengths() {
    std::vector<int> lengths(288, 8);
    for (int s = 144; s < 256; ++s) {
        lengths[s] = 9;
    }
    for (int s = 256; s < 280; ++s) {
        lengths[s] = 7;
    }
    return lengths;
}

inline std::vector<int> fixedDistanceLengths() {
    return std::vector<int>(30, 5);
}

inline void writeFixedBlock(BitWriter& w, const std::vector<Lz77Token>& tokens, bool last) {
    const std::vector<int> litLengths = fixedLiteralLengths();
    const std::vector<int> litCodes = canonicalCodes(litLengths);
    const std::vector<int> distCodes = canonicalCodes(fixedDistanceLengths());
    putBits(w, last ? 1 : 0, 1);
    putBits(w, 1, 2);
    for (const Lz77Token& t : tokens) {
        if (t.length == 0) {
            putCode(w, litCodes[t.literal], litLengths[t.literal]);
            continue;
        }
        const int k = lengthIndex(t.length);
        putCode(w, litCodes[257 + k], litLengths[257 + k]);
        putBits(w, t.length - kLengthBase[k], kLengthExtra[k]);
        const int d = distanceIndex(t.distance);
        putCode(w, distCodes[d], 5);
        putBits(w, t.distance - kDistanceBase[d], kDistanceExtra[d]);
    }
    putCode(w, litCodes[kEndOfBlock], litLengths[kEndOfBlock]);
}

inline Bytes deflateFixed(const Bytes& data) {
    BitWriter w;
    writeFixedBlock(w, findMatches(data, 64), true);
    return w.bytes;
}

inline Bytes zlibCompress(const Bytes& data) {
    const Bytes stored = zlibStore(data);
    const Bytes packed = deflateFixed(data);
    if (packed.size() + 6 >= stored.size()) {
        return stored;
    }
    Bytes z = {0x78, 0x01};
    z.insert(z.end(), packed.begin(), packed.end());
    putU32BE(z, adler32(data, 0, static_cast<int>(data.size())));
    return z;
}

inline std::string inflateCodes(BitReader& r, const std::vector<DecodeNode>& litTree,
                                const std::vector<DecodeNode>& distTree, Bytes& out) {
    while (true) {
        const int s = decodeSymbol(r, litTree);
        if (s < 0) {
            return "a bad literal or length code";
        }
        if (s < 256) {
            out.push_back(static_cast<std::uint8_t>(s));
            if (static_cast<long long>(out.size()) > kMaxInflated) {
                return "too much data";
            }
            continue;
        }
        if (s == kEndOfBlock) {
            return "";
        }
        if (s - 257 >= 29) {
            return "a bad length code";
        }
        const int k = s - 257;
        const int extra = getBits(r, kLengthExtra[k]);
        if (extra < 0) {
            return "the data ends inside a match";
        }
        const int d = decodeSymbol(r, distTree);
        if (d < 0) {
            return "a bad distance code";
        }
        const int dextra = getBits(r, kDistanceExtra[d]);
        if (dextra < 0) {
            return "the data ends inside a match";
        }
        const int length = kLengthBase[k] + extra;
        const int distance = kDistanceBase[d] + dextra;
        if (distance > static_cast<int>(out.size())) {
            return "a match reaches back before the start";
        }
        if (static_cast<long long>(out.size()) + length > kMaxInflated) {
            return "too much data";
        }
        const int from = static_cast<int>(out.size()) - distance;
        for (int i = 0; i < length; ++i) {
            const std::uint8_t b = out[from + i];
            out.push_back(b);
        }
    }
}

inline std::string readDynamicTrees(BitReader& r, std::vector<DecodeNode>& litTree,
                                    std::vector<DecodeNode>& distTree) {
    const int hlit = getBits(r, 5);
    const int hdist = getBits(r, 5);
    const int hclen = getBits(r, 4);
    if (hlit < 0 || hdist < 0 || hclen < 0) {
        return "the data ends inside a block header";
    }
    const int literalCount = hlit + 257;
    const int distanceCount = hdist + 1;
    if (literalCount > 286 || distanceCount > 30) {
        return "too many codes in a block header";
    }
    std::vector<int> lengthLengths(19, 0);
    for (int i = 0; i < hclen + 4; ++i) {
        const int v = getBits(r, 3);
        if (v < 0) {
            return "the data ends inside a block header";
        }
        lengthLengths[kCodeLengthOrder[i]] = v;
    }
    std::vector<DecodeNode> lengthTree;
    std::string problem = buildDecoder(lengthLengths, lengthTree);
    if (!problem.empty()) {
        return "code length codes: " + problem;
    }
    std::vector<int> lengths;
    const int total = literalCount + distanceCount;
    while (static_cast<int>(lengths.size()) < total) {
        const int s = decodeSymbol(r, lengthTree);
        if (s < 0) {
            return "a bad code length code";
        }
        if (s < 16) {
            lengths.push_back(s);
            continue;
        }
        int value = 0;
        int extraBits = 7;
        int base = 11;
        if (s == 16) {
            if (lengths.empty()) {
                return "a repeat with nothing to repeat";
            }
            value = lengths.back();
            extraBits = 2;
            base = 3;
        } else if (s == 17) {
            extraBits = 3;
            base = 3;
        }
        const int extra = getBits(r, extraBits);
        if (extra < 0) {
            return "the data ends inside a block header";
        }
        const int repeat = base + extra;
        if (static_cast<int>(lengths.size()) + repeat > total) {
            return "a bad repeat of code lengths";
        }
        lengths.insert(lengths.end(), repeat, value);
    }
    if (lengths[kEndOfBlock] == 0) {
        return "there is no end-of-block code";
    }
    const std::vector<int> litLengths(lengths.begin(), lengths.begin() + literalCount);
    const std::vector<int> distLengths(lengths.begin() + literalCount, lengths.end());
    problem = buildDecoder(litLengths, litTree);
    if (problem.empty()) {
        problem = buildDecoder(distLengths, distTree);
    }
    return problem;
}

inline std::string zlibDecompress(const Bytes& z, Bytes& out) {
    out.clear();
    if (z.size() > 2147483647u || !hasBytes(z, 0, 2)) {
        return "too short for the zlib header";
    }
    const int cmf = z[0];
    const int flg = z[1];
    if ((cmf & 0x0F) != 8) {
        return "not deflate data";
    }
    if ((cmf * 256 + flg) % 31 != 0) {
        return "the header check (% 31) fails";
    }
    if ((flg & 0x20) != 0) {
        return "a preset dictionary is not supported";
    }
    std::vector<DecodeNode> fixedLit;
    std::vector<DecodeNode> fixedDist;
    buildDecoder(fixedLiteralLengths(), fixedLit);
    buildDecoder(fixedDistanceLengths(), fixedDist);
    BitReader r{&z, 16};
    bool last = false;
    while (!last) {
        const int lastBit = getBit(r);
        const int type = getBits(r, 2);
        if (lastBit < 0 || type < 0) {
            return "the data ends before the last block";
        }
        last = (lastBit == 1);
        std::string problem;
        if (type == 0) {
            r.bit = (r.bit + 7) / 8 * 8;
            const int pos = static_cast<int>(r.bit / 8);
            if (!hasBytes(z, pos, 4)) {
                return "a block header is cut off";
            }
            const int length = getU16(z, pos);
            if (getU16(z, pos + 2) != (~length & 0xFFFF)) {
                return "LEN and NLEN do not match";
            }
            if (!hasBytes(z, pos + 4, length)) {
                return "a block is longer than the data";
            }
            out.insert(out.end(), z.begin() + pos + 4, z.begin() + pos + 4 + length);
            r.bit += 8LL * (4 + length);
        } else if (type == 1) {
            problem = inflateCodes(r, fixedLit, fixedDist, out);
        } else if (type == 2) {
            std::vector<DecodeNode> litTree;
            std::vector<DecodeNode> distTree;
            problem = readDynamicTrees(r, litTree, distTree);
            if (problem.empty()) {
                problem = inflateCodes(r, litTree, distTree, out);
            }
        } else {
            return "block type 3 does not exist";
        }
        if (!problem.empty()) {
            return problem;
        }
    }
    const int pos = static_cast<int>((r.bit + 7) / 8);
    if (!hasBytes(z, pos, 4)) {
        return "the Adler-32 is missing";
    }
    if (getU32BE(z, pos) != adler32(out, 0, static_cast<int>(out.size()))) {
        return "the Adler-32 is wrong";
    }
    return "";
}

inline Bytes makePngBytesCompressed(const Image& image,
                                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bpp = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bpp * static_cast<long long>(width)) * height > 100000000LL) {
        return file;
    }
    const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, kFilterBest);
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibCompress(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNGCompressed(const Image& image, const std::string& fileName,
                              const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytesCompressed(image, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline std::string decodePNGFull(const Bytes& file, Image& image,
                                 std::vector<std::uint8_t>* alpha = nullptr) {
    PngInfo info;
    Bytes zdata;
    std::string problem = readPngStart(file, info, zdata);
    if (!problem.empty()) {
        return problem;
    }
    Bytes rows;
    problem = zlibDecompress(zdata, rows);
    if (!problem.empty()) {
        return "IDAT: " + problem;
    }
    return pngPixels(info, rows, image, alpha);
}

inline bool loadPNGFull(const std::string& fileName, Image& image,
                        std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNGFull(file, image, alpha).empty();
}

#endif
