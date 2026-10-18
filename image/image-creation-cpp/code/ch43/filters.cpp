#include <cmath>
#include <iostream>
#include <string>
#include "pngfilter.h"

const char* const kFilterNames[6] = {"None", "Sub", "Up", "Average", "Paeth", "Best"};

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
}

std::string oneDecimal(double v) {
    const long long tenths = std::llround(v * 10.0);
    return std::to_string(tenths / 10) + "." + std::to_string(tenths % 10);
}

void printRow(const std::string& label, const Bytes& row) {
    std::cout << label;
    for (std::uint8_t v : row) {
        std::cout << padLeft(std::to_string(v), 4);
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
    const Bytes above = {100, 150, 200, 104, 152, 196, 108, 154, 192, 112, 156, 188};
    const Bytes row = {102, 151, 198, 106, 153, 194, 110, 155, 190, 114, 157, 186};
    printRow("above:      ", above);
    printRow("row:        ", row);
    for (int f = kFilterNone; f <= kFilterPaeth; ++f) {
        const Bytes filtered = filterRow(f, row, above, 3);
        const bool back = unfilterRow(f, filtered, above, 3) == row;
        printRow(padLeft(kFilterNames[f], 8) + " (" + std::to_string(f) + ")", filtered);
        std::cout << "              score " << rowScore(filtered)
                  << (back ? ", unfilters back to the row\n" : ", UNFILTER FAILED\n");
    }
    std::cout << "best filter for this row: " << kFilterNames[bestFilter(row, above, 3)] << "\n";

    const int tests[5][3] = {{50, 60, 70}, {100, 120, 100}, {50, 150, 100}, {10, 10, 10},
                             {200, 40, 60}};
    for (const auto& t : tests) {
        std::cout << "Paeth(a = " << t[0] << ", b = " << t[1] << ", c = " << t[2]
                  << ") = " << paethPredictor(t[0], t[1], t[2]) << "\n";
    }

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
    const std::string columns = "    None     Sub      Up Average   Paeth    Best\n";
    std::cout << "\nzero bytes, in %" << std::string(9, ' ') << columns;
    std::string scoreTable = "average score per byte" + std::string(3, ' ') + columns;
    for (int i = 0; i < 5; ++i) {
        const Bytes plain = makePngRows(*pictures[i], nullptr);
        std::cout << "  " << names[i] << std::string(23 - names[i].size(), ' ');
        scoreTable += "  " + names[i] + std::string(23 - names[i].size(), ' ');
        for (int mode = kFilterNone; mode <= kFilterBest; ++mode) {
            const Bytes rows = filterScanlines(plain, 900, 3, mode);
            long long zeros = 0;
            long long score = 0;
            for (int y = 0; y < 200; ++y) {
                const Bytes filtered(rows.begin() + y * 901 + 1, rows.begin() + y * 901 + 901);
                for (std::uint8_t v : filtered) {
                    zeros += (v == 0) ? 1 : 0;
                }
                score += rowScore(filtered);
            }
            std::cout << padLeft(std::to_string(std::llround(zeros * 100.0 / 180000.0)), 8);
            scoreTable += padLeft(oneDecimal(score / 180000.0), 8);
        }
        std::cout << "\n";
    }
    std::cout << scoreTable;

    std::cout << "\nfilters chosen by Best (rows):\n";
    for (int i = 0; i < 5; ++i) {
        const Bytes rows = filterScanlines(makePngRows(*pictures[i], nullptr), 900, 3, kFilterBest);
        int used[5] = {0, 0, 0, 0, 0};
        for (int y = 0; y < 200; ++y) {
            used[rows[y * 901]] += 1;
        }
        std::cout << "  " << names[i] << ":";
        for (int f = kFilterNone; f <= kFilterPaeth; ++f) {
            std::cout << " " << kFilterNames[f] << " " << used[f];
        }
        std::cout << "\n";
    }

    std::cout << "\nfiles:\n";
    for (int i = 0; i < 5; ++i) {
        const std::string fileName = names[i] + ".png";
        if (!savePNGFiltered(*pictures[i], fileName, kFilterBest)) {
            std::cout << "could not write " << fileName << "\n";
            return 1;
        }
        Image back(0, 0);
        Image oldBack(0, 0);
        const bool ok = loadPNGFiltered(fileName, back) && samePictures(*pictures[i], back);
        const bool oldOk = loadPNG(fileName, oldBack);
        std::cout << "  " << fileName << ": " << makePngBytesFiltered(*pictures[i], kFilterBest).size()
                  << " bytes (without filters " << makePngBytes(*pictures[i]).size() << "), read back "
                  << (ok ? "the same" : "DIFFERENT") << ", Chapter 42's loadPNG "
                  << (oldOk ? "accepts it" : "refuses it") << "\n";
    }

    Bytes rows = filterScanlines(makePngRows(sky, nullptr), 900, 3, kFilterBest);
    rows[901 * 7] = 5;
    Bytes broken;
    appendPngSignature(broken);
    appendChunk(broken, "IHDR", makeIhdr(300, 200, false));
    appendChunk(broken, "IDAT", zlibStore(rows));
    appendChunk(broken, "IEND", Bytes{});
    Image ignored(0, 0);
    const std::string problem = decodePNGFiltered(broken, ignored);
    std::cout << "row 7 with filter type 5: "
              << (problem.empty() ? "accepted" : "refused (" + problem + ")") << "\n";
    return 0;
}
