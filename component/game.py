#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .grid import Grid
from .grid import getEmptyArray

class Game():
	def __init__(self,size=4):
		self.size = size
		print('Game init',size)
		self.grid = Grid(self.size,getEmptyArray(self.size))
		self.grid.randAdd()
		self.grid.randAdd()

	def restart(self):
		print('restart')
		self.grid = Grid(self.size,getEmptyArray(self.size))

	def move(self,direction):
		print('direction',direction)
		tempMoveData = self.grid.move(direction)
		if tempMoveData['moveSign']:
			self.grid.randAdd()