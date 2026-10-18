#include <iostream>
#include <string>
#include <vector>
#include "pngfile.h"
#include "bezier.h"
#include "hsv.h"

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

Bytes pngFromParts(int width, int height, int bitDepth, int colourType, const Bytes& rows) {
    Bytes file;
    appendPngSignature(file);
    Bytes ihdr = makeIhdr(width, height, false);
    ihdr[8] = static_cast<std::uint8_t>(bitDepth);
    ihdr[9] = static_cast<std::uint8_t>(colourType);
    appendChunk(file, "IHDR", ihdr);
    appendChunk(file, "IDAT", zlibStore(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

void report(const char* label, const Bytes& file) {
    Image ignored(0, 0);
    std::string problem = decodePNG(file, ignored);
    std::cout << "  " << label << ": " << (problem.empty() ? "accepted" : "refused (" + problem + ")")
              << "\n";
}

int main() {
    Image tiny(3, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(0, 1, colours::white);
    tiny.setPixel(2, 1, colours::yellow);
    Bytes tinyPng = makePngBytes(tiny);
    std::cout << "tiny.png, " << tinyPng.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(tinyPng.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(tinyPng.size()); ++j) {
            std::cout << " " << hexByte(tinyPng[j]);
        }
        std::cout << "\n";
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> diskAlpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4));
        }
    }

    Image rainbow(301, 101);
    std::vector<std::uint8_t> fadeAlpha(301 * 101);
    for (int y = 0; y < 101; ++y) {
        for (int x = 0; x < 301; ++x) {
            rainbow.setPixel(x, y, toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0})));
            fadeAlpha[y * 301 + x] = static_cast<std::uint8_t>(255 - y * 255 / 100);
        }
    }

    if (!savePNG(tiny, "tiny.png") || !savePNG(heart, "heart.png") ||
        !savePNG(disk, "disk.png", &diskAlpha) || !savePNG(rainbow, "fade.png", &fadeAlpha) ||
        !saveBMP(heart, "heart.bmp")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "heart: PNG " << makePngBytes(heart).size() << " bytes, BMP "
              << makeBmpBytes(heart).size() << " bytes\n";

    Image heartBack(0, 0);
    Image diskBack(0, 0);
    std::vector<std::uint8_t> diskAlphaBack;
    Image fadeBack(0, 0);
    std::vector<std::uint8_t> fadeAlphaBack;
    bool ok = loadPNG("heart.png", heartBack) && loadPNG("disk.png", diskBack, &diskAlphaBack) &&
              loadPNG("fade.png", fadeBack, &fadeAlphaBack);
    std::cout << "read back: " << (ok ? "all loaded" : "LOAD FAILED") << ", heart "
              << (samePictures(heart, heartBack) ? "same" : "DIFFERENT") << ", disk "
              << (samePictures(disk, diskBack) && diskAlpha == diskAlphaBack ? "same" : "DIFFERENT")
              << ", fade "
              << (samePictures(rainbow, fadeBack) && fadeAlpha == fadeAlphaBack ? "same" : "DIFFERENT")
              << "\n";
    std::cout << "disk.png is " << makePngBytes(disk, &diskAlpha).size() << " bytes, fade.png is "
              << makePngBytes(rainbow, &fadeAlpha).size() << " bytes\n";

    std::cout << "broken PNG files:\n";
    report("the good file", tinyPng);
    Bytes wrong = tinyPng;
    wrong[19] = 9;
    report("width changed", wrong);
    Bytes rows = makePngRows(tiny, nullptr);
    report("colour type 3", pngFromParts(3, 2, 8, 3, rows));
    report("16 bits per channel", pngFromParts(3, 2, 16, 2, rows));
    Bytes filtered = rows;
    filtered[10] = 1;
    report("row 1 uses filter 1", pngFromParts(3, 2, 8, 2, filtered));
    report("one row missing", pngFromParts(3, 3, 8, 2, rows));
    wrong = tinyPng;
    wrong.resize(wrong.size() - 12);
    report("no IEND", wrong);
    return 0;
}
