#include <iostream>
#include <string>
#include <vector>
#include "png.h"

Bytes bytesOf(const std::string& text) {
    return Bytes(text.begin(), text.end());
}

std::string hex32(std::uint32_t v) {
    Bytes four;
    putU32BE(four, v);
    std::string s;
    for (std::uint8_t b : four) {
        s += hexByte(b);
    }
    return s;
}

int simpleSum(const Bytes& data) {
    int sum = 0;
    for (std::uint8_t b : data) {
        sum += b;
    }
    return sum % 256;
}

void printChunks(const char* label, const Bytes& file) {
    std::vector<PngChunk> chunks;
    std::string problem = listChunks(file, chunks);
    std::cout << label << ":";
    for (const PngChunk& c : chunks) {
        std::cout << " " << c.type << " (" << c.length << " bytes, CRC "
                  << (c.crcOk ? "ok" : "WRONG") << ")";
    }
    if (!problem.empty()) {
        std::cout << " -- " << problem;
    }
    std::cout << "\n";
}

int main() {
    Bytes check = bytesOf("123456789");
    std::cout << "CRC-32 of \"123456789\": bit by bit " << hex32(crc32Bitwise(check, 0, 9))
              << ", with the table " << hex32(crc32(check, 0, 9)) << "\n";
    Bytes iend = bytesOf("IEND");
    std::cout << "CRC-32 of \"IEND\": " << hex32(crc32(iend, 0, 4)) << "\n";
    const std::array<std::uint32_t, 256>& table = crcTable();
    std::cout << "table[1] = " << hex32(table[1]) << ", table[128] = " << hex32(table[128])
              << ", table[255] = " << hex32(table[255]) << "\n";

    Bytes ab = bytesOf("AB");
    Bytes ba = bytesOf("BA");
    std::cout << "simple sum: AB " << simpleSum(ab) << ", BA " << simpleSum(ba)
              << "; CRC-32: AB " << hex32(crc32(ab, 0, 2)) << ", BA " << hex32(crc32(ba, 0, 2))
              << "\n";

    Bytes file;
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(4, 2, false));
    appendChunk(file, "IEND", Bytes{});
    std::cout << "signature + IHDR + IEND = " << file.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(file.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(file.size()); ++j) {
            std::cout << " " << hexByte(file[j]);
        }
        std::cout << "\n";
    }

    printChunks("the chunks", file);
    Bytes damaged = file;
    damaged[19] = 5;
    printChunks("width changed to 5", damaged);
    Bytes cut = file;
    cut.resize(cut.size() - 6);
    printChunks("last 6 bytes missing", cut);
    Bytes notPng = file;
    notPng[1] = 'Q';
    printChunks("signature changed", notPng);
    return 0;
}
