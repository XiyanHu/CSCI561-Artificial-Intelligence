import sys
import Queue
import copy

#Function to solve the problem
def solve():
	#Deal with the input file
	inputFile = open(sys.argv[2],'r')
	lines = inputFile.readlines()
	algorithm = lines[0].strip()
	initialFuel = lines[1].strip()
	startNode = lines[2].strip()
	goalNode = lines[3].strip()

	pathDict = {}
	reversePathDict = {}

	#Store map data
	for index in range(4,len(lines)):
		reBlank = lines[index].strip().replace(' ','')
		nodeName = reBlank.split(":")[0]
		pathList = reBlank.split(":")[1].split(",")
		singleDict = {}
		for path in pathList:			
			singleDict[path.split("-")[0]] = path.split("-")[1]
		pathDict[nodeName] = sorted(singleDict.iteritems())
		#reversePathDict[nodeName] = sorted(singleDict.iteritems(),reverse=True)	

	if algorithm == "BFS":	
		output = BFS(initialFuel,startNode,goalNode,pathDict)
	elif algorithm == "DFS":
		output = DFS(initialFuel,startNode,goalNode,pathDict)
	elif algorithm == "UCS":
		output = UCS(initialFuel,startNode,goalNode,pathDict)

		
	if output == "No Path":
		outputStr = "No Path"
	else:
		outputStr = output[0] + " " + str(output[1])
	
	#Output the result 
	outputFile = open("output.txt","w")
	outputFile.write(outputStr);
	outputFile.close()


#BFS algorithm function	
def BFS(initialFuel,startNode,goalNode,pathDict):	
	res = []
	iniFuel = int(initialFuel)
	if startNode == goalNode:
		res.append((startNode,iniFuel))
		return res[0]
	frontier = Queue.Queue()
	visited = set()
	frontier.put((startNode,startNode+"-",iniFuel))
	
	while not frontier.empty():
		nodeTuple = frontier.get()
		node = nodeTuple[0]
		route = nodeTuple[1]
		leftFuel = nodeTuple[2]
		visited.add(node)
		for i in range(len(pathDict.get(node))):
			child = pathDict.get(node)[i][0]
			usedFuel = int(pathDict.get(node)[i][1])
			if child not in visited and (leftFuel - usedFuel) >= 0:
				if child == goalNode:
					res.append((route + child,leftFuel - usedFuel));
				if len(res) == 1:
					return res[0]
				visited.add(child)
				frontier.put((child,route + child + "-",leftFuel - usedFuel))
	return "No Path"

#DFS algorithm function
def DFS(initialFuel,startNode,goalNode,pathDict):
	res = []
	iniFuel = int(initialFuel)
	if startNode == goalNode:
		res.append((startNode,iniFuel))
		return res[0]
	frontier = []
	visited = set()
	visited.add(startNode)
	frontier.append((startNode,startNode +"-",iniFuel,visited))
	
	while frontier:
		isAvailable,isFound = checkAvailable(frontier,pathDict,goalNode,res)
		if not isAvailable:
			nodeTuple = frontier.pop()
			if not frontier and not res:
				return "No Path"
				break
			elif res:
				return res[0]
			node = nodeTuple[0]
			preNodeTuple = frontier[len(frontier) - 1]
			preNodeTuple[3].add(node)
		if isFound:
			break
	return res[0]

#Function used to check whether there is any child node available for a certain node
def checkAvailable(frontier,pathDict,goalNode,res):
	nodeTuple = frontier[len(frontier) - 1]
	node = nodeTuple[0]
	route = nodeTuple[1]
	leftFuel = nodeTuple[2]
	curVisited = nodeTuple[3]
	for i in range(len(pathDict.get(node))):
		child = pathDict.get(node)[i][0]
	 	usedFuel = int(pathDict.get(node)[i][1])
		if child not in curVisited and (leftFuel - usedFuel) >= 0:
			if child == goalNode:
				res.append((route + child, leftFuel - usedFuel))
				return False,True
			tmpVisited = copy.deepcopy(curVisited)
			tmpVisited.add(child)	
	 	 	frontier.append((child,route + child + "-",leftFuel - usedFuel,tmpVisited))
			return True,False
	return False,False

#UCS algorithm funciton
def UCS(initialFuel,startNode,goalNode,pathDict):
	res = []
	firstPath = ();
	iniFuel = int(initialFuel)

	if startNode == goalNode:
		res.append((startNode,iniFuel))
		return res[0]
	frontier = Queue.PriorityQueue() 
	frontier.put((0,startNode,0,startNode,iniFuel))
	visited = set()
	while not frontier.empty():
		nodeTuple = frontier.get()
		curCost = nodeTuple[0]
		node = nodeTuple[1]
		order = nodeTuple[2]
		route = nodeTuple[3]
		leftFuel = nodeTuple[4]
		if node == goalNode:
			res.append((route,leftFuel));
			return res[0]
		visited.add(node)
		for i in range(len(pathDict.get(node))):
			child = pathDict.get(node)[i][0]
			usedFuel = int(pathDict.get(node)[i][1])
			if child not in visited and (leftFuel - usedFuel) >= 0:
				size = frontier.qsize()
				oldOrder = -1
				for i in range(size):
					if child == frontier.queue[i][1]:
						oldOrder = frontier.queue[i][2]
				if oldOrder >= 0:
					frontier.put((usedFuel + curCost,child,oldOrder+1,route + "-" + child ,leftFuel - usedFuel))
				else:
					frontier.put((usedFuel + curCost,child,0,route + "-" + child ,leftFuel - usedFuel))
	return "No Path" 

solve()
