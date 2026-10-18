#include <iostream>
#include <string>
#include "bmpload.h"
#include "resize.h"

int countSame(const Image& a, const Image& b) {
    if (a.width() != b.width() || a.height() != b.height()) {
        return -1;
    }
    int same = 0;
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            Colour p = a.getPixel(x, y);
            Colour q = b.getPixel(x, y);
            if (p.r == q.r && p.g == q.g && p.b == q.b) {
                ++same;
            }
        }
    }
    return same;
}

void setU32(Bytes& file, int pos, std::uint32_t v) {
    Bytes four;
    putU32(four, v);
    for (int i = 0; i < 4; ++i) {
        file[pos + i] = four[i];
    }
}

Bytes makeTopDown(const Bytes& bottomUp, int width, int height) {
    Bytes file(bottomUp.begin(), bottomUp.begin() + kBmpHeaderSize);
    setU32(file, 22, static_cast<std::uint32_t>(-height));
    int rowSize = bmpRowSize(width);
    for (int row = height - 1; row >= 0; --row) {
        int start = kBmpHeaderSize + row * rowSize;
        file.insert(file.end(), bottomUp.begin() + start, bottomUp.begin() + start + rowSize);
    }
    return file;
}

Bytes make32Bit(const Image& image) {
    Bytes file = makeBmpBytes(image);
    file.resize(kBmpHeaderSize);
    int pixelBytes = 4 * image.width() * image.height();
    setU32(file, 2, kBmpHeaderSize + pixelBytes);
    file[28] = 32;
    setU32(file, 34, pixelBytes);
    for (int y = image.height() - 1; y >= 0; --y) {
        for (int x = 0; x < image.width(); ++x) {
            Colour c = image.getPixel(x, y);
            file.push_back(c.b);
            file.push_back(c.g);
            file.push_back(c.r);
            file.push_back(255);
        }
    }
    return file;
}

Image makeTestPattern(int width, int height) {
    Image pattern(width, height);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            pattern.setPixel(x, y, Colour{static_cast<std::uint8_t>(40 * x + 10),
                                          static_cast<std::uint8_t>(80 * y + 20),
                                          static_cast<std::uint8_t>(255 - 30 * x)});
        }
    }
    return pattern;
}

void report(const char* label, const Bytes& file) {
    std::string problem = bmpProblem(file);
    std::cout << "  " << label << ": " << (problem.empty() ? "accepted" : "refused (" + problem + ")")
              << "\n";
}

int main() {
    std::cout << "round trips in memory (pixels the same):";
    for (int w = 1; w <= 7; ++w) {
        Image original = makeTestPattern(w, 3);
        Image back(0, 0);
        bool ok = decodeBMP(makeBmpBytes(original), back);
        std::cout << " " << (ok ? countSame(original, back) : -1);
    }
    std::cout << "\n";

    Image pattern = makeTestPattern(7, 3);
    Bytes bottomUp = makeBmpBytes(pattern);
    Image fromTopDown(0, 0);
    decodeBMP(makeTopDown(bottomUp, 7, 3), fromTopDown);
    Image from32(0, 0);
    decodeBMP(make32Bit(pattern), from32);
    std::cout << "top-down file: " << countSame(pattern, fromTopDown) << " of 21 the same, "
              << "32-bit file: " << countSame(pattern, from32) << " of 21 the same\n";

    std::cout << "broken files:\n";
    report("the good file", bottomUp);
    report("empty", Bytes{});
    Bytes wrong = bottomUp;
    wrong[1] = 'X';
    report("signature BX", wrong);
    wrong = bottomUp;
    wrong[28] = 16;
    report("16 bits per pixel", wrong);
    wrong = bottomUp;
    setU32(wrong, 30, 1);
    report("compressed", wrong);
    wrong = bottomUp;
    setU32(wrong, 18, 0);
    report("width 0", wrong);
    wrong = bottomUp;
    wrong.resize(wrong.size() - 10);
    report("last 10 bytes missing", wrong);
    wrong = bottomUp;
    setU32(wrong, 10, 0xFFFFFFF0u);
    report("pixel offset far outside", wrong);
    wrong = bottomUp;
    setU32(wrong, 22, 0x7FFFFFFFu);
    report("height 2147483647", wrong);

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});
    Image loaded(0, 0);
    if (!saveBMP(heart, "heart.bmp") || !loadBMP("heart.bmp", loaded)) {
        std::cout << "could not save and load heart.bmp\n";
        return 1;
    }
    std::cout << "heart.bmp from disk: " << countSame(heart, loaded) << " of "
              << heart.width() * heart.height() << " pixels the same\n";

    Image small = resizeBox(loaded, 100, 100);
    Image flipped(100, 100);
    for (int y = 0; y < 100; ++y) {
        for (int x = 0; x < 100; ++x) {
            flipped.setPixel(x, y, small.getPixel(x, 99 - y));
        }
    }
    if (!saveBMP(small, "heart-small.bmp") || !saveBMP(flipped, "heart-flipped.bmp")) {
        std::cout << "could not write the small hearts\n";
        return 1;
    }
    Image check(0, 0);
    bool reloaded = loadBMP("heart-small.bmp", check);
    std::cout << "heart-small.bmp: " << (reloaded ? "loaded" : "failed") << ", " << check.width()
              << " x " << check.height() << "\n";
    return 0;
}
