#include <iostream>

bool isInside(int x, int y, int width, int height) {
    return x >= 0 && x < width && y >= 0 && y < height;
}

int main() {
    const int width = 8;
    const int height = 5;

    const int markX = 5;
    const int markY = 2;

    std::cout << "    ";
    for (int x = 0; x < width; ++x) {
        std::cout << x << ' ';
    }
    std::cout << "  <- x\n";

    for (int y = 0; y < height; ++y) {
        std::cout << y << " | ";
        for (int x = 0; x < width; ++x) {
            int dx = x - markX;
            int dy = y - markY;
            int distSquared = dx * dx + dy * dy;
            if (distSquared == 0) {
                std::cout << "X ";
            } else if (distSquared == 1) {
                std::cout << "o ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << "\n";
    }
    std::cout << "^\ny\n\n";

    const int cornerX = width - 1;
    const int cornerY = height - 1;
    const int stepX[4] = {1, -1, 0, 0};
    const int stepY[4] = {0, 0, 1, -1};

    std::cout << "Neighbours of (" << cornerX << ", " << cornerY << "):\n";
    for (int i = 0; i < 4; ++i) {
        int nx = cornerX + stepX[i];
        int ny = cornerY + stepY[i];
        std::cout << "  (" << nx << ", " << ny << ") ";
        if (isInside(nx, ny, width, height)) {
            std::cout << "inside\n";
        } else {
            std::cout << "outside\n";
        }
    }

    int mathsY = 0;
    int imageY = (height - 1) - mathsY;
    std::cout << "\nmaths y = " << mathsY << " is image y = " << imageY << "\n";
    return 0;
}
