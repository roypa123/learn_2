#include <iostream>
#include <fstream>
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

long long fileSize(const std::string& fileName) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return -1;
    }
    return static_cast<long long>(file.tellg());
}

bool writePGM_P5(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& grey) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P5\n" << width << " " << height << "\n255\n";
    file.write(reinterpret_cast<const char*>(grey.data()),
               static_cast<std::streamsize>(grey.size()));
    return static_cast<bool>(file);
}

std::vector<std::uint8_t> packBits(int width, int height,
                                   const std::vector<std::uint8_t>& mask) {
    const int rowBytes = (width + 7) / 8;
    std::vector<std::uint8_t> packed(rowBytes * height, 0);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            if (mask[y * width + x] != 0) {
                int byteIndex = y * rowBytes + x / 8;
                int bitNumber = 7 - (x % 8);
                packed[byteIndex] = static_cast<std::uint8_t>(
                    packed[byteIndex] | (1 << bitNumber));
            }
        }
    }
    return packed;
}

bool writePBM_P4(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& mask) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    std::vector<std::uint8_t> packed = packBits(width, height, mask);
    file << "P4\n" << width << " " << height << "\n";
    file.write(reinterpret_cast<const char*>(packed.data()),
               static_cast<std::streamsize>(packed.size()));
    return static_cast<bool>(file);
}

int main() {
    const int gw = 256;
    const int gh = 64;
    std::vector<std::uint8_t> grey(gw * gh, 0);
    for (int y = 0; y < gh; ++y) {
        for (int x = 0; x < gw; ++x) {
            grey[y * gw + x] = static_cast<std::uint8_t>(x);
        }
    }

    const int cw = 10;
    const int ch = 4;
    std::vector<std::uint8_t> checker(cw * ch, 0);
    for (int y = 0; y < ch; ++y) {
        for (int x = 0; x < cw; ++x) {
            if ((x + y) % 2 == 0) {
                checker[y * cw + x] = 1;
            }
        }
    }

    const int dw = 64;
    const int dh = 64;
    const double cx = 32.0;
    const double cy = 32.0;
    const double radius = 24.0;
    std::vector<std::uint8_t> disk(dw * dh, 0);
    for (int y = 0; y < dh; ++y) {
        for (int x = 0; x < dw; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (dx * dx + dy * dy <= radius * radius) {
                disk[y * dw + x] = 1;
            }
        }
    }

    std::vector<std::uint8_t> packed = packBits(cw, ch, checker);
    const int rowBytes = (cw + 7) / 8;
    std::cout << "checker packed bytes:\n";
    for (int y = 0; y < ch; ++y) {
        std::cout << "  row " << y << ":";
        for (int b = 0; b < rowBytes; ++b) {
            std::cout << " " << toHex(packed[y * rowBytes + b]);
        }
        std::cout << "\n";
    }

    bool ok = writePGM_P5("grey.pgm", gw, gh, grey);
    ok = ok && writePBM_P4("checker.pbm", cw, ch, checker);
    ok = ok && writePBM_P4("disk.pbm", dw, dh, disk);
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "grey.pgm:    " << fileSize("grey.pgm") << " bytes\n";
    std::cout << "checker.pbm: " << fileSize("checker.pbm") << " bytes\n";
    std::cout << "disk.pbm:    " << fileSize("disk.pbm") << " bytes\n";
    return 0;
}
