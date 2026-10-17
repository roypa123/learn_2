#include <iostream>
#include <cstdint>
#include <string>
#include <vector>

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

bool isInside(int x, int y, int width, int height) {
    return x >= 0 && x < width && y >= 0 && y < height;
}

void setPixel(std::vector<std::uint8_t>& pixels, int width, int height,
              int x, int y, std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    if (!isInside(x, y, width, height)) {
        return;
    }
    int i = (y * width + x) * 3;
    pixels[i]     = r;
    pixels[i + 1] = g;
    pixels[i + 2] = b;
}

int main() {
    const int width = 4;
    const int height = 3;
    std::vector<std::uint8_t> pixels(width * height * 3, 0);

    std::cout << "pixels: " << width * height
              << ", bytes: " << pixels.size() << "\n\n";

    setPixel(pixels, width, height, 0, 0, 255, 0, 0);
    setPixel(pixels, width, height, 3, 0, 0, 255, 0);
    setPixel(pixels, width, height, 1, 1, 255, 255, 255);
    setPixel(pixels, width, height, 3, 2, 0, 0, 255);
    setPixel(pixels, width, height, 9, 9, 255, 255, 0);

    for (int y = 0; y < height; ++y) {
        std::cout << "row " << y << ":";
        for (int x = 0; x < width; ++x) {
            int i = (y * width + x) * 3;
            std::cout << "  " << toHex(pixels[i])
                      << toHex(pixels[i + 1]) << toHex(pixels[i + 2]);
        }
        std::cout << "\n";
    }

    std::cout << "\nall bytes in memory order:\n";
    const int rowSize = width * 3;
    for (int i = 0; i < static_cast<int>(pixels.size()); ++i) {
        std::cout << toHex(pixels[i]) << ' ';
        if ((i + 1) % rowSize == 0) {
            std::cout << "\n";
        }
    }

    int index = 7;
    std::cout << "\npixel number " << index
              << " is at x = " << index % width
              << ", y = " << index / width << "\n";
    return 0;
}
