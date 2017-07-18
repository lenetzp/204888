#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .grid import Grid
from .grid import getEmptyArray
from .grid import traversalCells
from .grid import getDirection
from .grid import getDirectionDict
from .grid import getLevel
import time
import math

directionsArray = getDirection()
directionDict = getDirectionDict()

perSearchTime = 100

def getTime():
	return int(time.time()*1000)

def smoothness(gridObject):
	smoothnessResult = []
	value = 0
	def less(data):
		print(data)
		print(smoothnessResult)
		smoothnessResult -= data
	def callback_smoothness(data):
		if (data['value'] > 0):
			level = getLevel(data['value'],gridObject.randBaseValue)
			if data['x'] < gridObject.size - 1 and gridObject.cells[data['x']+1][data['y']] > 0:
				#smoothnessResult -= 
				smoothnessResult.append(level - getLevel(gridObject.cells[data['x']+1][data['y']],gridObject.randBaseValue))
			if data['y'] < gridObject.size - 1 and gridObject.cells[data['x']][data['y']+1] > 0:
				#smoothnessResult -= 
				smoothnessResult.append(level - getLevel(gridObject.cells[data['x']][data['y']+1],gridObject.randBaseValue))
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback_smoothness)
	for x in smoothnessResult:
		value -= x
	print('smoothness',value)
	return value

def islands(gridObject):
	def callback(data):
		if (data['value'] > 0):
			tempIsland = 0
			for direction in directionDict:
				try:
					if data['value'] == gridObject.cell[data['x'] + direction['x']][data['y'] + direction['y']]:
						continue
				except Exception as e:
					tempIsland += 1
					continue
				tempIsland += 1
			if tempIsland == 4:
				islands += 1
	islands = 0
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	return islands

def monotonicity2(gridObject):
	totals = [0, 0, 0, 0]
	keyX = 0
	keyY = 0
	while keyX < gridObject.size:
		current = 0;
		next = current+1;
		while next < gridObject.size:
			while (next < gridObject.size and gridObject.cells[keyX][next] == 0):
				next += 1
			if next >= 4:
				next -= 1
			currentValue = getLevel(gridObject.cells[keyX][current],gridObject.randBaseValue) if gridObject.cells[keyX][current] > 0 else 0
			nextValue = getLevel(gridObject.cells[keyX][next],gridObject.randBaseValue) if gridObject.cells[keyX][next] > 0 else 0
			if currentValue > nextValue:
				totals[0] += nextValue - currentValue
			elif nextValue > currentValue:
				totals[1] += currentValue - nextValue
			current = next
			next += 1
		keyX += 1
	while keyY < gridObject.size:
		current = 0;
		next = current+1;
		while next < gridObject.size:
			while (next < gridObject.size and gridObject.cells[next][keyY] == 0):
				next += 1
			if next >= 4:
				next -= 1
			currentValue = getLevel(gridObject.cells[current][keyY],gridObject.randBaseValue) if gridObject.cells[current][keyY] > 0 else 0
			nextValue = getLevel(gridObject.cells[next][keyY],gridObject.randBaseValue) if gridObject.cells[next][keyY] > 0 else 0
			if currentValue > nextValue:
				totals[2] += nextValue - currentValue
			elif nextValue > currentValue:
				totals[3] += currentValue - nextValue
			current = next
			next += 1
		keyY += 1
	print('monotonicity2',totals)
	return max(totals[0], totals[1]) + max(totals[2], totals[3]);

def maxValue(gridObject):
	def callback(data):
		if (max['max'] == None or data['value'] > max['max']['value']):
			max['max'] = data
	max = {'max':None}
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	return max['max']

def getEmpty(gridObject):
	def callback(data):
		if (data['value'] == 0):
			emptyList.append(data)
	emptyList = []
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	return emptyList

def getScoreOfGrid(gridObject):
	emptyCells = len(getEmpty(gridObject));
	smoothWeight = 0.1
	mono2Weight = 1.0
	emptyWeight = 2.7
	maxWeight = 1.0
	return  float(smoothness(gridObject)) * float(smoothWeight) + float(monotonicity2(gridObject)) * mono2Weight + math.log(emptyCells) * emptyWeight + getLevel(maxValue(gridObject)['value'],gridObject.randBaseValue) * maxWeight

class SimpleAI():
	def __init__(self, size=4,randBaseValue=2,gridObject=None):
		self.size = size
		self.randBaseValue = randBaseValue
		if gridObject != None:
			self.initGridObject = Grid(size=self.size,randBaseValue=self.randBaseValue,perGridObject=gridObject)
		else:
			self.initGridObject = Grid(size=self.size,randBaseValue=self.randBaseValue)

	def getBest(self):
		startTime = getTime()
		depth = 0
		best = None
		while getTime() - startTime < perSearchTime:
			tempBest = self.search(depth,gridObject=self.initGridObject)
			if (best == None or tempBest['score'] > best['score']) and tempBest['direction'] != -1:
				best = tempBest
		return best

	def search(self,depth=0,gridObject=None,turn=0):
		bestScore = None
		bestMove = -1;
		tempResult = None
		#directionsArray = [0,1,2,3]
		if turn == 0:
			for direction in directionsArray:
				tempGrid = Grid(size=gridObject.size,randBaseValue=gridObject.randBaseValue,perGridObject=gridObject)
				if tempGrid.move(direction)['moveSign']:
					if depth == 0:
						tempResult = {'direction':direction,'score':getScoreOfGrid(tempGrid)}
					else:
						tempResult = self.search(depth=(depth-1),gridObject=tempGrid,turn=1)
					if bestScore == None or bestScore < tempResult['score']:
						bestScore = tempResult['score']
						bestMove = tempResult['direction']
		else:
			candidates = []
			maxValue = None
			tempValue = None
			tempCells = getEmpty(gridObject)
			for emptyCell in tempCells:
				gridObject[emptyCell['x']][emptyCell['y']] = 2
				tempValue = -smoothness(gridObject) + islands(gridObject)
				if maxValue == None or tempValue > maxValue:
					candidates = []
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':2})
				elif tempValue == maxValue:
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':2})
				gridObject[emptyCell['x']][emptyCell['y']] = 4
				if maxValue == None or tempValue > maxValue:
					candidates = []
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':4})
				elif tempValue == maxValue:
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':4})
				tempValue = -smoothness(gridObject) + islands(gridObject)
				gridObject[emptyCell['x']][emptyCell['y']] = 0
			for candidateItem in candidates:
				tempGrid = Grid(size=gridObject.size,randBaseValue=gridObject.randBaseValue,perGridObject=gridObject)
				tempGrid.cells[candidateItem['x']][candidateItem['y']] = candidateItem['value']
				tempResult = self.search(depth=depth,gridObject=tempGrid)
				if bestScore == None or bestScore < tempResult['score']:
					bestScore = tempResult['score']
					bestMove = tempResult['direction']
		return {'direction':bestMove,'score':bestScore}