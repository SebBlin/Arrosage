# Arrosage

This is a personal project for the watering of my garden. The objective is to be able to configure, from my phone, the scheduling of the starts and durations of watering.
This project is built from diffrent parts/components:
- 4 diffrent sprinklers are connected to one solenoid valve for each; and solenoid valve are controled relays
- The 4 relays are controled by an arduino that is listening to a specific FR433 protocol
- The Crontab from the Raspberry is scheduled to send watering starts to the arduino by using this RF433 protocol
- The Raspberry also expose a Web GUI et API that make it easy to manage the crontab schedulings.

                                                                                                                          +---------------+
                                                                                                                          |               |
                                                                                                                          |  +---------+  |       +---------+
                          +-----------------------------------------+                                                     |  |         |  |       |         | Water
                          |     Raspberry                           |                                                   +----+ Relay 1 +--------->+ El Va 1 +--------->
                          |                                         |                                                   | |  |         |  |       |         |
                          |                                         |                                                   | |  +---------+  |       +---------+
                          |    +--------------+                     |                                                   | |               |
                          |    |              |                     |                                                   | |  +---------+  |       +---------+
                       +-------+  GUI Server  |                     |                                                   | |  |         |  |       |         | Water
+------------+         |  |    |              |                     |                                                   +--->+ Relay 2 +--------->+ El Va 2 +--------->
|   Browser  |         |  |    ---------------+                     |       RF433         +---------------------------+ | |  |         |  |       |         |
|            +---------+  |                                         |          +--+       |   Arduino                 | | |  +---------+  |       +---------+
|            |         |  |                                         |          |  |       |                           | | |               |
+------------+         |  |    +--------------+    +-------------+  |          |  |       |   +-----------------+     | | |  +---------+  |       +---------+
                       |  |    |              |    |             |  |          |  |       |   |                 |     +-+ |  |         |  |       |         | Water
                       +-------+  API Server  +--->+  Crontab    +----------+  |  +-------->  |  Manager        |     +----->+ Relay 3 +--------->+ El Va 3 +--------->
                          |    |              |    |             |  |       |  |          |   |                 |     | | |  |         |  |       |         |
                          |    +--------------+    +-------------+  |       |  |          |   +-----------------+     | | |  +---------+  |       +---------+
                          |                                         |       +--+          |                           | | |               |
                          +-----------------------------------------+                     +---------------------------+ | |  +---------+  |       +---------+
                                                                                                                        | |  |         |  |       |         | Water
                                                                                                                        +--->+ Relay 4 +--------->+ El Va 4 +--------->
                                                                                                                          |  |         |  |       |         |
                                                                                                                          |  +---------+  |       +-----+---+
                                                                                                                          |               |             ^
                                                                                                                          +---------------+             |
                                                                                                                                                        | Water
                                                                                                                                                        |
                                                                                                                                                        |
                                                                                                                                                        +

## Details of components

### Web GUI
The Web UI is build with 'react'. the source code is in the directory ./arrosage/. 
The main entry point is in `src/App.js`

There is a configuration point to point to the right API server endpoint, 


To start the Web GUI server, execute 
```
cd arrosage
export HOST=
npm start
```


### API SRV


### Arduino Manager


# setup 
install libs:
pip3 install Flask Flask_cors pandas
sudo apt-get install libatlas-base-dev

