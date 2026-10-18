#include <iostream>
#include <string>
#include "bmp.h"
#include "bezier.h"
#include "hsv.h"

int checkBmp(const Image& image, const Bytes& file) {
    if (!hasBytes(file, 0, kBmpHeaderSize) || file[0] != 'B' || file[1] != 'M') {
        return -1;
    }
    int offset = static_cast<int>(getU32(file, 10));
    int width = getS32(file, 18);
    int height = getS32(file, 22);
    if (width != image.width() || height != image.height() || getU16(file, 28) != 24) {
        return -1;
    }
    int rowSize = bmpRowSize(width);
    int matches = 0;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int at = offset + (height - 1 - y) * rowSize + x * 3;
            if (!hasBytes(file, at, 3)) {
                return -1;
            }
            Colour c = image.getPixel(x, y);
            if (file[at] == c.b && file[at + 1] == c.g && file[at + 2] == c.r) {
                ++matches;
            }
        }
    }
    return matches;
}

long long fileSizeOf(const std::string& fileName) {
    Bytes bytes;
    if (!readFileBytes(fileName, bytes)) {
        return -1;
    }
    return static_cast<long long>(bytes.size());
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

int main() {
    std::cout << "width, file size, expected size, pixels matching:\n";
    for (int w = 1; w <= 7; ++w) {
        Image test = makeTestPattern(w, 3);
        Bytes file = makeBmpBytes(test);
        int expected = kBmpHeaderSize + bmpRowSize(w) * 3;
        std::cout << "  " << w << ", " << file.size() << ", " << expected << ", "
                  << checkBmp(test, file) << " of " << w * 3 << "\n";
    }
    Image empty(0, 0);
    std::cout << "saving a 0 x 0 picture: " << (saveBMP(empty, "empty.bmp") ? "saved" : "refused")
              << "\n";

    Image gradient(256, 64);
    for (int x = 0; x < 256; ++x) {
        Colour c = lerpColour(colours::blue, colours::yellow, x / 255.0);
        for (int y = 0; y < 64; ++y) {
            gradient.setPixel(x, y, c);
        }
    }

    Image rainbow(301, 101);
    for (int x = 0; x < 301; ++x) {
        Colour c = toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0}));
        for (int y = 0; y < 101; ++y) {
            rainbow.setPixel(x, y, c);
        }
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image flower(300, 300, Colour{235, 245, 235});
    PointF middle{150.0, 150.0};
    for (int i = 0; i < 8; ++i) {
        double angle = degreesToRadians(i * 45.0);
        Colour col = toColour(hsvToRgb(HSV{320.0 + i * 5.0, 0.6, 0.95}));
        fillTiltedEllipseAA(flower, pointOnCircle(middle, 70.0, angle), 70.0, 24.0, angle, col);
    }
    fillCircleAA(flower, middle.x, middle.y, 30.0, Colour{250, 200, 40});

    const Image* pictures[4] = {&gradient, &rainbow, &heart, &flower};
    const std::string names[4] = {"gradient", "rainbow", "heart", "flower"};
    for (int i = 0; i < 4; ++i) {
        const Image& picture = *pictures[i];
        std::string bmpName = names[i] + ".bmp";
        std::string ppmName = names[i] + ".ppm";
        if (!saveBMP(picture, bmpName) || !picture.savePPM(ppmName)) {
            std::cout << "could not write " << names[i] << "\n";
            return 1;
        }
        Bytes back;
        int matches = readFileBytes(bmpName, back) ? checkBmp(picture, back) : -1;
        std::cout << names[i] << " " << picture.width() << " x " << picture.height() << ": BMP "
                  << fileSizeOf(bmpName) << " bytes, PPM " << fileSizeOf(ppmName)
                  << " bytes, read back: " << matches << " of "
                  << picture.width() * picture.height() << " pixels match\n";
    }
    if (!saveBMP(makeTestPattern(7, 3), "pattern.bmp")) {
        std::cout << "could not write pattern.bmp\n";
        return 1;
    }
    return 0;
}
