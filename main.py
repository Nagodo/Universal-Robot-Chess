import time
from threading import Thread
from chess.flask_app import WebInterface
from vision import Vision
from chess.board import Board
from robot.robot import Robot
from chess.engine import Engine

# robot = Robot()
# robot.connect()

# if robot.connection_state != 0:
#     robot.SetRecipes()
#     robot.SetDefaultRegister()
#     robot.StartDataSync()

chess = Board()
engine = Engine()

engine.set_elo(2800)

webInterface = WebInterface()
webThread = Thread(target=webInterface.RunServer)
webThread.start()

webInterface.setChessData(chess.board)

vision = Vision()
visionThread = Thread(target=vision.startVision)
visionThread.start()


# robotThread = Thread(target = robot.ControlLoop)
# robotThread.start()

while True:
    if chess.turn != chess.playercolor:
        engine.set_fen(chess.GetFEN())
        move = engine.get_best_move()
        print(move)
        chess.Move(move)
        webInterface.setChessData(chess.board)
    
    time.sleep(0.1)
