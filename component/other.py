def getCellName(level=0):
	return 0
	if level == 0:
		return 0
	elif level < 10:
		return '小黑' + str(int(level))
	elif level == 10:
		return '小丽子'
	else:
		return '小丽子' + str(int(level) - 9)