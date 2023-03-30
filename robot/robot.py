import robot.rtde.rtde as rtde
import robot.rtde.rtde_config as rtde_config
from robot.posistions import *
import time
import sys

ROBOT_HOST = '10.130.58.11'
ROBOT_PORT = 30004

config_filename = './robot/rtde_config.xml'

conf = rtde_config.ConfigFile(config_filename)

#ACTIONS
#0 = Idle
#1 = Move to base
#2 = Move piece to square
#3 = Grab piece
#4 = Move to capture

class Robot:
    def __init__(self):
        self.con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        self.connection_state = 0
        self.go_to_pos = [0.0, 0.0, 0.0]
        self.current_action = 0
        self.action_done = 0
        
       
    def connect(self):
        try:
            self.connection_state = self.con.connect()
            while self.connection_state == 0:
                self.con.connect()
                time.sleep(0.5)

            print("Connected to robot")
        except:
            print("Could not connect to robot")

    def MoveToBase(self):
        self.go_to_pos = [BASE[0], BASE[1], BASE[2]]
        self.current_action = 1
        
    def SetRecipes(self):
        state_names, state_types = conf.get_recipe('state')
        setp_names , setp_types  = conf.get_recipe('setp')
        watchdog_names, watchdog_types = conf.get_recipe('watchdog')

        self.con.send_output_setup(state_names, state_types)
        self.setp = self.con.send_input_setup(setp_names, setp_types)
        self.watchdog = self.con.send_input_setup(watchdog_names, watchdog_types)

    def SetDefaultRegister(self):
        self.setp.input_double_register_0 = 0
        self.setp.input_double_register_1 = 0
        self.setp.input_double_register_2 = 0

        self.watchdog.input_int_register_0 = 0

   
    def StartDataSync(self):
        if not self.con.send_start():
            sys.exit()

    def ControlLoop(self):
        
        while True:
            if self.connection_state != 0:
                state = self.con.receive()

                self.action_done = state.output_int_register_0
                if state is None:
                    print("Connection closed")
                    break

               
                self.UpdateRegister()
             
                self.con.send(self.watchdog)

        self.con.send_pause()
        self.con.disconnect()

    def UpdateRegister(self):
       
        send = self.setp
        for i in range(0, 3):
            send.__dict__["input_double_register_" + str(i)] = self.go_to_pos[i]
        
        
        send.__dict__["input_int_register_1"] = self.current_action

        self.con.send(send)

    def GrabPiece(self, square):
        l = square[0]
        n = square[1]
        take_from = (CHESSPOSITIONS[n], CHESSPOSITIONS[l], 0.140)
        self.go_to_pos = [take_from[0], take_from[1], take_from[2]]
        self.current_action = 3

    def MoveToCapture(self, color = 0):
        self.go_to_pos = [CAPTUREDPIECES[color][0], CAPTUREDPIECES[color][1], CAPTUREDPIECES[color][2]]
        CAPTUREDPIECES[color][0] -= 0.04
        self.current_action = 4

    def MoveToSquare(self, square):
        l = square[0]
        n = square[1]
        move_to = (CHESSPOSITIONS[n], CHESSPOSITIONS[l], 0.140)
        self.go_to_pos = [move_to[0], move_to[1], move_to[2]]
        self.current_action = 2

        
