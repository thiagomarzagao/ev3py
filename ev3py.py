'''
This module offers easy-to-understand methods that you can use to
interact with LEGO Mindstorms EV3 bricks.

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

Author: Thiago Marzagao (tmarzagao at gmail dot com)

See firmware source code (https://github.com/mindboards/ev3sources) for 
info on the data types and opcodes used here.
'''

from dec_to_hex import h # decimal-to-hexadecimal dictionary

# globals
PRIMPAR_SHORT = 0x00
PRIMPAR_LONG = 0x80
PRIMPAR_CONST = 0x00
PRIMPAR_VALUE = 0x3F
PRIMPAR_GLOBAL = 0x20
PRIMPAR_INDEX = 0x1F
PRIMPAR_VARIABEL = 0x40
PRIMPAR_1_BYTE = 1
PRIMPAR_2_BYTES = 2
PRIMPAR_4_BYTES = 3

def LC0(v):
    '''
    format 1-byte local constant
    '''
    byte1 = ((v & PRIMPAR_VALUE) | PRIMPAR_SHORT | PRIMPAR_CONST)
    return h[byte1]

def LC1(v):
    '''
    format 2-byte local constant
    '''    
    byte1 = (PRIMPAR_LONG | PRIMPAR_CONST | PRIMPAR_1_BYTE)
    byte2 = (v & 0xFF)
    return h[byte1] + h[byte2]

def LC2(v):
    '''
    format 3-byte local constant
    '''    
    byte1 = (PRIMPAR_LONG | PRIMPAR_CONST | PRIMPAR_2_BYTES)
    byte2 = (v & 0xFF)
    byte3 = ((v >> 8) & 0xFF)
    return h[byte1] + h[byte2] + h[byte3]

def LC4(v):
    '''
    format 5-byte local constant
    '''
    byte1 = (PRIMPAR_LONG  | PRIMPAR_CONST | PRIMPAR_4_BYTES)
    byte2 = (v & 0xFF)
    byte3 = ((v >> 8) & 0xFF)
    byte4 = ((v >> 16) & 0xFF)
    byte5 = ((v >> 24) & 0xFF)
    return h[byte1] + h[byte2] + h[byte3] + h[byte4] + h[byte5]

def GV0(v):
    '''
    format 1-byte global variable
    '''
    return h[((v & PRIMPAR_INDEX) | PRIMPAR_SHORT | PRIMPAR_VARIABEL | PRIMPAR_GLOBAL)]

