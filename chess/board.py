#Chess Board class
BOARDSETUP = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Board:
    def __init__(self):
        self.board = [[[] for i in range(8)] for j in range(8)]

        for y in range(8):
            for x in range(8):
                #Hvhsi den er hvid
                if (x + y) % 2 == 0:
                    self.board[y][x] = [0, "", 0, ""]
                else:
                    self.board[y][x] = [0, "", 1, ""]

        self.LoadFEN(BOARDSETUP)
        self.UpdateBoardImgs()
       
    def UpdateBoardImgs(self):
        for y in range(8):
            for x in range(8):
                img = ""
                if self.board[y][x][1] != "":
                    if self.board[y][x][0] == 1:
                        img = "b"
                    else:
                        img = "w"

                    img += self.board[y][x][1]
                    
                    self.board[y][x][3] = img 
                        

    def LoadFEN(self, fen):
        #Loop through each character in the FEN string
        x = 0
        y = 7
        for i in range(len(fen)):
            #Hvis tegnet er et mellemrum så stopper vi
            if fen[i] == " ":
                break

            if fen[i] == "/":
                y -= 1
                x = 0
                continue

            #Hvis tegnet er et tal så skal vi springe det antal pladser
            if fen[i] in "12345678":
                for j in range(int(fen[i])):
                    self.board[y][x][0] = 0
                    self.board[y][x][1] = ""
                    x += 1
                continue

            #Hvis tegnet er en bogstav så skal vi sætte det på brættet
            if fen[i] in "rnbqkp":
                self.board[y][x][0] = 0
                self.board[y][x][1] = fen[i]
                
                x += 1
            elif fen[i] in "RNBQKP":
                self.board[y][x][0] = 1
                self.board[y][x][1] = fen[i].lower()
                x += 1

        

            

    