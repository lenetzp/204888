#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from component.gui import GUI
from component.game import Game
import time, threading
import random,sys

class application():
	def __init__(self,size=4,randBaseValue=2):
		self.size = size
		self.game = Game(size=self.size,randBaseValue=randBaseValue)
		self.autoRunSign = False
		self.gui = GUI(size=self.size,handleObject={'restart':self.restartHandle,'move':self.moveHandle,'autoRun':self.autoRunHandle,'autoRunStop':self.autoRunStopHandle})

	def moveHandle(self,direction):
		moveResult = self.game.move(direction)
		self.gui.draw(self.game.grid.cells,moveResult)

	def restartHandle(self):
		self.game.restart()
		self.gui.draw(self.game.grid.cells)

	def autoRunHandle(self):
		self.autoRunSign = not self.autoRunSign
		if self.autoRunSign:
			tempThreading = threading.Thread(target=self.autoRunLoop)
			tempThreading.start()

	def autoRunLoop(self):
		while self.autoRunSign:
			self.moveHandle(random.randint(0, 3))
			#time.sleep(0.001)

	def autoRunStopHandle(self):
		self.autoRunSign = False

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