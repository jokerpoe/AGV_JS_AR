##  OI from Data-package wroten by Nam-san ##
##  ASTI 05102020
##  Ver. 0.0.1



class Namespace(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


BAUD_RATE           = 9600          #Base on "Physical interface" in Data-package MCU and MCP from Nam-san

CONTROL_OP          = Namespace(
    RESET_MCU               = 164, #0xA4,
    CONTROL_SPEED           = (0X5B,0XA3) ,  #DATA content 4 bytes: 2 high bytes are normal speed, 2 low bytes are slow speed

)

INFO_OP             = Namespace(
    BASIC_BATTERY           = 3, #0x03
    BASIC_SPEED             = 4,#0x04
    ERROR_STATUS            = 8 #0x08

)

OPCODES             = Namespace(
    START_BYTE              = 238,#0xEE
    END_BYTE                = 170,#0xAA
    XOR_VALUE               = 65535 #0XFFFF

)

REQUEST             = Namespace(
    SPEED_INFO              = 0xA3,
    BATTERY_INFO            = 0XB5,
    ERR_STATUS              = (0xB5, 0x08)
)
