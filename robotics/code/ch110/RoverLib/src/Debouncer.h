// Debouncer.h - one button or bumper, read with INPUT_PULLUP and debounced (Chapters 99 and 104)
// This file only DESCRIBES the class: what an object holds and what it can do.
#pragma once
#include <Arduino.h>

class Debouncer {
  public:
    Debouncer(uint8_t pin, unsigned long stableMs = 5);   // the constructor
    void begin();                      // call once, in setup()
    bool update();                     // call often; true once for each new press
    bool isPressed() const;            // the debounced state now
    unsigned long presses() const;     // how many presses so far

  private:
    uint8_t _pin;
    unsigned long _stableMs;           // how long a new level must stay before we believe it
    int _stable;                       // the level we believe
    int _last;                         // the level read last time
    unsigned long _changedAt;          // when _last last changed
    unsigned long _presses;
};
