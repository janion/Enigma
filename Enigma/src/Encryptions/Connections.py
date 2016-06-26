# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 11:02:50 2015

@author: erik_
"""

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
        
################################################################################
################################################################################

# Plug board which lies before (and after) the rotors
class PlugBoard():
    
    # Dictionary of character pairs
    mapping = {}
               
################################################################################
    
    # Set the mapping pairs to the dictionary: default to no pairs
    def __init__(self, pairs = []):
        for pair in pairs:
            self.setPair(pair)
        
################################################################################
    
    # Return mapped characeter or the character itself if it has no pair
    def mapChar(self, charIn):
        if charIn not in self.mapping.keys():
            return charIn
        else:
            return self.mapping[charIn]
        
################################################################################
    
    # Set a pair in the plugboard
    def setPair(self, pair):
        # If a character in the pair is already in a pair, remove that
        # previous pair from the mapping
        for item in pair:
            if item in self.mapping.keys():
                self.mapping.pop(self.mapping[item])
                self.mapping.pop(item)
        
        # Add the new pair to the mapping
        self.mapping[pair[0]] = pair[1]
        self.mapping[pair[1]] = pair[0]
        
################################################################################
################################################################################

# Reflector after the rotors
class Reflector():
    
    # Dictionary of the mapping pairs
    mapping = {}
               
################################################################################
    
    # Setup the mapping pairs
    def __init__(self, pairs):
        for pair in pairs:
            self.setPair(pair)
        
################################################################################
    
    # Return the result of the mapping
    def mapChar(self, charIn):
        return self.mapping[charIn]
        
################################################################################
    
    # Set a pair within the reflector
    def setPair(self, pair):
        self.mapping[pair[0]] = pair[1]
        self.mapping[pair[1]] = pair[0]
        
################################################################################
################################################################################