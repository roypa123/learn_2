#ifndef BYTES_H
#define BYTES_H

#include <cstdint>
#include <string>
#include <vector>
#include "image.h"

using Bytes = std::vector<std::uint8_t>;

inline void putU16(Bytes& out, std::uint16_t v) {
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
}

inline void putU32(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
}

inline void putS32(Bytes& out, std::int32_t v) {
    putU32(out, static_cast<std::uint32_t>(v));
}

inline std::uint16_t getU16(const Bytes& in, int pos) {
    return static_cast<std::uint16_t>(in[pos] | (in[pos + 1] << 8));
}

inline std::uint32_t getU32(const Bytes& in, int pos) {
    return static_cast<std::uint32_t>(in[pos]) | (static_cast<std::uint32_t>(in[pos + 1]) << 8) |
           (static_cast<std::uint32_t>(in[pos + 2]) << 16) |
           (static_cast<std::uint32_t>(in[pos + 3]) << 24);
}

inline std::int32_t getS32(const Bytes& in, int pos) {
    return static_cast<std::int32_t>(getU32(in, pos));
}

inline bool hasBytes(const Bytes& in, int pos, int count) {
    return pos >= 0 && count >= 0 && pos + count <= static_cast<int>(in.size());
}

inline std::string hexByte(std::uint8_t b) {
    const char digits[] = "0123456789ABCDEF";
    std::string s;
    s += digits[b >> 4];
    s += digits[b & 0x0F];
    return s;
}

inline int bmpRowSize(int width) {
    return (width * 3 + 3) / 4 * 4;
}

#endif
