ev3py
=====

This Python module lets you interact with LEGO Mindstorms EV3 bricks using intuitive, easy-to-understand methods. It communicates with the EV3's native firmware, so there is no need to create a bootable SD card; just turn on the brick and start coding.

For now the module is still inchoate; it only covers three basic functions (starting motors, stopping motors, and reading data from sensors) and it only works on Macs, and only via Bluetooth. The goal is to eventually cover all EV3 capability and make ev3py work with USB and WiFi and also with Linux and Windows.

No installation is necessary. Just download the two files (ev3py.py and dec_to_hex.py) and import the 'ev3' class from ev3py.

Usage example (starts motors in ports A and D, with 20% capacity):

    from ev3py import ev3

    mybrick = ev3()
    mybrick.connect('bt') # connect with EV3 via Bluetooth
    mybrick.start_motors(ports = 'ad', power = 20)
