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
from struct import Struct



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

#######################Helpful Cunctions For Control Area########################

    def Convert_speed(self,input_speed):
        '''
        Get m/s speed and return Hex in mm/s
        '''
        input_speedN = input_speed[0] * 1000
        input_speedSL = input_speed[1] * 1000

        return int(input_speedN), int(input_speedSL)

    def Read_respon_status(self):
        '''
        Read status from package after send control speed or reset to MCU
        '''
        sensor_pkt_len = 8

        time.sleep(0.015)  # wait 15 msec
        packet_byte_data = self.SCI.read(sensor_pkt_len)
        print(packet_byte_data)

        if len(packet_byte_data) != sensor_pkt_len:
            print('[WARN] Package data not 8 bytes long, it is: {}'.format(len(packet_byte_data)))
        elif self.Check_STARTnEND_BYTE(packet_byte_data) and self.Checksum_checker_ERR(packet_byte_data):
            Control_name = self.Find_control_name(packet_byte_data)
            Checker = Struct('B').unpack(packet_byte_data[2:3])[0]
            if Checker == 0x00:
                print('[INFO] {} control has been completed'.format(Control_name))
            elif Checker == 0x08:
                print('[WARN] {} respond pakage has problem'.format(Control_name))
            else:
                print('[ERR] {} pakage is wrong format'.format(Control_name))
        else:
            print('[ERR] Pakage is wrong lenght and format')

    def Find_control_name(self, packet_byte_data):
        '''
        Check the package position from 1-2 to know if the control is reset or change speed
        '''
        if Struct('B').unpack(packet_byte_data[1:2])[0] == 0xA3:
            return 'SPEED'
        elif Struct('B').unpack(packet_byte_data[1:2])[0] == 0xA4:
            return 'RESET'

    def Check_STARTnEND_BYTE(self, packet_byte_data):
        '''
        Check the start and end byte
        If true return true, otherwise flase
        '''
        len_pac = len(packet_byte_data)
        if Struct('B').unpack(packet_byte_data[0:1])[0] == OPCODES.START_BYTE:
            if Struct('B').unpack(packet_byte_data[len_pac-1:len_pac])[0] == OPCODES.END_BYTE:
                return True
            else:
                return False
        else:
            return False


    def Checksum_checker(self, packet_byte_data):
        '''
        Calcualtor the check sum from byte 0-4 and compare with checksum
        in position 5-7. If true return true, otherwise false
        '''
        len_pac = len(packet_byte_data)
        index = 0
        SUM = 0
        while index < len_pac - 3:
            SUM += Struct('B').unpack(packet_byte_data[index:index+1])[0]
            index += 1
        Checker = SUM ^ OPCODES.XOR_VALUE
        print(Checker)
        print(Struct('>H').unpack(packet_byte_data[len_pac-3:len_pac-1])[0])
        if Checker == Struct('>H').unpack(packet_byte_data[len_pac-3:len_pac-1])[0]:
            return True
        else:
            return False
            
###########################Control Area###########################

    def reset_RunData(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) RUN DATA
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x01,0x00))
        self.Read_respon_status()

    def reset_BySoftware(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) BySoftware
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x00,0x01))
        self.Read_respon_status()

    def reset_All(self):
        '''
        This command reset MCU (ARDUINO MEGA 2560) BySoftware and RUN DATA
        '''
        self.SCI.write(CONTROL_OP.RESET_MCU, data = (0x01,0x01))
        self.Read_respon_status()

    def Change_Speed(self, speedNormal, speedSlow):
        '''
        This command control speed of the AGV by sending tit normal speed and slow speed.
        4 bytes: 2 high bytes are normal speed, 2 low bytes are low speed
        Note: 
        - Big-endian
        - Input speed  m/s
        - mm/s = m/s*1000
        '''
        Hex_SpeedN, Hex_SpeedSL = self.Convert_speed((speedNormal, speedSlow))

        data_speed = struct.unpack('4B', struct.pack('>2h', Hex_SpeedN, Hex_SpeedSL))
        self.SCI.write(CONTROL_OP.CONTROL_SPEED, data = data_speed)
        self.Read_respon_status()

###########################Request Area###########################

    def Read_ERR_status(self):
        '''
        Process data to get the status of errors.
        Read OI to know the OPCODES
        Note: Frame format inside Data-package from Nam-san.
        '''
        self.SCI.write(REQUEST.ERR_STATUS)
        sensor_pkt_len = 11
        time.sleep(0.015)  # wait 15 msec
        packet_byte_data = self.SCI.read(sensor_pkt_len)
        print(packet_byte_data)

        if len(packet_byte_data) != sensor_pkt_len:
            print('[WARN] Package data not 11 bytes long, it is: {}'.format(len(packet_byte_data)))
        elif self.Check_STARTnEND_BYTE(packet_byte_data) and self.Checksum_checker(packet_byte_data):
            print('PUT ERR PROCESS INSIDE THIS FUNCTION')
    def Read_basic_information_batterry(self):
        '''
        #########
        '''
        self.SCI.write(REQUEST.INFORMATION_BATTERY)
        sensor_pkl_len=26
        time.sleep(0.05)
        packet_byte_data=self.SCI.read(sensor_pkl_len)
        print(packet_byte_data)
        if len(packet_byte_data) !=sensor_pkl_len:
            print("")
        elif self.Check_STARTnEND_BYTE(packet_byte_data) and self.Checksum_checker(packet_byte_data)
            print("")
            Total_voltage             = hex(int(str(packet_byte_data[4])+str(packet_byte_data[5])))
            Current                   = hex(int(str(packet_byte_data[6])+str(packet_byte_data[7])))
            The_remaining_capacity    = hex(int(str(packet_byte_data[8])+str(packet_byte_data[9])))
            Nominal_capacity          = hex(int(str(packet_byte_data[10])+str(packet_byte_data[11])))
            Cycles                    = hex(int(str(packet_byte_data[12])+str(packet_byte_data[13])))
            Software_version          = hex(packet_byte_data[14])
            Rsoc                      = hex(packet_byte_data[15])
            Fet_control_status        = hex(packet_byte_data[16])
            Number_of_battery_stirngs = hex(packet_byte_data[17])
            Number_of_temperature     = hex(packet_byte_data[18])
            The_first_temperature     = hex(packet_byte_data[19])
            Second_temperature        = hex(packet_byte_data[20])
            Third_temperature         = hex(packet_byte_data[21])
            Fourth_temperature        = hex(packet_byte_data[22])
            
        return Total_voltage,Current,The_remaining_capacity,Nominal_capacity,Cycles,Software_version,Rsoc,Fet_control_status,Number_of_battery_stirngs,Number_of_temperature,The_first_temperature,Second_temperature,Third_temperature,Fourth_temperature    

        
