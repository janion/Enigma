'''
Created on 26 Jun 2016

@author: Janion
'''
    
__specialChars = ["-", "_", "=", "+", "(", ")", ";", ":", "@", "'", "#", ",", ".", "/", "?", "\\", "!", "\"", "&", "*", " ", "\n"]
__specialCodes = [45, 95, 61, 43, 40, 41, 59, 58, 64, 39, 35, 44, 46, 47, 63, 92, 33, 34, 38, 42, 32, 13]

specialMap = {}

for x in xrange(len(__specialChars)):
    specialMap[__specialCodes[x]] = __specialChars[x]

alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
         "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
         "Y", "Z"
         ]
           
choiceList = ["I", "II", "III", "IV", "V"]
    
layout = [["Q", "W", "E", "R", "T", "Z", "U", "I", "O"],
          ["A", "S", "D", "F", "G", "H", "J", "K"],
          ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]
          ]

# Image file locations
litLocationFormat = 'keys/Lit/%s.png'
dimLocationFormat = 'keys/Dim/%s.png'
keyLocationFormat = 'keys/Key/%s.png'
spaceBarLocation = 'keys/Key/SPACE.png'
returnLocation = 'keys/Key/RETURN.png'


class Defaults():
    reflector = 0
    rotors = [0, 1, 2]
    positions = ["A", "A", "A"]
    
    reflectorChoices = ["A", "B", "C"]

class Connections():
    # A, B & C reflectors
    reflectors = [[["A", "E"], ["B", "J"], ["C", "M"], ["D", "Z"], ["F", "L"],
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
    rotors = [["E", "K", "M", "F", "L", "G", "D", "Q", "V", "Z",
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
    knockOn = ["R", "F", "W", "K", "A"]