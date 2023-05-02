import stockfish

class Engine:
    def __init__(self):
        self.engine = stockfish.Stockfish("./chess/stockfish/stockfish.exe")
        self.engine.set_depth(20)

    def set_depth(self, depth):
        self.engine.set_depth(depth)

    def set_elo(self, elo):
        self.engine.set_elo_rating(elo)

    def set_fen(self, fen):
        self.engine.set_fen_position(fen)

    def is_legal(self, move):
        return self.engine.is_move_correct(move)

    def get_best_move(self):
        return self.engine.get_best_move()
    
    def get_evaluation(self, fen):
        return self.engine.get_evaluation(fen)
    
engine = Engine()

FEN = "rnbqk2r/ppp1bppp/5n2/3p4/3P4/3B1N2/PPP1QPPP/RNB1K2R w KQkq - 5 7"

engine.set_fen(FEN)

move = engine.get_best_move()
print(move)