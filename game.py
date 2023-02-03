import pygame
from board import Board

#Pygame
pygame.init()
pygame.display.set_caption("Skak")
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()

#Chess Game


class Game:
    def __init__(self):
        self.board = Board()
        self.DrawBoard(screen)

    def DrawBoard(self, screen):
        screen.fill((0, 0, 0))
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, (195,160,101), (i * 100, j * 100, 100, 100))
                else:
                    pygame.draw.rect(screen, (131,89,53), (i * 100, j * 100, 100, 100))

        #Tegn brikkerne med deres farve ved brug af spritesheet
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
                    #Scale the sprite to 100x100
                    sprite = pygame.transform.scale(sprite, (100, 100))
                    screen.blit(sprite, (j * 100, i * 100))

                  


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
