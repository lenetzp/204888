#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import math

def getLevel(value,randBaseValue=2):
	return (math.log(value/randBaseValue)/math.log(2) + 1)

def getEmptyArray(size):
	cells = []
	keyX = 0
	keyY = 0
	while keyX < size:
		keyY = 0
		row = []
		while keyY < size:
			row.append(0)
			keyY += 1
		keyX += 1
		cells.append(row)
	return cells

def transitionCoordinate(x,y,direction,size):
	size = size - 1
	return {
		0:{'x':x,'y':y},
		1:{'x':size-y,'y':size-x},
		2:{'x':x,'y':size-y},
		3:{'x':y,'y':x}
	}[direction]

def getDirection():
	return [0,1,2,3]

def getDirectionDict():
	return {0:{'x':0,'y':1},1:{'x':1,'y':0},2:{'x':0,'y':-1},3:{'x':-1,'y':0}}

def traversalCells(data,size,callback=None,direction=0):
	cells = getEmptyArray(size)
	keyX = 0
	keyY = 0
	while keyX < size:
		keyY = 0
		while keyY < size:
			tempCoordinate = transitionCoordinate(x=keyX,y=keyY,direction=direction,size=size)
			tempData = {
				'value':data[tempCoordinate['x']][tempCoordinate['y']],
				'indexX':keyX,
				'indexY':keyY,
				'x':tempCoordinate['x'],
				'y':tempCoordinate['y']
			}
			if callback:
				callback(tempData)
			cells[tempData['indexX']][tempData['indexY']] = tempData
			keyY += 1
		keyX += 1
	return cells

class Grid():
	def __init__(self,size=4,perGridObject=None,randBaseValue=2):
		self.size = size;
		self.randBaseValue = randBaseValue
		self.cells = self.fromState(perGridObject) if perGridObject != None else getEmptyArray(self.size);

	def fromState(self,perGridObject):
		cells = getEmptyArray(self.size)
		keyX = 0
		keyY = 0
		while keyX < self.size:
			keyY = 0
			while keyY < self.size:
				cells[keyX][keyY] = perGridObject.cells[keyX][keyY]
				keyY += 1
			keyX += 1
		return cells

	# def empty(self):
	# 	return getEmptyArray(self.size)

	def randAdd(self):
		def callback(data):
			if (data['value'] == 0):
				emptyList.append(data)
		emptyList = []
		traversalCells(data=self.cells,size=self.size,callback=callback)
		if len(emptyList) == 0:
			return None
		tempData = emptyList[random.randint(0, len(emptyList) - 1)]
		self.cells[tempData['x']][tempData['y']] = (self.randBaseValue if random.random() > 0.3 else self.randBaseValue * 2)
		return tempData

	def isEnd(self):
		keyX = 0
		keyY = 0
		while keyX < self.size:
			keyY = 0
			while keyY < self.size:
				if self.cells[keyX][keyY] == 0:
					return False
				if keyY == self.size - 1:
					keyY += 1
					continue
				if self.cells[keyX][keyY] == self.cells[keyX][keyY + 1]:
					return False
				if keyX == self.size - 1:
					keyY += 1
					continue
				if self.cells[keyX][keyY] == self.cells[keyX + 1][keyY]:
					return False
				keyY += 1
			keyX += 1
		return True

	def move(self,direction):
		moveSign = False
		traversalData = traversalCells(data=self.cells,size=self.size,direction=direction)
		#print('traversalData',traversalData)
		keyX = 0
		keyY = 0
		tempData = None
		while keyX < self.size:
			keyY = 0
			tempData = None
			while keyY < self.size:
				if tempData != None and tempData['value'] == traversalData[keyX][keyY]['value']:
					moveSign = True
					tempData['value'] *= 2
					traversalData[keyX][keyY]['value'] = 0
					tempData = None
				if traversalData[keyX][keyY]['value'] > 0:
					tempData = traversalData[keyX][keyY]
				keyY += 1
			keyX += 1
		keyX = 0
		while keyX < self.size:
			keyY = 0
			tempData = None
			while keyY < self.size:
				if tempData != None and traversalData[keyX][keyY]['value'] > 0:
					moveSign = True
					tempData['value'] = traversalData[keyX][keyY]['value']
					traversalData[keyX][keyY]['value'] = 0
					tempData = None
					keyY = 0
				if tempData == None and traversalData[keyX][keyY]['value'] == 0:
					tempData = traversalData[keyX][keyY]
				keyY += 1
			keyX += 1
		keyX = 0
		while keyX < self.size:
			keyY = 0
			while keyY < self.size:
				self.cells[traversalData[keyX][keyY]['x']][traversalData[keyX][keyY]['y']] = traversalData[keyX][keyY]['value']
				keyY += 1
			keyX += 1
		#print('moveCell',self.cells)
		return {'moveSign':moveSign,'isEnd':self.isEnd()}
