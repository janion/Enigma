# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 20:40:51 2016

@author: Janion
"""


import wx

class RotorDlg(wx.Dialog):
    
    result = []
    
    def __init__(self, parent, idd, rOne, rTwo, rThree, choiceList):
        wx.Dialog.__init__(self, parent, idd, "Rotor selection", size=(180, 125))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        self.rOne = rOne
        self.rTwo = rTwo
        self.rThree = rThree
        
        #Create instructional text and a text box to enter the project name
        wx.StaticText(self.panel, -1, "Please select the three rotors:",
                      (10, 10)
                      )
                      
        self.choiceList = choiceList
        
        #Create text and hour entry box
        self.r1 = wx.Choice(self.panel, -1, choices = [rOne], pos=(10, 30),
                                 size=(40, -1)
                                 )
        self.r1.SetSelection(0)
        self.r2 = wx.Choice(self.panel, -1, choices = [rTwo], pos=(65, 30),
                                 size=(40, -1)
                                 )
        self.r2.SetSelection(0)
        self.r3 = wx.Choice(self.panel, -1, choices = [rThree], pos=(120, 30),
                                 size=(40, -1)
                                 )
        self.r3.SetSelection(0)
        self.SetChoices()

        #Create buttons to save new project and to cancel the action
        #self.save_btn = wx.Button(self.panel, -1, 'OK', pos=(10, 60), size=(70, -1), style = wx.ID_OK)
        self.ok_btn = wx.Button(self.panel, -1, "OK", pos=(10, 60), size=(70, -1))
        self.cancel_btn = wx.Button(self.panel, -1, 'Cancel', pos=(90, 60), size=(70, -1))

        #Bind events
        self.Bind(wx.EVT_CHOICE, self.modifyChoices, self.r1)
        self.Bind(wx.EVT_CHOICE, self.modifyChoices, self.r2)
        self.Bind(wx.EVT_CHOICE, self.modifyChoices, self.r3)
        self.Bind(wx.EVT_BUTTON, self.Close, self.cancel_btn)
        self.Bind(wx.EVT_BUTTON, self.Close, self.ok_btn)
        
################################################################################

    def Close(self, event):
        if event.GetEventObject() == self.cancel_btn:
            self.result = None
        self.Destroy()
        
################################################################################

    def modifyChoices(self, event):
        if event.GetEventObject() == self.r1:
            self.ChangeChoices(1)
        elif event.GetEventObject() == self.r2:
            self.ChangeChoices(2)
        elif event.GetEventObject() == self.r3:
            self.ChangeChoices(3)
        
################################################################################

    def SetChoices(self):
        self.ChangeChoices(1)
        self.ChangeChoices(2)
        
################################################################################

    def ChangeChoices(self, number):
        choice1 = self.r1.GetStringSelection()
        choice2 = self.r2.GetStringSelection()
        choice3 = self.r3.GetStringSelection()
        
        #self.r1.
        if number == 1:
            # Set rotor 2 choices
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice1 or choices[x] == choice3:
                    choices.pop(x)
            self.r2.SetItems(choices)
            self.r2.SetStringSelection(choice2)
            
            # Set rotor 3 choices
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice1 or choices[x] == choice2:
                    choices.pop(x)
            self.r3.SetItems(choices)
            self.r3.SetStringSelection(choice3)
            
        elif number == 2:
            # Set rotor1 choice
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice2 or choices[x] == choice3:
                    choices.pop(x)
            self.r1.SetItems(choices)
            self.r1.SetStringSelection(choice1)
            
            # Set rotor 3 choices
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice1 or choices[x] == choice2:
                    choices.pop(x)
            self.r3.SetItems(choices)
            self.r3.SetStringSelection(choice3)
            
        elif number == 3:
            # Set rotor 1 choices
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice2 or choices[x] == choice3:
                    choices.pop(x)
            self.r1.SetItems(choices)
            self.r1.SetStringSelection(choice1)
            
            # Set rotor 2 choices
            choices = list(self.choiceList)
            for x in xrange(len(choices) - 1, -1, -1):
                if choices[x] == choice1 or choices[x] == choice3:
                    choices.pop(x)
            self.r2.SetItems(choices)
            self.r2.SetStringSelection(choice2)
        
        self.result = [choice1, choice2, choice3]
        