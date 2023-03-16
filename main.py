import time
from robot import Robot

robot = Robot()

while robot.connection_state == 0:
    robot.connect()
    time.sleep(0.5)

print("Connected to robot")
