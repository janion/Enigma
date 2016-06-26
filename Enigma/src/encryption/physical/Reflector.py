'''
Created on 26 Jun 2016

@author: Janion
'''

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
        