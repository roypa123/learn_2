// avr_regs.h - the ATmega328P's registers on the PC test bench (Chapter 106)
//
// Include it after run.h (or Arduino.h) and before the sketch. It adds:
//   - the port registers PORTB/C/D, DDRB/C/D and PINB/C/D (Chapter 98), which change the simulated
//     pins directly and take about 2 clock ticks (125 ns), as on a real Uno;
//   - Timer0's prescaler bits in TCCR0B: changing them changes the speed of millis(), micros() and delay();
//   - Timer1 (16 bits) and Timer2 (8 bits) counting the 16 MHz clock through their prescalers,
//     in normal, CTC and fast PWM modes, with their compare and overflow interrupts, and the
//     hardware outputs OC1A (pin 9), OC1B (pin 10), OC2A (pin 11) and OC2B (pin 3);
//   - ISR(vector) { ... } for Timer1 and Timer2 interrupts.
// Not simulated: phase-correct PWM modes, input capture, the watchdog, the "write 1 to clear" flag trick.
// At power-on the Arduino core leaves Timer1 and Timer2 in phase-correct mode (for analogWrite);
// a sketch that uses them sets TCCRnA and TCCRnB itself, as every sketch in this course does.
#pragma once
#include "Arduino.h"
#include <map>
#include <string>

#define _BV(b) (1 << (b))
inline void sei() { interrupts(); }
inline void cli() { noInterrupts(); }

// ---------------------------------------------------------------- bit names (from the datasheet)
enum : uint8_t {
    PB0 = 0, PB1, PB2, PB3, PB4, PB5, PB6, PB7,
    PC0 = 0, PC1, PC2, PC3, PC4, PC5, PC6,
    PD0 = 0, PD1, PD2, PD3, PD4, PD5, PD6, PD7,
    CS00 = 0, CS01 = 1, CS02 = 2, WGM02 = 3, WGM00 = 0, WGM01 = 1,
    CS10 = 0, CS11 = 1, CS12 = 2, WGM12 = 3, WGM13 = 4, ICES1 = 6, ICNC1 = 7,
    WGM10 = 0, WGM11 = 1, COM1B0 = 4, COM1B1 = 5, COM1A0 = 6, COM1A1 = 7,
    TOIE1 = 0, OCIE1A = 1, OCIE1B = 2, ICIE1 = 5, TOV1 = 0, OCF1A = 1, OCF1B = 2,
    CS20 = 0, CS21 = 1, CS22 = 2, WGM22 = 3, WGM20 = 0, WGM21 = 1,
    COM2B0 = 4, COM2B1 = 5, COM2A0 = 6, COM2A1 = 7,
    TOIE2 = 0, OCIE2A = 1, OCIE2B = 2, TOV2 = 0, OCF2A = 1, OCF2B = 2,
};

// ---------------------------------------------------------------- port registers
namespace sim {
inline int port_pin(int port, int bit) {          // port 0 = B (pins 8-13), 1 = C (A0-A5), 2 = D (pins 0-7)
    if (port == 0) return bit <= 5 ? 8 + bit : -1;
    if (port == 1) return bit <= 5 ? 14 + bit : -1;
    return bit;
}
inline void set_level(int p, int v) {
    if (level[p] != v && trace_pins) std::printf("%spin %d -> %s\n", stamp(), p, v ? "HIGH" : "LOW");
    level[p] = v;
}
}  // namespace sim

