#include <iostream>
#include <cstdint>
#include <climits>

int main() {
    std::cout << "C++ version number: " << __cplusplus << "\n";

    if (__cplusplus >= 201703L) {
        std::cout << "C++17 or newer: OK\n";
    } else {
        std::cout << "C++17 or newer: NO - please add -std=c++17\n";
    }

    std::cout << "Bits in one char: " << CHAR_BIT << "\n";
    std::cout << "Size of std::uint8_t: " << sizeof(std::uint8_t) << " byte\n";
    std::cout << "Size of std::uint32_t: " << sizeof(std::uint32_t) << " bytes\n";

    if (CHAR_BIT == 8 && sizeof(std::uint32_t) == 4) {
        std::cout << "Byte sizes: OK\n";
    } else {
        std::cout << "Byte sizes: unusual computer\n";
    }

    std::cout << "Ready to make images!\n";
    return 0;
}
