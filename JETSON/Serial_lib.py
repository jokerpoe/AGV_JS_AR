# The MIT License
#
# Copyright (c) 2017 Kevin Walchko
#
# This is basically the interface between the Create2 and pyserial

#######ASTI AGV#######
######################
# Author :  Son     ##
# Date:     02102020##
# Version:  0.0.1   ##
######################

import serial # type:ignore
import struct
from OI import OPCODES

class SerialCommandInterface(object):
    """
    This class handles sending commands to the Create2. Writes will take in tuples
    and format the data to transfer to the Create.
    """

    def __init__(self):
        """
        Constructor.

        Creates the serial port, but doesn't open it yet. Call open(port) to open
        it.
        """
        self.ser = serial.Serial()

    def __del__(self):
        """
        Destructor.

        Closes the serial port
        """
        self.close()

    def open(self, port, baud=115200, timeout=1):
        """
        Opens a serial port to the create.

        port: the serial port to open, ie, '/dev/ttyUSB0'
        buad: default is 115200, but can be changed to a lower rate via the create api
        """
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.timeout = timeout
        # print self.ser.name
        if self.ser.is_open:
            self.ser.close()
        self.ser.open()
        if self.ser.is_open:
            # print("Create opened serial: {}".format(self.ser))
            print('-'*40)
            print(' Create opened serial connection')
            print('   port: {}'.format(self.ser.port))
            print('   datarate: {} bps'.format(self.ser.baudrate))
            print('-'*40)
        else:
            raise Exception('Failed to open {} at {}'.format(port, baud))

    def write(self, opcode, data=None):
        """
        Writes a command to the create. There needs to be an opcode and optionally
        data. Not all commands have data associated with it.

        opcode: see creaet api
        data: a tuple with data associated with a given opcode (see api)
        """
        msg = (opcode,)

        # Sometimes opcodes don't need data. Since we can't add
        # a None type to a tuple, we have to make this check.
        if data:
            msg += data
        msg = OPCODES.START_BYTE + msg + OPCODES.END_BYTE
        print(">> write:", msg)
        self.ser.write(struct.pack('B' * len(msg), *msg))

    def Cal_Checksum(self, data):
        return data ^ OPCODES.XOR_VALUE


    def read(self, num_bytes):
        """
        Read a string of 'num_bytes' bytes from the robot.

        Arguments:
            num_bytes: The number of bytes we expect to read.
        """
        if not self.ser.is_open:
            raise Exception('You must open the serial port first')

        data = self.ser.read(num_bytes)

        return data

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser.is_open:
            print('Closing port {} @ {}'.format(self.ser.port, self.ser.baudrate))
            self.ser.close()

    def Check_TTLUART_module(self, Max_USB_port=10):
        '''return None if no USB TTL UART is plugged, otherwise ID of UART port'''
        self.index = 0
        import subprocess
        while self.index <= Max_USB_port:
            self.port_id = "/dev/ttyUSB"+str(self.index)
            self.port_command = "--name=" + self.port_id
            self.command_find_port = ["udevadm","info",self.port_command,"--attribute-walk"]
            try:
                self.raw_string_devices = subprocess.check_output(self.command_find_port,universal_newlines=True)
                self.result_check_port = self.raw_string_devices.find("CP2102 USB to UART Bridge Controller")
                break
            except:
                self.index = self.index + 1
                self.port_id = None
        return self.port_id
