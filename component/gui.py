#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox as messagebox

keyList = [38,39,40,37]
keyDict = {38:0,39:1,40:2,37:3}
keyNameDict = {0:'up',1:'right',2:'down',3:'left'}

perCell = 70

class GUI(Frame):
    def __init__(self,size=4,master=None,handleObject=None):
        Frame.__init__(self, master)
        self.size = size
        self.handleObject = handleObject
        self.grid()
        self.createWidgets()
        self.bind_all('<KeyPress>', self.keyHandle)

    def createWidgets(self):
        self.restartButton = Button(self, text='restart', command=self.restart)
        self.restartButton.grid(row=0, column=2, columnspan=3)
        width = self.size * perCell
        self.canvas = Canvas(self, width=width,height=width)
        self.canvas.grid(row=1)

    def restart(self):
        self.handleObject['restart']()

    def displayString(self,x,y,value):
        self.canvas.create_text(x * perCell + (perCell/2),y * perCell + (perCell/2),text= value, font = "time 10 bold", tags = "cell")

    def displayClear(self):
        self.canvas.delete("cell")

    def draw(self,data):
        print('draw',data)
        self.displayClear()
        for x in range(self.size):
            for y in range(self.size):
                if data[x][y] > 0:                
                    self.displayString(y,x,data[x][y])

    def keyHandle(self,event):
        try:
            keyList.index(event.keycode)
        except:
            return
        key = keyDict[event.keycode]
        #print(keyNameDict[key])
        self.handleObject['move'](key)