struct PortReg {                                  // kind 0 = PORTx, 1 = DDRx, 2 = PINx
    int port, kind;
    uint8_t get() const {
        uint8_t v = 0;
        for (int b = 0; b < 8; b++) {
            int p = sim::port_pin(port, b);
            if (p < 0) continue;
            int bit;
            if (kind == 1) bit = sim::mode[p] == OUTPUT;
            else if (kind == 0) bit = sim::mode[p] == OUTPUT ? sim::level[p] : sim::mode[p] == INPUT_PULLUP;
            else bit = sim::mode[p] == OUTPUT ? sim::level[p] : sim::pin_from_outside(p);
            v |= bit << b;
        }
        return v;
    }
    void put(uint8_t v) {
        for (int b = 0; b < 8; b++) {
            int p = sim::port_pin(port, b);
            if (p < 0) continue;
            int bit = (v >> b) & 1;
            if (kind == 1) {                      // DDR: 1 = output
                if (bit) sim::mode[p] = OUTPUT;
                else if (sim::mode[p] == OUTPUT) sim::mode[p] = sim::level[p] ? INPUT_PULLUP : INPUT;
            } else if (kind == 0) {               // PORT: output level, or pull-up for an input
                if (sim::mode[p] == OUTPUT) { sim::pwm[p] = -1; sim::set_level(p, bit); }
                else sim::mode[p] = bit ? INPUT_PULLUP : INPUT;
            } else if (bit && sim::mode[p] == OUTPUT) {
                sim::set_level(p, !sim::level[p]);   // writing 1 to PINx toggles the pin
            }
        }
    }
    operator uint8_t() const { sim::advance(125); return get(); }   // about 2 clock ticks
    PortReg &operator=(int v) { sim::advance(125); put((uint8_t)v); return *this; }
    PortReg &operator|=(int v) { sim::advance(125); put(get() | (uint8_t)v); return *this; }
    PortReg &operator&=(int v) { sim::advance(125); put(get() & (uint8_t)v); return *this; }
    PortReg &operator^=(int v) { sim::advance(125); put(get() ^ (uint8_t)v); return *this; }
};
inline PortReg PORTB{0, 0}, DDRB{0, 1}, PINB{0, 2};
inline PortReg PORTC{1, 0}, DDRC{1, 1}, PINC{1, 2};
inline PortReg PORTD{2, 0}, DDRD{2, 1}, PIND{2, 2};

// ---------------------------------------------------------------- timer registers
// Values at the start of setup(), as the Arduino core leaves them.
inline volatile uint8_t TCCR0A = 0x03, TCCR0B = 0x03;              // Timer0: prescaler 64 for millis()
inline volatile uint8_t TCCR1A = 0x01, TCCR1B = 0x03, TIMSK1 = 0, TIFR1 = 0;
inline volatile uint16_t TCNT1 = 0, OCR1A = 0, OCR1B = 0, ICR1 = 0;
inline volatile uint8_t TCCR2A = 0x01, TCCR2B = 0x04, TIMSK2 = 0, TIFR2 = 0;
inline volatile uint8_t TCNT2 = 0, OCR2A = 0, OCR2B = 0;

// ---------------------------------------------------------------- interrupt vectors
namespace sim {
inline std::map<std::string, void (*)()> &vectors() { static std::map<std::string, void (*)()> v; return v; }
struct VectorReg { VectorReg(const char *name, void (*f)()) { vectors()[name] = f; } };
inline void run_vector(const char *name) {
    auto it = vectors().find(name);
    if (it == vectors().end()) return;
    bool saved = int_enabled;
    int_enabled = false;                          // an ISR runs with interrupts off
    it->second();
    int_enabled = saved;
}
}  // namespace sim
#define ISR(vect) \
    void vect##_isr(); \
    static sim::VectorReg vect##_reg(#vect, vect##_isr); \
    void vect##_isr()

