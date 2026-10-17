#include <iostream>
#include <cstdint>
#include <string>

struct Colour {
    std::uint8_t r;
    std::uint8_t g;
    std::uint8_t b;
};

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

void printSwatch(Colour c) {
    std::cout << "\x1b[48;2;" << static_cast<int>(c.r) << ';'
              << static_cast<int>(c.g) << ';'
              << static_cast<int>(c.b) << "m      \x1b[0m";
}

void printColour(const std::string& name, Colour c) {
    printSwatch(c);
    std::cout << "  " << name;
    for (int i = static_cast<int>(name.size()); i < 9; ++i) {
        std::cout << ' ';
    }
    std::cout << " #" << toHex(c.r) << toHex(c.g) << toHex(c.b)
              << "  (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", "
              << static_cast<int>(c.b) << ")\n";
}

int main() {
    printColour("black",   {0, 0, 0});
    printColour("red",     {255, 0, 0});
    printColour("green",   {0, 255, 0});
    printColour("blue",    {0, 0, 255});
    printColour("yellow",  {255, 255, 0});
    printColour("cyan",    {0, 255, 255});
    printColour("magenta", {255, 0, 255});
    printColour("white",   {255, 255, 255});
    printColour("grey",    {128, 128, 128});
    printColour("orange",  {255, 128, 0});

    Colour orange = {255, 128, 0};
    Colour opposite = {
        static_cast<std::uint8_t>(255 - orange.r),
        static_cast<std::uint8_t>(255 - orange.g),
        static_cast<std::uint8_t>(255 - orange.b)
    };
    std::cout << "\nopposite of orange:\n";
    printColour("opposite", opposite);

    double g = orange.g / 255.0;
    int back = static_cast<int>(g * 255.0 + 0.5);
    std::cout << "\ngreen of orange as 0..1: " << g << "\n";
    std::cout << "and back to 0..255:      " << back << "\n";
    return 0;
}
