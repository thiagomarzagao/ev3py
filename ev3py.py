'''
This module implements the class 'EV3', which you can use to interact 
with LEGO Mindstorms EV3 bricks.

Tested on: 
- OS X 10.9.3 with Python 2.7.6

To do:
- all other EV3 commands! (only a couple are implemented here)
- USB capability
- WiFi capability
- error checking
- multiple layers support
- Linux support
- Windows support

Last modified: 21/06/2014
Author: Thiago Marzagao (tmarzagao at gmail dot com)
'''

from dec_to_hex import h # decimal-to-hexadecimal dictionary

# globals    
PRIMPAR_SHORT = 0x00
PRIMPAR_LONG = 0x80
PRIMPAR_CONST = 0x00
PRIMPAR_VALUE = 0x3F
PRIMPAR_1_BYTE = 1
PRIMPAR_2_BYTES = 2
PRIMPAR_4_BYTES = 4

def LC0(v):
    '''
    format 1-byte argument
    '''
    byte1 = ((v & PRIMPAR_VALUE) | PRIMPAR_SHORT | PRIMPAR_CONST)
    return h[byte1]

def LC1(v):
    '''
    format 2-byte argument
    '''    
    byte1 = (PRIMPAR_LONG | PRIMPAR_CONST | PRIMPAR_1_BYTE)
    byte2 = (v & 0xFF)
    return h[byte1] + h[byte2]

def LC2(v):
    '''
    format 3-byte argument
    '''    
    byte1 = (PRIMPAR_LONG | PRIMPAR_CONST | PRIMPAR_2_BYTES)
    byte2 = (v & 0xFF)
    byte3 = ((v >> 8) & 0xFF)
    return h[byte1] + h[byte2] + h[byte3]

class ev3:

    '''
    this class lets you interact with EV3 bricks
    '''

    def __init__(self):

        '''
        data used by several methods
        '''

        self.port_to_hex = {'a': 1, 'b': 2, 'c': 4, 'd': 8}

    def connect(self, mode):
    
        '''
        connect to EV3

        mode: 'bt' (bluetooth), 'usb', 'wifi'
        '''

        modes = {'bt': '/dev/tty.EV3-SerialPort',
                 'usb': '', # must add usb support
                 'wifi': ''} # must add wifi support
        self.brick = open(modes[mode], mode = 'w+', buffering = 0)

    def start_motor(self, ports, power, layer=0):

        '''
        start motors at specified ports, power, and layer
        
        ports: a, b, c, d, any combinations thereof
            type: str or iterable
            examples: 'a', 'bcd', ['d', 'c'], ['a'], ('c', 'b')
        power: -100...+100
            type: int
            obs.: -100 is full power backward, 100 is full power forward
        layer: 0, 1, 2, 3 (use 0 unless you have multiple EV3 bricks)
            type: int
        '''

        # map ports: str->int
        ports = [self.port_to_hex[port] for port in ports]

        # write out command for each port
        commands = []
        for port in ports:

            # opOUTPUT_POWER
            comm_1 = '\xA4' + LC0(layer) + LC0(port) + LC1(power)

            # opOUTPUT_START
            comm_2 = '\xA6' + LC0(layer) + LC0(port)

            # set message size, message counter, command type, vars
            msg_size = len(comm_1 + comm_2) + 5
            comm_0 = h[msg_size] + '\x00\x00\x00\x80\x00\x00'

            # assemble command
            command = comm_0 + comm_1 + comm_2
            commands.append(command)

        # send command to each port        
        for command in commands:
            self.brick.write(command)
        
    def stop_motor(self, ports, mode='coast', layer=0):
 
        '''
        stop motors at specified ports and layer
        
        ports: a, b, c, d, any combinations thereof
            type: str or iterable
            examples: 'a', 'bcd', ['d', 'c'], ['a'], ('c', 'b')
        mode: 'break', 'coast'
        layer: 0, 1, 2, 3 (use 0 unless you have multiple EV3 bricks)
        '''

        # map ports: str->int
        ports = [self.port_to_hex[port] for port in ports]

        # map mode: str->int
        modes = {'break': 1, 'coast': 0}
        mode = modes[mode]
 
        # set message size, message counter, command type, vars
        comm_0 = '\x09\x00\x01\x00\x80\x00\x00'

        for port in ports:

            # opOUTPUT_STOP
            comm_1 = '\xA3' + LC0(layer) + LC0(port) + LC0(mode)

            # assemble command and send
            command = comm_0 + comm_1
            self.brick.write(command)

    def read_sensor(self, port, layer=0):
        
        '''
        read sensor from specified port (unit: percentage)
        
        port: 0, 1, 2, 3
        layer: 0, 1, 2, 3 (use 0 unless you have multiple EV3 bricks)
        '''

        # set message size, message counter, command type, vars
        comm_0 = '\x0B\x00\x00\x00\x00\x01\x00'

        # opINPUT_READ
        comm_1 = '\x9A' + LC0(layer) + LC0(port) + '\x00\x00\x60'

        # assemble command and send
        command = comm_0 + comm_1
        self.brick.write(command)
        sensor_data = self.brick.read(6)
        return int(hex(ord(sensor_data[5])), 16)
        
    def disconnect(self):
        self.brick.close()
