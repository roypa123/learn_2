// soft_tx.ino - the software UART transmitter, fixed: each bit starts at its own planned time
class SoftTx {
  public:
    SoftTx(int pin, long baud) {
      _pin = pin;
      _bitUs = 1000000L / baud;
    }
    void begin() {
      pinMode(_pin, OUTPUT);
      digitalWrite(_pin, HIGH);
    }
    void write(byte b) {
      noInterrupts();
      unsigned long t0 = micros();     // the moment the start bit begins
      digitalWrite(_pin, LOW);
      for (int k = 1; k <= 9; k++) {   // bits 1 to 8 are data, bit 9 is the stop bit
        int level = (k <= 8) ? (b >> (k - 1)) & 1 : HIGH;
        while (micros() - t0 < (unsigned long)k * _bitUs) {
        }                              // wait for this bit's planned start: errors cannot add up
        digitalWrite(_pin, level);
      }
      while (micros() - t0 < 10UL * _bitUs) {
      }                                // let the stop bit last its full time
      interrupts();
    }
    void print(const char *s) {
      while (*s) {
        write(*s);
        s++;
      }
    }

  private:
    int _pin;
    unsigned int _bitUs;
};

SoftTx slow(4, 9600);
SoftTx fast(5, 19200);

void setup() {
  slow.begin();
  fast.begin();
  slow.print("Rover 9600");
  fast.print("Rover 19200");
}

void loop() {
}
