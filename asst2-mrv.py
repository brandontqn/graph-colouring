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

# Helper function to find the colour of some target node in our solution
def getCol(target, solution):
    for node in solution:
        if(node[0] == target): # the node label equal target
            return node[1] # the colour of node
    return False # node hasn't yet been added to the solution, i.e not coloured yet

# Helper function to find an eligible colour assignment for some target node
def selectUnassignedColour(target, solution, k, G):
    colours = [i for i in range(1,k+1)] # make a list of colours 1..k
    for neighbour in G[target-1][1:]: # neighbours are adjacent nodes of target, target-1 because we start indicies at 0 but nodes start at 1
        col = getCol(neighbour, solution) # get the colour of current neighbour
        if(col): # colour is found, i.e. this node has already been added to our solution
            if(col in colours): # only remove col from colours if it hasn't already been removed
                colours.remove(col) # remove this colour from our list of potential assignments, as it is not eligible given our CSP
    if(colours != []): # if our list of potential assignments is not empty, return the first available assignment
        return colours[0] # *** CANDIDATE LINE TO IMPLEMENT LEAST CONSTRAINING VALUE
    return False # no available assignments, return False

def getMoves(target, solution, k, G):
    colours = [i for i in range(1,k+1)] # make a list of colours 1..k
    for neighbour in G[target[0]-1][1:]: # neighbours are adjacent nodes of target, target-1 because we start indicies at 0 but nodes start at 1
        col = getCol(neighbour, solution) # get the colour of current neighbour
        if(col): # colour is found, i.e. this node has already been added to our solution
            if(col in colours): # only remove col from colours if it hasn't already been removed
                colours.remove(col) # remove this colour from our list of potential assignments, as it is not eligible given our CSP
    return len(colours)

def mrv(solution, k, G):
    legalMoves = []
    solutionNodes = [x[0] for x in solution]
    for node in G:
        if(not(node[0] in solutionNodes)):
            legalMoves.append((getMoves(node, solution, k, G), node[0]))
    if(legalMoves != []):
        return min(legalMoves)
    return False

# Recursive backtracking search algorithm to find and return a solution(colouring), or False if no colouring is possible
def recursiveBacktrackSearch(solution, n, k, G):
    if(len(solution) == n): # the length of our solution is equal to number of vertices, all nodes have been coloured, return solution
        return solution # solution is a list of tuples representing [(node, colour), ...]
    node = mrv(solution, k, G)[1]
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
