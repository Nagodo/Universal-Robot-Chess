from flask import Flask, render_template, request
from turbo_flask import Turbo
import time
import json


class WebInterface:
    def __init__(self):    
        self.app = Flask(__name__)
        self.turbo = Turbo()
        self.turbo.init_app(self.app)
        self.chessData = []
        
        @self.app.route("/")
        def main():
            return render_template("index.html", board_data = self.chessData)
        
        @self.app.route("/getchessposition", methods=['POST']) 
        def get_chess_position():
                return render_template("board.html", board_data = self.chessData)
                
 
    def RunServer(self):
        self.app.run()
        


    def setChessData(self, data):
        self.chessData = data
