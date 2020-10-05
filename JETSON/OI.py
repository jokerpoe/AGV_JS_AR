##  OI from Data-package wroten by Nam-san ##
##  ASTI 05102020
##  Ver. 0.0.1



class Namespace(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


BAUD_RATE           = 9600 #Base on "Physical interface" in Data-package MCU and MCP from Nam-san

CONTROL_OP          = Namespace(
    RESET_MCU               = 0xA4
    CONTROL_SPEED           = 0X03 # DATA content 4 bytes: 2 high bytes are normal speed, 2 low bytes are slow speed


)

INFO_OP             = Namespace(
    BASIC_BATTERY           = 0X03
    BASIC_SPEED             = 0X04
    ERROR_STATUS            = 0X08

)

OPCODES             = Namespace(
    START_BYTE              = 0XEE
    END_BYTE                = 0XAA

)

CHECKSUM_OP         = Namespace(
    XOR_VALUE               = 0XFFFF
    SUM_VALUE               = 0X0420

)
