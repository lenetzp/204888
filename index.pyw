#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from component.gui import GUI
from component.game import Game
from component.simpleAI import SimpleAI
import time, threading
import random,sys

class application():
	def __init__(self,size=4,randBaseValue=2):
		self.size = size
		self.randBaseValue = randBaseValue
		self.game = Game(size=self.size,randBaseValue=self.randBaseValue)
		self.autoRunSign = False
		self.aiRunSign = False
		self.gui = GUI(size=self.size,handleObject={
			'restart':self.restartHandle,
			'move':self.moveHandle,
			'autoRun':self.autoRunHandle,
			'autoRunStop':self.autoRunStopHandle,
			'aiRunStopHandle':self.aiRunStopHandle,
			'aiRun':self.aiRunHandle,
			'quit':self.quitHandle
		})

	def moveHandle(self,direction):
		moveResult = self.game.move(direction)
		self.gui.draw(self.game.grid.cells,moveResult)

	def restartHandle(self):
		self.game.restart()
		self.gui.draw(self.game.grid.cells)

	def quitHandle(self):
		self.aiRunSign = False
		self.autoRunSign = False

	def autoRunHandle(self):
		self.autoRunSign = not self.autoRunSign
		if self.autoRunSign:
			self.aiRunSign = False
			tempThreading = threading.Thread(target=self.autoRunLoop)
			tempThreading.start()

	def autoRunLoop(self):
		while self.autoRunSign:
			self.moveHandle(random.randint(0, 3))
			#time.sleep(0.001)

	def aiRunHandle(self):
		self.aiRunSign = not self.aiRunSign
		if self.aiRunSign:
			self.autoRunSign = False
			tempThreading = threading.Thread(target=self.aiRunLoop)
			tempThreading.start()

	def aiRunLoop(self):
		while self.aiRunSign:
			tempBest = SimpleAI(size=self.size,randBaseValue=self.randBaseValue,gridObject=self.game.grid).getBest()
			if tempBest == None:
				self.aiRunSign = False
				break
			self.moveHandle(tempBest['direction'])
			#time.sleep(0.001)

	def autoRunStopHandle(self):
		self.autoRunSign = False

	def aiRunStopHandle(self):
		self.aiRunSign = False

	def run(self):
		self.gui.draw(self.game.grid.cells)
		self.gui.master.title('204888-press "h"')
		self.gui.mainloop()

print('params',sys.argv)

size = 4
randBaseValue = 2
if len(sys.argv) > 1:
 	size = int(sys.argv[1])
if len(sys.argv) > 2:
 	randBaseValue = int(sys.argv[2])

application(size,randBaseValue).run()