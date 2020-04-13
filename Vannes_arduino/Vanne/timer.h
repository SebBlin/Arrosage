#ifndef timer_h
#define timer_h

#include "Arduino.h"

class timer
{
  public:
    timer(char delay);
    bool tick();
    void start(unsigned long nb_ms);
    bool is_active();
    void reset();
  private:
    char _delay;
    int _modulo;
    bool _ticked;
    unsigned long _start_time;
    unsigned long _nb_ms;

};

#endif