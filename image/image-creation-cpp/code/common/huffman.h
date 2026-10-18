#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>
#include "pngfilter.h"

const int kMaxCodeLength = 30;

inline std::vector<long long> countBytes(const Bytes& data) {
    std::vector<long long> counts(256, 0);
    for (std::uint8_t v : data) {
        counts[v] += 1;
    }
    return counts;
}

struct HuffmanNode {
    long long weight = 0;
    int symbol = -1;
    int left = -1;
    int right = -1;
};

inline int takeSmallest(const std::vector<HuffmanNode>& nodes, std::vector<bool>& taken) {
    int best = -1;
    for (int i = 0; i < static_cast<int>(nodes.size()); ++i) {
        if (!taken[i] && (best < 0 || nodes[i].weight < nodes[best].weight)) {
            best = i;
        }
    }
    taken[best] = true;
    return best;
}

inline std::vector<int> huffmanLengths(const std::vector<long long>& counts) {
    std::vector<int> lengths(counts.size(), 0);
    std::vector<HuffmanNode> nodes;
    for (int s = 0; s < static_cast<int>(counts.size()); ++s) {
        if (counts[s] > 0) {
            nodes.push_back(HuffmanNode{counts[s], s, -1, -1});
        }
    }
    if (nodes.empty()) {
        return lengths;
    }
    if (nodes.size() == 1) {
        lengths[nodes[0].symbol] = 1;
        return lengths;
    }
    std::vector<bool> taken(nodes.size(), false);
    int waiting = static_cast<int>(nodes.size());
    while (waiting > 1) {
        const int first = takeSmallest(nodes, taken);
        const int second = takeSmallest(nodes, taken);
        nodes.push_back(HuffmanNode{nodes[first].weight + nodes[second].weight, -1, first, second});
        taken.push_back(false);
        waiting -= 1;
    }
    std::vector<int> depth(nodes.size(), 0);
    for (int i = static_cast<int>(nodes.size()) - 1; i >= 0; --i) {
        if (nodes[i].symbol >= 0) {
            lengths[nodes[i].symbol] = depth[i];
        } else {
            depth[nodes[i].left] = depth[i] + 1;
            depth[nodes[i].right] = depth[i] + 1;
        }
    }
    return lengths;
}

inline std::vector<int> canonicalCodes(const std::vector<int>& lengths) {
    int maxLength = 0;
    for (int len : lengths) {
        maxLength = std::max(maxLength, len);
    }
    std::vector<int> countOfLength(maxLength + 1, 0);
    for (int len : lengths) {
        if (len > 0) {
            countOfLength[len] += 1;
        }
    }
    std::vector<long long> nextCode(maxLength + 1, 0);
    long long code = 0;
    for (int len = 1; len <= maxLength; ++len) {
        code = (code + countOfLength[len - 1]) << 1;
        nextCode[len] = code;
    }
    std::vector<int> codes(lengths.size(), -1);
    for (int s = 0; s < static_cast<int>(lengths.size()); ++s) {
        const int len = lengths[s];
        if (len > 0 && nextCode[len] < (1LL << len)) {
            codes[s] = static_cast<int>(nextCode[len]);
        }
        if (len > 0) {
            nextCode[len] += 1;
        }
    }
    return codes;
}

inline long long codedBits(const std::vector<long long>& counts, const std::vector<int>& lengths) {
    long long bits = 0;
    for (int s = 0; s < static_cast<int>(counts.size()); ++s) {
        bits += counts[s] * lengths[s];
    }
    return bits;
}

inline double entropyBits(const std::vector<long long>& counts) {
    long long total = 0;
    for (long long c : counts) {
        total += c;
    }
    double bits = 0.0;
    for (long long c : counts) {
        if (c > 0) {
            bits -= c * std::log2(static_cast<double>(c) / total);
        }
    }
    return bits;
}

struct BitWriter {
    Bytes bytes;
    int used = 0;
};

inline void putBit(BitWriter& w, int bit) {
    if (w.used == 0) {
        w.bytes.push_back(0);
    }
    if (bit != 0) {
        w.bytes.back() = static_cast<std::uint8_t>(w.bytes.back() | (1 << w.used));
    }
    w.used = (w.used + 1) % 8;
}

