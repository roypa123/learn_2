#ifndef HISTOGRAM_H
#define HISTOGRAM_H

#include <algorithm>
#include <array>
#include "pointops.h"

using Histogram = std::array<long long, 256>;

inline Histogram greyHistogram(const Image& image) {
    Histogram h{};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            h[greyByte(image.getPixel(x, y))] += 1;
        }
    }
    return h;
}

inline Histogram channelHistogram(const Image& image, int channel) {
    Histogram h{};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            const int v = (channel == 0) ? c.r : (channel == 1) ? c.g : c.b;
            h[v] += 1;
        }
    }
    return h;
}

inline Histogram cumulative(const Histogram& h) {
    Histogram c{};
    long long sum = 0;
    for (int v = 0; v < 256; ++v) {
        sum += h[v];
        c[v] = sum;
    }
    return c;
}

inline long long histogramTotal(const Histogram& h) {
    return cumulative(h)[255];
}

inline int lowestValue(const Histogram& h) {
    for (int v = 0; v < 256; ++v) {
        if (h[v] > 0) {
            return v;
        }
    }
    return 0;
}

inline int highestValue(const Histogram& h) {
    for (int v = 255; v >= 0; --v) {
        if (h[v] > 0) {
            return v;
        }
    }
    return 0;
}

inline int usedValues(const Histogram& h) {
    int used = 0;
    for (long long n : h) {
        used += (n > 0) ? 1 : 0;
    }
    return used;
}

inline double histogramMean(const Histogram& h) {
    long long total = 0;
    double sum = 0.0;
    for (int v = 0; v < 256; ++v) {
        total += h[v];
        sum += static_cast<double>(v) * h[v];
    }
    return (total == 0) ? 0.0 : sum / total;
}

inline int percentile(const Histogram& h, double fraction) {
    const Histogram c = cumulative(h);
    const double wanted = fraction * c[255];
    for (int v = 0; v < 256; ++v) {
        if (c[v] >= wanted && c[v] > 0) {
            return v;
        }
    }
    return 255;
}

inline LookupTable autoLevelsTable(const Histogram& h, double clipFraction) {
    return levelsTable(percentile(h, clipFraction), percentile(h, 1.0 - clipFraction));
}

inline LookupTable equaliseTable(const Histogram& h) {
    const Histogram c = cumulative(h);
    const long long total = c[255];
    const long long first = h[lowestValue(h)];
    if (total == first) {
        return identityTable();
    }
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = (c[v] <= first) ? 0 : clampByte((c[v] - first) * 255.0 / (total - first));
    }
    return t;
}

inline void drawHistogram(Image& image, int x, int y, int height, const Histogram& h, Colour c) {
    const long long highest = *std::max_element(h.begin(), h.end());
    strokeRect(image, makeRect(x, y, 258, height + 2), 1, Colour{170, 170, 170});
    for (int v = 0; v < 256; ++v) {
        const int bar = (highest == 0) ? 0 : static_cast<int>((h[v] * height + highest / 2) / highest);
        fillRect(image, makeRect(x + 1 + v, y + 1 + height - bar, 1, bar), c);
    }
    drawText(image, x, y + height + 5, "0", colours::black);
    drawText(image, x + 258 - textWidth("255", 1), y + height + 5, "255", colours::black);
}

#endif
