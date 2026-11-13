// soft_tx_naive.ino - a software UART transmitter written as a C++ class: a first, simple try
class SoftTx {
  public:
    SoftTx(int pin, long baud) {       // the constructor: runs when an object is made
      _pin = pin;
      _bitUs = 1000000L / baud;        // microseconds per bit
    }
    void begin() {
      pinMode(_pin, OUTPUT);
      digitalWrite(_pin, HIGH);        // a UART line rests HIGH (Chapter 107)
    }
    void write(byte b) {
      noInterrupts();                  // nothing may stretch a bit (Chapter 105)
      digitalWrite(_pin, LOW);         // the start bit
      delayMicroseconds(_bitUs);
      for (int k = 0; k < 8; k++) {    // the data bits, lowest first
        digitalWrite(_pin, (b >> k) & 1);
        delayMicroseconds(_bitUs);
      }
      digitalWrite(_pin, HIGH);        // the stop bit
      delayMicroseconds(_bitUs);
      interrupts();
    }
    void print(const char *s) {
      while (*s) {
        write(*s);
        s++;
      }
    }

  private:
    int _pin;                          // each object has its own pin ...
    unsigned int _bitUs;               // ... and its own bit time
};

SoftTx slow(4, 9600);                  // two objects of the same class
SoftTx fast(5, 19200);

void setup() {
  slow.begin();
  fast.begin();
  slow.print("Rover 9600");
  fast.print("Rover 19200");
}

void loop() {
}
