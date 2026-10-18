#ifndef PNG_H
#define PNG_H

#include <array>
#include <cstdint>
#include <string>
#include <vector>
#include "tga.h"

inline void putU32BE(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
}

inline std::uint32_t getU32BE(const Bytes& in, int pos) {
    return (static_cast<std::uint32_t>(in[pos]) << 24) |
           (static_cast<std::uint32_t>(in[pos + 1]) << 16) |
           (static_cast<std::uint32_t>(in[pos + 2]) << 8) | static_cast<std::uint32_t>(in[pos + 3]);
}

inline std::uint32_t crc32Bitwise(const Bytes& data, int from, int count) {
    std::uint32_t crc = 0xFFFFFFFFu;
    for (int i = from; i < from + count; ++i) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; ++bit) {
            if (crc & 1u) {
                crc = (crc >> 1) ^ 0xEDB88320u;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFFu;
}

inline std::array<std::uint32_t, 256> makeCrcTable() {
    std::array<std::uint32_t, 256> table{};
    for (std::uint32_t n = 0; n < 256; ++n) {
        std::uint32_t c = n;
        for (int bit = 0; bit < 8; ++bit) {
            c = (c & 1u) ? ((c >> 1) ^ 0xEDB88320u) : (c >> 1);
        }
        table[n] = c;
    }
    return table;
}

inline const std::array<std::uint32_t, 256>& crcTable() {
    static const std::array<std::uint32_t, 256> table = makeCrcTable();
    return table;
}

inline std::uint32_t crc32(const Bytes& data, int from, int count) {
    const std::array<std::uint32_t, 256>& table = crcTable();
    std::uint32_t crc = 0xFFFFFFFFu;
    for (int i = from; i < from + count; ++i) {
        crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFFu;
}

inline void appendPngSignature(Bytes& out) {
    const std::uint8_t signature[8] = {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A};
    out.insert(out.end(), signature, signature + 8);
}

inline void appendChunk(Bytes& out, const std::string& type, const Bytes& data) {
    putU32BE(out, static_cast<std::uint32_t>(data.size()));
    const int typeStart = static_cast<int>(out.size());
    for (char ch : type) {
        out.push_back(static_cast<std::uint8_t>(ch));
    }
    out.insert(out.end(), data.begin(), data.end());
    putU32BE(out, crc32(out, typeStart, 4 + static_cast<int>(data.size())));
}

inline Bytes makeIhdr(int width, int height, bool withAlpha) {
    Bytes data;
    putU32BE(data, static_cast<std::uint32_t>(width));
    putU32BE(data, static_cast<std::uint32_t>(height));
    data.push_back(8);
    data.push_back(withAlpha ? 6 : 2);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    return data;
}

struct PngChunk {
    std::string type;
    int dataStart = 0;
    int length = 0;
    bool crcOk = false;
};

inline std::string listChunks(const Bytes& file, std::vector<PngChunk>& chunks) {
    chunks.clear();
    const std::uint8_t signature[8] = {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A};
    if (file.size() > 2147483647u || !hasBytes(file, 0, 8)) {
        return "too short for the signature";
    }
    for (int i = 0; i < 8; ++i) {
        if (file[i] != signature[i]) {
            return "no PNG signature";
        }
    }
    int pos = 8;
    while (pos < static_cast<int>(file.size())) {
        if (!hasBytes(file, pos, 8)) {
            return "a chunk header is cut off";
        }
        const std::uint32_t length = getU32BE(file, pos);
        if (static_cast<long long>(pos) + 12 + length > static_cast<long long>(file.size())) {
            return "a chunk is longer than the file";
        }
        PngChunk chunk;
        for (int i = 0; i < 4; ++i) {
            chunk.type += static_cast<char>(file[pos + 4 + i]);
        }
        chunk.dataStart = pos + 8;
        chunk.length = static_cast<int>(length);
        const std::uint32_t stored = getU32BE(file, chunk.dataStart + chunk.length);
        chunk.crcOk = (stored == crc32(file, pos + 4, 4 + chunk.length));
        chunks.push_back(chunk);
        pos = chunk.dataStart + chunk.length + 4;
        if (chunk.type == "IEND") {
            break;
        }
    }
    return "";
}

#endif
