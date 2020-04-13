#include "Arduino.h"
#include "timer.h"


timer::timer(char delay)
{
  _delay = delay;
  _start_time = 0;
  if (delay == 's')
  {
      _modulo = 1000;
  }
  if (delay == 'd')
  {
      _modulo = 10000;
  }

}

bool timer::tick()
{
  unsigned long ct = millis();
  if (ct % _modulo == 0)
  {
    if (_ticked)
    {
        return false;
    } else {
        _ticked = true;
        return true;
    }
  } else
  {
    _ticked = false;
    return false;
  }
}

void timer::start(unsigned long nb_ms)
{
    _start_time = millis();
    _nb_ms = nb_ms;
}

bool timer::is_active()
{
    unsigned long ct = millis();
    if (_nb_ms == 0) { return false;}
    if (ct - _start_time > _nb_ms) 
    {  // timer finished
        reset();
        return false;
    } else
    {
        return true;
    }
}

void timer::reset()
{
    _start_time = 0;
    _nb_ms = 0;
}
