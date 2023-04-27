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

# vision = Vision()
# visionThread = Thread(target=vision.startVision)
# visionThread.start()

if not DISABLEROBOT:
    robotThread = Thread(target = robot.ControlLoop)
    robotThread.start()

robot.MoveToBase()
WaitForActionDone()


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

def ConvertToIndex(letter):
        l_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        return l_dict[letter]

def MakeRobotMove(move):   
    if move[0] == "O":
        
        if chess.playercolor == "w":
            king = "e8"
            king_to = "g8"
        else:
            king = "e1"
            king_to = "g1"
        if move[1] == "O":
            if chess.playercolor == "w":
                rook = "h8"
                rook_to = "f8"
            else:
                rook = "h1"
                rook_to = "f1"
            
            robot.GrabPiece(rook)
            WaitForActionDone()
            robot.MoveToSquare(rook_to)
            WaitForActionDone()
            robot.GrabPiece(king)
            WaitForActionDone()
            robot.MoveToSquare(king_to)
        else:
            if chess.playercolor == "w":
                rook = "a8"
                rook_to = "d8"
            else:
                rook = "a1"
                rook_to = "d1"
            
            robot.GrabPiece(rook)
            WaitForActionDone()
            robot.MoveToSquare(rook_to)
            WaitForActionDone()
            robot.GrabPiece(king)
            WaitForActionDone()
            robot.MoveToSquare(king_to)
            WaitForActionDone()
        
    else:
        sqr = engine.get_what_is_on_square(move[2] + move[3])
        if sqr != None:
            robot.GrabPiece(move[2] + move[3])
            WaitForActionDone()
            if chess.playercolor == "w":
                robot.MoveToCapture()
            else:
                robot.MoveToCapture(1)
            WaitForActionDone()
        robot.GrabPiece(move[0] + move[1])
        WaitForActionDone()
        robot.MoveToSquare(move[2] + move[3])
        WaitForActionDone()

    robot.MoveToBase()
    WaitForActionDone()

while True:
    #Find næste robot træk hvis det ikke er spillerens tur
    if chess.turn != chess.playercolor:
        engine.set_fen(chess.GetFEN())
        move = engine.get_best_move()
        print("Robot move:" + move)
        chess.Move(move)
        MakeRobotMove(move)
        webInterface.setChessData(chess.board)
    else:
        move = input("Move: ")
        chess.Move(move)
        webInterface.setChessData(chess.board)
    
    
    time.sleep(0.1)