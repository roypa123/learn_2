// Arduino.h - "an Arduino Uno on your PC": lets a sketch compile and run with g++ (the PC test bench)
//
// It pretends to be an Arduino Uno: a clock, 20 pins, an ADC, PWM, interrupts on pins 2 and 3,
// and a serial port with the real 64-byte buffers and the real time each character takes.
// A test file includes this header, then the sketch, and then tells the simulation what is
// connected to the input pins (see run.h). Timings are close to a real Uno but not exact.
//
// Differences from a real Uno that matter:
//   - int is 32 bits here, 16 bits on the Uno. Sketches in this course use types that behave
//     the same on both, or say so (Chapter 96).
//   - double is 64 bits here, 32 bits (the same as float) on the Uno.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <vector>
#include <deque>
#include <functional>

typedef uint8_t byte;
typedef bool boolean;
typedef uint16_t word;

#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define LED_BUILTIN 13
#define CHANGE 1
#define FALLING 2
#define RISING 3
#define DEC 10
#define HEX 16
#define OCT 8
#define BIN 2
#define PI 3.1415926535897932384626433832795
#define F(s) (s)
#define PROGMEM

const uint8_t A0 = 14, A1 = 15, A2 = 16, A3 = 17, A4 = 18, A5 = 19;
const uint8_t SDA = 18, SCL = 19, SS = 10, MOSI = 11, MISO = 12, SCK = 13;

// ---------------------------------------------------------------- the simulated world
namespace sim {
const int NPINS = 20;
inline uint64_t now_ns = 0;                       // simulated time since power-on, nanoseconds
inline int mode[NPINS] = {0};                     // INPUT, OUTPUT or INPUT_PULLUP
inline int level[NPINS] = {0};                    // what an OUTPUT pin is driving
inline int pwm[NPINS] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
inline std::function<int(double)> din[NPINS];     // what is connected to a digital input: f(time in s) -> HIGH/LOW
inline std::function<double(double)> ain[NPINS];  // what is connected to an analog input: f(time in s) -> volts
inline bool trace_pins = false;                   // print every change of an output pin
inline bool trace_pwm = false;                    // print every analogWrite
inline bool serial_time = false;                  // put the time in front of each line the sketch prints
inline uint32_t loop_ns = 2000;                   // time one empty pass of loop() takes
inline uint32_t step_ns = 1000;                   // time step used while interrupts are watched
inline uint32_t rng = 12345;                      // for floating pins and random()
inline bool int_enabled = true;
inline void (*isr[2])() = {nullptr, nullptr};
inline int isr_mode[2] = {0, 0};
inline int isr_last[2] = {0, 0};
inline bool isr_pending[2] = {false, false};
inline std::vector<std::function<void()>> tick_hooks;   // other simulated hardware (timers, buses)

inline double t() { return now_ns / 1e9; }
inline const char *stamp() {
    static char buf[32];
    std::snprintf(buf, sizeof buf, "[%9.4f s] ", t());
    return buf;
}
inline uint32_t next_random() { rng = rng * 1103515245u + 12345u; return (rng >> 8) & 0xFFFFFF; }

inline int pin_from_outside(int p) {              // the level the outside world puts on an input pin
    if (din[p]) return din[p](t()) ? HIGH : LOW;
    if (ain[p]) return ain[p](t()) > 2.5 ? HIGH : LOW;
    if (mode[p] == INPUT_PULLUP) return HIGH;
    if (mode[p] == OUTPUT) return level[p];
    return (next_random() >> 7) & 1;              // a floating input: nobody knows (Chapter 83)
}

inline void run_isr(int n) {
    if (!isr[n]) return;
    bool saved = int_enabled;
    int_enabled = false;                          // an ISR runs with interrupts off
    isr[n]();
    int_enabled = saved;
}

inline void check_interrupts() {
    for (int n = 0; n < 2; n++) {
        if (!isr[n]) continue;
        int p = n == 0 ? 2 : 3;
        int v = pin_from_outside(p);
        int old = isr_last[n];
        isr_last[n] = v;
        bool fire = (isr_mode[n] == CHANGE && v != old) || (isr_mode[n] == RISING && v && !old) ||
                    (isr_mode[n] == FALLING && !v && old);
        if (fire) isr_pending[n] = true;          // hardware remembers ONE waiting interrupt
        if (isr_pending[n] && int_enabled) { isr_pending[n] = false; run_isr(n); }
    }
}

inline bool watching() { return isr[0] || isr[1] || !tick_hooks.empty(); }

struct Stop {};                                   // thrown when the test's time is up
inline uint64_t end_ns = UINT64_MAX;

inline void advance(uint64_t ns) {                // let simulated time pass
    if (now_ns + ns >= end_ns) {                  // the run ends during this wait
        if (watching()) ns = end_ns - now_ns;
        else { now_ns = end_ns; throw Stop{}; }
    }
    if (!watching()) { now_ns += ns; return; }
    while (ns > 0) {
        uint64_t dt = ns < step_ns ? ns : step_ns;
        now_ns += dt;
        ns -= dt;
        for (auto &h : tick_hooks) h();
        check_interrupts();
    }
    if (now_ns >= end_ns) throw Stop{};
}
}  // namespace sim

