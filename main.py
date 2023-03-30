import time
from threading import Thread
from chess.flask_app import WebInterface
from vision import Vision
from chess.board import Board
from robot.robot import Robot
from chess.engine import Engine
from CONFIG import *
import logging

#Fjerner POST request fra loggen
log = logging.getLogger('werkzeug')
log.disabled = True


def WaitForActionDone():
    time.sleep(1)
    while robot.action_done == 0:
        
        time.sleep(0.1)
    print("Action done")

if not DISABLEROBOT:
    robot = Robot()
    robot.connect()

    if robot.connection_state != 0:
        robot.SetRecipes()
        robot.SetDefaultRegister()
        robot.StartDataSync()

chess = Board()
engine = Engine()

engine.set_elo(3000)

webInterface = WebInterface()
webThread = Thread(target=webInterface.RunServer)
webThread.start()

webInterface.setChessData(chess.board)

vision = Vision()
visionThread = Thread(target=vision.startVision)
visionThread.start()

if not DISABLEROBOT:
    robotThread = Thread(target = robot.ControlLoop)
    robotThread.start()

# robot.MoveToBase()
# WaitForActionDone()
vision.UpdateOldFrame()


# robot.GrabPiece("b1")
# WaitForActionDone()

# robot.MoveToCapture()
# WaitForActionDone()

# robot.GrabPiece("h7")
# WaitForActionDone()

# robot.MoveToCapture(1)
# WaitForActionDone()

# robot.GrabPiece("d7")
# WaitForActionDone()

# robot.MoveToSquare("d5")
# WaitForActionDone()

#robot.current_action = 0

while True:
    #Find næste robot træk hvis det ikke er spillerens tur
    # if chess.turn != chess.playercolor:
    #     engine.set_fen(chess.GetFEN())
    #     move = engine.get_best_move()
    #     print(move)
    #     chess.Move(move)
    #     webInterface.setChessData(chess.board)

    
    
    time.sleep(0.1)

