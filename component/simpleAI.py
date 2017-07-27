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

def getDataByMonotonicity3DirectionDataTest(gridObject,monotonicity3DirectionData):
	key = 0
	print('test=====================')
	while key < gridObject.size * gridObject.size:
		getDataByMonotonicity3DirectionData(gridObject,index=key,directionItemData=monotonicity3DirectionData[3])
		key += 1
	print('test=====================')

def getDataByMonotonicity3DirectionData(gridObject,index,directionItemData):
	keyX = None
	keyY = None
	if directionItemData['direction']['x'] == 0:
		keyX = directionItemData['startPosition']['x'] + int(index / gridObject.size) * directionItemData['direction']['x']
		if keyX % 2 == directionItemData['startPosition']['x'] % 2:
			keyY = directionItemData['startPosition']['y'] + directionItemData['direction']['y'] * (index % gridObject.size)
		else:
			keyY = (gridObject.size - 1 if 0 == directionItemData['startPosition']['y'] else 0) + directionItemData['direction']['y'] * (index % gridObject.size) * -1
	else:
		keyY = directionItemData['startPosition']['y'] + int(index / gridObject.size) * directionItemData['direction']['y']
		if keyY % 2 == directionItemData['startPosition']['y'] % 2:
			keyX = directionItemData['startPosition']['x'] + directionItemData['direction']['x'] * (index % gridObject.size)
		else:
			keyX = (gridObject.size - 1 if 0 == directionItemData['startPosition']['x'] else 0) + directionItemData['direction']['x'] * (index % gridObject.size) * -1
	#print('keyX-keyY',keyX,keyY)
	return {'x':keyX,'y':keyY,'value':gridObject.cells[keyX][keyY]}

def getTime():
	return int(time.time()*1000)

def smoothness(gridObject):
	smoothnessResult = []
	value = 0
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
	#print('smoothness',value)
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
				islandsResult.append(1)
	islandsResult = []
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	#print('islands',len(islandsResult))
	return len(islandsResult)

def monotonicity2(gridObject):
	totals = [0, 0, 0, 0]
	keyX = 0
	keyY = 0
	while keyX < gridObject.size:
		current = 0
		next = current+1
		while next < gridObject.size:
			while (next < gridObject.size and gridObject.cells[keyX][next] == 0):
				next += 1
			if next >= gridObject.size:
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
		current = 0
		next = current+1
		while next < gridObject.size:
			while (next < gridObject.size and gridObject.cells[next][keyY] == 0):
				next += 1
			if next >= gridObject.size:
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
	#print('monotonicity2',totals)
	return max(max(totals[0], totals[1]), max(totals[2], totals[3]))

def monotonicity3(gridObject,monotonicity3DirectionData):
	totals = [0,0,0,0,0,0,0,0]
	keyX = 0
	keyY = 0
	countOfCells = gridObject.size * gridObject.size
	while keyX < len(totals):
		current = 0
		next = current + 1
		while next < countOfCells:
			tempNextCellItemData = getDataByMonotonicity3DirectionData(gridObject=gridObject,index=next,directionItemData=monotonicity3DirectionData[keyX])
			tempCurrentCellItemData = getDataByMonotonicity3DirectionData(gridObject=gridObject,index=current,directionItemData=monotonicity3DirectionData[keyX])
			# while (next < countOfCells and tempNextCellItemData['value'] == 0):
			# 	if next == countOfCells - 1:
			# 		break
			# 	next += 1
			# 	tempNextCellItemData = getDataByMonotonicity3DirectionData(gridObject=gridObject,index=next,directionItemData=monotonicity3DirectionData[keyX])
			currentValue = getLevel(tempCurrentCellItemData['value'],gridObject.randBaseValue) if tempCurrentCellItemData['value'] > 0 else 0
			nextValue = getLevel(tempNextCellItemData['value'],gridObject.randBaseValue) if tempNextCellItemData['value'] > 0 else 0
			totals[keyX] += currentValue - nextValue
			current = next
			next += 1
		keyX += 1
	#print('monotonicity3',totals)
	return max(totals)

def maxValue(gridObject):
	def callback(data):
		if (max['max'] == None or data['value'] > max['max']['value']):
			max['max'] = data
	max = {'max':None}
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	#print('maxValue',max['max'])
	return max['max']

def getEmpty(gridObject):
	def callback(data):
		if (data['value'] == 0):
			emptyList.append(data)
	emptyList = []
	traversalCells(data=gridObject.cells,size=gridObject.size,callback=callback)
	return emptyList

def getScoreOfGrid(gridObject,monotonicity3DirectionData):
	emptyCells = len(getEmpty(gridObject))
	smoothWeight = 0.1
	mono2Weight = 1.3
	emptyWeight = 2.7
	maxWeight = 1.0
	mono3Weight = 0.1
	valueArray = []
	finalValue = 0
	valueArray.append(float(smoothness(gridObject)) * smoothWeight)
	valueArray.append(float(monotonicity2(gridObject)) * mono2Weight)
	valueArray.append(float(monotonicity3(gridObject,monotonicity3DirectionData)) * mono3Weight)
	valueArray.append(math.log(emptyCells) * emptyWeight)
	valueArray.append(getLevel(maxValue(gridObject)['value'],gridObject.randBaseValue) * maxWeight)
	for x in valueArray:
		finalValue += x
	return  finalValue

