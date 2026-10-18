#include <iostream>
#include <string>
#include <vector>
#include "tga.h"
#include "antialias.h"

void printBytes(const char* label, const Bytes& b, int from, int count) {
    std::cout << label;
    for (int i = from; i < from + count && i < static_cast<int>(b.size()); ++i) {
        std::cout << " " << hexByte(b[i]);
    }
    std::cout << "\n";
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
    Image tiny(4, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(3, 0, colours::white);
    Bytes plain = makeTgaBytes(tiny, nullptr, false);
    std::cout << "a 4 x 2 TGA is " << plain.size() << " bytes\n";
    printBytes("header:", plain, 0, kTgaHeaderSize);
    printBytes("top row:", plain, kTgaHeaderSize, 12);

    Bytes row;
    const Colour rowColours[8] = {colours::red,  colours::red,  colours::red,  colours::red,
                                  colours::green, colours::blue, colours::blue, colours::blue};
    for (Colour c : rowColours) {
        row.push_back(c.b);
        row.push_back(c.g);
        row.push_back(c.r);
    }
    Bytes packed;
    encodeRleRow(packed, row, 3);
    std::cout << "8 pixels, " << row.size() << " bytes, packed into " << packed.size() << ":\n";
    printBytes(" ", packed, 0, static_cast<int>(packed.size()));

    Image flag(300, 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            Colour c = colours::white;
            if (x < 100) {
                c = Colour{0, 85, 164};
            } else if (x >= 200) {
                c = Colour{239, 65, 53};
            }
            flag.setPixel(x, y, c);
        }
    }
    Image noise(300, 200);
    unsigned int seed = 12345;
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            seed = seed * 1103515245u + 12345u;
            std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }
    Image sky(300, 200);
    for (int y = 0; y < 200; ++y) {
        Colour c = lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, y / 199.0);
        for (int x = 0; x < 300; ++x) {
            sky.setPixel(x, y, c);
        }
    }

    const Image* pictures[3] = {&flag, &sky, &noise};
    const std::string names[3] = {"flag", "sky", "noise"};
    for (int i = 0; i < 3; ++i) {
        Bytes raw = makeTgaBytes(*pictures[i], nullptr, false);
        Bytes rle = makeTgaBytes(*pictures[i], nullptr, true);
        Image back(0, 0);
        std::string problem = decodeTGA(rle, back);
        bool same = problem.empty() && samePictures(*pictures[i], back);
        std::cout << names[i] << ": uncompressed " << raw.size() << " bytes, RLE " << rle.size()
                  << " bytes, read back " << (same ? "the same" : "DIFFERENT") << "\n";
        if (!saveTGA(*pictures[i], names[i] + ".tga", true)) {
            std::cout << "could not write " << names[i] << ".tga\n";
            return 1;
        }
    }

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> alpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            double coverage = circleCoverage(100.0, 100.0, 80.0, x, y, 4);
            alpha[y * 200 + x] = toByte(coverage);
        }
    }
    if (!saveTGA(disk, "disk.tga", true, &alpha)) {
        std::cout << "could not write disk.tga\n";
        return 1;
    }
    Image diskBack(0, 0);
    std::vector<std::uint8_t> alphaBack;
    if (!loadTGA("disk.tga", diskBack, &alphaBack)) {
        std::cout << "could not load disk.tga\n";
        return 1;
    }
    std::cout << "disk.tga: alpha at the centre " << static_cast<int>(alphaBack[100 * 200 + 100])
              << ", at a corner " << static_cast<int>(alphaBack[0]) << ", alpha the same: "
              << (alphaBack == alpha ? "yes" : "no") << "\n";

    std::cout << "broken files:\n";
    Bytes good = makeTgaBytes(tiny, nullptr, true);
    Bytes tests[6] = {good, good, good, good, good, good};
    tests[1][2] = 1;
    tests[2][16] = 16;
    tests[3][12] = 0;
    tests[3][13] = 0;
    tests[4].resize(tests[4].size() - 2);
    tests[5][kTgaHeaderSize] = 0xFF;
    const char* labels[6] = {"the good file", "type 1", "16 bits per pixel", "width 0",
                             "last 2 bytes missing", "a run of 128 pixels"};
    for (int i = 0; i < 6; ++i) {
        Image ignored(0, 0);
        std::string problem = decodeTGA(tests[i], ignored);
        std::cout << "  " << labels[i] << ": "
                  << (problem.empty() ? "accepted" : "refused (" + problem + ")") << "\n";
    }
    return 0;
}
