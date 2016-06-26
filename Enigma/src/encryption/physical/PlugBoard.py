'''
Created on 26 Jun 2016

@author: Janion
'''

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