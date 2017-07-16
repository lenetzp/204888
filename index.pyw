#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from component.gui import GUI
from component.game import Game

size = 4

class application():
	def __init__(self,size=4):
		self.size = size
		self.game = Game(size=self.size)
		self.gui = GUI(size=self.size,handleObject={'restart':self.restartHandle,'move':self.moveHandle})

	def moveHandle(self,direction):
		self.game.move(direction)
		self.gui.draw(self.game.grid.cells)

	def restartHandle(self):
		self.game.restart()
		self.gui.draw(self.game.grid.cells)

	def run(self):
		self.gui.draw(self.game.grid.cells)
		self.gui.master.title('204888')
		self.gui.mainloop()

application(size).run()