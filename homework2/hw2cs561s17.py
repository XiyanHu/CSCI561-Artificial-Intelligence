import sys
bestAction = None
bestScore = float('-inf')
maxDepth = 0
graph = {}
p1PreferList = {}
p2PreferList = {}
assigned = {}
curPath = []
currDomains = {}
colorList = {}
def read_file():
	global maxDepth
	global graph
	global p1PreferList
	global p2PreferList
	global assigned
	global curPath
	global currDomains
	global colorList
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

	initialforwardCheck(assigned)
	
	alpha = float('-inf')
	beta = float('inf')
	outputFile = open("output.txt","w")
	bestResult = maxValue(0,alpha,beta,outputFile)	
	outputFile.write(bestAction[0]+", "+bestAction[1] +", "+str(bestResult));
	outputFile.close()

def initialforwardCheck(assigned):
	global currDomains
	for node in assigned:
		for neighbor in graph[node]:
			if neighbor not in assigned and len(currDomains[node]) > 0:
				if currDomains[node][0] in currDomains[neighbor]:
					currDomains[neighbor].remove(currDomains[node][0])

def forwardCheck(assigned,action):
	global currDomains
	node = action[0]
	for neighbor in graph[node]:
		if  neighbor not in assigned and len(currDomains[node]) > 0:
			if action[1] in currDomains[neighbor]:
				currDomains[neighbor].remove(action[1])

#Set up initial domains	
def InitializeDomains(colorList,p1Action,p2Action):
	currDomains = { variable: list(colorList) for variable in graph}
	for action in p1Action:
		currDomains[action] = []
		currDomains[action].append(p1Action[action])
	for action in p2Action:
		currDomains[action] = []
		currDomains[action].append(p2Action[action])
	return currDomains

def minValue(depth,alpha,beta,outputFile):
	global maxDepth
	global assigned
	global curPath
	lastAction = curPath[len(curPath)-1]
	possibleActions = findPossActions(assigned)
	if depth == int(maxDepth) or not possibleActions:	
		evalScore = calEvalScore(curPath)
		output = [lastAction[0],', ',lastAction[1],', ',str(depth),', ',str(evalScore),', ',str(alpha),', ',str(beta),'\n']
		outputFile.write(''.join(output))
		return evalScore
	v = float('inf')
	output = [lastAction[0],', ',lastAction[1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
	outputFile.write(''.join(output))
	for action in possibleActions:
		assigned[action[0]] = action[1]		
		curPath.append((action[0],action[1]))
		modifiedDomain = currDomains[action[0]][:]
		forwardCheck(assigned,action)
		evalScore = maxValue(depth+1,alpha,beta,outputFile)
		recoverDomains(action,modifiedDomain)
		del assigned[action[0]]
		del curPath[len(curPath)-1]
		v = min(v,evalScore)
		if v <= alpha:
			output = [curPath[len(curPath)-1][0],', ',curPath[len(curPath)-1][1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
			outputFile.write(''.join(output))
			return v
		beta = min(beta,v)
		output = [curPath[len(curPath)-1][0],', ',curPath[len(curPath)-1][1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
		outputFile.write(''.join(output))
	return v
		
def maxValue(depth,alpha,beta,outputFile):
	global maxDepth
	global bestAction
	global bestScore
	global assigned
	global curPath
	lastAction = curPath[len(curPath)-1]
	possibleActions = findPossActions(assigned)
	if depth == int(maxDepth) or not possibleActions:
		evalScore = calEvalScore(curPath)
		output = [lastAction[0],', ',lastAction[1],', ',str(depth),', ',str(evalScore),', ',str(alpha),', ',str(beta),'\n']
		outputFile.write(''.join(output))
		return evalScore
	v = float('-inf')
	output = [lastAction[0],', ',lastAction[1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
	outputFile.write(''.join(output))
	for action in possibleActions:
		assigned[action[0]] = action[1]
		recordStep = ((action[0],action[1]))
		curPath.append((action[0],action[1]))
		modifiedDomain = currDomains[action[0]][:]
		forwardCheck(assigned,action)
		evalScore = minValue(depth+1,alpha,beta,outputFile)
		recoverDomains(action,modifiedDomain)
		del assigned[action[0]]
		del curPath[len(curPath)-1]		
		if depth == 0 and evalScore > bestScore:
			bestScore = evalScore
			bestAction = recordStep
		v = max(v,evalScore)		
		if v >= beta:
			output = [curPath[len(curPath)-1][0],', ',curPath[len(curPath)-1][1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
			outputFile.write(''.join(output))
			return v		
		alpha = max(alpha,v)		
		output = [curPath[len(curPath)-1][0],', ',curPath[len(curPath)-1][1],', ',str(depth),', ',str(v),', ',str(alpha),', ',str(beta),'\n']
		outputFile.write(''.join(output))
	return v	

def recoverDomains(action,modifiedDomain):
	for neighbor in graph[action[0]]:
		if neighbor not in assigned:
			currDomains[neighbor] = colorList[:]
			for childNeighbor in graph[neighbor]:
				if childNeighbor in assigned and childNeighbor != action[0]:
					if assigned[childNeighbor] in currDomains[neighbor]:
						currDomains[neighbor].remove(assigned[childNeighbor])
	currDomains[action[0]] = modifiedDomain
	return currDomains

def findPossActions(assigned):
	tmpSet = set()
	for preAction in assigned:
		for action in graph[preAction]:
			if action not in assigned:
				for color in currDomains[action]:
					tmpSet.add((action,color))
	possibleActions = list(tmpSet)
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