// ---------------------------------------------------------------- time
namespace sim {
// millis(), micros() and delay() are driven by Timer0. If a sketch changes Timer0's prescaler
// (avr_regs.h), they run at t0_rate times the right speed (1.0 = normal).
inline double t0_rate = 1.0;
inline uint64_t t0_base_now = 0;                  // when t0_rate last changed
inline double t0_base_val = 0.0;                  // the Timer0 clock (ns) at that moment
inline uint64_t t0_ns() {                         // what Timer0 believes the time is, in ns
    if (t0_rate == 1.0 && t0_base_now == 0) return now_ns;
    return (uint64_t)(t0_base_val + (double)(now_ns - t0_base_now) * t0_rate);
}
inline void set_t0_rate(double r) {
    t0_base_val = (double)t0_ns();
    t0_base_now = now_ns;
    t0_rate = r;
}
}  // namespace sim
inline unsigned long millis() {                   // 32 bits: wraps after 49.7 days
    unsigned long m = (unsigned long)(sim::t0_ns() / 1000000ULL);
    sim::advance(1000);                           // reading the clock takes about 1 us on an Uno
    return m;
}
inline unsigned long micros() {                   // wraps after 71.6 minutes
    unsigned long u = (unsigned long)(sim::t0_ns() / 1000ULL);
    sim::advance(3000);                           // about 3 us
    return u;
}
inline void delay(unsigned long ms) {             // counts Timer0's time, like the real delay()
    if (sim::t0_rate <= 0) { while (true) sim::advance(1000000ULL); }   // Timer0 stopped: waits for ever
    sim::advance((uint64_t)((double)ms * 1000000.0 / sim::t0_rate));
}
inline void delayMicroseconds(unsigned int us) { sim::advance((uint64_t)us * 1000ULL); }

