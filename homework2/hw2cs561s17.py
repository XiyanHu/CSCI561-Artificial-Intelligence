import sys
import copy
bestAction = None
bestScore = float('-inf')
maxDepth = 0
graph = {}
p1PreferList = {}
p2PreferList = {}
def read_file():
	global maxDepth
	global graph
	global p1PreferList
	global p2PreferList
	inputFile = open(sys.argv[2],'r')
	lines = inputFile.readlines()
	
	#set up colorlist
	colors = lines[0].strip()
	colorList = colors.replace(' ','').split(",")


	initialActions = lines[1].strip().replace(' ','').split(",")
	maxDepth = lines[2].strip()
	# Set up prefer list
	p1Prefer = lines[3].strip().replace(' ','').split(",")
	p2Prefer = lines[4].strip().replace(' ','').split(",")
	p1PreferList = { prefer.split(":")[0]:prefer.split(":")[1] for prefer in p1Prefer}
	p2PreferList = { prefer.split(":")[0]:prefer.split(":")[1] for prefer in p2Prefer}
	# set up graph
	for index in range(5,len(lines)):
		reBlank = lines[index].strip().replace(' ','')
		nodeName = reBlank.split(":")[0]
		neighborList = reBlank.split(":")[1].split(",")
		graph[nodeName] = sorted(neighborList)
	
	p1Action = {}
	p2Action = {}
	assigned = {}
	curPath = []
	for initialAction in initialActions:
		action = initialAction.split("-")
		detail = action[0].split(":")
		if action[1] == "1":   
			p1Action[detail[0]] = detail[1]
		else:
			p2Action[detail[0]] = detail[1]
		assigned[detail[0]] = detail[1]
		curPath.append((detail[0],detail[1]))

	currDomains = InitializeDomains(colorList,p1Action,p2Action)
	initialEval = 0
	for action in p1Action:
		initialEval += int(p1PreferList[p1Action[action]])
	for action in p2Action:
		initialEval -= int(p2PreferList[p2Action[action]])

	forwardCheck(assigned,currDomains)
	
	alpha = float('-inf')
	beta = float('inf')
	outputFile = open("output.txt","w")
	bestResult = maxValue(0,assigned,currDomains,curPath,alpha,beta,outputFile)	
	outputFile.write(bestAction[0]+", "+bestAction[1] +", "+str(bestResult));
	outputFile.close()

def forwardCheck(assigned,currDomains):
	for node in assigned:
		for neighbor in graph[node]:
			if (len(currDomains[node]) > 0):
				if currDomains[node][0] in currDomains[neighbor]:
					currDomains[neighbor].remove(currDomains[node][0])
	return True
#Set up initial domains	
def InitializeDomains(colorList,p1Action,p2Action):
	currDomains = { variable: list(colorList) for variable in graph}
	for action in p1Action:
		currDomains[action] = list(p1Action[action])   # delete p1action?
	for action in p2Action:
		currDomains[action] = list(p2Action[action])
	return currDomains

def minValue(depth,assigned,currDomains,curPath,alpha,beta,outputFile):
	global maxDepth
	lastAction = curPath[len(curPath)-1]
	possibleActions = findPossActions(assigned,currDomains)
	if depth == int(maxDepth) or not possibleActions:	
		evalScore = calEvalScore(curPath)
		outputFile.write( lastAction[0] + ", " + lastAction[1] + ", " + str(depth) + ", " + str(evalScore) + ", " + str(alpha) + ", " + str(beta)+"\n")
		return evalScore
	v = float('inf')
	outputFile.write( lastAction[0] + ", " + lastAction[1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
	
	for action in possibleActions:
		tempAssigned = copy.deepcopy(assigned)
		tempAssigned[action[0]] = action[1]
		tmpPath = copy.deepcopy(curPath)
		tmpPath.append((action[0],action[1]))
		tempDomain = copy.deepcopy(currDomains)
		tempDomain[action[0]] = list(action[1])
		forwardCheck(tempAssigned,tempDomain)
		evalScore = maxValue(depth+1,tempAssigned,tempDomain,tmpPath,alpha,beta,outputFile)
		v = min(v,evalScore)
		if v <= alpha:
			outputFile.write( curPath[len(curPath)-1][0] + ", " + curPath[len(curPath)-1][1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
			return v
		beta = min(beta,v)
		outputFile.write( curPath[len(curPath)-1][0] + ", " + curPath[len(curPath)-1][1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
	return v
		
def maxValue(depth,assigned,currDomains,curPath,alpha,beta,outputFile):
	global maxDepth
	global bestAction
	global bestScore
	lastAction = curPath[len(curPath)-1]
	possibleActions = findPossActions(assigned,currDomains)
	if depth == int(maxDepth) or not possibleActions:
		evalScore = calEvalScore(curPath)
		outputFile.write( lastAction[0] + ", " + lastAction[1] + ", " + str(depth) + ", " + str(evalScore) + ", " + str(alpha) + ", " + str(beta)+"\n")
		return evalScore
	v = float('-inf')
	outputFile.write( lastAction[0] + ", " + lastAction[1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
	
	for action in possibleActions:
		tempAssigned = copy.deepcopy(assigned)
		tempAssigned[action[0]] = action[1]
		tmpPath = copy.deepcopy(curPath)
		tmpPath.append((action[0],action[1]))
		tempDomain = copy.deepcopy(currDomains)
		tempDomain[action[0]] = list(action[1])
		
		forwardCheck(tempAssigned,tempDomain)
		evalScore = minValue(depth+1,tempAssigned,tempDomain,tmpPath,alpha,beta,outputFile)
		if depth == 0 and evalScore > bestScore:
			bestScore = evalScore
			bestAction = tmpPath[len(tmpPath)-1]
		v = max(v,evalScore)		
		if v >= beta:
			outputFile.write( curPath[len(curPath)-1][0] + ", " + curPath[len(curPath)-1][1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
			return v		
		alpha = max(alpha,v)		
		outputFile.write( curPath[len(curPath)-1][0] + ", " + curPath[len(curPath)-1][1] + ", " + str(depth) + ", " + str(v) + ", " + str(alpha) + ", " + str(beta)+"\n")
	return v	


def findPossActions(assigned,currDomains):
	possibleActions = []
	for preAction in assigned:
		for action in graph[preAction]:
			if action not in assigned:
				for color in currDomains[action]:
					if (action,color) not in possibleActions:
						possibleActions.append((action,color))
	return sorted(possibleActions)

def calEvalScore(curPath):
	result = 0
	for index in range(len(curPath)):
		if (index%2) == 0:
			result +=  int(p1PreferList[curPath[index][1]])
		else:
			result -= int(p2PreferList[curPath[index][1]])
	return result

read_file()