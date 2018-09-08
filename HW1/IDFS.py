# Iterative DFS algorithm for the cannibals-missionaries problem
# For python 2.7

right = "Right"
left = "Left"

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

# DFS recursive function. It takes the current node (root), the goal, and the current depth
def DFS(root, goal, d):

    # If the depth has reached 0, this node shouldn't be explored. It will in the next iteration.
    if d <= 0:
        return None
    # If the current node is the goal, return an array with an array containing the object.
    # The second number is not important here. Its the action that the node does towards the goal.
    if root == goal:
        result = [[root, 0]]
        return result

    # Successor calculation.
    # Negative action type origin from the right. Positive form the left. The number determines the number of
    # entities transported from the side.
    successors = []
    # If boat is currently on the left.
    if root.boat == left:
        # States if missionaries exist
        if root.mLeft >= 2:
            successors.append((State(root.mLeft-2, root.cLeft, root.mRight+2, root.cRight, right), 1))
        if root.mLeft >= 1:
            successors.append((State(root.mLeft-1, root.cLeft, root.mRight+1, root.cRight, right), 2))
        # States if cannibal exist
        if root.cLeft >= 2:
            successors.append((State(root.mLeft, root.cLeft-2, root.mRight, root.cRight+2, right), 3))
        if root.cLeft >= 1:
            successors.append((State(root.mLeft, root.cLeft-1, root.mRight, root.cRight+1, right), 4))
        # If both sxist
        if root.cLeft >= 1 and root.mLeft >= 1:
            successors.append((State(root.mLeft-1, root.cLeft-1, root.mRight+1, root.cRight+1, right), 5))
    # If boat is currently on the right.
    else:
        # States if missionaries exist
        if root.mRight >= 2:
            successors.append((State(root.mLeft+2, root.cLeft, root.mRight-2, root.cRight, left), -1))
        if root.mRight >= 1:
            successors.append((State(root.mLeft+1, root.cLeft, root.mRight-1, root.cRight, left), -2))
        # States if cannibal exist
        if root.cRight >= 2:
            successors.append((State(root.mLeft, root.cLeft+2, root.mRight, root.cRight-2, left), -3))
        if root.cRight >= 1:
            successors.append((State(root.mLeft, root.cLeft+1, root.mRight, root.cRight-1, left), -4))
        # If both sxist
        if root.cRight >= 1 and root.mRight >= 1:
            successors.append((State(root.mLeft+1, root.cLeft+1, root.mRight-1, root.cRight-1, left), -5))
    
    # Iterate trough all possible successor states
    for (next, type) in successors:
        # If next it's an invalid end state, skip it.
        if(next.mRight!= 0 and next.cRight > next.mRight) or (next.mLeft != 0 and next.cLeft > next.mLeft):
            continue
        # Recurse trough the next node
        result = DFS(next, goal, d-1)
        # If the recursion returns something, it means the goal node was found.
        # Appends the node to the data, with the action type to arrive to the next node in the path.
        if result != None:     
            result.append([root, type])
            return result

    return None

# Iterative DFS
def IDFS(max):
    # Definition of initial and goal states
    initialState = State(3,3,0,0,left)
    goal = State(0,0,3,3,right)
    # Incremental depth max
    for i in range(1, max+1):
        result = DFS(initialState, goal, i)
        # If current iteration return something, goal node was found.
        if(result != None):
            # Print array of states and actions
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