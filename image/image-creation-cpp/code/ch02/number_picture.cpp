#include <iostream>
#include <string>

int main() {
    const int width = 7;
    const int height = 7;

    const int picture[height][width] = {
        {0, 0, 0, 0, 0, 0, 0},
        {0, 9, 9, 0, 9, 9, 0},
        {0, 9, 9, 0, 9, 9, 0},
        {0, 0, 0, 0, 0, 0, 0},
        {0, 9, 0, 0, 0, 9, 0},
        {0, 0, 9, 9, 9, 0, 0},
        {0, 0, 0, 0, 0, 0, 0},
    };

    const std::string shades = " .:-=+*#%@";

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int value = picture[y][x];
            char c = shades[value];
            std::cout << c << c;
        }
        std::cout << "\n";
    }
    return 0;
}
