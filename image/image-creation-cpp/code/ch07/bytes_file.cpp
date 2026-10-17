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

bool writeBytes(const std::string& fileName, const std::vector<std::uint8_t>& data) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file.write(reinterpret_cast<const char*>(data.data()),
               static_cast<std::streamsize>(data.size()));
    return static_cast<bool>(file);
}

std::vector<std::uint8_t> readBytes(const std::string& fileName) {
    std::vector<std::uint8_t> data;
    std::ifstream file(fileName, std::ios::binary);
    if (!file) {
        return data;
    }
    char c;
    while (file.get(c)) {
        data.push_back(static_cast<std::uint8_t>(c));
    }
    return data;
}

void hexDump(const std::vector<std::uint8_t>& data) {
    const int count = static_cast<int>(data.size());
    for (int i = 0; i < count; ++i) {
        if (i % 16 == 0) {
            std::cout << toHex(static_cast<std::uint8_t>((i >> 8) & 0xFF))
                      << toHex(static_cast<std::uint8_t>(i & 0xFF)) << ":  ";
        }
        std::cout << toHex(data[i]) << ' ';
        if (i % 16 == 15 || i == count - 1) {
            std::cout << "\n";
        }
    }
}

int main() {
    const std::vector<std::uint8_t> data = {
        72, 105, 33, 10, 0, 13, 128, 255,
        0xCA, 0xFE, 0xBA, 0xBE, 1, 2, 3, 4,
        5, 6, 7, 8
    };

    if (!writeBytes("bytes.bin", data)) {
        std::cout << "Could not write bytes.bin\n";
        return 1;
    }
    std::cout << "wrote " << data.size() << " bytes to bytes.bin\n";

    std::vector<std::uint8_t> back = readBytes("bytes.bin");
    std::cout << "read back " << back.size() << " bytes:\n";
    hexDump(back);

    std::cout << (back == data ? "same bytes: OK\n" : "bytes are different!\n");

    {
        std::ofstream textFile("text_mode.txt");
        textFile << "A\nB";
    }
    {
        std::ofstream binFile("binary_mode.txt", std::ios::binary);
        binFile << "A\nB";
    }
    std::cout << "\ntext mode file:   ";
    hexDump(readBytes("text_mode.txt"));
    std::cout << "binary mode file: ";
    hexDump(readBytes("binary_mode.txt"));
    return 0;
}
