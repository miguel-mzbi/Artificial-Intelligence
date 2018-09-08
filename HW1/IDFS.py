# Iterative DFS algorithm for the cannibals-missionaries problem
# For python 2.7

right = "Right"
left = "Left"

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
    
def DFS(root, goal, d):
    initialState = State(3,3,0,0,left)
    goal = State(0,0,3,3,right)

    if d <= 0:
        return None

    if root == goal:
        result = [[root, 0]]
        return result

    successors = []
    if root.boat == left:
        if root.mLeft >= 2:
            successors.append((State(root.mLeft-2, root.cLeft, root.mRight+2, root.cRight, right), 1))
        if root.mLeft >= 1:
            successors.append((State(root.mLeft-1, root.cLeft, root.mRight+1, root.cRight, right), 2))

        if root.cLeft >= 2:
            successors.append((State(root.mLeft, root.cLeft-2, root.mRight, root.cRight+2, right), 3))
        if root.cLeft >= 1:
            successors.append((State(root.mLeft, root.cLeft-1, root.mRight, root.cRight+1, right), 4))
        
        if root.cLeft >= 1 and root.mLeft >= 1:
            successors.append((State(root.mLeft-1, root.cLeft-1, root.mRight+1, root.cRight+1, right), 5))
    else:
        if root.mRight >= 2:
            successors.append((State(root.mLeft+2, root.cLeft, root.mRight-2, root.cRight, left), -1))
        if root.mRight >= 1:
            successors.append((State(root.mLeft+1, root.cLeft, root.mRight-1, root.cRight, left), -2))
        
        if root.cRight >= 2:
            successors.append((State(root.mLeft, root.cLeft+2, root.mRight, root.cRight-2, left), -3))
        if root.cRight >= 1:
            successors.append((State(root.mLeft, root.cLeft+1, root.mRight, root.cRight-1, left), -4))
        
        if root.cRight >= 1 and root.mRight >= 1:
            successors.append((State(root.mLeft+1, root.cLeft+1, root.mRight-1, root.cRight-1, left), -5))
    
    for (next, type) in successors:
        if(next.mRight!= 0 and next.cRight > next.mRight) or (next.mLeft != 0 and next.cLeft > next.mLeft):
            continue
        
        result = DFS(next, goal, d-1)
        if result != None:     
            result.append([root, type])
            return result

    return None


def IDFS(max):
    initialState = State(3,3,0,0,left)
    goal = State(0,0,3,3,right)
    for i in range(1, max+1):
        result = DFS(initialState, goal, i)
        if(result != None):
            print "INITIAL STATE"
            for i in range(len(result)-1, 0, -1):
                node, action = result[i]
                print node
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
            print "GOAL STATE"
            print result[0][0]
            break



def main():
    IDFS(50)
    

if __name__ == '__main__':
    main()