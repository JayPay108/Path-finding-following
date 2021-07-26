from Path import Path
from Node import *
import time
import random

PATHFINDINGSLEEPTIME = 0.01 # Slow down pathfinding representation
MAZEGENERATIONSLEEPTIME = 0.02 # Slow down maze generation

class Graph:
    def __init__(self, size):
        self.rows = size[1]
        self.cols = size[0]

        nodeNumber = 0
        self.nodes = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.nodes.append(Node(nodeNumber, 0, 0, 0, 0, (col * 30) + 1, (row * 30) + 1))
                nodeNumber += 1

        # Start and finish node locations
        # self.first = ((self.rows // 2) * self.cols) + 3
        # self.last = (((self.rows // 2) + 1) * (self.cols)) - 4
        self.first = 0
        self.last = (self.rows * self.cols) - 1

        self.nodes[self.first].first = True
        self.nodes[self.last].last = True   

    def getConnections(self, currentNodeNumber):
        currentRow = currentNodeNumber // self.cols
        currentCol = currentNodeNumber % self.cols

        connections = []
        
        for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            newRow = currentRow + direction[0]
            newCol = currentCol + direction[1]
            newNodeNumber = (newRow * self.cols) + newCol
            
            if newRow in range(self.rows) and newCol in range(self.cols):
                if not self.nodes[newNodeNumber].wall:
                    connections.append(newNodeNumber)

        return connections

    def findLowest(self, openNodes):
        lowestTotal = float('inf')

        for nodeIndex in openNodes:
            node = self.nodes[nodeIndex]

            if node.estimatedTotal < lowestTotal:
                lowestTotal = node.estimatedTotal
                resultNodeIndex = nodeIndex

        return resultNodeIndex


    def findPath(self, screen):
        for i in range(len(self.nodes)):
            self.nodes[i].status = UNVISITED
            self.nodes[i].previous = None
            self.nodes[i].costSoFar = float('inf')

        self.nodes[self.first].status = OPEN
        self.nodes[self.first].costSoFar = 0
        openNodes = [self.first]

        self.nodes[self.first].draw(screen)
        pygame.display.update()

        while len(openNodes) > 0:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            time.sleep(PATHFINDINGSLEEPTIME)

            currentNodeNumber = self.findLowest(openNodes)

            if currentNodeNumber == self.last:
                break

            currentConnections = self.getConnections(currentNodeNumber)

            for toNodeNumber in currentConnections:
                toCost = self.nodes[currentNodeNumber].costSoFar + 1

                if toCost < self.nodes[toNodeNumber].costSoFar:
                    self.nodes[toNodeNumber].status = OPEN
                    self.nodes[toNodeNumber].costSoFar = toCost
                    self.nodes[toNodeNumber].estimatedHeuristic = self.nodes[toNodeNumber].distanceFrom(self.nodes[self.last])
                    self.nodes[toNodeNumber].estimatedTotal = self.nodes[toNodeNumber].costSoFar + self.nodes[toNodeNumber].estimatedHeuristic
                    self.nodes[toNodeNumber].previous = currentNodeNumber
                    self.nodes[toNodeNumber].draw(screen)
                    
                    if toNodeNumber not in openNodes:
                        openNodes.append(toNodeNumber)
                        pygame.display.update()
            
            
            self.nodes[currentNodeNumber].status = CLOSED
            openNodes.remove(currentNodeNumber)
            self.nodes[currentNodeNumber].draw(screen)
            pygame.display.update()


    def retrievePath(self):
        x = []
        y = []

        current = self.last
        while (current != self.first) and (current != None):
            x.append(self.nodes[current].xLocation)
            y.append(self.nodes[current].yLocation)

            current = self.nodes[current].previous

        if current == self.first:
            x.append(self.nodes[current].xLocation)
            y.append(self.nodes[current].yLocation)

            path = Path(x[::-1], y[::-1])
        else:
            path = None

        return path

    def draw(self, screen):
        screen.fill((128, 128, 128))
        
        for node in self.nodes:
            node.draw(screen)
        pygame.display.update()

    def getSelected(self, pos):
        for row in range(self.rows):
            for col in range(self.cols):
                nodeNumber = (row * self.cols) + col

                nodeBox = pygame.Rect(self.nodes[nodeNumber].xLocation - 1, self.nodes[nodeNumber].yLocation - 1, 30, 30)

                if nodeBox.collidepoint(pos):
                    return nodeNumber        

        return None

    def generateMaze(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                nodeNumber = (row * self.cols) + col

                self.nodes[nodeNumber].wall = True
                self.nodes[nodeNumber].inMaze = False
                self.nodes[nodeNumber].directions = {'U': False, 'D': False, 'L': False, 'R': False}

        locations = [self.last]
        self.nodes[self.last].inMaze = True

        self.nodes[self.last].wall = False

        self.draw(screen) # Updating entire graph

        while locations != []:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            current = locations[-1]

            next = self.makeMazeConnection(current, screen)
            if next != None and next != self.first:
                locations.append(next)
                
                time.sleep(MAZEGENERATIONSLEEPTIME)
            else:
                del locations[-1]

        if self.rows % 2 == 0 and self.cols % 2 == 0:
            self.nodes[1].wall = False
            self.nodes[1].draw(screen)
            pygame.display.update()
    
    def makeMazeConnection(self, nodeNumber, screen):
        neighbors = [('U', -self.cols), ('D', self.cols), ('L', -1), ('R', 1)]
        random.shuffle(neighbors)

        for neighbor in neighbors:
            newNodeNumber = nodeNumber + (2 * neighbor[1])

            direction = neighbor[0]
            if direction == 'D':
                fromDirection = 'U'
            elif direction == 'U':
                fromDirection = 'D'
            elif direction == 'L':
                fromDirection = 'R'
            else:
                fromDirection = 'L'

            currentRow = nodeNumber // self.cols
            newRow = newNodeNumber // self.cols
            if direction == 'L' or direction == 'R':
                if currentRow != newRow:
                    continue

            if newNodeNumber in range(len(self.nodes)) and not self.nodes[newNodeNumber].inMaze:
                self.nodes[nodeNumber].directions[direction] = True
                self.nodes[nodeNumber].inMaze = True
                self.nodes[nodeNumber].draw(screen)

                self.nodes[nodeNumber + neighbor[1]].wall = False
                self.nodes[nodeNumber + neighbor[1]].draw(screen)

                self.nodes[newNodeNumber].directions[fromDirection] = True
                self.nodes[newNodeNumber].inMaze = True
                self.nodes[newNodeNumber].wall = False
                self.nodes[newNodeNumber].draw(screen)

                pygame.display.update() # Updating newly drawn nodes

                return newNodeNumber

        return None

