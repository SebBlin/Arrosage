/*
  Example for receiving
  
  https://github.com/sui77/rc-switch/
  
  If you want to visualize a telegram copy the raw data and 
  paste it into http://test.sui.li/oszi/
*/

#include <RCSwitch.h>
#include "Vanne.h"
#include "timer.h"
#include "DHT.h"

#define DHTPIN 7
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

RCSwitch mySwitch = RCSwitch();

const bool DEBUG = false;

const int hard_code = 125;

// definition of status 
const int WAIT_CMD     = 1;
const int WAIT_CONFIRM = 2;

int stat_status = WAIT_CMD;

unsigned long rec_val = 0;
unsigned long conf_val = 0;
unsigned long confirm_code = 0;

unsigned long cur_time = 0;

timer t('s');
timer t_confirm('s');
  
struct cmd {
  byte code;
  byte vanne;
  byte stat;
};

const int nb_vannes = 5;
const int vanne_pin[nb_vannes] = {8,9,10,11};
Vanne l_vannes[nb_vannes] ;

cmd checkcommand(unsigned long code) {
  cmd c;
  c.code = code >> 8 ;
  c.vanne = (code >> 4) & 15 ;
  c.stat = code & 15 ;
  return c ;
}

void debug(String msg) {
  if (DEBUG) {
    Serial.println(msg);
  }
}

unsigned long get_confirm_code(cmd c) {
  return c.code + c.vanne * 7 + c.stat;
}

bool validatecommand(cmd c) {
  return (c.code == hard_code) & (c.vanne > 0) & (c.vanne < 10) & (c.stat >= 0) & (c.stat < 2);
}

int do_action(cmd c) {
  // do something
  if (c.stat) {
    l_vannes[c.vanne-1].open();  
  } else 
  {
    l_vannes[c.vanne-1].close();      
  }
}

void read_temp() {
  // https://github.com/adafruit/DHT-sensor-library
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("H: "));
  Serial.print(h);
  Serial.print(F("%  T: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.println("");
//  Serial.print(f);
//  Serial.print(F("°F  Heat index: "));
//  Serial.print(hic);
//  Serial.print(F("°C "));
//  Serial.print(hif);
//  Serial.println(F("°F"));
}




void setup() {
  Serial.begin(9600);
  mySwitch.enableReceive(0);  // Receiver on interrupt 0 => that is pin #2
  for (int i = 0 ; i < nb_vannes ; i += 1)
  {
    l_vannes[i].set_pin(vanne_pin[i]);
    }
  dht.begin();
}


void loop() {
  cmd c;
  cur_time = millis() ;
  if (mySwitch.available()) {
    debug("--stat-- " + String(stat_status));
    if (stat_status == WAIT_CMD) {
      debug("------------------------");
      // output(mySwitch.getReceivedValue(), mySwitch.getReceivedBitlength(), mySwitch.getReceivedDelay(), mySwitch.getReceivedRawdata(),mySwitch.getReceivedProtocol());
      rec_val = mySwitch.getReceivedValue();
      debug("Found : " + String(rec_val));
  
      c = checkcommand(rec_val);
      String msg = "code : " + String(c.code) + " ; vanne : " + String(c.vanne) + " ; stat : " + String(c.stat) ;
      debug(msg);
  
      if (validatecommand(c)) {
        debug("Command validated");
        Serial.println(msg);
        confirm_code = get_confirm_code(c);
        conf_val = 0 ;
        stat_status = WAIT_CONFIRM;
        t_confirm.start(2000);
      } else {
        debug("Command not validated"); 
      }
      mySwitch.resetAvailable();
    }
    if (stat_status == WAIT_CONFIRM) {
      debug("++++++++++++++++++++++++");
      conf_val = mySwitch.getReceivedValue();
      debug("Found : " + String(conf_val));
      debug("wait for : " + String(confirm_code));

      if (confirm_code == conf_val) {
        // Code confirmed Do action
        int res = do_action(c);
        debug(" => DO ACTION !");
        stat_status = WAIT_CMD;
      }
      mySwitch.resetAvailable();
      if (!t_confirm.is_active()) {
        debug("! delai dépassé !");
        stat_status = WAIT_CMD;
      }
    }
    mySwitch.resetAvailable();  
  }
  if (cur_time % 1000 == 0) {
    // Serial.println(cur_time);
  }
  for (int i = 0 ; i < nb_vannes ; i += 1)
  {
    l_vannes[i].handle_status();
    }

  if (t.tick()) {
    // read_temp();
  }


}
