import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import time

ROBOT_HOST = '10.x.58.x'
ROBOT_PORT = 30004

config_filename = 'rtde_config.xml'

conf = rtde_config.ConfigFile(config_filename)

class Robot:
    def __init__(self):
        self.con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    
    def connect(self):
        connection_state = self.con.connect()

        while not connection_state:
            print("Waiting for connection")
            connection_state = self.con.connect()
            time.sleep(0.5)

        print("Connected to robot")


    def MoveToPos(self, p1, p2):
        
