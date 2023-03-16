import pygame
from board import Board

#Pygame
pygame.init()
pygame.display.set_caption("Skak")
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()



#Chess Game
isPlaying = False
boardOffest = (50, 50)

class Game:
    def __init__(self):
        self.board = Board()
        self.DrawBoard(screen)
        self.DrawNotation()

    def DrawBoard(self, screen):
        screen.fill((0, 0, 0))
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, (195,160,101), ((i * 100) + boardOffest[0] , (j * 100) + boardOffest[1], 100, 100))
                else:
                    pygame.draw.rect(screen, (131,89,53), ((i * 100) + boardOffest[0] , (j * 100) + boardOffest[1], 100, 100))

        #Frame the board
        pygame.draw.rect(screen, (100, 100, 100), (boardOffest[0], boardOffest[1], 800, 800), 10)
        
        #Draw letters and numbers
        for i in range(8):  
            font = pygame.font.SysFont("Arial", 30)
            text = font.render(str(8 - i), True, (255, 255, 255))
            screen.blit(text, (boardOffest[0] - 30, (i * 100) + boardOffest[1] + 40))
            text = font.render(chr(97 + i), True, (255, 255, 255))
            screen.blit(text, ((i * 100) + boardOffest[0] + 40, 850))

    def DrawNotation(self):
        pygame.draw.rect(screen, (100, 100, 100), (900, 50, 250, 800), 5)
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] != [0, ""]:
                    s = ""
                    if self.board.board[i][j][0] == 0:
                        s = "w-"
                    else:
                        s = "b-"

                    if self.board.board[i][j][1] == "p":
                        s += "pawn"
                    elif self.board.board[i][j][1] == "r":
                        s += "rook"
                    elif self.board.board[i][j][1] == "n":
                        s += "knight"
                    elif self.board.board[i][j][1] == "b":
                        s += "bishop"
                    elif self.board.board[i][j][1] == "q":
                        s += "queen"
                    elif self.board.board[i][j][1] == "k":
                        s += "king"

                    sprite = pygame.image.load("./sprites/" + s + ".png")
                    
                    sprite = pygame.transform.scale(sprite, (100, 100))
                    screen.blit(sprite, ((j * 100) + boardOffest[0], (i * 100) + boardOffest[1]))

                  


#Game Loop
def main():
    game = Game()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
