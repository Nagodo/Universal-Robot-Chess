#Chess Board class
BOARDSETUP = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Board:
    def __init__(self):
        self.board = [[[] for i in range(8)] for j in range(8)]
        self.playercolor = "w"
        self.turn = "w"
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
        if move[0] == "O":
            if move[1] == "O":
                if self.turn == "w":
                    self.board[7][4][0] = 0
                    self.board[7][4][1] = ""
                    self.board[7][6][0] = 1
                    self.board[7][6][1] = "K"
                    self.board[7][7][0] = 0
                    self.board[7][7][1] = ""
                    self.board[7][5][0] = 1
                    self.board[7][5][1] = "R"
                else:
                    self.board[0][4][0] = 0
                    self.board[0][4][1] = ""
                    self.board[0][6][0] = 2
                    self.board[0][6][1] = "K"
                    self.board[0][7][0] = 0
                    self.board[0][7][1] = ""
                    self.board[0][5][0] = 2
                    self.board[0][5][1] = "R"
            else:
                if self.turn == "w":
                    self.board[7][4][0] = 0
                    self.board[7][4][1] = ""
                    self.board[7][2][0] = 1
                    self.board[7][2][1] = "K"
                    self.board[7][0][0] = 0
                    self.board[7][0][1] = ""
                    self.board[7][3][0] = 1
                    self.board[7][3][1] = "R"
                else:
                    self.board[0][4][0] = 0
                    self.board[0][4][1] = ""
                    self.board[0][2][0] = 2
                    self.board[0][2][1] = "K"
                    self.board[0][0][0] = 0
                    self.board[0][0][1] = ""
                    self.board[0][3][0] = 2
                    self.board[0][3][1] = "R"
        else:
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

        

            

    