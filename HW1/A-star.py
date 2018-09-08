# A* algorithm for the cannibals-missionaries problem
# For python 2.7

import Queue as Q

right = "Right"
left = "Left"

class MyPriorityQueue(Q.PriorityQueue):
    def __init__(self):
        Q.PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        Q.PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = Q.PriorityQueue.get(self, *args, **kwargs)
        return item

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
    
    # def __cmp__(self, other):
    #     return cmp(self.priority, other.priority)
    
    def __str__(self):
        return "Left: Missionaries=" + str(self.mLeft) + " Cannibals=" + str(self.cLeft) + "\n"\
            + "Right: Missionaries=" + str(self.mRight) + " Cannibals=" + str(self.cRight) + "\n"\
            + "Boat=" + self.boat + "\n"
        # return str(hash(str(self.mLeft) + str(self.cLeft) + str(self.mRight) + str(self.cRight) + self.boat))

    def __hash__(self):
        # print(str(self.mLeft) + str(self.cLeft) + str(self.mRight) + str(self.cRight) + self.boat)
        # print(hash(str(self.mLeft) + str(self.cLeft) + str(self.mRight) + str(self.cRight) + self.boat))
        return hash(str(self.mLeft) + str(self.cLeft) + str(self.mRight) + str(self.cRight) + self.boat)

# def sameState(stateA, stateB):
#     return stateA.mLeft == stateB.mLeft\
#         and stateA.cLeft == stateB.cRight\
#         and stateA.mRight == stateB.mRight\
#         and stateA.cRight == stateB.cRight\
#         and stateA.boat == stateB.boat

def h(state):
    return (state.cLeft + state.mLeft)/2.0
    
def aStar():
    initialState = State(3,3,0,0,left)
    goal = State(0,0,3,3,right)

    queue = MyPriorityQueue()
    queue.put(initialState, 0)

    parent = {}
    parent[initialState] = None
    actionFromParent = {}
    actionFromParent[initialState] = 0
    g = {}
    g[initialState] = 0
    
    # currentNode = queue.get()
    # if currentNode == goal:
    #     print "GOAL"
    # input()

    while not queue.empty():
        currentNode = queue.get()

        if currentNode == goal:
            backtrack = []
            backtrack.append((currentNode, actionFromParent[currentNode]))
            while currentNode != initialState:
                backtrack.append((parent[currentNode], actionFromParent[parent[currentNode]]))
                currentNode = parent[currentNode]
            
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
        # print parent[currentNode]
        # print currentNode
        
        successors = []
        if currentNode.boat == left:
            if currentNode.mLeft >= 2:
                successors.append((State(currentNode.mLeft-2, currentNode.cLeft, currentNode.mRight+2, currentNode.cRight, right), 1))
            if currentNode.mLeft >= 1:
                successors.append((State(currentNode.mLeft-1, currentNode.cLeft, currentNode.mRight+1, currentNode.cRight, right), 2))

            if currentNode.cLeft >= 2:
                successors.append((State(currentNode.mLeft, currentNode.cLeft-2, currentNode.mRight, currentNode.cRight+2, right), 3))
            if currentNode.cLeft >= 1:
                successors.append((State(currentNode.mLeft, currentNode.cLeft-1, currentNode.mRight, currentNode.cRight+1, right), 4))
            
            if currentNode.cLeft >= 1 and currentNode.mLeft >= 1:
                successors.append((State(currentNode.mLeft-1, currentNode.cLeft-1, currentNode.mRight+1, currentNode.cRight+1, right), 5))
        else:
            if currentNode.mRight >= 2:
                successors.append((State(currentNode.mLeft+2, currentNode.cLeft, currentNode.mRight-2, currentNode.cRight, left), -1))
            if currentNode.mRight >= 1:
                successors.append((State(currentNode.mLeft+1, currentNode.cLeft, currentNode.mRight-1, currentNode.cRight, left), -2))
            
            if currentNode.cRight >= 2:
                successors.append((State(currentNode.mLeft, currentNode.cLeft+2, currentNode.mRight, currentNode.cRight-2, left), -3))
            if currentNode.cRight >= 1:
                successors.append((State(currentNode.mLeft, currentNode.cLeft+1, currentNode.mRight, currentNode.cRight-1, left), -4))
            
            if currentNode.cRight >= 1 and currentNode.mRight >= 1:
                successors.append((State(currentNode.mLeft+1, currentNode.cLeft+1, currentNode.mRight-1, currentNode.cRight-1, left), -5))
        
        nextCost = g[currentNode] + 1

        for (next, type) in successors:
            if(next.mRight!= 0 and next.cRight > next.mRight) or (next.mLeft != 0 and next.cLeft > next.mLeft):
                continue
            if next not in g or nextCost < g[next]:
                # if next in g:
                #     print nextCost, "vs", g[next]
                # if next not in g:
                #     print next
                g[next] = nextCost
                queue.put(next, nextCost + h(next))
                parent[next] = currentNode
                actionFromParent[next] = type

        # i = raw_input()

def main():
    aStar()
    

if __name__ == '__main__':
    main()