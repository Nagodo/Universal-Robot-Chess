import robot.rtde.rtde as rtde
import robot.rtde.rtde_config as rtde_config
import time

ROBOT_HOST = '10.130.58.11'
ROBOT_PORT = 30004

config_filename = 'rtde_config.xml'

conf = rtde_config.ConfigFile(config_filename)

class Robot:
    def __init__(self):
        self.con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        self.connection_state = 0
        pass
    
    def connect(self):
        self.connection_state = self.con.connect()

    def MoveToPos(self, p1, p2):
        pass