class ev3:

    '''
    this class lets you interact with EV3 bricks
    
    arguments used in several methods:
    
    ports: a, b, c, d, any combinations thereof
        type: str or iterable
        obs.: motor ports
        examples: 'a', 'bcd', ['d', 'c'], ['a'], ('c', 'b')        
    port: 0, 1, 2, 3
        type: int
        obs.: sensor port
    power: -100...+100
        type: int
        obs.: -100 is full power backward, 100 is full power forward
    layer: 0, 1, 2, 3
        type: int
        obs.: use 0 unless you have multiple EV3 bricks
    '''

    def __init__(self):

        '''
        data used by several methods
        '''

        self.ports_to_int = {'a': 1, 'b': 2, 'c': 4, 'd': 8}
        self.stops = {'brake': 1, 'coast': 0}

    def connect(self, conn_type):
    
        '''
        connect to EV3

        conn: 'bt' (bluetooth), 'usb', 'wifi'
        '''

        conn_types = {'bt': '/dev/tty.EV3-SerialPort',
                      'usb': '', # must add usb support
                      'wifi': ''} # must add wifi support
        self.brick = open(conn_types[conn_type], mode = 'w+', buffering = 0)

    def start_motors(self, ports, power, layer=0):

        '''
        start motors at specified ports, power, and layer        
        '''

        # map ports: str->int
        ports = sum([self.ports_to_int[port] for port in ports])

        # opOUTPUT_POWER
        comm_1 = '\xA4' + LC0(layer) + LC0(ports) + LC1(power)

        # opOUTPUT_START
        comm_2 = '\xA6' + LC0(layer) + LC0(ports)

        # set message size, message counter, command type, vars
        msg_size = len(comm_1 + comm_2) + 5
        comm_0 = h[msg_size] + '\x00\x00\x00\x80\x00\x00'

        # assemble command and send to EV3
        command = comm_0 + comm_1 + comm_2
        self.brick.write(command)
                
    def stop_motors(self, ports, stop='coast', layer=0):
 
        '''
        stop motors at specified ports and layer

        stop: 'brake', 'coast'
            type: str
        '''

        # map ports: str->int
        ports = sum([self.ports_to_int[port] for port in ports])

        # map mode: str->int
        stop = self.stops[stop]
 
        # set message size, message counter, command type, vars
        comm_0 = '\x09\x00\x01\x00\x80\x00\x00'

        # opOUTPUT_STOP
        comm_1 = '\xA3' + LC0(layer) + LC0(ports) + LC0(stop)

        # assemble command and send to EV3
        command = comm_0 + comm_1
        self.brick.write(command)

    def start_motors_degrees(self, ports, power, degrees, stop='brake', 
                             ramp_up=0, ramp_down=0, layer=0):

        '''
        start motors at specified ports, power, and layer, and
        stop them after specified number of degrees (accurate to
        +/- 1 degree)
        
        degrees: 0...MAX
            type: int
            obs.: unit is degrees (360 degrees = 1 full turn)
        mode: 'brake', 'coast'
            type: str
        ramp_up: 0...MAX
            type: int
            obs.: makes acceleration constant; unit is degrees
        ramp_down: 0...MAX
            type: int
            obs.: makes deceleration constant; unit is degrees
        '''        

        # map ports: str->int
        ports = sum([self.ports_to_int[port] for port in ports])

        # map mode: str->int
        stop = self.stops[stop]

        # opOUTPUT_STEP_POWER
        comm_1 = '\xAC' + LC0(layer) + LC0(ports) + LC1(power) \
                 + LC4(ramp_up) + LC4(degrees) + LC4(ramp_down) \
                 + LC0(stop)
    
        # opOUTPUT_START
        comm_2 = '\xA6' + LC0(layer) + LC0(ports)

        msg_size = len(comm_1 + comm_2) + 5
        comm_0 = h[msg_size] + '\x00\x00\x00\x80\x00\x00'

        # assemble command and send to EV3
        command = comm_0 + comm_1 + comm_2
        self.brick.write(command)

    def start_motors_time(self, ports, power, time, stop='brake', 
                             ramp_up=0, ramp_down=0, layer=0):

        '''
        start motors at specified ports, power, and layer, and
        stop them after specified number of milliseconds
        
        time: 0...MAX
            type: int
            obs.: unit is milliseconds
        mode: 'brake', 'coast'
            type: str
        ramp_up: 0...MAX
            type: int
            obs.: makes acceleration constant; unit is milliseconds
        ramp_down: 0...MAX
            type: int
            obs.: makes deceleration constant; unit is milliseconds
        '''        

        # map ports: str->int
        ports = sum([self.ports_to_int[port] for port in ports])

        # map mode: str->int
        stop = self.stops[stop]

        # opOUTPUT_STEP_POWER
        comm_1 = '\xAD' + LC0(layer) + LC0(ports) + LC1(power) \
                 + LC4(ramp_up) + LC4(time) + LC4(ramp_down) \
                 + LC0(stop)
    
        # opOUTPUT_START
        comm_2 = '\xA6' + LC0(layer) + LC0(ports)

        msg_size = len(comm_1 + comm_2) + 5
        comm_0 = h[msg_size] + '\x00\x00\x00\x80\x00\x00'

        # assemble command and send to EV3
        command = comm_0 + comm_1 + comm_2
        self.brick.write(command)

    def read_sensor(self, port, layer=0):
        
        '''
        read sensor from specified port (unit: percentage)
        '''

        # set message size, message counter, command type, vars
        comm_0 = '\x0B\x00\x00\x00\x00\x01\x00'

        # opINPUT_READ
        comm_1 = '\x9A' + LC0(layer) + LC0(port) + '\x00\x00\x60'

        # assemble command and send to EV3
        command = comm_0 + comm_1
        self.brick.write(command)

        # retrieve sensor value (5th byte) and convert to int
        sensor_data = self.brick.read(6)
        return int(hex(ord(sensor_data[5])), 16)

    def disconnect(self):
        self.brick.close()
