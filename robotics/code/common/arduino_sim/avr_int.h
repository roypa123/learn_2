// avr_int.h - make "int" behave like the Arduino Uno's 16-bit int on the PC test bench
//
// Use it in a test file, AFTER run.h and BEFORE the sketch:
//     #include "run.h"
//     #include "avr_int.h"      // asks simrun.py to build the sketch with the Uno's 16-bit int
//     #include "../my_sketch/my_sketch.ino"
// simrun.py then rewrites the sketch's text before compiling it (never the file itself):
//     int -> avr_int,   const int -> const int16_t,   unsigned int -> uint16_t
// (words inside strings and comments are left alone).
//
// int arithmetic then wraps at 16 bits exactly as on the Uno: 32767 + 1 gives -32768, and
// 300 * 200 gives -5536 even when the result is stored in a long. Mixing an int with a long,
// float or double gives a long, float or double, as on the Uno. Limits: constants (const int) are
// 16-bit but do their sums in 32 bits; write number literals above 32767 with an L (40000L); and
// "c ? an_int : 0" needs a cast on one side.
#pragma once
#include <cstdint>
#include <type_traits>

struct avr_int {
    int16_t v;
    constexpr avr_int() : v(0) {}
    template <class T, class = typename std::enable_if<std::is_arithmetic<T>::value>::type>
    constexpr avr_int(T x) : v((int16_t)(long long)x) {}           // storing any number keeps only 16 bits
    constexpr avr_int(const avr_int &o) : v(o.v) {}
    avr_int(const volatile avr_int &o) : v(o.v) {}
    avr_int &operator=(const avr_int &o) { v = o.v; return *this; }
    void operator=(const avr_int &o) volatile { v = o.v; }
    constexpr operator int16_t() const { return v; }
    operator int16_t() const volatile { return v; }
};

namespace avr_detail {
inline avr_int wrap(long x) { return avr_int((int16_t)x); }
// numbers that stay 16-bit when mixed with an int on the Uno: int, short, char, bool, byte
template <class T> struct small : std::integral_constant<bool,
    std::is_integral<T>::value && (sizeof(T) <= 2 || std::is_same<T, int>::value)> {};
template <class T> using if_small = typename std::enable_if<small<T>::value, avr_int>::type;
// numbers that make the result bigger: long, unsigned long, float, double (computed only for real number types)
template <class T, bool = std::is_arithmetic<T>::value && !small<T>::value> struct big {};
template <class T> struct big<T, true> { using type = decltype((int16_t)0 * T()); };
template <class T> using if_big = typename big<T>::type;
}  // namespace avr_detail

#define AVR_INT_OP(op)                                                                                  \
    inline avr_int operator op(avr_int a, avr_int b) { return avr_detail::wrap((long)a.v op(long) b.v); } \
    template <class T> avr_detail::if_small<T> operator op(avr_int a, T b) {                              \
        return avr_detail::wrap((long)a.v op(long)(int16_t) b);                                             \
    }                                                                                                    \
    template <class T> avr_detail::if_small<T> operator op(T a, avr_int b) {                              \
        return avr_detail::wrap((long)(int16_t)a op(long) b.v);                                             \
    }                                                                                                    \
    template <class T> avr_detail::if_big<T> operator op(avr_int a, T b) { return a.v op b; }             \
    template <class T> avr_detail::if_big<T> operator op(T a, avr_int b) { return a op b.v; }
AVR_INT_OP(+)
AVR_INT_OP(-)
AVR_INT_OP(*)
AVR_INT_OP(/)
#undef AVR_INT_OP

#define AVR_INT_IOP(op)                                                                                 \
    inline avr_int operator op(avr_int a, avr_int b) { return avr_detail::wrap((long)a.v op(long) b.v); } \
    template <class T, class = typename std::enable_if<std::is_integral<T>::value>::type>                \
    avr_int operator op(avr_int a, T b) { return avr_detail::wrap((long)a.v op(long)(int16_t) b); }       \
    template <class T, class = typename std::enable_if<std::is_integral<T>::value>::type>                \
    avr_int operator op(T a, avr_int b) { return avr_detail::wrap((long)(int16_t)a op(long) b.v); }
AVR_INT_IOP(%)
AVR_INT_IOP(&)
AVR_INT_IOP(|)
AVR_INT_IOP(^)
#undef AVR_INT_IOP
inline avr_int operator<<(avr_int a, int n) { return avr_detail::wrap((long)a.v << n); }
inline avr_int operator>>(avr_int a, int n) { return avr_detail::wrap((long)a.v >> n); }
inline avr_int operator-(avr_int a) { return avr_detail::wrap(-(long)a.v); }
inline avr_int operator~(avr_int a) { return avr_detail::wrap(~(long)a.v); }

#define AVR_INT_CMP(op)                                                                       \
    inline bool operator op(avr_int a, avr_int b) { return a.v op b.v; }                        \
    template <class T, class = typename std::enable_if<std::is_arithmetic<T>::value>::type>   \
    bool operator op(avr_int a, T b) { return a.v op b; }                                       \
    template <class T, class = typename std::enable_if<std::is_arithmetic<T>::value>::type>   \
    bool operator op(T a, avr_int b) { return a op b.v; }
AVR_INT_CMP(==)
AVR_INT_CMP(!=)
AVR_INT_CMP(<)
AVR_INT_CMP(>)
AVR_INT_CMP(<=)
AVR_INT_CMP(>=)
#undef AVR_INT_CMP

#define AVR_INT_ASSIGN(op, base)                                                               \
    template <class T> avr_int &operator op(avr_int &a, T b) { a = a base b; return a; }         \
    template <class T> void operator op(volatile avr_int &a, T b) { avr_int t = a; t = t base b; a = t; }
AVR_INT_ASSIGN(+=, +)
AVR_INT_ASSIGN(-=, -)
AVR_INT_ASSIGN(*=, *)
AVR_INT_ASSIGN(/=, /)
AVR_INT_ASSIGN(%=, %)
#undef AVR_INT_ASSIGN
inline avr_int &operator++(avr_int &a) { a = a + 1; return a; }
inline avr_int operator++(avr_int &a, int) { avr_int t = a; a = a + 1; return t; }
inline avr_int &operator--(avr_int &a) { a = a - 1; return a; }
inline avr_int operator--(avr_int &a, int) { avr_int t = a; a = a - 1; return t; }
inline void operator++(volatile avr_int &a) { avr_int t = a; a = t + 1; }
inline avr_int operator++(volatile avr_int &a, int) { avr_int t = a; a = t + 1; return t; }
inline void operator--(volatile avr_int &a) { avr_int t = a; a = t - 1; }

inline avr_int min(avr_int a, avr_int b) { return a < b ? a : b; }
inline avr_int max(avr_int a, avr_int b) { return a > b ? a : b; }
inline avr_int abs(avr_int a) { return a < 0 ? -a : a; }

// analogRead gives an int on the Uno, so 1023 * 5000 overflows there too
#define analogRead(p) avr_int(::analogRead(p))

