#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tkinter import *
import tkinter.messagebox as messagebox
from .grid import getLevel

keyList = [38,39,40,37]
keyDict = {38:0,39:1,40:2,37:3}
keyNameDict = {0:'up',1:'right',2:'down',3:'left'}

tileStyleMap = {
    0:{
        'background': '#faf8ef'
    },
    1:{
        'color': '#776e65',
        'background': '#eee4da'
    },
    2:{
        'color': '#776e65',
        'background': '#ede0c8'
    },
    3:{
        'color': '#f9f6f2;',
        'background': '#f2b179'
    },
    4:{
        'color': '#f9f6f2;',
        'background': '#f59563'
    },
    5:{
        'color': '#f9f6f2;',
        'background': '#f67c5f'
    },
    6:{
        'color': '#f9f6f2;',
        'background': '#f65e3b'
    },
    7:{
        'color': '#f9f6f2;',
        'background': '#edcf72'
    },
    8:{
        'color': '#f9f6f2;',
        'background': '#edcc61'
    },
    9:{
        'color': '#f9f6f2;',
        'background': '#edc850'
    },
    10:{
        'color': '#f9f6f2;',
        'background': '#edc53f'
    },
    11:{
        'color': '#f9f6f2;',
        'background': '#edc22e'
    }
}

perCell = 70
border = 1

class GUI(Frame):
    def __init__(self,size=4,master=None,randBaseValue=2,handleObject=None):
        Frame.__init__(self, master)
        self.size = size
        self.handleObject = handleObject
        self.width = self.size * perCell
        self.randBaseValue = randBaseValue
        self.pack()
        self.master.geometry(str(int(self.width)) + 'x' + str(int(self.width)))
        self.master.background = '#776e65'
        self.createWidgets()
        self.bind_all('<KeyPress>', self.keyHandle)

    def createWidgets(self):
        # self.restartButton = Button(self, text='restart', command=self.restart)
        # self.restartButton.grid(row=0, column=2, columnspan=3)
        self.canvas = Canvas(self, width=self.width,height=self.width)
        self.canvas.pack()

    def restart(self):
        self.handleObject['restart']()

    def displayString(self,x,y,value):
        styleObject = None
        if value > 2048:
            styleObject = tileStyleMap[11]
        else:
            styleObject = tileStyleMap[(getLevel(value,randBaseValue=self.randBaseValue) if value != 0 else 0)]
        rectparam = x * perCell + border,y * perCell + border,x * perCell + perCell - border,y * perCell + perCell - border
        self.canvas.create_rectangle(rectparam,tags = "rect",fill=styleObject['background'],width=0)
        if value > 0:
            showValue = value
            if value > 1073741824:
                showValue = (str(int(value / 1073741824)) + 'G')
            else:
                if value > 1048576:
                    showValue = (str(int(value / 1048576)) + 'M')
                else:
                    if value >= 16384:
                        showValue = (str(int(value / 1024)) + 'K')
            self.canvas.create_text(x * perCell + (perCell/2),y * perCell + (perCell/2),text=showValue, font = ("微软雅黑 "+str(int(perCell/4 if value > 64 else perCell/3))+" bold"),fill=styleObject['color'], tags = "cell")

    def displayClear(self):
        self.canvas.delete("cell","rect")

    def draw(self,data,moveResult=None):
        #print('draw',data)
        self.displayClear()
        self.canvas.create_rectangle(0,0,self.width,self.width,tags = "rect",fill='#776e65',width=0)
        for x in range(self.size):
            for y in range(self.size):              
                self.displayString(x,y,data[x][y])
        if moveResult != None:
            if moveResult['isEnd']:
                self.handleObject['autoRunStop']()
                messagebox.showinfo('result', 'it\'s end;"r" for restart;"ESC" for exit')

    def keyHandle(self,event):
        #print(event.keycode)
        if event.keycode == 27:
            self.handleObject['quit']()
            sys.exit()
            return
        if event.keycode == 72:
            messagebox.showinfo('help', '"r" for restart;"h" for help;"ESC" for exit')
            return
        if event.keycode == 82:
            self.restart()
            return
        if event.keycode == 65:
            self.handleObject['autoRun']()
            return
        if event.keycode == 73:
            self.handleObject['aiRun']()
            return
        try:
            keyList.index(event.keycode)
        except:
            return
        key = keyDict[event.keycode]
        #print(keyNameDict[key])
        self.handleObject['move'](key)