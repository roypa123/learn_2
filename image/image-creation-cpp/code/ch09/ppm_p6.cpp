#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <vector>

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

bool writePPM_P3(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& pixels) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P3\n" << width << " " << height << "\n255\n";
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int i = (y * width + x) * 3;
            file << static_cast<int>(pixels[i]) << " "
                 << static_cast<int>(pixels[i + 1]) << " "
                 << static_cast<int>(pixels[i + 2]) << "\n";
        }
        file << "\n";
    }
    return static_cast<bool>(file);
}

bool writePPM_P6(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& pixels) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P6\n" << width << " " << height << "\n255\n";
    file.write(reinterpret_cast<const char*>(pixels.data()),
               static_cast<std::streamsize>(pixels.size()));
    return static_cast<bool>(file);
}

long long fileSize(const std::string& fileName) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return -1;
    }
    return static_cast<long long>(file.tellg());
}

int main() {
    const int width = 3;
    const int height = 2;
    std::vector<std::uint8_t> pixels(width * height * 3, 0);
    setPixel(pixels, width, height, 0, 0, 255, 0, 0);
    setPixel(pixels, width, height, 1, 0, 0, 255, 0);
    setPixel(pixels, width, height, 2, 0, 0, 0, 255);
    setPixel(pixels, width, height, 0, 1, 255, 255, 0);
    setPixel(pixels, width, height, 1, 1, 255, 255, 255);
    setPixel(pixels, width, height, 2, 1, 0, 0, 0);

    const int size = 256;
    std::vector<std::uint8_t> gradient(size * size * 3, 0);
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x) {
            setPixel(gradient, size, size, x, y,
                     static_cast<std::uint8_t>(x),
                     static_cast<std::uint8_t>(y),
                     128);
        }
    }

    bool ok = writePPM_P6("first_binary.ppm", width, height, pixels);
    ok = ok && writePPM_P3("gradient_p3.ppm", size, size, gradient);
    ok = ok && writePPM_P6("gradient_p6.ppm", size, size, gradient);
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    std::cout << "first_binary.ppm: " << fileSize("first_binary.ppm") << " bytes\n";
    std::cout << "gradient_p3.ppm:  " << fileSize("gradient_p3.ppm") << " bytes\n";
    std::cout << "gradient_p6.ppm:  " << fileSize("gradient_p6.ppm") << " bytes\n";
    return 0;
}
