#Chess Board class
boardSetup = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Board:
    def __init__(self):
        self.board = [[[] for i in range(8)] for j in range(8)]

        self.LoadFEN(boardSetup)
       

    def LoadFEN(self, fen):
        #Loop through each character in the FEN string
        x = 0
        y = 0
        for i in range(len(fen)):
            #Hvis tegnet er et mellemrum så stopper vi
            if fen[i] == " ":
                break

            if fen[i] == "/":
                y += 1
                x = 0
                continue

            #Hvis tegnet er et tal så skal vi springe det antal pladser
            if fen[i] in "12345678":
                for j in range(int(fen[i])):
                    self.board[y][x] = [0, ""]
                    x += 1
                continue

            #Hvis tegnet er en bogstav så skal vi sætte det på brættet
            if fen[i] in "rnbqkp":
                self.board[y][x] = [0, fen[i]]
                x += 1
            elif fen[i] in "RNBQKP":
                self.board[y][x] = [1, fen[i].lower()]
                x += 1

    