// ---------------------------------------------------------------- the timers themselves
namespace sim {
struct Timer {
    bool sixteen;                                 // Timer1: 16 bits; Timer2: 8 bits
    uint64_t last_cycle = 0;                      // CPU clock cycles already counted
    uint64_t spare = 0;                           // cycles not yet making a whole timer tick
    // a "logic analyser" on output A's pin (9 or 11), counted at every timer tick, for tests
    uint64_t an_ticks = 0, an_high = 0, an_rises = 0;
    int an_last = 0;
    int presc() const {
        int cs = (sixteen ? TCCR1B : TCCR2B) & 7;
        static const int t1[8] = {0, 1, 8, 64, 256, 1024, 0, 0};
        static const int t2[8] = {0, 1, 8, 32, 64, 128, 256, 1024};
        return sixteen ? t1[cs] : t2[cs];
    }
    int wgm() const {
        if (sixteen) return ((TCCR1B >> 3) & 3) << 2 | (TCCR1A & 3);
        return ((TCCR2B >> 3) & 1) << 2 | (TCCR2A & 3);
    }
    // TOP for this mode, or -1 if the mode is not simulated
    long top() const {
        int m = wgm();
        if (sixteen) {
            switch (m) {
                case 0: return 0xFFFF;
                case 4: case 15: return OCR1A;
                case 12: case 14: return ICR1;
                case 5: return 0xFF;
                case 6: return 0x1FF;
                case 7: return 0x3FF;
            }
        } else {
            switch (m) {
                case 0: case 3: return 0xFF;
                case 2: case 7: return OCR2A;
            }
        }
        return -1;
    }
    bool fast_pwm() const {
        int m = wgm();
        return sixteen ? (m == 5 || m == 6 || m == 7 || m == 14 || m == 15) : (m == 3 || m == 7);
    }
    bool ctc() const { int m = wgm(); return sixteen ? (m == 4 || m == 12) : m == 2; }
    void tick() {
        long t = top();
        uint16_t cnt = sixteen ? TCNT1 : TCNT2;
        uint16_t ocra = sixteen ? OCR1A : OCR2A, ocrb = sixteen ? OCR1B : OCR2B;
        volatile uint8_t &flags = sixteen ? TIFR1 : TIFR2;
        bool wrapped = false;
        if (cnt >= t) { cnt = 0; wrapped = true; } else cnt++;
        if (wrapped && !ctc()) flags |= 1;        // overflow flag (TOV): at MAX, or at TOP in fast PWM
        bool ma = cnt == ocra, mb = cnt == ocrb;
        if (ma) flags |= 2;
        if (mb) flags |= 4;
        if (sixteen) TCNT1 = cnt; else TCNT2 = (uint8_t)cnt;
        uint8_t ctrl = sixteen ? TCCR1A : TCCR2A;
        int pa = sixteen ? 9 : 11, pb = sixteen ? 10 : 3;
        int coma = (ctrl >> 6) & 3, comb = (ctrl >> 4) & 3;
        if (fast_pwm()) {                         // non-inverting: HIGH from BOTTOM until the compare match
            if (coma == 2 && mode[pa] == OUTPUT) set_level(pa, cnt <= ocra);
            if (comb == 2 && mode[pb] == OUTPUT) set_level(pb, cnt <= ocrb);
        } else {                                  // normal or CTC: COMnx = 1 toggles the pin at each match
            if (coma == 1 && ma && mode[pa] == OUTPUT) set_level(pa, !level[pa]);
            if (comb == 1 && mb && mode[pb] == OUTPUT) set_level(pb, !level[pb]);
        }
        an_ticks++;
        if (level[pa]) an_high++;
        if (level[pa] && !an_last) an_rises++;
        an_last = level[pa];
    }
    void update() {
        uint64_t cyc = now_ns * 2 / 125;          // 16 MHz: 16 cycles per microsecond
        uint64_t d = cyc - last_cycle;
        last_cycle = cyc;
        int p = presc();
        if (p == 0 || top() < 0) { spare = 0; return; }   // stopped, or a mode the bench does not simulate
        spare += d;
        while (spare >= (uint64_t)p) { spare -= p; tick(); }
    }
    void interrupts_due() {
        volatile uint8_t &flags = sixteen ? TIFR1 : TIFR2;
        uint8_t mask = sixteen ? TIMSK1 : TIMSK2;
        static const char *n1[3] = {"TIMER1_OVF_vect", "TIMER1_COMPA_vect", "TIMER1_COMPB_vect"};
        static const char *n2[3] = {"TIMER2_OVF_vect", "TIMER2_COMPA_vect", "TIMER2_COMPB_vect"};
        for (int k : {1, 2, 0}) {                 // the datasheet's priority order: COMPA, COMPB, OVF
            if (!int_enabled) return;
            if ((flags >> k & 1) && (mask >> k & 1)) {
                flags &= ~(1 << k);               // the hardware clears the flag when the ISR starts
                run_vector(sixteen ? n1[k] : n2[k]);
            }
        }
    }
};
inline Timer timer1{true}, timer2{false};
inline uint8_t last_tccr0b = 0x03;
inline bool in_timer_hook = false;
inline void timer_hook() {
    if (in_timer_hook) return;                    // an ISR is running: catch up afterwards
    in_timer_hook = true;
    if (TCCR0B != last_tccr0b) {                  // Timer0's prescaler changed: millis() changes speed
        last_tccr0b = TCCR0B;
        static const int t0[8] = {0, 1, 8, 64, 256, 1024, 0, 0};
        int p = t0[TCCR0B & 7];
        set_t0_rate(p ? 64.0 / p : 0.0);
    }
    timer1.update();
    timer2.update();
    timer1.interrupts_due();
    timer2.interrupts_due();
    in_timer_hook = false;
}
struct TimerHookReg { TimerHookReg() { tick_hooks.push_back(timer_hook); } };
inline TimerHookReg timer_hook_reg;
}  // namespace sim
