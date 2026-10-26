#ifndef RANDOM_H
#define RANDOM_H

#include <cstdint>
#include "warp.h"

inline std::uint32_t lcgNext(std::uint32_t& state) {
    state = state * 1103515245u + 12345u;
    return state;
}

inline std::uint32_t xorshiftNext(std::uint32_t& state) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

struct Random {
    std::uint32_t state = 2463534242u;
};

inline Random makeRandom(std::uint32_t seed) {
    return Random{(seed == 0) ? 2463534242u : seed};
}

inline std::uint32_t nextNumber(Random& r) {
    return xorshiftNext(r.state);
}

inline double randomDouble(Random& r) {
    return (nextNumber(r) >> 8) / 16777216.0;
}

inline double randomRange(Random& r, double low, double high) {
    return low + (high - low) * randomDouble(r);
}

inline int randomInt(Random& r, int low, int high) {
    return low + static_cast<int>(randomDouble(r) * (high - low + 1));
}

inline std::uint32_t hash2(int x, int y, std::uint32_t seed) {
    std::uint32_t h = seed + static_cast<std::uint32_t>(x) * 374761393u +
                      static_cast<std::uint32_t>(y) * 668265263u;
    h = (h ^ (h >> 13)) * 1274126177u;
    return h ^ (h >> 16);
}

inline double hashDouble(int x, int y, std::uint32_t seed) {
    return (hash2(x, y, seed) >> 8) / 16777216.0;
}

inline double jitteredOffset(int i, int n, Random& r) {
    return (i + randomDouble(r)) / n;
}

inline Image whiteNoise(int width, int height, Random& r) {
    Image noise(width, height);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            const std::uint8_t v = static_cast<std::uint8_t>(nextNumber(r) >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }
    return noise;
}

#endif
