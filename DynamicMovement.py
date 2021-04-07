from Vector import Vector
import math

# Data class to store linear and angular acceleration
class Steering:
    def __init__(self, linear = Vector(0, 0), angular = 0):
        self.linear = linear
        self.angular = angular

# Character class to store each individual character's movements
class Character:
    def __init__(self, position = Vector(0, 0), velocity = Vector(0, 0), linear = Vector(0, 0), orientation = 0, rotation = 0,
                angular = 0, maxSpeed = 0, maxAccleration = 0, offset = 0):

        self.position = position
        self.velocity = velocity
        self.linear = linear
        self.orientation = orientation
        self.rotation = rotation
        self.angular = angular
        self.maxSpeed = maxSpeed
        self.maxAcceleration = maxAccleration
        self.offset = offset

    def followPath(self, path):
        currentParam = path.getParam(self.position) # Getting the closest path parameter to the character's current position

        targetParam = currentParam + self.offset   # Adding the character's offset to the closest parameter, this is what makes the character progress along the path
        
        # If the the target param is greater than 1, set it to 1 so the character does not pass the ending point
        if targetParam > 1:
            targetParam = 1

        targetPos = path.getPosition(targetParam) # Getting the location on the graph of the path parameter
        steering = self.getSteeringSeek(targetPos)   # Returning the value of the Dynamic Seek algorithm targeting the new position on the path

        self.dynamicUpdate(steering)


    # Seek algorithm described in book
    def getSteeringSeek(self, targetPos):
        result = Steering()

        # Get the direction to the target
        result.linear = targetPos - self.position

        # Give full acceleration along this direction
        result.linear.normalize()
        result.linear *= self.maxAcceleration

        result.angular = 0
        return result

    # Dynamically update the character's values using the new steering calculated from steering algorithms
    def dynamicUpdate(self, steering, timeStep = 0.5):
        self.linear = steering.linear
        self.angular = steering.angular

        # Updating the character's position and orientation
        self.position += (self.velocity * timeStep)
        self.orientation += (self.rotation * timeStep)

        # Updating character's velocity and rotation using the current acceleration
        self.velocity += (steering.linear * timeStep)
        self.rotation += (steering.angular * timeStep)
        
        # If character's velocity is greater than their max speed
        if self.velocity.length() > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed

        self.orientation = math.atan2(self.velocity.y, self.velocity.x)

        