#ifndef MATRIX_H
#define MATRIX_H

#include <cmath>
#include <vector>
#include "transform.h"

struct Mat3 {
    double m[3][3] = {{1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.0, 0.0, 1.0}};
};

inline Mat3 identity() {
    return Mat3{};
}

inline Mat3 translation(double tx, double ty) {
    Mat3 r;
    r.m[0][2] = tx;
    r.m[1][2] = ty;
    return r;
}

inline Mat3 scaling(double sx, double sy) {
    Mat3 r;
    r.m[0][0] = sx;
    r.m[1][1] = sy;
    return r;
}

inline Mat3 rotation(double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    Mat3 r;
    r.m[0][0] = c;
    r.m[0][1] = -s;
    r.m[1][0] = s;
    r.m[1][1] = c;
    return r;
}

inline Mat3 skew(double kx, double ky) {
    Mat3 r;
    r.m[0][1] = kx;
    r.m[1][0] = ky;
    return r;
}

inline Mat3 operator*(const Mat3& a, const Mat3& b) {
    Mat3 r;
    for (int row = 0; row < 3; ++row) {
        for (int col = 0; col < 3; ++col) {
            double sum = 0.0;
            for (int k = 0; k < 3; ++k) {
                sum += a.m[row][k] * b.m[k][col];
            }
            r.m[row][col] = sum;
        }
    }
    return r;
}

inline Vec2 applyToPoint(const Mat3& t, Vec2 p) {
    return Vec2{t.m[0][0] * p.x + t.m[0][1] * p.y + t.m[0][2],
                t.m[1][0] * p.x + t.m[1][1] * p.y + t.m[1][2]};
}

inline Vec2 applyToDirection(const Mat3& t, Vec2 v) {
    return Vec2{t.m[0][0] * v.x + t.m[0][1] * v.y, t.m[1][0] * v.x + t.m[1][1] * v.y};
}

inline std::vector<PointF> applyToPoints(const Mat3& t, const std::vector<PointF>& points) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(applyToPoint(t, p));
    }
    return result;
}

inline double determinant(const Mat3& t) {
    return t.m[0][0] * t.m[1][1] - t.m[0][1] * t.m[1][0];
}

#endif
