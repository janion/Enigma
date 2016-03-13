# -*- coding: utf-8 -*-
"""
Created on Fri Feb 05 21:38:52 2016

@author: Janion
"""

import wx

class ReflectorDlg(wx.Dialog):
    
    result = []
    
    def __init__(self, parent, idd, refNum):
        wx.Dialog.__init__(self, parent, idd, "Reflector selection", size=(180, 125))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        #Create instructional text and a text box to enter the project name
        wx.StaticText(self.panel, -1, "Please select the reflector:",
                      (10, 10)
                      )
        
        #Create text and hour entry box
        self.r1 = wx.Choice(self.panel, -1, choices = ["A", "B", "C"], pos=(10, 30),
                                 size=(150, -1)
                                 )
        self.r1.SetSelection(refNum)

        #Create buttons to save new project and to cancel the action
        self.ok_btn = wx.Button(self.panel, -1, "OK", pos=(10, 60), size=(70, -1))
        self.cancel_btn = wx.Button(self.panel, -1, 'Cancel', pos=(90, 60), size=(70, -1))

        #Bind events
        self.Bind(wx.EVT_BUTTON, self.Close, self.cancel_btn)
        self.Bind(wx.EVT_BUTTON, self.Close, self.ok_btn)
        
################################################################################

    def Close(self, event):
        if event.GetEventObject() == self.cancel_btn:
            self.result = None
        else:
            self.result = self.r1.GetSelection()
        self.Destroy()
        
################################################################################

    def getResult(self):
        return self.result