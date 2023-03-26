import robot.rtde.rtde as rtde
import robot.rtde.rtde_config as rtde_config
import time
import sys

ROBOT_HOST = '10.130.58.11'
ROBOT_PORT = 30004

config_filename = './robot/rtde_config.xml'

conf = rtde_config.ConfigFile(config_filename)

class Robot:
    def __init__(self):
        self.con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        self.connection_state = 0
        self.go_to_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        pass
    
    def connect(self):
        try:
            self.connection_state = self.con.connect()
            while self.connection_state == 0:
                self.con.connect()
                time.sleep(0.5)

            print("Connected to robot")
        except:
            print("Could not connect to robot")
        
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
        self.setp.input_double_register_3 = 0
        self.setp.input_double_register_4 = 0
        self.setp.input_double_register_5 = 0

        self.watchdog.input_int_register_0 = 0

   
    def StartDataSync(self):
        if not self.con.send_start():
            sys.exit()

    def ControlLoop(self):
        
        while True:
            if self.connection_state != 0:
                state = self.con.receive()

                

                if state is None:
                    print("Connection closed")
                    break

                #Tjek om robottet er fremme og stop hvis det er
                if self.should_move:
                    current_pos = state.actual_tcp_pose
                    if abs(current_pos[0] - self.go_to_pos[0]) < 0.01 and abs(current_pos[1] - self.go_to_pos[1]) < 0.01 and abs(current_pos[2] - self.go_to_pos[2]) < 0.01:
                        self.should_move = False


                if state.output_int_register_0 != 0:
                
                    print("Sending")
                    self.UpdateRegister()
                

                self.con.send(self.watchdog)

        self.con.send_pause()
        self.con.disconnect()

    def UpdateRegister(self):
       
        send = None
        for i in range(0, 6):
            send.__dict__["input_double_register_" + str(i)] = self.go_to_pos[i]

        s_move = 0
        if self.should_move:
            s_move = 1

        send.__dict__["input_int_register_1"] = s_move

        self.con.send(send)


    def Move(self, move):
        pass
        
