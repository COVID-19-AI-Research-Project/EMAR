############################################################################################
#
# Project:       Peter Moss COVID-19 AI Research Project
# Repository:    COVID-19 Medical Support System Server
# Project:       EMAR, Emergency Assistance Robot
#
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# Contributors:
# Title:         EMAR Emergency Assistance Robot Class
# Description:   The EMAR Emergency Assistance Robot Class is the the core wrapper class 
#                for the EMAR software.
# License:       MIT License
# Last Modified: 2020-04-19
#
############################################################################################

import json, sys

from threading import Thread

from Classes.Helpers import Helpers
from Classes.iotJumpWay import iotJumpWay
from Classes.Wheels import Wheels
from Classes.Arm import Arm
from Classes.CamRead import CamRead
from Classes.CamStream import CamStream

class EMAR():
    """ EMAR Emergency Assistance Robot Class
    
    The EMAR Emergency Assistance Robot Class is the the core wrapper class
    for the EMAR software.
    """
    
    def __init__(self):
        """ Initializes the class. """

        self.Helpers = Helpers("EMAR")
        
        # Starts the iotJumpWay
        self.iotJumpWay = iotJumpWay()
        self.iotJumpWay.startMQTT()
        
        self.iotJumpWay.CLI.dvcTpcSub(self.Helpers.confs["iotJumpWay"]["channels"]["commands"])
        self.iotJumpWay.CLI.dvcCmmdCbck = self.commands

        self.Helpers.logger.info("EMAR awaiting commands.")
        
        # Loads core modules
        self.Wheels = Wheels()
        self.Arm = Arm()

        self.Helpers.logger.info("EMAR Emergency Assistance Robot Class initialization complete.")
        
    def threading(self):
        """ Creates required module threads. """
        
        Thread(target=CamRead.run, args=(self, )).start()
        Thread(target=CamStream.run, args=(self,)).start()
            
    def commands(self, topic, payload):
        """ 
        iotJumpWay Commands Callback
        
        The callback function that is triggerend in the event of a
        command communication from the iotJumpWay.
        """
        
        self.Helpers.logger.info("Recieved iotJumpWay Command Data : " + str(payload))
        command = json.loads(payload.decode("utf-8"))
        
        if command['WarningType'] == "Wheels":
            # If Wheels warning, send command to wheels
            self.Wheels.move(command['WarningValue'])
        
        if command['WarningType'] == "Arm":
            # If Arm warning, send command to arm
            self.Arm.move(command['WarningValue'])
        
EMAR = EMAR()

def main():
    # Starts threading
    EMAR.threading()
    # Kills the iotJumpWay connection if threads stop
    exit()

if __name__ == "__main__":
    main()