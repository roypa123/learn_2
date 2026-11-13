// Debouncer.cpp - how a Debouncer does its work
#include "Debouncer.h"

Debouncer::Debouncer(uint8_t pin, unsigned long stableMs) {
  _pin = pin;
  _stableMs = stableMs;
  _stable = HIGH;
  _last = HIGH;
  _changedAt = 0;
  _presses = 0;
}

void Debouncer::begin() {
  pinMode(_pin, INPUT_PULLUP);
  _stable = digitalRead(_pin);
  _last = _stable;
  _changedAt = millis();
}

bool Debouncer::update() {
  int now = digitalRead(_pin);
  if (now != _last) {                  // still changing: start timing again
    _last = now;
    _changedAt = millis();
  }
  if (_stable != _last && millis() - _changedAt >= _stableMs) {   // steady long enough: believe it
    _stable = _last;
    if (_stable == LOW) {              // pressed (the pull-up makes free = HIGH)
      _presses++;
      return true;
    }
  }
  return false;
}

bool Debouncer::isPressed() const {
  return _stable == LOW;
}

unsigned long Debouncer::presses() const {
  return _presses;
}
