#ifndef ZLIB_H
#define ZLIB_H

#include <algorithm>
#include <cstdint>
#include <string>
#include "png.h"

const std::uint32_t kAdlerModulus = 65521;
const int kMaxStoredBlock = 65535;

inline std::uint32_t adler32(const Bytes& data, int from, int count) {
    std::uint32_t a = 1;
    std::uint32_t b = 0;
    for (int i = from; i < from + count; ++i) {
        a = (a + data[i]) % kAdlerModulus;
        b = (b + a) % kAdlerModulus;
    }
    return (b << 16) | a;
}

inline Bytes zlibStore(const Bytes& data) {
    Bytes out;
    out.push_back(0x78);
    out.push_back(0x01);
    const int total = static_cast<int>(data.size());
    int pos = 0;
    do {
        const int length = std::min(kMaxStoredBlock, total - pos);
        const bool last = (pos + length == total);
        out.push_back(last ? 0x01 : 0x00);
        putU16(out, static_cast<std::uint16_t>(length));
        putU16(out, static_cast<std::uint16_t>(~length & 0xFFFF));
        out.insert(out.end(), data.begin() + pos, data.begin() + pos + length);
        pos += length;
    } while (pos < total);
    putU32BE(out, adler32(data, 0, total));
    return out;
}

inline std::string zlibUnstore(const Bytes& z, Bytes& out) {
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
    int pos = 2;
    bool last = false;
    while (!last) {
        if (!hasBytes(z, pos, 1)) {
            return "the data ends before the last block";
        }
        const int header = z[pos];
        last = (header & 0x01) != 0;
        const int type = (header >> 1) & 0x03;
        if (type != 0) {
            return "compressed blocks are not supported yet";
        }
        if (!hasBytes(z, pos + 1, 4)) {
            return "a block header is cut off";
        }
        const int length = getU16(z, pos + 1);
        const int check = getU16(z, pos + 3);
        if (check != (~length & 0xFFFF)) {
            return "LEN and NLEN do not match";
        }
        pos += 5;
        if (!hasBytes(z, pos, length)) {
            return "a block is longer than the data";
        }
        out.insert(out.end(), z.begin() + pos, z.begin() + pos + length);
        pos += length;
    }
    if (!hasBytes(z, pos, 4)) {
        return "the Adler-32 is missing";
    }
    if (getU32BE(z, pos) != adler32(out, 0, static_cast<int>(out.size()))) {
        return "the Adler-32 is wrong";
    }
    return "";
}

#endif
