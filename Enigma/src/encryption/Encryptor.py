# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 10:25:12 2015

@author: erik_
"""

# from Connections import Rotor, PlugBoard, Reflector
from physical.Rotor import Rotor
from physical.Reflector import Reflector
from physical.PlugBoard import PlugBoard
import Constants

################################################################################
################################################################################

# Contains the rotors, reflectors and plugboard
class Mechanics():
    
    # Constants and global variables
    __plugBoard = PlugBoard()
    __reflector = None
    
    # rotor 1, 2, 3
    __r1 = None
    __r2 = None
    __r3 = None
    rotorSet = [__r1, __r2, __r3]
                
################################################################################
    
    # Create the rotors and the reflector
    def __init__(self, r1, r2, r3, reflector):
        self.setRotors(r1, r2, r3)
        self.setReflector(reflector)
        
################################################################################
        
    # Create the selected reflector
    def setReflector(self, a):
        self.__reflector = Reflector(Constants.Connections.reflectors[a])
        
################################################################################
        
    # Create the rotors in place
    def setRotor(self, pos, rotorNum):
        self.rotorSet[pos] = Rotor(Constants.Connections.rotors[rotorNum], Constants.Connections.knockOn[rotorNum])
        
################################################################################
        
    # Create the rotors in place
    def setRotors(self, a, b, c):
        self.__r1 = Rotor(Constants.Connections.rotors[a], Constants.Connections.knockOn[a])
        self.__r2 = Rotor(Constants.Connections.rotors[b], Constants.Connections.knockOn[b])
        self.__r3 = Rotor(Constants.Connections.rotors[c], Constants.Connections.knockOn[c])
        
################################################################################
    
    # Encrypt the incoming character
    def encrypt(self, charIn):
        # Turn over the right rotor and check if any others are knocked over
        turnOvers = self.keyPressed()
        
        # Perform the transformations
        charOut = self.__plugBoard.mapChar(
                    self.__r1.mapCharBackward(
                        self.__r2.mapCharBackward(
                            self.__r3.mapCharBackward(
                                self.__reflector.mapChar(
                                    self.__r3.mapCharForward(
                                        self.__r2.mapCharForward(
                                            self.__r1.mapCharForward(
                                                self.__plugBoard.mapChar(charIn)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
        # Return the encrypted character and the knock over states
        return (charOut, turnOvers)
        
################################################################################
    
    # Manually turn over a single rotor
    def manualTurn(self, rotorNum, isOnward):
        if rotorNum == 0:
            self.__r1.turn(isOnward)
        elif rotorNum == 1:
            self.__r2.turn(isOnward)
        elif rotorNum == 2:
            self.__r3.turn(isOnward)
            
################################################################################
    
    # Reset rotors to start position
    def resetRotors(self):
        self.__r1.reset()
        self.__r2.reset()
        self.__r3.reset()
            
################################################################################
    
    # Turn over the rotors by the pressing of a key
    def keyPressed(self):
        over = [False, False]
        knockOver = self.__r1.turn(True)
        
        # If a rotor kicks over a slower rotor, record it and return it
        if knockOver:
            knockOver = self.__r2.turn(True)
            over[0] = True
            
            if knockOver:
                self.__r3.turn(True)
                over[1] = True
        
        return over
            
################################################################################
    
    # Turn over the rotors by the pressing of a key
    def backSpaceRotors(self):
        over = [False, False]
        
        if self.__r1.getCurrentChar() == self.__r1.getKnockOverChar():
            over[0] = True
        
        self.__r1.turn(False)
        
        if over[0] == True:
            if self.__r2.getCurrentChar() == self.__r2.getKnockOverChar():
                over[1] = True
                self.__r3.turn(False)
            self.__r2.turn(False)
        
        return over
        
################################################################################
################################################################################