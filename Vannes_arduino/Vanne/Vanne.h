/*
  Vanne.h - Library for managing electrovannes.
  Created by Sébastien Blin.
*/
#ifndef Vannes_h
#define Vanne_h

#include "Arduino.h"

class Vanne
{
  public:
    Vanne(int pin);
    Vanne();
    void set_pin(int pin);
    void open();
    void close();
    bool is_open();
    void handle_status();
  private:
    int _pin;
    unsigned long opentime;
    bool _is_open;
};

#endif
