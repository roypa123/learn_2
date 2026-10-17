#ifndef IMAGE_H
#define IMAGE_H

#include <cstdint>
#include <fstream>
#include <string>
#include <vector>

struct Colour {
    std::uint8_t r = 0;
    std::uint8_t g = 0;
    std::uint8_t b = 0;
};

namespace colours {
    const Colour black   {0, 0, 0};
    const Colour white   {255, 255, 255};
    const Colour red     {255, 0, 0};
    const Colour green   {0, 255, 0};
    const Colour blue    {0, 0, 255};
    const Colour yellow  {255, 255, 0};
    const Colour cyan    {0, 255, 255};
    const Colour magenta {255, 0, 255};
}

class Image {
public:
    Image(int width, int height, Colour fill = colours::black)
        : width_(width > 0 ? width : 0),
          height_(height > 0 ? height : 0),
          pixels_(width_ * height_ * 3, 0) {
        clear(fill);
    }

    int width() const { return width_; }
    int height() const { return height_; }

    bool isInside(int x, int y) const {
        return x >= 0 && x < width_ && y >= 0 && y < height_;
    }

    void setPixel(int x, int y, Colour c) {
        if (!isInside(x, y)) {
            return;
        }
        int i = index(x, y);
        pixels_[i]     = c.r;
        pixels_[i + 1] = c.g;
        pixels_[i + 2] = c.b;
    }

    Colour getPixel(int x, int y) const {
        if (!isInside(x, y)) {
            return colours::black;
        }
        int i = index(x, y);
        return Colour{pixels_[i], pixels_[i + 1], pixels_[i + 2]};
    }

    void clear(Colour c) {
        for (int p = 0; p < width_ * height_; ++p) {
            pixels_[p * 3]     = c.r;
            pixels_[p * 3 + 1] = c.g;
            pixels_[p * 3 + 2] = c.b;
        }
    }

    const std::vector<std::uint8_t>& data() const { return pixels_; }

    bool savePPM(const std::string& fileName) const {
        std::ofstream file(fileName, std::ios::binary);
        if (!file) {
            return false;
        }
        file << "P6\n" << width_ << " " << height_ << "\n255\n";
        file.write(reinterpret_cast<const char*>(pixels_.data()),
                   static_cast<std::streamsize>(pixels_.size()));
        return static_cast<bool>(file);
    }

private:
    int index(int x, int y) const {
        return (y * width_ + x) * 3;
    }

    int width_;
    int height_;
    std::vector<std::uint8_t> pixels_;
};

#endif
