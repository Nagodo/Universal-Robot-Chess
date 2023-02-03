#Chess Board class
boardSetup = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class Board:
    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]

        self.LoadFEN(boardSetup)
       

    def LoadFEN(self, fen):
        #Loop through each character in the FEN string
        for i in range(len(fen)):
            #Hvis tegnet er et mellemrum så stopper vi
            if fen[i] == " ":
                break

            #Hvis tegnet er et tal skal vi placere det antal tomme felter
            elif fen[i].isdigit():
                for j in range(int(fen[i])):
                    self.board[i][j] = 0

            # Hvis tegnet er en bogstav skal vi placere en brik
            elif fen[i].isalpha():
                self.board[i][j] = fen[i]

            #Hvis tegnet er en skråstreg skal vi gå en række ned
            elif fen[i] == "/":
                i += 1
                j = 0
            #If the character is anything else, then we know we have an invalid FEN string
            else:
                print("Invalid FEN string")
                break


    