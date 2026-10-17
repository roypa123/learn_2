#include <iostream>
#include <cstdint>
#include <string>

std::string toBinary(std::uint8_t value) {
    std::string result;
    for (int bit = 7; bit >= 0; --bit) {
        if ((value >> bit) & 1) {
            result += '1';
        } else {
            result += '0';
        }
    }
    return result;
}

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

int main() {
    const std::uint8_t values[] = {0, 1, 13, 128, 200, 255};
    for (std::uint8_t v : values) {
        std::cout << "decimal " << static_cast<int>(v)
                  << " = binary " << toBinary(v)
                  << " = hex " << toHex(v) << "\n";
    }

    const std::uint32_t orange = 0xFF8000;
    std::uint8_t red   = static_cast<std::uint8_t>((orange >> 16) & 0xFF);
    std::uint8_t green = static_cast<std::uint8_t>((orange >> 8) & 0xFF);
    std::uint8_t blue  = static_cast<std::uint8_t>(orange & 0xFF);
    std::cout << "\norange #FF8000:\n";
    std::cout << "  red   = " << static_cast<int>(red)   << " (hex " << toHex(red)   << ")\n";
    std::cout << "  green = " << static_cast<int>(green) << " (hex " << toHex(green) << ")\n";
    std::cout << "  blue  = " << static_cast<int>(blue)  << " (hex " << toHex(blue)  << ")\n";

    std::uint32_t joined = (static_cast<std::uint32_t>(red) << 16)
                         | (static_cast<std::uint32_t>(green) << 8)
                         | static_cast<std::uint32_t>(blue);
    std::cout << "  joined back = " << joined
              << (joined == orange ? " (same as before)" : " (different!)") << "\n";

    std::uint8_t bright = 250;
    bright = static_cast<std::uint8_t>(bright + 10);
    std::cout << "\n250 + 10 in one byte = " << static_cast<int>(bright) << "\n";

    std::uint8_t letter = 65;
    std::cout << "uint8_t 65 printed directly: " << letter << "\n";
    std::cout << "uint8_t 65 printed as int:   " << static_cast<int>(letter) << "\n";
    return 0;
}
