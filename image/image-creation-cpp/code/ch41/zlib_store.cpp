#include <iostream>
#include <string>
#include "zlib.h"

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

void printBytes(const char* label, const Bytes& b) {
    std::cout << label;
    for (std::uint8_t v : b) {
        std::cout << " " << hexByte(v);
    }
    std::cout << "\n";
}

void report(const char* label, const Bytes& z) {
    Bytes out;
    std::string problem = zlibUnstore(z, out);
    std::cout << "  " << label << ": "
              << (problem.empty() ? "accepted, " + std::to_string(out.size()) + " bytes"
                                  : "refused (" + problem + ")")
              << "\n";
}

int main() {
    Bytes wiki = bytesOf("Wiki");
    std::uint32_t a = 1;
    std::uint32_t b = 0;
    std::cout << "Adler-32 step by step for \"Wiki\":\n";
    for (std::uint8_t ch : wiki) {
        a = (a + ch) % kAdlerModulus;
        b = (b + a) % kAdlerModulus;
        std::cout << "  '" << static_cast<char>(ch) << "' (" << static_cast<int>(ch) << "): a = " << a
                  << ", b = " << b << "\n";
    }
    std::cout << "Adler-32 of \"Wiki\" = " << hex32(adler32(wiki, 0, 4)) << ", of \"Wikipedia\" = "
              << hex32(adler32(bytesOf("Wikipedia"), 0, 9)) << "\n";

    const int headers[3] = {0x7801, 0x789C, 0x78DA};
    for (int h : headers) {
        std::cout << "header " << hexByte(static_cast<std::uint8_t>(h >> 8))
                  << hexByte(static_cast<std::uint8_t>(h & 0xFF)) << " = " << h << " = 31 x "
                  << h / 31 << " remainder " << h % 31 << "\n";
    }

    Bytes hello = bytesOf("hello");
    Bytes packed = zlibStore(hello);
    printBytes("zlib of \"hello\":", packed);

    Bytes big(150000);
    for (int i = 0; i < 150000; ++i) {
        big[i] = static_cast<std::uint8_t>(i % 251);
    }
    Bytes bigPacked = zlibStore(big);
    Bytes back;
    std::string problem = zlibUnstore(bigPacked, back);
    std::cout << "150000 bytes stored in " << bigPacked.size() << " bytes, read back "
              << (problem.empty() && back == big ? "the same" : "DIFFERENT") << "\n";
    std::cout << "the second block starts with:";
    for (int i = 2 + 5 + kMaxStoredBlock; i < 2 + 5 + kMaxStoredBlock + 5; ++i) {
        std::cout << " " << hexByte(bigPacked[i]);
    }
    std::cout << "\n";
    Bytes empty;
    printBytes("zlib of nothing:", zlibStore(empty));

    std::cout << "broken zlib data:\n";
    report("the good data", packed);
    Bytes wrong = packed;
    wrong[1] = 0x02;
    report("header check broken", wrong);
    wrong = packed;
    wrong[2] = 0x03;
    report("block type 1", wrong);
    wrong = packed;
    wrong[5] = 0x00;
    report("NLEN wrong", wrong);
    wrong = packed;
    wrong.resize(10);
    report("cut short", wrong);
    wrong = packed;
    wrong[7] = 'j';
    report("one letter changed", wrong);

    Image tiny(3, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(0, 1, colours::white);
    tiny.setPixel(2, 1, colours::yellow);
    Bytes rows;
    for (int y = 0; y < tiny.height(); ++y) {
        rows.push_back(0);
        for (int x = 0; x < tiny.width(); ++x) {
            Colour c = tiny.getPixel(x, y);
            rows.push_back(c.r);
            rows.push_back(c.g);
            rows.push_back(c.b);
        }
    }
    printBytes("PNG rows of a 3 x 2 picture:", rows);
    printBytes("and stored with zlib:", zlibStore(rows));
    return 0;
}
