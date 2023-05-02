#Chess Board class
#BOARDSETUP = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
BOARDSETUP = "r1bqk2r/ppp2pp1/2np1n1p/4p3/2B1P3/P1PP1N2/P4PPP/R1BQ1RK1 b kq - 0 8"


class Board:
    def __init__(self):
        self.board = [[[] for i in range(8)] for j in range(8)]
        self.playercolor = "w"
        self.turn = "b"
        self.white_castle = [True, True]
        self.black_castle = [True, True]

        for y in range(8):
            for x in range(8):
                #Hvhsi den er hvid
                if (x + y) % 2 == 0:
                    self.board[y][x] = [0, "", 0, ""]
                else:
                    self.board[y][x] = [0, "", 1, ""]

        self.LoadFEN(BOARDSETUP)
        self.UpdateBoardImgs()
        print(self.GetFEN())

    def Move(self, move):
        #Hvis det er en rokade
        
            
        from_y = self.ConvertToIndex(move[1])
        from_x = self.ConvertToIndex(move[0])
        to_y = self.ConvertToIndex(move[3])
        to_x = self.ConvertToIndex(move[2])
        print(from_x, from_y, to_x, to_y)
        #Hvis det er en promotion
        if len(move) == 5:
            self.board[to_y][to_x][0] = self.board[from_y][from_x][0]
            self.board[to_y][to_x][1] = move[4]
            self.board[from_y][from_x][0] = 0
            self.board[from_y][from_x][1] = ""
        else:
            self.board[to_y][to_x][0] = self.board[from_y][from_x][0]
            self.board[to_y][to_x][1] = self.board[from_y][from_x][1]
            self.board[from_y][from_x][0] = 0
            self.board[from_y][from_x][1] = ""

        self.UpdateBoardImgs()
        self.ChangeTurn()

    def ConvertToIndex(self, letter):
        l_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        return l_dict[letter]
    

    def ChangeTurn(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"
            
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

    def GetFEN(self):
        fen = ""
        for y in range(8):
            empty = 0
            for x in range(8):
                if self.board[y][x][0] == 0 and self.board[y][x][1] == "":
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    if self.board[y][x][0] == 0:
                        fen += self.board[y][x][1].upper()
                    else:
                        fen += self.board[y][x][1]
            if empty > 0:
                fen += str(empty)
            if y != 7:
                fen += "/"

        fen += " " + self.turn + " "
        if self.white_castle[0]:
            fen += "K"
        if self.white_castle[1]:
            fen += "Q"
        if self.black_castle[0]:
            fen += "k"
        if self.black_castle[1]:
            fen += "q"

        return fen

        

            

    