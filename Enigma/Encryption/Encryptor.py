# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 10:25:12 2015

@author: erik_
"""

from Connections import Rotor, PlugBoard, Reflector

################################################################################
################################################################################

# Contains the rotors, reflectors and plugboard
class Mechanics():
    
    # Constants and global variables
    __plugBoard = PlugBoard()
    
    # A, B & C reflectors
    __reflectors = [[["A", "E"], ["B", "J"], ["C", "M"], ["D", "Z"], ["F", "L"],
                     ["G", "Y"], ["H", "X"], ["I", "V"], ["K", "W"], ["N", "R"],
                     ["O", "Q"], ["P", "U"], ["S", "T"]
                     ],
                    [["A", "Y"], ["B", "R"], ["C", "U"], ["D", "H"], ["E", "Q"],
                     ["F", "S"], ["G", "L"], ["I", "P"], ["J", "X"], ["K", "N"],
                     ["M", "O"], ["T", "Z"], ["V", "W"]
                     ],
                    [["A", "F"], ["B", "V"], ["C", "P"], ["D", "J"], ["E", "I"],
                     ["G", "O"], ["H", "Y"], ["K", "R"], ["L", "Z"], ["M", "X"],
                     ["N", "W"], ["T", "Q"], ["S", "U"]
                     ]
                    ]
    
    # I, II, III, IV & V rotors
    # Map alphabet to:
    __rotors = [["E", "K", "M", "F", "L", "G", "D", "Q", "V", "Z",
                 "N", "T", "O", "W", "Y", "H", "X", "U", "S", "P",
                 "A", "I", "B", "R", "C", "J"
                 ],
                ["A", "J", "D", "K", "S", "I", "R", "U", "X", "B",
                 "L", "H", "W", "T", "M", "C", "Q", "G", "Z", "N",
                 "P", "Y", "F", "V", "O", "E"
                 ],
                ["B", "D", "F", "H", "J", "L", "C", "P", "R", "T",
                 "X", "V", "Z", "N", "Y", "E", "I", "W", "G", "A",
                 "K", "M", "U", "S", "Q", "O"
                 ],
                ["E", "S", "O", "V", "P", "Z", "J", "A", "Y", "Q",
                 "U", "I", "R", "H", "X", "L", "N", "F", "T", "G",
                 "K", "D", "C", "M", "W", "B"
                 ],
                ["V", "Z", "B", "R", "G", "I", "T", "Y", "U", "P",
                 "S", "D", "N", "H", "L", "X", "A", "W", "M", "J",
                 "Q", "O", "F", "E", "C", "K"
                 ]
                ]
                
    # Knock on positions for the five rotors
    __knockOn = ["R", "F", "W", "K", "A"]
    
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
        self.__reflector = Reflector(self.__reflectors[a])
        
################################################################################
        
    # Create the rotors in place
    def setRotor(self, pos, rotorNum):
        self.rotorSet[pos] = Rotor(self.__rotors[rotorNum], self.__knockOn[rotorNum])
        
################################################################################
        
    # Create the rotors in place
    def setRotors(self, a, b, c):
        self.__r1 = Rotor(self.__rotors[a], self.__knockOn[a])
        self.__r2 = Rotor(self.__rotors[b], self.__knockOn[b])
        self.__r3 = Rotor(self.__rotors[c], self.__knockOn[c])
        
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