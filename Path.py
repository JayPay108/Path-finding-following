from Vector import Vector
import math

# Takes two position coordinates as input in the form of vectors
# Returns the total distance between the two coordinates
def distanceBetweenPoints(pos1, pos2):
    return math.sqrt(math.pow(pos2.x - pos1.x, 2) + math.pow(pos2.y - pos1.y, 2))

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns the distance from the point to the line
def distanceToLine(point, lineStart, lineEnd): 
    numerator = abs(((lineEnd.x - lineStart.x) * (lineStart.y - point.y)) - ((lineStart.x - point.x) * (lineEnd.y - lineStart.y)))
    denominator = math.sqrt(math.pow(lineEnd.x - lineStart.x, 2) + math.pow(lineEnd.y - lineStart.y))

    return numerator / denominator

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns coordinates to a position (in the form of a vector) on the line that is closest to the given point
def closestPointOnLine(point, lineStart, lineEnd):
    T = (point - lineStart).dot(lineEnd - lineStart) / (lineEnd - lineStart).dot(lineEnd - lineStart)

    return (lineStart + ((lineEnd - lineStart) * T))

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns coordinates to a position (in the form of a vector) on the line segment (between the two ends) that is closest to the given point
def closestPointOnSegment(point, lineStart, lineEnd):
    T = (point - lineStart).dot(lineEnd - lineStart) / (lineEnd - lineStart).dot(lineEnd - lineStart)

    if T <= 0: 
        return lineStart
    elif T >= 1:
        return lineEnd
    else:
        return (lineStart + ((lineEnd - lineStart) * T))

class Path:
    # Constructor takes the path ID, a list of all X coordinates, and a list of all Y coordinates as input
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.segments = len(x) - 1  # Path segments will always be the amount of nodes - 1
        self.distance = [0] * (self.segments + 1)   # Initializing distance to be an array of 0s (with length equal to the amount of nodes)

        # Setting distance to be correct values
        for i in range(1, self.segments + 1):
            distanceFromLastNode = distanceBetweenPoints(Vector(x[i - 1], y[i - 1]), Vector(x[i], y[i]))
            # Total distance travelled at any node is the total distance travelled from the last node plus the distance from the last node
            self.distance[i] = self.distance[i - 1] + distanceFromLastNode

        # The entire distance for the path will always be equal to the stored total distance of the last node in the path
        entirePathDistance = self.distance[-1]

        self.param = [0] * (self.segments + 1) # Initializing param to be an array of 0s (with length equal to the amount of nodes)
        for i in range(1, self.segments + 1):
            # param will be equal to the current distance travelled at any given node divided by the entire path distance
            self.param[i] = self.distance[i] / entirePathDistance
        
    # Given a normalized path paramater, getPosition will return the position coordinates on the path for that parameter
    def getPosition(self, param):
        # Finding the last node travelled to get to the given paramater
        for i in range(self.segments + 1):
            if param > self.param[i]:
                pointIndex = i                
            else:
                break
        
        # Defining the last and next nodes for the given parameter
        lineStart = Vector(self.x[pointIndex], self.y[pointIndex])
        lineEnd = Vector(self.x[pointIndex + 1], self.y[pointIndex + 1])

        # Calulating the position of the parameter
        T = (param - self.param[pointIndex]) / (self.param[pointIndex + 1] - self.param[pointIndex])
        return (lineStart + ((lineEnd - lineStart) * T))

    # Given a position somewhere on the graph (on or off the path), getParam will return the normalized parameter value closest to the given position
    def getParam(self, position):
        closestDistance = float('inf')  # Initializing the closest distance to infinity so it will immediately get overwritten

        for i in range(self.segments):  # Looping through all segments on path
            # Two ending nodes to current segment
            lineStart = Vector(self.x[i], self.y[i])
            lineEnd = Vector(self.x[i + 1], self.y[i + 1])

            checkPoint = closestPointOnSegment(position, lineStart, lineEnd)    # Getting the closest point on the current segment to the given position
            checkDistance = distanceBetweenPoints(position, checkPoint) # Getting the distance between the calculated closest point and the position

            if checkDistance < closestDistance: # If the last distance calculated was less than the previously lowest distance, overwrite the closest position and distance
                closestPoint = checkPoint
                closestDistance = checkDistance
                closestSegment = i

        # Setting up node variables to preform calculations with
        lineStart = Vector(self.x[closestSegment], self.y[closestSegment])
        startParam = self.param[closestSegment]

        lineEnd = Vector(self.x[closestSegment + 1], self.y[closestSegment + 1])
        endParam = self.param[closestSegment + 1]

        # Calculating the normalized path parameter given the position
        T = (closestPoint - lineStart).length() / (lineEnd - lineStart).length()
        return (startParam + ((endParam - startParam) * T))