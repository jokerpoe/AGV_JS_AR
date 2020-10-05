#######ASTI AGV#######
######################
# Author :  Son     ##
# Date:     02102020##
# Version:  0.0.1   ##
######################

from Serial_lib import SerialCommandInterface
import time
from OI import *
import API




AGV = API.AGV()
while True:
    AGV.reset_RunData()
    time.sleep(2)