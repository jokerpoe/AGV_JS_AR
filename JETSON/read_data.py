import serial 
import struct

unpack_bool_byte = struct('?').unpack         # 1 byte bool
unpack_byte = struct('b').unpack              # 1 signed byte
unpack_unsigned_byte = struct('B').unpack     # 1 unsigned byte
unpack_short = struct('>h').unpack            # 2 signed bytes (short)
unpack_unsigned_short = struct('>H').unpack   # 2 unsigned bytes (ushort)

def read(num_bytes):
    ser=serial.Serial()
    """
    Read a string of 'num_bytes' bytes from the robot.

    Arguments:
        num_bytes: The number of bytes we expect to read.
    """
    if not ser.is_open:
        raise Exception('You must open the serial port first')

    data = ser.read(num_bytes)

    return data

data_unpack=[]
def unpack_data(data):
 
    data=read(data)
    if data==oxEE:
        data_unpack[0]=oxEE
    data_unpack.append(data)
    if data==oxAA:
        data_unpack[-1]=oxAA
        return data_unpack