#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .grid import Grid
from .grid import getEmptyArray

class Game():
	def __init__(self,size=4,randBaseValue=2):
		self.size = size
		self.randBaseValue = randBaseValue
		print('Game init',size)
		self.init()

	def restart(self):
		print('restart')
		self.init()

	def move(self,direction):
		print('direction',direction)
		tempMoveData = self.grid.move(direction)
		tempAddData = None
		if tempMoveData['moveSign']:
			tempAddData = self.grid.randAdd()
		return {'randAdd':tempAddData,'isEnd':tempMoveData['isEnd']}

	def init(self):
		self.grid = Grid(self.size,randBaseValue=self.randBaseValue)
		self.grid.randAdd()
		self.grid.randAdd()