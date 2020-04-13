/*
  Morse.cpp - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "Arduino.h"
#include "Vanne.h"

const int time_stay_open = 30000;

Vanne::Vanne(int pin)
{
  Vanne::set_pin(pin);
  digitalWrite(_pin, LOW);
}

Vanne::Vanne()
{
  _pin = -1;
}

void Vanne::set_pin(int pin)
{
  _pin = pin;
  pinMode(_pin, OUTPUT);
  Vanne::close();
}

void Vanne::open()
{
  digitalWrite(_pin, LOW);
  Vanne::_is_open = true;
  Vanne::opentime = millis();
}

void Vanne::close()
{
  digitalWrite(_pin, HIGH);
  Vanne::_is_open = false;
}

bool Vanne::is_open()
{
    return Vanne::_is_open;
}

void Vanne::handle_status()
{
    if ((millis() - Vanne::opentime) > time_stay_open)
    {
        Vanne::close();
    }
}