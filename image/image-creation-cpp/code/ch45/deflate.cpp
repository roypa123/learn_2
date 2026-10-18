#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "deflate.h"
#include "antialias.h"

const Bytes kOtherPng = {
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x08, 0x08, 0x02, 0x00, 0x00, 0x00, 0x4B, 0x6D, 0x29,
    0xDC, 0x00, 0x00, 0x00, 0x75, 0x49, 0x44, 0x41, 0x54, 0x78, 0xDA, 0x0D, 0xCB, 0x41, 0x01, 0x00,
    0x30, 0x08, 0x02, 0x40, 0xC3, 0x10, 0xC6, 0x32, 0x74, 0xA0, 0x82, 0x65, 0xCC, 0x40, 0x06, 0xCB,
    0xB0, 0xDD, 0xFF, 0xAA, 0x4A, 0x28, 0x77, 0x89, 0xE5, 0x29, 0x6D, 0xF9, 0x4A, 0x29, 0x57, 0xC1,
    0x80, 0x1A, 0x26, 0x34, 0xF0, 0x42, 0x07, 0x07, 0xAA, 0x6A, 0xA1, 0xDD, 0x2D, 0xB6, 0xA7, 0xB5,
    0xED, 0x6B, 0xA5, 0xFF, 0xA0, 0x41, 0x35, 0x4D, 0x6A, 0xE8, 0xA5, 0x8E, 0x0E, 0xFF, 0x18, 0x61,
    0xDC, 0x23, 0x8E, 0x67, 0xB4, 0xE3, 0x1B, 0x65, 0xFE, 0x58, 0x63, 0xD5, 0x6B, 0xAE, 0x66, 0xBD,
    0xAB, 0x5B, 0x67, 0xFF, 0x38, 0xE1, 0xDC, 0x27, 0x9E, 0xE7, 0xB4, 0xE7, 0x3B, 0xE5, 0xFE, 0x88,
    0x11, 0x75, 0xCC, 0x68, 0xE2, 0x8D, 0x2E, 0x4E, 0xF4, 0x00, 0x96, 0xAD, 0x68, 0x91, 0x8A, 0x0D,
    0x4C, 0xBF, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82};

std::string oneDecimal(double v) {
    const long long tenths = std::llround(v * 10.0);
    return std::to_string(tenths / 10) + "." + std::to_string(tenths % 10);
}

void printTokens(const std::string& text) {
    const Bytes data(text.begin(), text.end());
    std::cout << "\"" << text << "\":";
    for (const Lz77Token& t : findMatches(data, 64)) {
        if (t.length == 0) {
            std::cout << " '" << static_cast<char>(t.literal) << "'";
        } else {
            std::cout << " (" << t.length << ", " << t.distance << ")";
        }
    }
    std::cout << "\n";
}

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

void report(const char* label, const Bytes& z) {
    Bytes out;
    const std::string problem = zlibDecompress(z, out);
    std::cout << "  " << label << ": "
              << (problem.empty() ? "accepted, " + std::to_string(out.size()) + " bytes"
                                  : "refused (" + problem + ")")
              << "\n";
}

