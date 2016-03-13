# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 23:29 2015

@author: Janion
"""

import wx
from Encryption.Encryptor import Mechanics
from dlgs.RotorSelection import RotorDlg
from dlgs.ReflectorSelection import ReflectorDlg
from time import sleep

# plugboard selection
# multiple deletion???
#   Get selection and position then remove and redo
# change my phasse

################################################################################
################################################################################

# Simulates an enigma machine with 3 rotors and a plugboard
class Window(wx.Frame):
    
    specialChars = ["-", "_", "=", "+", "(", ")", ";", ":", "@", "'", "#", ",", ".", "/", "?", "\\", "!", "\"", "&", "*", " ", "\n"]
    specialCodes = [45, 95, 61, 43, 40, 41, 59, 58, 64, 39, 35, 44, 46, 47, 63, 92, 33, 34, 38, 42, 32, 13]
    
    specialMap = {}
    
    for x in xrange(len(specialChars)):
        specialMap[specialCodes[x]] = specialChars[x]
    
    # Constants and global variables
    __alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
               "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
               "Y", "Z"
               ]
               
    choiceList = ["I", "II", "III", "IV", "V"]
        
    letters = [["Q", "W", "E", "R", "T", "Z", "U", "I", "O"],
               ["A", "S", "D", "F", "G", "H", "J", "K"],
               ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]
               ]
    lights = [ [], [], [] ]
    keys = [ [], [], [] ]
    rotorWindows = [None, None, None]
    arrows = [ [], [] ]
    r1 = 0
    r2 = 1
    r3 = 2
    reflector = 0
    rotors = Mechanics(r1, r2, r3, reflector)
    
################################################################################
    
    # Build window and initialise objects
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(610, 685))
        self.panel = wx.Panel(self, -1)
        
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetMinSize())
        
        self.createRotorWindows()
        self.createKeysAndLights()
        self.setupMenu()
        
        self.resetBtn = wx.Button(self.panel, -1, "Reset", pos=(470, 55))
        
        # Place the text boxes at the bottom
        wx.StaticText(self.panel, -1, "Message in", pos=(20, 515))
        wx.StaticText(self.panel, -1, "Message out", pos=(305, 515))
        
        self.textIn = wx.TextCtrl(self.panel, -1, "", pos=(20, 535), size=(270,80),
                                  style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER
                                  )
        self.textOut = wx.TextCtrl(self.panel, -1, "", pos=(305, 535), size=(270,80),
                                   style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER
                                   )
        self.textOut.SetEditable(False)
        
        self.textIn.Bind(wx.EVT_CHAR, self.keyTyped)
        self.textIn.Bind(wx.EVT_LEFT_DOWN, self.resetCursor)
        self.textIn.Bind(wx.EVT_LEFT_DCLICK, self.resetCursor)
        self.textIn.SetFocus()
        
        # Initialised to ensure
        self._index = [0, 0]
        self.panel.Bind(wx.EVT_LEFT_UP, self.lightOff)
        self.resetBtn.Bind(wx.EVT_BUTTON, self.resetRotors)
            
################################################################################
            
    def setupMenu(self):
        menuBar = wx.MenuBar()
        
        # Shortcuts
        menu1 = wx.Menu()
        menu1.Append(101, "Select rotors")
        menu1.Append(102, "Select reflector")
        menuBar.Append(menu1, "Configurations")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.ChangeRotorDlg, id=101)
        self.Bind(wx.EVT_MENU, self.ChangeReflectorDlg, id=102)
            
################################################################################
            
    def resetRotors(self, event):
        self.rotors.resetRotors()
        self.textIn.SetValue("")
        self.textOut.SetValue("")
        for x in xrange(3):
            self.rotorWindows[x].SetValue("A")
        self.textIn.SetFocus()
            
################################################################################
            
    def ChangeReflectorDlg(self, event):
        dlg = ReflectorDlg(self, -1, self.reflector)
        dlg.ShowModal()
        
        if dlg.result != None:
            self.reflector = dlg.result
            self.rotors.setReflector(self.reflector)
            self.resetRotors(None)
            
################################################################################
            
    def ChangeRotorDlg(self, event):
        choice1 = self.choiceList[self.r1]
        choice2 = self.choiceList[self.r2]
        choice3 = self.choiceList[self.r3]
        
        dlg = RotorDlg(self, -1, choice1, choice2, choice3, self.choiceList)
        dlg.ShowModal()
        
        if dlg.result != [] and dlg.result != None:
            self.resetRotors(None)
            
            self.r1 = self.choiceList.index(dlg.result[0])
            self.r2 = self.choiceList.index(dlg.result[1])
            self.r3 = self.choiceList.index(dlg.result[2])
            
            self.rotors = Mechanics(self.r1, self.r2, self.r3, 0)
            
            for rotorNum in xrange(3):
                self.rotorWindows[rotorNum].SetValue("A")
            
            self.resetRotors(None)
            
################################################################################
            
    def createKeysAndLights(self):
        # Keys and lights
        xPos = [40, 65, 30]
        yPos = [130, 180, 230]
        for y in xrange(3):
            for x in xrange(len(self.letters[y])):
                # Add lit image
                img = wx.Image(('keys\\Lit\\%s.png' %self.letters[y][x]),
                               wx.BITMAP_TYPE_PNG
                               ).ConvertToBitmap()
                bmp = wx.StaticBitmap(self.panel, -1, img, pos=(xPos[y]+(x*60),
                                                                yPos[y])
                                      )
                
                # Hide lit image behind the dim image
                img = wx.Image(('keys\\Dim\\%s.png' %self.letters[y][x]),
                               wx.BITMAP_TYPE_PNG
                               ).ConvertToBitmap()
                bmp = wx.StaticBitmap(self.panel, -1, img, pos=(xPos[y]+(x*60),
                                                                yPos[y])
                                      )
                # Store dim image for later use
                self.lights[y].append(bmp)
                
                # Place the key image below the lights
                img = wx.Image(('keys\\Key\\%s.png' %self.letters[y][x]),
                               wx.BITMAP_TYPE_PNG
                               ).ConvertToBitmap()
                bmp = wx.BitmapButton(self.panel, -1, img, pos=(xPos[y]+(x*60),
                                                                yPos[y] + 220),
                                      style=wx.NO_BORDER
                                      )
                # Bind events
                bmp.Bind(wx.EVT_LEFT_DOWN, self.lightOn)
                bmp.Bind(wx.EVT_LEFT_UP, self.lightOff)
                # Store key button
                self.keys[y].append(bmp)
                
        # Place the Space bar
        img = wx.Image(('keys\\Key\\SPACE.png'), wx.BITMAP_TYPE_PNG
                       ).ConvertToBitmap()

        xPos = (self.GetSize()[0] / 2) - img.GetSize()[0] - 10
        yPos = 290
        
        self.space = wx.BitmapButton(self.panel, -1, img, pos=(xPos, yPos),
                                     style=wx.NO_BORDER
                                     )
        self.space.Bind(wx.EVT_BUTTON, self.spaceBar)
        
        # Place the return key
        img = wx.Image(('keys\\Key\\RETURN.png'), wx.BITMAP_TYPE_PNG
                       ).ConvertToBitmap()
        
        xPos = (self.GetSize()[0] / 2) + 10
        enter = wx.BitmapButton(self.panel, -1, img, pos=(xPos,290),
                                style=wx.NO_BORDER
                                )
        enter.Bind(wx.EVT_BUTTON, self.enter)
            
################################################################################
    
    # Key typed
    def createRotorWindows(self):
        # Rotor windows
        for x in xrange(2, -1, -1):
            self.rotorWindows[x] = (wx.TextCtrl(self.panel, -1, "A",
                                                pos=(380 - (100 * x), 60),
                                                size=(20,20))
                                    )
            self.rotorWindows[x].SetEditable(False)
            self.rotorWindows[x].SetBackgroundColour("WHITE")
        
        # Buttons for changing the rotors
        symbols = [u'\u25b2', u'\u25bc']
        for x in xrange(2):
            for y in xrange(3):
                    self.arrows[x].append(wx.Button(self.panel, -1, symbols[x],
                                          pos=(210 + (y*100), 50 + (x*20)),
                                          size=(20,20))
                                          )
                    self.arrows[x][y].Bind(wx.EVT_BUTTON, self.rotorButton)
            
################################################################################
    
    # Key typed
    def keyTyped(self, event):
        code = event.GetKeyCode()
        self.typeKey(code, event)
#         if code in [314, 315, 316, 317, 8]:
#             self.typeKey(code, event)
#         else:
#             pos = self.textIn.GetInsertionPoint()
#             
#             raw = self.textIn.GetValue()
#             rawBefore = raw[0: pos]
#             rawAfter = raw[pos:]
#             
#             #print "before ", rawBefore
#             #print "after ", rawAfter
#             
#             cryptBefore = self.textOut.GetValue()[0: pos]
#             
#             self.textIn.SetValue(rawBefore)
#             self.textOut.SetValue(cryptBefore)
#             
#             for char in rawAfter:
#                 if char in self.__alpha:
#                     self.rotorBackSpace()
#             
#             self.typeKey(event.GetKeyCode())
#                     
#             for char in rawAfter:
#                 if char in self.__alpha:
#                     self.typeKey(self.__alpha.index(char.upper()) + 65)
#                 else:
#                     for code, letter in self.specialMap.iteritems():
#                         if letter == char:
#                             self.typeKey(code)
#             
#             self.textIn.SetInsertionPoint(pos + 1)
            
################################################################################
    
    # Rotor manually changed
    def spaceBar(self, event):
        self.typeKey(32)
        self.space.Hide()
        sleep(0.01)
        self.space.Show()
            
################################################################################
    
    # Rotor manually changed
    def enter(self, event):
        self.typeKey(13)
            
################################################################################
    
    # Rotor manually changed
    def typeKey(self, key, event = None):
        
        if 97 <= key <= 122: # Lower case
            self.textIn.AppendText(self.__alpha[key - 97])
            self.getEncryptedChar(self.__alpha[key - 97])
            self.textOut.AppendText(self._charOut)
        elif 65 <= key <= 90: # Upper case
            self.textIn.AppendText(self.__alpha[key - 65])
            self.getEncryptedChar(self.__alpha[key - 65])
            self.textOut.AppendText(self._charOut)
#         elif key == 314 or key == 315 or key == 316 or key == 317: # Left, up, right or down keys
#             event.Skip()
        elif key == 22: # Paste
            self.paste()
        elif self.specialMap.has_key(key):
            self.textIn.AppendText(self.specialMap[key])
            self.textOut.AppendText(self.specialMap[key])
        elif key == 8: # BackSpace
            self.backSpace(event)
                          
################################################################################
                            
    def backSpace(self, event):
        textLen = len(self.textIn.GetValue())
        event.Skip()
        if textLen > 0:
            lastChar = self.textIn.GetValue()[-1]
            # Remve last character
            self.textOut.SetValue(self.textOut.GetValue()[0 : len(self.textIn.GetValue()) - 1])
            
            if lastChar not in ["\n", " "] and lastChar not in self.specialChars:
                knockOver = self.rotors.backSpaceRotors()
                
                currentCharIndex = self.__alpha.index(self.rotorWindows[0].GetValue())
                self.rotorWindows[0].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
                
                if knockOver[0] == True:
                    currentCharIndex = self.__alpha.index(self.rotorWindows[1].GetValue())
                    self.rotorWindows[1].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
                    
                    if knockOver[1] == True:
                        currentCharIndex = self.__alpha.index(self.rotorWindows[2].GetValue())
                        self.rotorWindows[2].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
#         selection = self.textIn.GetSelection()
#         
#         if selection[0] == selection[1]:
#             pos1 = selection[0] - 1
#             pos2 = selection[0]
#             pos2 = 0
#         else:
#             pos1 = selection[0]
#             pos2 = selection[1]
#         
# #        raw = self.textIn.GetValue()
# #        returnCount = 0
# #        for x in xrange(pos2 - 1):
# #            if raw[x] == "\n":
# #                returnCount += 1
# #            if x == pos1:
# #                pos1 += returnCount
# #        pos2 += returnCount
#             
#         if pos2 > 0:
#             raw = self.textIn.GetValue()
#             rawBefore = raw[0: pos1]
#             rawAfter = raw[pos2:]
#             
#             cryptBefore = self.textOut.GetValue()[0: pos1]
#             
#             self.textIn.SetValue(rawBefore)
#             self.textOut.SetValue(cryptBefore)
#             
#             deleted = raw[pos1: pos2]
#             
#             for char in deleted + rawAfter:
#                 if char in self.__alpha:
#                     self.rotorBackSpace()
#                     
#             for char in rawAfter:
#                 if char in self.__alpha:
#                     self.typeKey(self.__alpha.index(char.upper()) + 65)
#             
#             self.textIn.SetInsertionPoint(pos1)
                          
################################################################################  
                            
    def rotorBackSpace(self):
        knockOver = self.rotors.backSpaceRotors()
        
        currentCharIndex = self.__alpha.index(self.rotorWindows[0].GetValue())
        self.rotorWindows[0].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
        
        if knockOver[0] == True:
            currentCharIndex = self.__alpha.index(self.rotorWindows[1].GetValue())
            self.rotorWindows[1].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
            
            if knockOver[1] == True:
                currentCharIndex = self.__alpha.index(self.rotorWindows[2].GetValue())
                self.rotorWindows[2].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
                          
################################################################################  
                            
    def paste(self):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                for char in do.GetText():
                    if char.upper() in self.__alpha:
                        self.typeKey(self.__alpha.index(char.upper()) + 65)
                    else:
                        for code, letter in self.specialMap.iteritems():
                            if letter == char:
                                self.typeKey(code)
            
################################################################################
    
    # Rotor manually changed
    def rotorButton(self, event):
        # Identify the button pressed
        for x in xrange(len(self.arrows)):
            for y in xrange(len(self.arrows[x])):
                if self.arrows[x][y] == event.GetEventObject():
                    # Update the window and the rotor objects
                    self.turnRotor(2 - y, x, True)
                    return
            
################################################################################
    
    # Update the rotor window and the rotor objects
    def turnRotor(self, rotorNum, direction, isManual):
        # Get index of current rotor position
        currentCharIndex = self.__alpha.index(self.rotorWindows[rotorNum].GetValue())
        
        # Set new value in the rotor window and turn the rotor object
        # if it is a manual turn
        if direction == 0:
            self.rotorWindows[rotorNum].SetValue(self.__alpha[(currentCharIndex + 1) % 26])
            if isManual: self.rotors.manualTurn(rotorNum, True)
        else:
            self.rotorWindows[rotorNum].SetValue(self.__alpha[(currentCharIndex - 1) % 26])
            if isManual: self.rotors.manualTurn(rotorNum, False)
            
################################################################################
    
    # Turn resultant light on
    def lightOn(self, event):
        # Identify the key pressed
        for row in xrange(len(self.keys)):
            if self.keys[row].count(event.GetEventObject()) > 0:
                index = self.keys[row].index(event.GetEventObject())
                charIn = self.letters[row][index]
        
        key = self.__alpha.index(charIn) + 65
        self.typeKey(key)
        
        # Find the encrypted character
        for row in xrange(len(self.keys)):
            if self.letters[row].count(self._charOut) > 0:
                # Store the indices of the encrypted character
                self._index = [row, self.letters[row].index(self._charOut)]
                # Hide the dim image to reveal the lit image
                self.lights[self._index[0]][self._index[1]].Hide()
                
################################################################################
    
    def getEncryptedChar(self, charIn):
        # Encrypt the character
        (self._charOut, turnOvers) = self.rotors.encrypt(charIn)
        
        # Update rotor positions
        self.turnRotor(0, 0, False)
        if turnOvers[0]:
            self.turnRotor(1, 0, False)
        if turnOvers[1]:
            self.turnRotor(2, 0, False)
                
################################################################################
    
    def lightOff(self, event):
        # Show the dim image to hide the lit image
        self.lights[self._index[0]][self._index[1]].Show()
                
################################################################################
    
    def resetCursor(self, event):
        self.textIn.SetFocus()
        self.textIn.SetInsertionPointEnd()
        
################################################################################
################################################################################


if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Enigma Cypher Machine')
    fr.Show()
    app.MainLoop()