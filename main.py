import time
from threading import Thread
from chess.flask_app import WebInterface
from vision import Vision
from chess.board import Board
from robot.robot import Robot

robot = Robot()
robot.connect()

if robot.connection_state != 0:
    robot.SetRecipes()
    robot.SetDefaultRegister()
    robot.StartDataSync()

chess = Board()

webInterface = WebInterface()
webThread = Thread(target=webInterface.app.run)
webThread.start()
webInterface.setChessData(chess.board)

vision = Vision()
visionThread = Thread(target=vision.startVision)
visionThread.start()


robotThread = Thread(target = robot.ControlLoop)
robotThread.start()
