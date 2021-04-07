from Path import Path
from Node import *
import time

SLEEPTIME = 0

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

        self.first = ((self.rows // 2) * self.cols) + 3
        self.last = (((self.rows // 2) + 1) * (self.cols)) - 4

        self.nodes[self.first].first = True
        self.nodes[self.last].last = True   

    def getConnections(self, currentNodeNumber):
        currentRow = currentNodeNumber // self.cols
        currentCol = currentNodeNumber % self.rows

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

            time.sleep(SLEEPTIME)

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