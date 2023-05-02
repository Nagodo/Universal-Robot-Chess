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

robot.MoveToBase()
WaitForActionDone()


def ConvertToIndex(letter):
        l_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        return l_dict[letter]

def MakeRobotMove(move):   
    
    sqr = engine.get_on_square(move[2] + move[3])
    if sqr != None:
        robot.GrabPiece(move[2] + move[3])
        WaitForActionDone()
        if chess.playercolor == "w":
            robot.MoveToCapture()
        else:
            robot.MoveToCapture(1)
        WaitForActionDone()

    if (move) == "e8g8":
        robot.GrabPiece(move[0] + move[1])
        WaitForActionDone()
        robot.MoveToSquare(move[2] + move[3])
        WaitForActionDone()
        robot.GrabPiece("h8")
        WaitForActionDone()
        robot.MoveToSquare("f8")
        WaitForActionDone()
    elif (move) == "e8c8":
        robot.GrabPiece(move[0] + move[1])
        WaitForActionDone()
        robot.MoveToSquare(move[2] + move[3])
        WaitForActionDone()
        robot.GrabPiece("a8")
        WaitForActionDone()
        robot.MoveToSquare("d8")
        WaitForActionDone()
    else:

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
        vision.UpdateOldFrame()
        webInterface.setChessData(chess.board)
    else:
        if vision.newPlayerMove:
            vision.newPlayerMove = False
            type = vision.playerMoveType
            move01 = vision.playerMove[0]
            move02 = vision.playerMove[1]
            
            if type == 2:
                move_to =""
                move_from = ""
                sqr01 = engine.get_on_square(move01)
                sqr02 = engine.get_on_square(move02)
       
                if sqr01 and sqr02:
                    color01 = str(sqr01).split(".")[1]
                    color01 = color01.split("_")[0]
                    
                    if color01 == "WHITE" and chess.playercolor == "w":
                        move_to = move02
                        move_from = move01
                    elif color01 == "BLACK" and chess.playercolor == "b":
                        move_to = move02
                        move_from = move01

                elif sqr01:
                    move_to = move02
                    move_from = move01
                else:
                    move_to = move01
                    move_from = move02

            
            chess.Move(move_from + move_to)
            webInterface.setChessData(chess.board)
            print("Player move: " + move_from + move_to)


    
    
    
    time.sleep(0.1)