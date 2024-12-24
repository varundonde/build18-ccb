"""
Module for dispensing drinks

Contains dispense function, which takes in an array of ratios and
interfaces with Raspberry Pi pins to dispense drink
"""


# TODO: write ratio_to_time once hardware is assembled
# TODO: check if any other functions for dispensing are needed

#--------------------IMPORTS--------------------
from machine import Pin
import time

#--------------------CONSTANTS--------------------
PUMPS = [Pin(i, Pin.OUT) for i in range(6)]

#--------------------HELPERS--------------------
# @brief Converts a given ratio (1-100) to a dispensing time in seconds

def ratio_to_time(ratio): 
    pass

#--------------------FUNCTIONS--------------------
def dispense(ratios):
    for i, pump in enumerate(PUMPS):
        # Get ratio
        ratio = ratios[i]
        # Convert to duration
        duration = ratio_to_time(ratio)
        if duration > 0: 
            pump.on()
            time.sleep(duration)
            pump.off()

    return
