// test_reaction_game.cpp - the reaction game with the pretend player of world_reaction.h, for 25 seconds
#include "run.h"
#include "avr_int.h"
#include "world_reaction.h"
#include "../reaction_game/reaction_game.ino"

int main() {
  world_setup();
  sim::serial_time = true;
  sim::run_ms(25000);
}
