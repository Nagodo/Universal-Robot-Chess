import time
from threading import Thread
from chess.flask_app import WebInterface
from chess.board import Board
from robot.robot import Robot

robot = Robot()
chess = Board()

webInterface = WebInterface()
webThread = Thread(target=webInterface.app.run)

webInterface.setChessData(chess.board)

# while robot.connection_state == 0:
#     robot.connect()
#     time.sleep(0.5)

# print("Connected to robot")

if __name__ == "__main__":
    webThread.start()
   