// ---------------------------------------------------------------- pins
inline void pinMode(uint8_t p, uint8_t m) {
    sim::mode[p] = m;
    if (m == INPUT_PULLUP || m == INPUT) sim::level[p] = 0;
}
inline void digitalWrite(uint8_t p, uint8_t v) {
    sim::advance(4000);                           // digitalWrite takes about 4 us on an Uno
    v = v ? HIGH : LOW;
    if (sim::mode[p] != OUTPUT) {                 // on a real Uno this turns the pull-up on or off
        sim::mode[p] = v ? INPUT_PULLUP : INPUT;
        return;
    }
    if (sim::pwm[p] >= 0) sim::pwm[p] = -1;      // digitalWrite stops PWM on that pin
    if (sim::level[p] != v && sim::trace_pins)
        std::printf("%spin %d -> %s\n", sim::stamp(), p, v ? "HIGH" : "LOW");
    sim::level[p] = v;
}
inline int digitalRead(uint8_t p) {
    sim::advance(4000);                           // about 4 us
    return sim::pin_from_outside(p);
}
#define DEFAULT 1
#define INTERNAL 3
#define EXTERNAL 0
namespace sim {
inline std::function<double(double)> vcc = [](double) { return 5.0; };   // the 5 V rail, which may sag
inline double internal_ref = 1.1;                 // this chip's own "1.1 V" reference (each chip differs a little)
inline int ref_mode = DEFAULT;
}  // namespace sim
inline int analogRead(uint8_t p) {
    if (p < 14) p += 14;                          // analogRead(0) means A0
    sim::advance(112000);                         // one ADC conversion takes about 112 us (Chapter 101)
    double vref = sim::ref_mode == INTERNAL ? sim::internal_ref : sim::vcc(sim::t());
    double v = sim::ain[p] ? sim::ain[p](sim::t()) : (sim::next_random() % 1024) * vref / 1024;
    int n = (int)(v / vref * 1024.0);             // the ADC rounds down to a whole step
    return n < 0 ? 0 : (n > 1023 ? 1023 : n);
}
inline void analogReference(uint8_t mode) { sim::ref_mode = mode; }
inline void analogWrite(uint8_t p, int v) {
    sim::advance(5000);
    if (v < 0) v = 0;
    if (v > 255) v = 255;
    sim::mode[p] = OUTPUT;
    bool pwm_pin = (p == 3 || p == 5 || p == 6 || p == 9 || p == 10 || p == 11);
    if (!pwm_pin || v == 0 || v == 255) {         // not a PWM pin, or fully off/on: a plain digital output
        if (!pwm_pin && v > 0 && v < 255) v = v < 128 ? 0 : 255;
        sim::pwm[p] = -1;
        int lv = v >= 128 ? HIGH : LOW;
        if (sim::trace_pwm && sim::level[p] != lv) std::printf("%spin %d -> %s\n", sim::stamp(), p, lv ? "HIGH" : "LOW");
        sim::level[p] = lv;
        return;
    }
    if (sim::trace_pwm && sim::pwm[p] != v)
        std::printf("%spin %d PWM %d/255 (%.1f%%)\n", sim::stamp(), p, v, v * 100.0 / 255);
    sim::pwm[p] = v;
}
inline unsigned long pulseIn(uint8_t p, uint8_t state, unsigned long timeout = 1000000UL) {
    uint64_t start = sim::now_ns, limit = (uint64_t)timeout * 1000ULL;
    while (sim::pin_from_outside(p) == state) { sim::advance(1000); if (sim::now_ns - start > limit) return 0; }
    while (sim::pin_from_outside(p) != state) { sim::advance(1000); if (sim::now_ns - start > limit) return 0; }
    uint64_t rise = sim::now_ns;
    while (sim::pin_from_outside(p) == state) { sim::advance(1000); if (sim::now_ns - start > limit) return 0; }
    return (unsigned long)((sim::now_ns - rise) / 1000ULL);
}
inline void tone(uint8_t p, unsigned int hz, unsigned long ms = 0) {
    if (sim::trace_pins) {
        if (ms) std::printf("%spin %d tone %u Hz for %lu ms\n", sim::stamp(), p, hz, ms);
        else std::printf("%spin %d tone %u Hz\n", sim::stamp(), p, hz);
    }
}
inline void noTone(uint8_t p) { if (sim::trace_pins) std::printf("%spin %d tone off\n", sim::stamp(), p); }

// ---------------------------------------------------------------- interrupts
inline int digitalPinToInterrupt(uint8_t p) { return p == 2 ? 0 : (p == 3 ? 1 : -1); }
inline void attachInterrupt(int n, void (*f)(), int m) {
    if (n < 0 || n > 1) return;
    sim::isr[n] = f;
    sim::isr_mode[n] = m;
    sim::isr_last[n] = sim::pin_from_outside(n == 0 ? 2 : 3);
}
inline void detachInterrupt(int n) { if (n >= 0 && n <= 1) sim::isr[n] = nullptr; }
inline void noInterrupts() { sim::int_enabled = false; }
inline void interrupts() {
    sim::int_enabled = true;
    for (int n = 0; n < 2; n++)
        if (sim::isr_pending[n]) { sim::isr_pending[n] = false; sim::run_isr(n); }
}

