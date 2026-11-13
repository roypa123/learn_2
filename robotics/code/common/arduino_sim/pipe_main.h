// pipe_main.h - run a sketch on the PC test bench under the control of another program (Chapter 111)
//
// Include it after the sketch (and after any world_setup() function). It provides main(), which
// reads commands on stdin, one per line, and answers on stdout:
//   S <hex bytes>   the PC sends these bytes to the sketch's Serial now      -> answers "OK"
//   R <ms>          let <ms> milliseconds of simulated time pass             -> answers "T <hex bytes>"
//                   with every byte the sketch's Serial sent meanwhile
//   Q               stop
// The program at the other end (code/common/bench_link/bench_serial.py) makes this look like
// a serial port to Python code written for pyserial.
#pragma once
#include <iostream>
#include <sstream>
#include <string>

void world_setup();                        // the test's pretend world: inputs, chips (may be empty)

int main() {
    std::string pending;
    Serial.tx_hook = [&](uint8_t b) {
        char h[4];
        std::snprintf(h, sizeof h, "%02X", b);
        pending += h;
    };
    world_setup();
    std::string line;
    uint64_t target_ns = 0;                // where the controlling program's clock is
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        std::string cmd;
        in >> cmd;
        if (cmd == "Q") break;
        if (cmd == "S") {
            std::vector<uint8_t> bytes;
            std::string hex;
            while (in >> hex) bytes.push_back((uint8_t)std::stoul(hex, nullptr, 16));
            sim::serial_send_bytes(sim::t() * 1000.0, bytes);
            std::cout << "OK" << std::endl;
        } else if (cmd == "R") {
            double ms = 0;
            in >> ms;
            target_ns += (uint64_t)(ms * 1e6);
            if (sim::now_ns < target_ns) sim::run_until_ns(target_ns);   // a long loop() pass may end a little later
            std::cout << "T " << pending << std::endl;
            pending.clear();
        }
    }
    return 0;
}
