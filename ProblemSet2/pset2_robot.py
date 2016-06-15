# -*- coding: utf-8 -*-
'''
This is the code from Problem Set 2: "Simulating robots", from online
course MITx:6.00.2x Introduction to Computational Thinking and Data
Science I have finished on May. Position class and a skeleton of the
solution were provided.

The simulation was aimed to compare how much time a group of Roomba-like
robots will take to clean the floor of a room using two different strategies.
Results are presented using pylab.plot.
'''

import math
import random
import pylab


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        self.cleaned.append([x,y])
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
 
        if [m, n] in self.cleaned:
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        """
        total_clean = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.isTileCleaned(x, y):
                    total_clean += 1
        return total_clean

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        """
        x = random.randrange(self.width) 
        y = random.randrange(self.height)
        
        pos = Position(x, y)
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX() 
        y = pos.getY()

        #Check if the position is inside the room
        if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
            return True
        return False



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.
    """

    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        room.cleanTileAtPosition(self.position)
        self.direction = random.randint(0, 360) 

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction 

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        room = self.room
        position = self.getRobotPosition() 
        direction = self.getRobotDirection()
        speed = self.speed

        # Get the new position of the robot
        position = position.getNewPosition(direction, speed)

        # Check if new position is inside the room
        # If so - clean the tile
        if room.isPositionInRoom(position):
            self.setRobotPosition(position)
            room.cleanTileAtPosition(position)
        # If not - choose different position  
        else:
            direction = random.randint(0, 360)
            self.setRobotDirection(direction)    

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        room = self.room
        position = self.getRobotPosition() 
        direction = self.getRobotDirection()
        speed = self.speed

        # Get the new position of the robot
        position = position.getNewPosition(direction, speed)
        # Check if new position is inside the room
        # If so - clean the tile
        if room.isPositionInRoom(position): 
            self.setRobotPosition(position)
            room.cleanTileAtPosition(position)
            direction = random.randint(0, 360)
            self.setRobotDirection(direction)
        # If not - choose different position
        else:
            direction = random.randint(0, 360)
            self.setRobotDirection(direction)  
            
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    number_of_steps = []

    # Run the simulation num_trials times           
    for simulation in range(num_trials):
        # NoS - Number of Steps
        NoS = 0
        percent_clean = 0
        
        room = RectangularRoom(width, height)
        robots = []

        # Append activated robots to the list
        for i in range(num_robots):
            i = robot_type(room, speed)
            robots.append(i)

        # Clean MIN_COVERAGE of the room
        while percent_clean < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
            # Keep track of number of steps    
            NoS += 1
            percent_clean = room.getNumCleanedTiles()/float(room.getNumTiles())

        number_of_steps.append(NoS)
    # Get the the mean number of steps needed to clean the room     
    mean_trials = sum(number_of_steps) / num_trials
    
    return float(mean_trials)

def showPlot(title, x_label, y_label):
    """
    Uses pylab to present the results of the simulation
    """
    num_robot_range = range(1, 5)
    timesStandard = []
    timesRandom = []

    # Run the simulation
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        timesStandard.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        timesRandom.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))

    # Plot the results
    pylab.plot(num_robot_range, timesStandard)
    pylab.plot(num_robot_range, timesRandom)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

#showPlot('80%', 'Num of robots', 'Time')


