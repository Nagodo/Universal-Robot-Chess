from flask import Flask, render_template, request
import time
import json

class WebInterface:
    def __init__(self):    
        self.app = Flask(__name__)
        self.chessData = []
        
        @self.app.route("/")
        def main():
            return render_template("index.html", board_data = self.chessData)
        
        @self.app.route("/getchessposition", methods=['POST']) 
        def get_chess_position():
            
            #ChessData to JSON
            jsonData = json.dumps(self.chessData)


            return jsonData
 
    def RunServer(self):
        self.app.run()
        


    def setChessData(self, data):
        self.chessData = data
