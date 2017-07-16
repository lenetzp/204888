#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

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
	return {
		0:{'x':x,'y':y},
		1:{'x':size-y,'y':x},
		2:{'x':size-x,'y':y},
		3:{'x':y,'y':x}
	}[direction]

def traversalCells(data,size,callback,direction=0):
	keyX = 0
	keyY = 0
	while keyX < size:
		keyY = 0
		while keyY < size:
			tempCoordinate = transitionCoordinate(x=keyX,y=keyY,direction=direction,size=size)
			callback({
				'value':data[tempCoordinate['x']][tempCoordinate['y']],
				'indexX':keyX,
				'indexY':keyY,
				'x':tempCoordinate['x'],
				'y':tempCoordinate['y']
			})
			keyY += 1
		keyX += 1

class Grid():
	def __init__(self,size=4,perGridObject=None):
		self.size = size;
		self.cells = self.fromState(perGridObject) if perGridObject else self.empty();

	def fromState(self,perGridObject):
		cells = getEmptyArray(self.size)
		keyX = 0
		keyY = 0
		while keyX < self.size:
			keyY = 0
			while keyY < self.size:
				cells[keyX][keyY] = perGridObject[keyX][keyY]
				keyY += 1
			keyX += 1
		return cells

	def empty(self):
		return getEmptyArray(self.size)

	def randAdd(self):
		def callback(data):
			if (data['value'] == 0):
				emptyList.append(data)
		emptyList = []
		traversalCells(data=self.cells,size=self.size,callback=callback)
		if len(emptyList) == 0:
			return False
		tempData = emptyList[random.randint(0, len(emptyList))]
		self.cells[tempData['x']][tempData['y']] = (2 if random.random() > 0.5 else 4)
		return True

	def move(self,direction):
		cells = self.cells
		moveSign = False
		tempRow = None
		tempMoveRow = None
		tempRowIndex = None
		tempMoveRowIndex = None
		def sumCallback(data):
			if None == tempRow:
				tempRow = []
			tempRow.append(data)
			if self.size == len(tempRow):
				for tempRowIndex in tempRow:
					if tempRowIndex > 0 and cells[tempRow[tempRowIndex - 1]['x']][tempRow[tempRowIndex - 1]['y']] == cells[tempRow[tempRowIndex]['x']][tempRow[tempRowIndex]['y']] and cells[tempRow[tempRowIndex]['x']][tempRow[tempRowIndex]['y']] != 0:
						cells[tempRow[tempRowIndex - 1]['x']][tempRow[tempRowIndex - 1]['y']] *= 2
						cells[tempRow[tempRowIndex]['x']][tempRow[tempRowIndex]['y']] = 0
				tempRow = None
		def moveCallback(data):
			if None == tempRow:
				tempRow = []
			tempRow.append(data)
			if self.size == len(tempRow):
				tempRowIndex = 0
				tempMoveRowIndex = 0
				tempMoveRow = []
				while tempRowIndex < self.size:
					if tempRowIndex < len(tempRow) and tempRow[tempRowIndex]['value'] > 0:
						tempMoveRow.push(tempRow[tempRowIndex]['value'])
					else:
						tempMoveRow.push(0)
					tempRowIndex += 1
				tempRowIndex = 0
				while tempRowIndex < self.size:
					cells[tempRow[tempRowIndex]['x']][tempRow[tempRowIndex]['y']] = tempMoveRow.push(tempRowIndex)
					tempRowIndex += 1
				tempRow = None
		traversalCells(data=self.cells,size=self.size,callback=sumCallback,direction=direction)
		tempRow = None
		tempRowIndex = None
		traversalCells(data=self.cells,size=self.size,callback=moveCallback,direction=direction)
		self.cells = cells
		return {'moveSign':moveSign}
