import time
n = 10 # Number of vertices
k = 4 # Number of colours
G = [[1, 2, 3, 4, 6, 7, 10],
        [2, 1, 3, 4, 5, 6],
        [3, 1, 2],
        [4, 1, 2],
        [5, 2, 6],
        [6, 1, 2, 5, 7, 8],
        [7, 1, 6, 8, 9, 10],
        [8, 6, 7, 9],
        [9, 7, 8, 10],
        [10, 1, 7, 9]] # ADJACENCY LIST for a graph

### Set of functions needed for MRV
# Helper function to find the colour of some target node in our solution
def getCol(target, solution):
    for node in solution:
        if(node[0] == target): # the node label equal target
            return node[1] # the colour of node
    return False # node hasn't yet been added to the solution, i.e not coloured yet

def getMoves(target, solution, k, G):
    colours = [i for i in range(1,k+1)] # make a list of colours 1..k
    for neighbour in G[target-1][1:]: # neighbours are adjacent nodes of target, target-1 because we start indicies at 0 but nodes start at 1
        col = getCol(neighbour, solution) # get the colour of current neighbour
        if(col): # colour is found, i.e. this node has already been added to our solution
            if(col in colours): # only remove col from colours if it hasn't already been removed
                colours.remove(col) # remove this colour from our list of potential assignments, as it is not eligible given our CSP
    return colours # return a list of ints, representing legal colours we may want to assign

### Set of functions needed for DH
# Helper function to find the number of unassigned variables neighbouring a target node
def getDeg(target, solution, k, G):
    deg = len(G[target[1]-1])-1 # start with the number of neighbours to target node
    neighbours = [x[0] for x in solution] # a list of nodes (only the nodes, not colours) already written into our solution
    for neighbour in G[target[1]-1][1:]:  # iterate through neighbours of our target node
        if(neighbour in neighbours): # cross-check current neighbour node with our solutions nodes
            deg = deg - 1 # subtract one from degree for every neighbour that is in our solution, aka finding the number of unassigned neighbours
    return deg # return an integer, representing the number of unassigned nodes adjacent to target node

# Helper function to find the least constraining value, i.e. the colour that allows for the most variation among remaining variables
def lcv(target, colours, solution, k, G):
    constraintsList = [] # a list that will hold the sum of possible colourings for remaining variables, given a colouring
    solutionNodes = [x[0] for x in solution] # a list of nodes (as integers) from our solution, we will use this to cross-check values
    for col in colours: # assign each colour to target node to check which colour gives the most possible future colourings, i.e. least constraint value
        numCols = 0 # a sum that represents total possible colourings for neighbouring nodes, given a colour
        solution.append((target, col)) # temporarily assign target node with current colour to our solution
        for neighbour in G[target-1][1:]: # for every neighbour to our current node
            if(not(neighbour in solutionNodes)): # if neighbour hasn't been assigned a colour yet
                cols = len(getMoves(neighbour, solution, k, G)) # add its possible colourings to our sum
                numCols = numCols + cols
        constraintsList.append((numCols, col)) # add this sum to our list of sums for each colour
        solution.remove((target, col)) # remove target node from our solution
    return max(constraintsList)[1] # return the colour with the most possible colourings for neighbouring nodes, i.e. the LCV

# Helper function to find an eligible colour assignment for some target node
def selectUnassignedColour(target, solution, k, G):
    colours = [i for i in range(1,k+1)] # make a list of colours 1..k
    for neighbour in G[target-1][1:]: # neighbours are adjacent nodes of target, target-1 because we start indicies at 0 but nodes start at 1
        col = getCol(neighbour, solution) # get the colour of current neighbour
        if(col): # colour is found, i.e. this node has already been added to our solution
            if(col in colours): # only remove col from colours if it hasn't already been removed
                colours.remove(col) # remove this colour from our list of potential assignments, as it is not eligible given our CSP
    if(colours != []): # if our list of potential assignments is not empty, return the first available assignment
        return lcv(target, colours, solution, k, G)
    return False # no available assignments, return False

# Minimum Remaining Value heuristic, chooses the node with the fewest available legal moves
def mrv(solution, k, G):
    legalMoves = [] # list to accumulate legal moves for every node not yet in solution
    degList = [] # list to accumulate degrees for nodes in our set of legal moves
    solutionNodes = [x[0] for x in solution] # extract node number from solution, separate from colour
    for node in G:
        if(not(node[0] in solutionNodes)): # if node isn't in our solution then we append (legal_moves, node) to our legalMoves set
            moves = getMoves(node[0], solution, k, G)
            legalMoves.append((len(moves), node[0]))
    if(legalMoves != []): # check if there are nodes with legal moves
        minMoves = min(legalMoves)[0]
        for node in legalMoves:
            if(node[0] == minMoves):
                degList.append(node)
        if(len(degList) > 1):
            return dh(degList, solution, k, G)
        return min(legalMoves)
    return False

# Handles tie-breakers between nodes with same number of legal moves, picks the node with most constraints on unassigned nodes
def dh(potentialVariables, solution, k, G):
    degList = [] # a list representing the number of constraints each variable in our potentialVariables has on unassigned variables
    for node in potentialVariables:
        deg = getDeg(node, solution, k, G)
        degList.append((deg, node))
    return max(degList)[1] # return the variable with highest constraints on unassigned variables

# Recursive backtracking search algorithm to find and return a solution(colouring), or False if no colouring is possible
def recursiveBacktrackSearch(solution, n, k, G):
    if(len(solution) == n): # the length of our solution is equal to number of vertices, all nodes have been coloured, return solution
        return solution # solution is a list of tuples representing [(node, colour), ...]
    node = mrv(solution, k, G)[1] # choose next node to colour using MRV heuristic, use second argument to access node itself
    # print(node)
    col = selectUnassignedColour(node, solution, k, G) # find acceptable colour assignment for node
    if(col): # there are available, acceptable assignments
        solution.append((node, col)) # append (node, col) to our solution
        result = recursiveBacktrackSearch(solution, n, k, G) # recursively call our backtracking algorithm
        if(result != []): # moving ahead does not result in failure
            return result
        solution.remove((node, col)) # moving ahead results in failure, remove current node+colour from solution *****
    return [] # return empty list because of no acceptable colour assignment

# implement basic backtracking search along with the MRV, degree, and least constraining value heuristic
def solve(n, k, G):
    return recursiveBacktrackSearch([], n, k, G)

start_time = time.time()
solution = solve(n,k,G)
print("--- %s seconds ---" % (time.time() - start_time))
print(solution)
