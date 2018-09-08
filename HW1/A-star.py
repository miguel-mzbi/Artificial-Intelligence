# A* algorithm for the cannibals-missionaries problem
# For python 2.7

import Queue as Q

right = "Right"
left = "Left"

# Abstraction of priority queue. It lets the insertion of objects with priority.
class MyPriorityQueue(Q.PriorityQueue):
    def __init__(self):
        Q.PriorityQueue.__init__(self)

    def put(self, item, priority):
        Q.PriorityQueue.put(self, (priority, item))

    def get(self):
        _, item = Q.PriorityQueue.get(self)
        return item
    
# State object. Contains values of missionaries and cannibals on each side and boat position.
# It also contains overrides for object manipulation
class State:
    def __init__(self, mLeft, cLeft, mRight, cRight, boat):
        self.mLeft = mLeft
        self.cLeft = cLeft
        self.mRight = mRight
        self.cRight = cRight
        self.boat = boat

    def __cmp__(self, other):
        if(isinstance(other, State)):
            res = cmp(self.mLeft, other.mLeft)\
            and cmp(self.cLeft, other.cLeft)\
            and cmp(self.mRight, other.mRight)\
            and cmp(self.cRight, other.cRight)\
            and cmp(self.boat, other.boat)
            return res
        return -1

    def __eq__(self, other):
        if(isinstance(other, State)):
            return self.mLeft == other.mLeft\
            and self.cLeft == other.cLeft\
            and self.mRight == other.mRight\
            and self.cRight == other.cRight\
            and self.boat == other.boat
        return False

    def __ne__(self, other):
        if(isinstance(other, State)):
            return not self.__eq__(other)
        return False
    
    def __str__(self):
        return "Left: Missionaries=" + str(self.mLeft) + " Cannibals=" + str(self.cLeft) + "\n"\
            + "Right: Missionaries=" + str(self.mRight) + " Cannibals=" + str(self.cRight) + "\n"\
            + "Boat=" + self.boat + "\n"
    
    # To identify as equal two states with different id, but with the same values,
    # we combine the values of the object as strings, and hash that string.
    # This only works when comparing keys inside a dictionary
    def __hash__(self):
        return hash(str(self.mLeft) + str(self.cLeft) + str(self.mRight) + str(self.cRight) + self.boat)

# Heuristic function
def h(state):
    return (state.cLeft + state.mLeft)/2.0

# A* function
def aStar():
    # Definition of initial and goal states
    initialState = State(3,3,0,0,left)
    goal = State(0,0,3,3,right)
    # Priority queue for future node exploring
    queue = MyPriorityQueue()
    queue.put(initialState, 0)
    # Dictionary that stores the best parent for a node
    parent = {}
    parent[initialState] = None
    # Stores the action the parent realized to get to the state
    actionFromParent = {}
    actionFromParent[initialState] = 0
    # Stores the total cost so far until the node
    g = {}
    g[initialState] = 0

    # Explore nodes until queue is empty
    while not queue.empty():
        # Get current node for exporation
        currentNode = queue.get()
        # Print path if the current node is the goal
        if currentNode == goal:
            # Find path that leaded to goal node. Store path in array
            backtrack = []
            backtrack.append((currentNode, actionFromParent[currentNode]))
            while currentNode != initialState:
                backtrack.append((parent[currentNode], actionFromParent[parent[currentNode]]))
                currentNode = parent[currentNode]
            
            # Print states and actions that lead to next state
            print "INITIAL STATE"
            print backtrack[len(backtrack)-1][0]
            for i in range(len(backtrack)-2, -1, -1):
                node, action = backtrack[i]
                if abs(action) == 1:
                    print "Moved 2 missionaries",
                elif abs(action) == 2:
                    print "Moved 1 missionary",
                elif abs(action) == 3:
                    print "Moved 2 cannibals",
                elif abs(action) == 4:
                    print "Moved 1 cannibal",
                elif abs(action) == 5:
                    print "Moved 1 missionary and 1 cannibal",
                if action < 0:
                    print "from right to left\n"
                else:
                    print "from left to right\n"
                if i == 0:
                    print "GOAL STATE"
                print node
            break
        
        # Successor calculation.
        # Negative action type origin from the right. Positive form the left. The number determines the number of
        # entities transported from the side.
        successors = []
        # If boat is currently on the left.
        if currentNode.boat == left:
            # States if missionaries exist
            if currentNode.mLeft >= 2:
                successors.append((State(currentNode.mLeft-2, currentNode.cLeft, currentNode.mRight+2, currentNode.cRight, right), 1))
            if currentNode.mLeft >= 1:
                successors.append((State(currentNode.mLeft-1, currentNode.cLeft, currentNode.mRight+1, currentNode.cRight, right), 2))
            # States if cannibal exist  
            if currentNode.cLeft >= 2:
                successors.append((State(currentNode.mLeft, currentNode.cLeft-2, currentNode.mRight, currentNode.cRight+2, right), 3))
            if currentNode.cLeft >= 1:
                successors.append((State(currentNode.mLeft, currentNode.cLeft-1, currentNode.mRight, currentNode.cRight+1, right), 4))
             # If both sxist
            if currentNode.cLeft >= 1 and currentNode.mLeft >= 1:
                successors.append((State(currentNode.mLeft-1, currentNode.cLeft-1, currentNode.mRight+1, currentNode.cRight+1, right), 5))
        # If boat is currently on the right.
        else:
            # States if missionaries exist
            if currentNode.mRight >= 2:
                successors.append((State(currentNode.mLeft+2, currentNode.cLeft, currentNode.mRight-2, currentNode.cRight, left), -1))
            if currentNode.mRight >= 1:
                successors.append((State(currentNode.mLeft+1, currentNode.cLeft, currentNode.mRight-1, currentNode.cRight, left), -2))
            # States if cannibal exist
            if currentNode.cRight >= 2:
                successors.append((State(currentNode.mLeft, currentNode.cLeft+2, currentNode.mRight, currentNode.cRight-2, left), -3))
            if currentNode.cRight >= 1:
                successors.append((State(currentNode.mLeft, currentNode.cLeft+1, currentNode.mRight, currentNode.cRight-1, left), -4))
            # If both sxist
            if currentNode.cRight >= 1 and currentNode.mRight >= 1:
                successors.append((State(currentNode.mLeft+1, currentNode.cLeft+1, currentNode.mRight-1, currentNode.cRight-1, left), -5))
        
        # Calculate cost for child nodes
        nextCost = g[currentNode] + 1
        # Iterate trought all possible child nodes
        for (next, type) in successors:
            # If next it's an invalid end state, skip it.
            if(next.mRight!= 0 and next.cRight > next.mRight) or (next.mLeft != 0 and next.cLeft > next.mLeft):
                continue
            # If the node hasn't been explored
            # or it has been explored but the path to arrive to that node is cheaper than the stored
            if next not in g or nextCost < g[next]:
                # Store new cost
                g[next] = nextCost
                # Put node in queue for exploring
                queue.put(next, nextCost + h(next))
                # Store new parent
                parent[next] = currentNode
                # Store action that lead parent to node
                actionFromParent[next] = type

def main():
    aStar()
    

if __name__ == '__main__':
    main()