// ---------------------------------------------------------------- small helpers from the Arduino core
template <class T, class L, class H> T constrain(T x, L lo, H hi) { return x < lo ? (T)lo : (x > hi ? (T)hi : x); }
inline long map(long x, long in_min, long in_max, long out_min, long out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
template <class T, class U> auto min(T a, U b) -> decltype(a < b ? a : b) { return a < b ? a : b; }
template <class T, class U> auto max(T a, U b) -> decltype(a > b ? a : b) { return a > b ? a : b; }
inline long random(long hi) { return hi <= 0 ? 0 : (long)(sim::next_random() % (uint32_t)hi); }
inline long random(long lo, long hi) { return hi <= lo ? lo : lo + random(hi - lo); }
inline void randomSeed(unsigned long s) { sim::rng = (uint32_t)s; }
#define bitRead(v, b) (((v) >> (b)) & 0x01)
#define bitSet(v, b) ((v) |= (1UL << (b)))
#define bitClear(v, b) ((v) &= ~(1UL << (b)))
#define bitWrite(v, b, x) ((x) ? bitSet(v, b) : bitClear(v, b))
#define bit(b) (1UL << (b))
#define lowByte(w) ((uint8_t)((w) & 0xff))
#define highByte(w) ((uint8_t)((w) >> 8))
#define sq(x) ((x) * (x))

// ---------------------------------------------------------------- String (a small part of Arduino's String class)
class String {
  public:
    std::string s;
    String() {}
    String(const char *c) : s(c ? c : "") {}
    String(const std::string &x) : s(x) {}
    String(char c) : s(1, c) {}
    String(int v, int base = 10) { from_long(v, base); }
    String(unsigned int v, int base = 10) { from_ulong(v, base); }
    String(long v, int base = 10) { from_long(v, base); }
    String(unsigned long v, int base = 10) { from_ulong(v, base); }
    String(double v, int decimals = 2) { char b[64]; std::snprintf(b, sizeof b, "%.*f", decimals, v); s = b; }
    unsigned int length() const { return (unsigned int)s.size(); }
    const char *c_str() const { return s.c_str(); }
    char charAt(unsigned int i) const { return i < s.size() ? s[i] : 0; }
    char operator[](unsigned int i) const { return charAt(i); }
    String &operator+=(const String &o) { s += o.s; return *this; }
    String &operator+=(const char *o) { s += o; return *this; }
    String &operator+=(char c) { s += c; return *this; }
    String &operator+=(int v) { s += String(v).s; return *this; }
    bool operator==(const String &o) const { return s == o.s; }
    bool operator==(const char *o) const { return s == o; }
    bool operator!=(const String &o) const { return s != o.s; }
    bool operator!=(const char *o) const { return s != o; }
    bool equals(const String &o) const { return s == o.s; }
    bool startsWith(const String &o) const { return s.compare(0, o.s.size(), o.s) == 0; }
    long toInt() const { return std::strtol(s.c_str(), nullptr, 10); }
    float toFloat() const { return (float)std::strtod(s.c_str(), nullptr); }
    int indexOf(char c, unsigned int from = 0) const { auto i = s.find(c, from); return i == std::string::npos ? -1 : (int)i; }
    int indexOf(const String &o, unsigned int from = 0) const { auto i = s.find(o.s, from); return i == std::string::npos ? -1 : (int)i; }
    String substring(unsigned int a) const { return a < s.size() ? String(s.substr(a)) : String(); }
    String substring(unsigned int a, unsigned int b) const {
        if (a > b) std::swap(a, b);
        if (a >= s.size()) return String();
        return String(s.substr(a, b - a));
    }
    void trim() {
        size_t a = s.find_first_not_of(" \t\r\n");
        size_t b = s.find_last_not_of(" \t\r\n");
        s = a == std::string::npos ? "" : s.substr(a, b - a + 1);
    }
    void toUpperCase() { for (auto &c : s) c = (char)std::toupper((unsigned char)c); }
    void toLowerCase() { for (auto &c : s) c = (char)std::tolower((unsigned char)c); }

  private:
    void from_ulong(unsigned long v, int base) {
        char b[40]; int i = 39; b[i] = 0;
        if (v == 0) b[--i] = '0';
        while (v) { int d = v % base; b[--i] = (char)(d < 10 ? '0' + d : 'A' + d - 10); v /= base; }
        s = b + i;
    }
    void from_long(long v, int base) {
        if (v < 0 && base == 10) { from_ulong((unsigned long)(-v), 10); s = "-" + s; }
        else from_ulong((unsigned long)v, base);
    }
};
inline String operator+(const String &a, const String &b) { return String(a.s + b.s); }
inline String operator+(const String &a, const char *b) { return String(a.s + b); }
inline String operator+(const char *a, const String &b) { return String(std::string(a) + b.s); }
inline String operator+(const String &a, char c) { return String(a.s + c); }
inline String operator+(const String &a, int v) { return a + String(v); }
inline String operator+(const String &a, long v) { return a + String(v); }
inline String operator+(const String &a, unsigned long v) { return a + String(v); }
inline String operator+(const String &a, double v) { return a + String(v); }

// ---------------------------------------------------------------- Serial
class HardwareSerial {
  public:
    unsigned long baud = 0;
    unsigned long timeout_ms = 1000;
    struct In { uint64_t t0; size_t idx; char c; };
    std::deque<In> incoming;                          // characters the PC will send: start time, position, character
    std::deque<char> rx;                              // the 64-byte receive buffer
    uint64_t tx_free_ns = 0;                          // when the transmitter will have sent everything
    bool at_line_start = true;
    unsigned long lost = 0;                           // characters lost because the receive buffer was full
    std::function<void(uint8_t)> tx_hook;            // if set, sent bytes go here instead of to the screen

    void begin(unsigned long b) { baud = b; }
    void end() { baud = 0; }
    explicit operator bool() const { return true; }
    uint64_t char_ns() const { return baud ? 10ULL * 1000000000ULL / baud : 0; }   // 10 bits per character

    size_t write(uint8_t c) {
        if (!baud) return 0;
        uint64_t per = char_ns();
        sim::advance(5000);                           // the CPU's own work to hand over one character
        // the transmit buffer holds 64 characters; if it is full, wait (this is where printing gets slow)
        while (tx_free_ns > sim::now_ns && (tx_free_ns - sim::now_ns) / per >= 64) sim::advance(per / 4 + 1);
        tx_free_ns = (tx_free_ns > sim::now_ns ? tx_free_ns : sim::now_ns) + per;
        if (tx_hook) { tx_hook(c); return 1; }      // a test that reads binary data takes the byte
        if (at_line_start && sim::serial_time) std::fputs(sim::stamp(), stdout);
        std::fputc(c, stdout);
        at_line_start = (c == '\n');
        return 1;
    }
    size_t write(const char *str) { size_t n = 0; while (*str) n += write((uint8_t)*str++); return n; }
    size_t write(const uint8_t *buf, size_t len) { size_t n = 0; for (size_t i = 0; i < len; i++) n += write(buf[i]); return n; }
    void flush() { if (tx_free_ns > sim::now_ns) sim::advance(tx_free_ns - sim::now_ns); }
    int availableForWrite() {
        if (tx_free_ns <= sim::now_ns || !baud) return 63;
        int q = (int)((tx_free_ns - sim::now_ns) / char_ns());
        return q >= 63 ? 0 : 63 - q;
    }

    size_t print(const char *str) { return write(str); }
    size_t print(const String &str) { return write(str.c_str()); }
    size_t print(char c) { return write((uint8_t)c); }
    size_t print(unsigned long v, int base = DEC) { return write(String(v, base).c_str()); }
    size_t print(long v, int base = DEC) { return write(String(v, base).c_str()); }
    size_t print(unsigned int v, int base = DEC) { return print((unsigned long)v, base); }
    size_t print(int v, int base = DEC) { return print((long)v, base); }
    size_t print(unsigned char v, int base = DEC) { return print((unsigned long)v, base); }
    size_t print(bool v) { return print((int)v); }
    size_t print(long long v, int base = DEC) { return print((long)v, base); }
    size_t print(unsigned long long v, int base = DEC) { return print((unsigned long)v, base); }
    size_t print(double v, int digits = 2) {        // the same method as the real Arduino Print class
        if (std::isnan(v)) return print("nan");
        if (std::isinf(v)) return print("inf");
        if (v > 4294967040.0 || v < -4294967040.0) return print("ovf");
        size_t n = 0;
        if (v < 0.0) { n += print('-'); v = -v; }
        double rounding = 0.5;
        for (int i = 0; i < digits; ++i) rounding /= 10.0;
        v += rounding;
        unsigned long whole = (unsigned long)v;
        double rest = v - (double)whole;
        n += print(whole);
        if (digits > 0) n += print('.');
        while (digits-- > 0) { rest *= 10.0; unsigned int d = (unsigned int)rest; n += print(d); rest -= d; }
        return n;
    }
    template <class T> size_t println(T v) { size_t n = print(v); return n + print("\r\n"); }
    template <class T> size_t println(T v, int f) { size_t n = print(v, f); return n + print("\r\n"); }
    size_t println() { return print("\r\n"); }

    // receiving
    void pull() {                                     // move characters that have arrived into the buffer
        uint64_t per = baud ? char_ns() : 1041667;
        while (!incoming.empty() && incoming.front().t0 + (incoming.front().idx + 1) * per <= sim::now_ns) {
            if (rx.size() < 64) rx.push_back(incoming.front().c);
            else lost++;
            incoming.pop_front();
        }
    }
    int available() { sim::advance(1000); pull(); return (int)rx.size(); }
    int read() { pull(); if (rx.empty()) return -1; char c = rx.front(); rx.pop_front(); return (unsigned char)c; }
    int peek() { pull(); return rx.empty() ? -1 : (unsigned char)rx.front(); }
    void setTimeout(unsigned long ms) { timeout_ms = ms; }
    int timed_read() {
        uint64_t start = sim::now_ns;
        while (true) {
            int c = read();
            if (c >= 0) return c;
            if (sim::now_ns - start >= (uint64_t)timeout_ms * 1000000ULL) return -1;
            sim::advance(100000);
        }
    }
    String readStringUntil(char end) {
        String r;
        int c;
        while ((c = timed_read()) >= 0 && c != end) r += (char)c;
        return r;
    }
    String readString() { String r; int c; while ((c = timed_read()) >= 0) r += (char)c; return r; }
    long parseInt() {
        int c;
        do { c = timed_read(); } while (c >= 0 && c != '-' && (c < '0' || c > '9'));
        if (c < 0) return 0;
        bool neg = c == '-';
        long v = neg ? 0 : c - '0';
        while ((c = peek()) >= '0' && c <= '9') { read(); v = v * 10 + (c - '0'); }
        return neg ? -v : v;
    }
};
inline HardwareSerial Serial;

namespace sim {
// The PC sends text to the sketch, starting at time at_ms (as if typed in the Serial Monitor and sent).
inline void serial_send(double at_ms, const char *text) {
    uint64_t t0 = (uint64_t)(at_ms * 1e6);           // each character arrives one character-time after the one before
    for (size_t i = 0; text[i]; i++) Serial.incoming.push_back({t0, i, text[i]});
}
// The same for any bytes, including 0 and values above 127 (binary packets, Chapter 107).
inline void serial_send_bytes(double at_ms, const std::vector<uint8_t> &bytes) {
    uint64_t t0 = (uint64_t)(at_ms * 1e6);
    for (size_t i = 0; i < bytes.size(); i++) Serial.incoming.push_back({t0, i, (char)bytes[i]});
}
}  // namespace sim
