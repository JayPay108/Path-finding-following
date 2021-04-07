import pygame
import math

UNVISITED = 1
OPEN = 2
CLOSED = 3

class Node:
    def __init__(self, nodeNumber, costSoFar, estimatedHeuristic, estimatedTotal, previous, xLocation, yLocation):
        self.nodeNumber = nodeNumber
        self.costSoFar = costSoFar
        self.estimatedHeuristic = estimatedHeuristic
        self.estimatedTotal = estimatedTotal
        self.previous = previous
        self.xLocation = xLocation
        self.yLocation = yLocation

        self.status = 0
        self.wall = False
        self.first = False
        self.last = False

    # Calculating distance between two nodes using standard Euclidean distance formula
    def distanceFrom(self, node2):
        x1 = self.xLocation
        y1 = self.yLocation
        x2 = node2.xLocation
        y2 = node2.yLocation

        # Formula for calculating Euclidian Distance
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    def draw(self, screen, noPath = False):
        if self.first or self.last:
            if noPath:
                color = (200, 0, 0)
            else:
                color = (224, 231, 34)
        elif self.wall:
            color = (100, 100, 100)
        elif self.status == OPEN:
            color = (144, 238, 144)
        elif self.status == CLOSED:
            color = (0,200,200)
        else:
            color = (218, 218, 218)

        pygame.draw.rect(screen, color, (self.xLocation, self.yLocation, 28, 28))

    def makeWall(self, wall, screen):
        if not self.first and not self.last:
            self.wall = wall

        self.draw(screen)
        pygame.display.update()