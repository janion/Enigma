'''
Created on 26 Jun 2016

@author: Janion
'''

import Constants

################################################################################
################################################################################

# A single rotor which turns in the machine
class Rotor():
    
    # Constants and global variables
    __offset = 0
               
################################################################################
    
    # Setup the encryption mapping and the knock on character
    def __init__(self, mapping, knockOn):
        self.__knockOn = knockOn
        self.setMapping(mapping)
        
################################################################################
    
    # Return encrypted character with signal coming from the plugboard side
    def reset(self):
        self.__offset = 0
        
################################################################################
    
    # Return encrypted character with signal coming from the plugboard side
    def mapCharForward(self, charIn):
        # Maps char using the positioning relative to the machine inputs
        charOut = self.mapping[(Constants.alpha.index(charIn) + self.__offset) % 26]
        absPos = Constants.alpha[(Constants.alpha.index(charOut) - self.__offset) % 26]
        return absPos
        
################################################################################
    
    # Return encrypted character with signal coming from the reflector side
    def mapCharBackward(self, charIn):
        # Maps char using the positioning relative to the machine inputs
        # Get the absolute character incoming
        charIn = Constants.alpha[(Constants.alpha.index(charIn) + self.__offset) % 26]
        
        charOut = Constants.alpha[self.mapping.index(charIn)]
        absPos = Constants.alpha[(Constants.alpha.index(charOut) - self.__offset) % 26]
        return absPos
        
################################################################################
    
    # Set the mapping of the rotor
    def setMapping(self, mapping):
        self.mapping = mapping
        
################################################################################
    
    # Set the mapping of the rotor
    def getKnockOverChar(self):
        return self.__knockOn
        
################################################################################
    
    # Set the mapping of the rotor
    def getCurrentChar(self):
        return Constants.alpha[self.__offset]
        
################################################################################
    
    # Turn the rotor
    def turn(self, isOnward):
        # The return is only inspected for turns initiated by a key press
        # The return is the knock on state of the turn
        if isOnward:
            self.__offset = (self.__offset + 1) % 26
            if Constants.alpha[self.__offset] == self.__knockOn:
                return True
            else:
                return False
        else:
            self.__offset = (self.__offset - 1) % 26
            return False