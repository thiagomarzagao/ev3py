ev3py
=====

This module implements the class 'EV3', which you can use to interact with LEGO Mindstorms EV3 bricks. 

For now the module is still inchoate; it only covers two basic functions (starting motors and reading data from sensors) and it only works on Macs, and only via Bluetooth. The goal is to eventually cover all EV3 capability and make ev3py work with USB and WiFi and also with Linux and Windows.

No installation is necessary. Just download the two files (ev3py.py and dec_to_hex.py) and import the ev3 class from ev3py.

Usage example:

# start motor in port A with 20% maximum power

from ev3py import ev3

mybrick = ev3()
mybrick.connect('bt')
mybrick.start_motor(port = 'a', power = 20)
