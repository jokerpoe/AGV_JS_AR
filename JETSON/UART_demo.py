#######ASTI AGV#######
######################
# Author :  Son     ##
# Date:     02102020##
# Version:  0.0.1   ##
######################

from Serial_lib import SerialCommandInterface
import time

AGV = SerialCommandInterface()


a= AGV.Check_TTLUART_module()
print(a)
'''
AGV.open(port='/dev/ttyUSB0', baud=9600)
time.sleep(2)
AGV.write(0xEE)
print('Writed 0xEE')

time.sleep(2)
AGV.close()
'''

'''
class AGV_robot():

    def __init__(self):
        print(self.Check_TTLUART_module(self.Max_USB_port = 10))
    
    def Check_TTLUART_module(self, Max_USB_port):
        '''return None if no USB TTL UART is plugged, otherwise ID of UART port'''
        self.index = 1
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
'''
AGV= AGV_robot()