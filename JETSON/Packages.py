##  OI from Data-package wroten by Nam-san ##
##  ASTI 06102020
##  Ver. 0.0.1
##  Special thanks to pycreate2 in pipy
from struct import Struct
from collections import namedtuple


# build some packet decoders:
#   use: unpack_bool_byte(data)[0] -> returns tuple, but grab 0 entry
unpack_bool_byte = Struct('?').unpack         # 1 byte bool
unpack_byte = Struct('b').unpack              # 1 signed byte
unpack_unsigned_byte = Struct('B').unpack     # 1 unsigned byte
unpack_short = Struct('>h').unpack            # 2 signed bytes (short)
unpack_unsigned_short = Struct('>H').unpack   # 2 unsigned bytes (ushort)


#   Data name
Sensors = namedtuple('Sensors', [
    'Total_votage',
    'Current',
    'Remaining_capacity',
    'Normal_capacity',
    'Cycles',
    'Software_version',
    'RSOC',
    'FET_control_status',
    'Number_of_battery_string',
    'Number_temp',
    'The_first_temp',
    'The_second_temp',
    'The_third_temp',
    'The_fourth_temp'
])

def Data_packs_decoder(Data_packs):
    """
    This function decodes a AGV packet 26 and returns a data package object,
    which is really a namedtuple. The data class holds all sensor values for
    the AGV. It is basically like a C struct.
    """

    if len(Data_packs) != 26:
        return None

    sensors = Sensors(
        unpack_unsigned_short(Data_packs[4:6])[0],      # Total voltage
        unpack_unsigned_short(Data_packs[6:8])[0],      # Current
        unpack_unsigned_short(Data_packs[8:10])[0],     # Remaining capacity
        unpack_unsigned_short(Data_packs[10:12])[0],    # Normal capacity
        unpack_unsigned_short(Data_packs[12:14])[0],    # Cycles
        unpack_unsigned_byte(Data_packs[14:15])[0],     # Software Version
        unpack_unsigned_byte(Data_packs[15:16])[0],     # RSOC
        unpack_unsigned_byte(Data_packs[16:17])[0],     # FET control status
        unpack_unsigned_byte(Data_packs[17:18])[0],     # Number of battery string
        unpack_unsigned_byte(Data_packs[18:19])[0],     # Num of tem
        unpack_unsigned_byte(Data_packs[19:20])[0],     # 1st temp
        unpack_unsigned_byte(Data_packs[20:21])[0],     # 2nd temp
        unpack_unsigned_byte(Data_packs[21:22])[0],     # 3nd temp
        unpack_unsigned_byte(Data_packs[22:23])[0]      # 4nd temp
    )

    return sensors