class SimpleAI():
	def __init__(self, size=4,randBaseValue=2,gridObject=None):
		self.size = size
		self.randBaseValue = randBaseValue
		self.monotonicity3DirectionData = [{
			'startPosition':{
				'x':0,
				'y':0
			},
			'direction':{
				'x':1,
				'y':0
			}
		},{
			'startPosition':{
				'x':0,
				'y':0
			},
			'direction':{
				'x':0,
				'y':1
			}
		},{
			'startPosition':{
				'x':self.size - 1,
				'y':0
			},
			'direction':{
				'x':-1,
				'y':0
			}
		},{
			'startPosition':{
				'x':self.size - 1,
				'y':0
			},
			'direction':{
				'x':0,
				'y':1
			}
		},{
			'startPosition':{
				'x':0,
				'y':self.size - 1
			},
			'direction':{
				'x':1,
				'y':0
			}
		},{
			'startPosition':{
				'x':0,
				'y':self.size - 1
			},
			'direction':{
				'x':0,
				'y':-1
			}
		},{
			'startPosition':{
				'x':self.size - 1,
				'y':self.size - 1
			},
			'direction':{
				'x':-1,
				'y':0
			}
		},{
			'startPosition':{
				'x':self.size - 1,
				'y':self.size - 1
			},
			'direction':{
				'x':0,
				'y':-1
			}
		}]
		if gridObject != None:
			self.initGridObject = Grid(size=self.size,randBaseValue=self.randBaseValue,perGridObject=gridObject)
		else:
			self.initGridObject = Grid(size=self.size,randBaseValue=self.randBaseValue)
		#getDataByMonotonicity3DirectionDataTest(self.initGridObject,self.monotonicity3DirectionData)

	def getBest(self):
		startTime = getTime()
		depth = 0
		best = None
		while getTime() - startTime < perSearchTime:
			tempBest = self.search(depth,gridObject=self.initGridObject)
			if (best == None or (tempBest['score'] and tempBest['score'] > best['score']) and tempBest['direction'] != -1):
				best = tempBest
			depth += 1
		print(best,depth,'best===================')
		if best['direction'] == -1:
			return None
		return best

	def search(self,depth=0,gridObject=None,turn=0):
		bestScore = None
		bestMove = -1
		tempResult = None
		#directionsArray = [0,1,2,3]
		if turn == 0:
			for direction in directionsArray:
				tempGrid = Grid(size=gridObject.size,randBaseValue=gridObject.randBaseValue,perGridObject=gridObject)
				tempMoveResult = tempGrid.move(direction)
				if tempMoveResult['moveSign']:
					if depth == 0:
						tempResult = {'direction':direction,'score':getScoreOfGrid(tempGrid,monotonicity3DirectionData=self.monotonicity3DirectionData)}
					else:
						tempResult = self.search(depth=(depth-1),gridObject=tempGrid,turn=1)
					if bestScore == None or (tempResult['score'] and bestScore < tempResult['score']):
						#print('0',tempResult)
						bestScore = tempResult['score']
						bestMove = direction
						#tempResult['direction']
		else:
			candidates = []
			maxValue = None
			tempValue = None
			tempCells = getEmpty(gridObject)
			for emptyCell in tempCells:
				gridObject.cells[emptyCell['x']][emptyCell['y']] = gridObject.randBaseValue
				tempValue = -smoothness(gridObject) + islands(gridObject)
				if maxValue == None or tempValue > maxValue:
					candidates = []
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':gridObject.randBaseValue})
				elif tempValue == maxValue:
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':gridObject.randBaseValue})
				gridObject.cells[emptyCell['x']][emptyCell['y']] = gridObject.randBaseValue * 2
				tempValue = -smoothness(gridObject) + islands(gridObject)
				if maxValue == None or tempValue > maxValue:
					candidates = []
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':gridObject.randBaseValue * 2})
				elif tempValue == maxValue:
					candidates.append({'x':emptyCell['x'],'y':emptyCell['y'],'value':gridObject.randBaseValue * 2})
				tempValue = -smoothness(gridObject) + islands(gridObject)
				gridObject.cells[emptyCell['x']][emptyCell['y']] = 0
			for candidateItem in candidates:
				tempGrid = Grid(size=gridObject.size,randBaseValue=gridObject.randBaseValue,perGridObject=gridObject)
				tempGrid.cells[candidateItem['x']][candidateItem['y']] = candidateItem['value']
				tempResult = self.search(depth=depth,gridObject=tempGrid)
				if bestScore == None or (tempResult['score'] != -1 and bestScore < tempResult['score']):
					#print('1',tempResult)
					bestScore = tempResult['score']
					bestMove = tempResult['direction']
		return {'direction':bestMove,'score':bestScore}