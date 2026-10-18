#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "huffman.h"

std::string asBinary(int code, int length) {
    std::string s;
    for (int i = length - 1; i >= 0; --i) {
        s += ((code >> i) & 1) ? '1' : '0';
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

int main() {
    const std::string text = "ABRACADABRA";
    const Bytes data(text.begin(), text.end());
    const std::vector<long long> counts = countBytes(data);
    const std::vector<int> lengths = huffmanLengths(counts);
    const std::vector<int> codes = canonicalCodes(lengths);
    std::cout << "\"" << text << "\":\n";
    for (int s = 0; s < 256; ++s) {
        if (counts[s] > 0) {
            std::cout << "  '" << static_cast<char>(s) << "' count " << counts[s] << ", length "
                      << lengths[s] << ", code " << asBinary(codes[s], lengths[s]) << "\n";
        }
    }
    std::cout << "  " << codedBits(counts, lengths) << " bits instead of " << 8 * data.size()
              << "; the best possible is " << entropyBits(counts) << " bits\n";

    BitWriter w;
    std::string allBits;
    for (std::uint8_t v : data) {
        putCode(w, codes[v], lengths[v]);
        allBits += asBinary(codes[v], lengths[v]);
    }
    std::cout << "  the bits in order: " << allBits << "\n";
    printBytes("  packed into bytes:", w.bytes);

    BitWriter order;
    putCode(order, 6, 3);
    putBits(order, 5, 3);
    std::cout << "putCode(110, 3 bits) then putBits(5, 3 bits) gives the byte "
              << hexByte(order.bytes[0]) << "\n";

    const Bytes packed = huffmanCompress(data);
    Bytes back;
    std::string problem = huffmanDecompress(packed, back);
    const std::string result = problem.empty() ? std::string(back.begin(), back.end()) : problem;
    std::cout << "compressed: " << packed.size() << " bytes (4 + 256 + " << packed.size() - 260
              << "), decompressed: " << result << "\n";

    std::vector<int> bad(256, 0);
    bad['A'] = 1;
    bad['B'] = 1;
    bad['C'] = 1;
    std::vector<DecodeNode> tree;
    std::cout << "three codes of length 1: " << buildDecoder(bad, tree) << "\n";
    Bytes cut = packed;
    cut.pop_back();
    problem = huffmanDecompress(cut, back);
    std::cout << "the last byte missing: " << problem << "\n";

    Image flag(300, 200);
    Image sky(300, 200);
    Image blend(300, 200);
    Image noise(300, 200);
    unsigned int seed = 12345;
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            Colour c = colours::white;
            if (x < 100) {
                c = Colour{0, 85, 164};
            } else if (x >= 200) {
                c = Colour{239, 65, 53};
            }
            flag.setPixel(x, y, c);
            sky.setPixel(x, y, lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, y / 199.0));
            blend.setPixel(x, y, Colour{static_cast<std::uint8_t>(x * 255 / 299),
                                        static_cast<std::uint8_t>(y * 255 / 199),
                                        static_cast<std::uint8_t>((x + y) * 255 / 498)});
            seed = seed * 1103515245u + 12345u;
            const std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Image* pictures[4] = {&flag, &sky, &blend, &noise};
    const std::string names[4] = {"flag", "sky", "blend", "noise"};
    std::cout << "\nthe PNG rows of each picture (180200 bytes), Huffman-coded:\n";
    for (int i = 0; i < 4; ++i) {
        const Bytes plain = makePngRows(*pictures[i], nullptr);
        const Bytes filtered = filterScanlines(plain, 900, 3, kFilterBest);
        const Bytes small = huffmanCompress(filtered);
        problem = huffmanDecompress(small, back);
        const bool same = problem.empty() && back == filtered;
        const long long limit = std::llround(std::ceil(entropyBits(countBytes(filtered)) / 8.0));
        std::cout << "  " << names[i] << ": no filter " << huffmanCompress(plain).size()
                  << ", best filters " << small.size() << " bytes (limit " << limit + 260 << "), "
                  << (same ? "decoded the same" : "DECODE FAILED") << "\n";
    }
    return 0;
}
