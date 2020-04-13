#!/usr/bin/env python3

import argparse
import logging
import json
from time import sleep
 
from rpi_rf import RFDevice

STAT_ON  = 1
STAT_OFF = 0

def send_start_cmd(vanne: int):
    code = calc_code(vanne, STAT_ON)
    rfdevice.tx_code(code, config['protocol'], config['pulselength'])
    cs = calc_check_code(vanne, STAT_ON)
    rfdevice.tx_code(cs, config['protocol'], config['pulselength'])

def send_stop_cmd(vanne: int):
    code = calc_code(vanne, STAT_OFF)
    rfdevice.tx_code(code, config['protocol'], config['pulselength'])
    cs = calc_check_code(vanne, STAT_OFF)
    rfdevice.tx_code(cs, config['protocol'], config['pulselength'])


def calc_code(vanne, stat):
    const = 125
    ev    = vanne
    st    = stat
    code  = const<<8 | ev<<4 | st
    return code

def calc_check_code(vanne, stat):
    const = 125
    ev    = vanne
    st    = stat
    cs    = const + 7*ev + st
    return cs

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

parser = argparse.ArgumentParser(description='Start arrosage')
parser.add_argument('vanne', metavar='VANNE', type=int, help="number of Vanne")                
parser.add_argument('duree', metavar='DUREE', type=int, help="length of watering (in min)")
parser.add_argument('-g', dest='gpio', type=int, default=17, help="GPIO pin (Default: 17)")
parser.add_argument('-p', dest='pulselength', type=int, default=None, help="Pulselength (Default: 350)")
args = parser.parse_args()


config_file = 'arrosage.json'
with open(config_file, "r") as read_file:
    config = json.load(read_file)

rfdevice = RFDevice(config['gpio'])
rfdevice.enable_tx()

duree_s = args.duree * 60
lsw = config['len_seq_watering']
nb_iter = duree_s // (lsw - 3)
rest = duree_s % (lsw - 3)
print (nb_iter )
print(rest)

send_start_cmd(args.vanne)
for i in range(nb_iter):
    sleep(lsw - 3)
    send_start_cmd(args.vanne)
sleep(rest)
send_stop_cmd(args.vanne)


rfdevice.cleanup()