bool samePictures(const Image& a, const Image& b) {
    if (a.width() != b.width() || a.height() != b.height()) {
        return false;
    }
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            Colour p = a.getPixel(x, y);
            Colour q = b.getPixel(x, y);
            if (p.r != q.r || p.g != q.g || p.b != q.b) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    printTokens("AAAAAAAAAA");
    printTokens("ABRACADABRA ABRACADABRA");
    printTokens("blah blah blah blah!");

    const std::vector<int> litLengths = fixedLiteralLengths();
    const std::vector<int> litCodes = canonicalCodes(litLengths);
    const int symbols[8] = {0, 65, 143, 144, 255, 256, 257, 280};
    for (int s : symbols) {
        std::cout << "fixed code of symbol " << s << ": " << asBinary(litCodes[s], litLengths[s])
                  << "\n";
    }
    const int k = lengthIndex(11);
    const int d = distanceIndex(12);
    std::cout << "length 11 = symbol " << 257 + k << " + " << kLengthExtra[k] << " extra bit ("
              << 11 - kLengthBase[k] << "); distance 12 = distance code " << d << " + "
              << kDistanceExtra[d] << " extra bits (" << 12 - kDistanceBase[d] << ")\n";

    const std::string text = "ABRACADABRA ABRACADABRA";
    const Bytes data(text.begin(), text.end());
    const Bytes z = zlibCompress(data);
    printBytes("zlib:", z);
    Bytes back;
    std::string problem = zlibDecompress(z, back);
    std::cout << z.size() << " bytes instead of " << zlibStore(data).size() << " (stored); read back: "
              << (problem.empty() ? std::string(back.begin(), back.end()) : problem) << "\n";

    Image flag(300, 200);
    Image sky(300, 200);
    Image sunset(300, 200);
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
            sunset.setPixel(x, y, lerpColour(Colour{250, 120, 40}, Colour{80, 20, 120}, x / 299.0));
            blend.setPixel(x, y, Colour{static_cast<std::uint8_t>(x * 255 / 299),
                                        static_cast<std::uint8_t>(y * 255 / 199),
                                        static_cast<std::uint8_t>((x + y) * 255 / 498)});
            seed = seed * 1103515245u + 12345u;
            const std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Image* pictures[5] = {&flag, &sky, &sunset, &blend, &noise};
    const std::string names[5] = {"flag", "sky", "sunset", "blend", "noise"};
    std::cout << "\nfile sizes (BMP, PNG of Chapter 42, compressed PNG):\n";
    for (int i = 0; i < 5; ++i) {
        const int bmp = static_cast<int>(makeBmpBytes(*pictures[i]).size());
        const int png = static_cast<int>(makePngBytesCompressed(*pictures[i]).size());
        const std::string fileName = names[i] + ".png";
        Image loaded(0, 0);
        const bool ok = savePNGCompressed(*pictures[i], fileName) && loadPNGFull(fileName, loaded) &&
                        samePictures(*pictures[i], loaded);
        std::cout << "  " << names[i] << ": " << bmp << ", " << makePngBytes(*pictures[i]).size()
                  << ", " << png << " (" << oneDecimal(static_cast<double>(bmp) / png)
                  << " times smaller than BMP), read back " << (ok ? "the same" : "DIFFERENT") << "\n";
    }

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> diskAlpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4));
        }
    }
    Image diskBack(0, 0);
    std::vector<std::uint8_t> alphaBack;
    const bool diskOk = savePNGCompressed(disk, "disk.png", &diskAlpha) &&
                        loadPNGFull("disk.png", diskBack, &alphaBack) && alphaBack == diskAlpha;
    std::cout << "  disk (RGBA): Chapter 42 " << makePngBytes(disk, &diskAlpha).size() << ", now "
              << makePngBytesCompressed(disk, &diskAlpha).size() << ", alpha read back "
              << (diskOk ? "the same" : "DIFFERENT") << "\n";

    std::cout << "\na PNG made by another program (" << kOtherPng.size() << " bytes):\n";
    Image other(0, 0);
    std::cout << "  Chapter 42's decodePNG: " << decodePNG(kOtherPng, other) << "\n";
    PngInfo info;
    Bytes zdata;
    readPngStart(kOtherPng, info, zdata);
    BitReader r{&zdata, 16};
    const int lastBit = getBit(r);
    const int type = getBits(r, 2);
    const int hlit = getBits(r, 5);
    const int hdist = getBits(r, 5);
    const int hclen = getBits(r, 4);
    std::cout << "  zlib header " << hexByte(zdata[0]) << " " << hexByte(zdata[1]) << ", last block "
              << lastBit << ", block type " << type << ", " << hlit + 257 << " literal/length codes, "
              << hdist + 1 << " distance codes, " << hclen + 4 << " code length codes\n";
    problem = decodePNGFull(kOtherPng, other);
    std::cout << "  decodePNGFull: " << (problem.empty() ? "accepted" : problem) << ", "
              << other.width() << " x " << other.height() << " pixels\n";
    const Colour first = other.getPixel(0, 0);
    const Colour last = other.getPixel(7, 7);
    std::cout << "  pixel (0, 0) = " << static_cast<int>(first.r) << " " << static_cast<int>(first.g)
              << " " << static_cast<int>(first.b) << ", pixel (7, 7) = " << static_cast<int>(last.r)
              << " " << static_cast<int>(last.g) << " " << static_cast<int>(last.b) << "\n";
    std::cout << "  our savePNGCompressed makes it " << makePngBytesCompressed(other).size()
              << " bytes\n";

    std::cout << "\nbroken zlib data:\n";
    const Bytes hello = {'h', 'e', 'l', 'l', 'o'};
    const Bytes good = zlibCompress(hello);
    report("the good data", good);
    Bytes wrong = good;
    wrong[2] = static_cast<std::uint8_t>(wrong[2] | 0x06);
    report("block type 3", wrong);
    wrong = good;
    wrong.back() = static_cast<std::uint8_t>(wrong.back() ^ 0x01);
    report("Adler-32 changed", wrong);
    wrong = good;
    wrong.resize(5);
    report("cut after 5 bytes", wrong);
    BitWriter w;
    writeFixedBlock(w, std::vector<Lz77Token>{Lz77Token{0, 5, 3}}, true);
    wrong = Bytes{0x78, 0x01};
    wrong.insert(wrong.end(), w.bytes.begin(), w.bytes.end());
    report("a copy from 3 bytes back at the start", wrong);
    return 0;
}
