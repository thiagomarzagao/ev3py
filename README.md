###ev3py

This Python module lets you interact with LEGO Mindstorms EV3 bricks using intuitive, easy-to-understand methods. It communicates with the EV3's native firmware, so there is no need to create a bootable SD card; just turn on the brick and start coding.

No installation is necessary. Just download the two files (ev3py.py and dec_to_hex.py) and import the 'ev3' class from ev3py.

Usage example (start motors in ports A and D, with 20% capacity):

from ev3py import ev3

mybrick = ev3()
mybrick.connect('bt') # connect with EV3 via Bluetooth
mybrick.motor_start(ports = 'ad', power = 20)

For now the module is still inchoate; it only covers some basic functions (motor- and sensor-related functions) and it only works on Macs, and only via Bluetooth. The goal is to eventually cover all EV3 capability and make ev3py work with USB and WiFi and also with Linux and Windows.

Help is wanted! If you can help implement more EV3 commands that would be really good karma for you (think of the kids! no, really: think of the kids who may choose a career in STEM because you helped write a module that makes it easier for them to program LEGO Mindstorms).
