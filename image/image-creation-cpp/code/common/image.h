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

inline bool readFileBytes(const std::string& fileName, std::vector<std::uint8_t>& bytes) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return false;
    }
    const std::streamsize size = static_cast<std::streamsize>(file.tellg());
    if (size < 0) {
        return false;
    }
    file.seekg(0, std::ios::beg);
    bytes.resize(size);
    file.read(reinterpret_cast<char*>(bytes.data()), size);
    return static_cast<bool>(file);
}

inline bool isSpace(std::uint8_t c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

inline void skipSpaceAndComments(const std::vector<std::uint8_t>& bytes, int& pos) {
    const int n = static_cast<int>(bytes.size());
    while (pos < n) {
        if (isSpace(bytes[pos])) {
            ++pos;
        } else if (bytes[pos] == '#') {
            while (pos < n && bytes[pos] != '\n') {
                ++pos;
            }
        } else {
            return;
        }
    }
}

inline bool readNumber(const std::vector<std::uint8_t>& bytes, int& pos, int& value) {
    skipSpaceAndComments(bytes, pos);
    const int n = static_cast<int>(bytes.size());
    if (pos >= n || bytes[pos] < '0' || bytes[pos] > '9') {
        return false;
    }
    value = 0;
    while (pos < n && bytes[pos] >= '0' && bytes[pos] <= '9') {
        value = value * 10 + (bytes[pos] - '0');
        if (value > 1000000) {
            return false;
        }
        ++pos;
    }
    return true;
}

inline std::uint8_t scaleToByte(int value, int maxval) {
    if (value > maxval) {
        value = maxval;
    }
    return static_cast<std::uint8_t>((value * 255 + maxval / 2) / maxval);
}

inline bool loadPPM(const std::string& fileName, Image& image) {
    std::vector<std::uint8_t> bytes;
    if (!readFileBytes(fileName, bytes) || bytes.size() < 2) {
        return false;
    }
    if (bytes[0] != 'P' || (bytes[1] != '3' && bytes[1] != '6')) {
        return false;
    }
    const bool binary = (bytes[1] == '6');
    int pos = 2;
    int width = 0;
    int height = 0;
    int maxval = 0;
    if (!readNumber(bytes, pos, width) || !readNumber(bytes, pos, height) ||
        !readNumber(bytes, pos, maxval)) {
        return false;
    }
    if (width <= 0 || height <= 0 || maxval <= 0 || maxval > 255) {
        return false;
    }
    if (static_cast<long long>(width) * height > 100000000LL) {
        return false;
    }

    Image result(width, height);
    if (binary) {
        if (pos >= static_cast<int>(bytes.size()) || !isSpace(bytes[pos])) {
            return false;
        }
        ++pos;
        const long long needed = static_cast<long long>(width) * height * 3;
        if (static_cast<long long>(bytes.size()) - pos < needed) {
            return false;
        }
        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                Colour c{scaleToByte(bytes[pos], maxval),
                         scaleToByte(bytes[pos + 1], maxval),
                         scaleToByte(bytes[pos + 2], maxval)};
                result.setPixel(x, y, c);
                pos += 3;
            }
        }
    } else {
        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                int r = 0;
                int g = 0;
                int b = 0;
                if (!readNumber(bytes, pos, r) || !readNumber(bytes, pos, g) ||
                    !readNumber(bytes, pos, b)) {
                    return false;
                }
                if (r > maxval || g > maxval || b > maxval) {
                    return false;
                }
                result.setPixel(x, y, Colour{scaleToByte(r, maxval),
                                             scaleToByte(g, maxval),
                                             scaleToByte(b, maxval)});
            }
        }
    }
    image = result;
    return true;
}

inline double lerp(double a, double b, double t) {
    return a + (b - a) * t;
}

inline std::uint8_t lerpByte(std::uint8_t a, std::uint8_t b, double t) {
    double v = lerp(a, b, t);
    if (v < 0.0) {
        v = 0.0;
    }
    if (v > 255.0) {
        v = 255.0;
    }
    return static_cast<std::uint8_t>(v + 0.5);
}

inline Colour lerpColour(Colour a, Colour b, double t) {
    return Colour{lerpByte(a.r, b.r, t), lerpByte(a.g, b.g, t), lerpByte(a.b, b.b, t)};
}

#endif
