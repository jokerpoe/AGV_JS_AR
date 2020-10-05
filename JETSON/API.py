# ASTI License

# This is main api for ASTI AGV

#######ASTI AGV#######
######################
# Author :  Son     ##
# Date:     02102020##
# Version:  0.0.1   ##
######################

import struct                               # to collect opcode into frame or unpack them.
import time                                 # IF need delay
from OI import *                            # OPCODEs to process
import Serial_lib as ser                    # Serial module




class AGV(object):
    """
    The top level class for controlling AGV ASTI.
    All functions to control AGV ASTI should be place inside this file only.
    """
    def __init__(self, port, baudf=OI.BAUD_RATE):
        '''Setup for class
        - check for port
        - creates serial port
        - create decoder
        '''
