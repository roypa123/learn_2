// timer1_blink.ino - blink the LED from a Timer1 interrupt: exact timing, and loop() is completely free
ISR(TIMER1_COMPA_vect) {               // runs every time Timer1's count reaches OCR1A
  PINB = (1 << PB5);                   // writing 1 to a PIN bit toggles that pin: pin 13 (PB5)
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  noInterrupts();                      // no interrupts while we set the timer up
  TCCR1A = 0;                          // clear the Arduino core's settings for Timer1
  TCCR1B = 0;
  TCNT1 = 0;                           // start counting from 0
  OCR1A = 31249;                       // 16,000,000 / 256 / 2 - 1: two compare matches per second
  TCCR1B = (1 << WGM12) | (1 << CS12); // CTC mode (count to OCR1A, then back to 0), prescaler 256
  TIMSK1 = (1 << OCIE1A);              // call the ISR at each compare match
  interrupts();
}

void loop() {
  delay(3000);                         // loop() may do anything, even wait: the blinking does not change
}