inline void putBits(BitWriter& w, int value, int count) {
    for (int i = 0; i < count; ++i) {
        putBit(w, (value >> i) & 1);
    }
}

inline void putCode(BitWriter& w, int code, int length) {
    for (int i = length - 1; i >= 0; --i) {
        putBit(w, (code >> i) & 1);
    }
}

struct BitReader {
    const Bytes* bytes = nullptr;
    long long bit = 0;
};

inline int getBit(BitReader& r) {
    const long long at = r.bit / 8;
    if (at >= static_cast<long long>(r.bytes->size())) {
        return -1;
    }
    const int bit = ((*r.bytes)[at] >> (r.bit % 8)) & 1;
    r.bit += 1;
    return bit;
}

inline int getBits(BitReader& r, int count) {
    int value = 0;
    for (int i = 0; i < count; ++i) {
        const int bit = getBit(r);
        if (bit < 0) {
            return -1;
        }
        value |= bit << i;
    }
    return value;
}

struct DecodeNode {
    int child[2] = {-1, -1};
    int symbol = -1;
};

inline std::string buildDecoder(const std::vector<int>& lengths, std::vector<DecodeNode>& tree) {
    tree.assign(1, DecodeNode{});
    for (int len : lengths) {
        if (len < 0 || len > kMaxCodeLength) {
            return "a code length is out of range";
        }
    }
    const std::vector<int> codes = canonicalCodes(lengths);
    for (int s = 0; s < static_cast<int>(lengths.size()); ++s) {
        if (lengths[s] == 0) {
            continue;
        }
        if (codes[s] < 0) {
            return "too many codes for their lengths";
        }
        int node = 0;
        for (int i = lengths[s] - 1; i >= 0; --i) {
            const int bit = (codes[s] >> i) & 1;
            if (tree[node].child[bit] < 0) {
                tree[node].child[bit] = static_cast<int>(tree.size());
                tree.push_back(DecodeNode{});
            }
            node = tree[node].child[bit];
        }
        tree[node].symbol = s;
    }
    return "";
}

inline int decodeSymbol(BitReader& r, const std::vector<DecodeNode>& tree) {
    int node = 0;
    while (tree[node].symbol < 0) {
        const int bit = getBit(r);
        if (bit < 0) {
            return -1;
        }
        node = tree[node].child[bit];
        if (node < 0) {
            return -1;
        }
    }
    return tree[node].symbol;
}

inline Bytes huffmanCompress(const Bytes& data) {
    Bytes out;
    const std::vector<int> lengths = huffmanLengths(countBytes(data));
    for (int len : lengths) {
        if (len > kMaxCodeLength) {
            return out;
        }
    }
    const std::vector<int> codes = canonicalCodes(lengths);
    putU32BE(out, static_cast<std::uint32_t>(data.size()));
    for (int len : lengths) {
        out.push_back(static_cast<std::uint8_t>(len));
    }
    BitWriter w;
    for (std::uint8_t v : data) {
        putCode(w, codes[v], lengths[v]);
    }
    out.insert(out.end(), w.bytes.begin(), w.bytes.end());
    return out;
}

inline std::string huffmanDecompress(const Bytes& packed, Bytes& out) {
    out.clear();
    if (!hasBytes(packed, 0, 4 + 256)) {
        return "too short for the header";
    }
    const std::uint32_t count = getU32BE(packed, 0);
    if (count > 100000000u) {
        return "too much data";
    }
    std::vector<int> lengths(256);
    for (int s = 0; s < 256; ++s) {
        lengths[s] = packed[4 + s];
    }
    std::vector<DecodeNode> tree;
    const std::string problem = buildDecoder(lengths, tree);
    if (!problem.empty()) {
        return problem;
    }
    BitReader r{&packed, 8LL * (4 + 256)};
    for (std::uint32_t i = 0; i < count; ++i) {
        const int s = decodeSymbol(r, tree);
        if (s < 0) {
            return "a code is missing or unknown";
        }
        out.push_back(static_cast<std::uint8_t>(s));
    }
    return "";
}

#endif
