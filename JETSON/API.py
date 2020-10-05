# ASTI License

# This is main api for ASTI AGV

#######ASTI AGV#######
######################
# Author :  Son     ##
# Date:     02102020##
# Version:  0.0.1   ##
######################

import struct                                   # to collect opcode into frame or unpack them.
import time                                     # IF need delay
from OI import *                                # OPCODEs to process
from Serial_lib import SerialCommandInterface   # Serial module





class AGV(object):
    """
    The top level class for controlling AGV ASTI.
    All functions to control AGV ASTI should be place inside this file only.
    """
    def __init__(self, baud=BAUD_RATE):
        '''Setup for class
        - check for port
        - creates serial port
        - create decoder
        '''
        self.SCI     = SerialCommandInterface()
        self.port    = self.SCI.Check_TTLUART_module()
        self.SCI.open(self.port, baud)
        self.decoder = None

    def __del__(self):
        '''Clean everything before leaving'''
        pass

###########################Helpful Area###########################

def Speed2Hex(self,input_speed):
    '''
    Get m/s speed and return Hex in mm/s
    '''
    input_speed = input_speed * 1000
    return hex(input_speed)

###########################Control Area###########################
    def reset_RunData(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) RUN DATA
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x01,0x00))

    def reset_BySoftware(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) BySoftware
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x00,0x01))

    def reset_All(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) BySoftware and RUN DATA
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x01,0x01))

    def Change_Normal_Speed(self, speedNormal):
        '''
        This command control speed of the AGV by sending tit normal speed and slow speed.
        4 bytes: 2 high bytes are normal speed, 2 low bytes are low speed
        Note: 
        - Big-endian
        - Input speed  m/s
        - mm/s = m/s*1000
        '''
        Hex_SpeedN = self.Speed2Hex(speedNormal)
        struct.unpack('2B',(struct.pack('>1h',data_out)))
        self.SCI.write(CONTROL_OP.CONTROL_SPEED, data = ())
    
