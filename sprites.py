#Program that spilts the sprite sheet into individual sprites and saves them as .png files

import pygame

pygame.init()

#Load the sprite sheet
spriteSheet = pygame.image.load("./sprites/sheet.png")

#Create a new surface for each sprite the dimesions of the spritesheet is 2560x853 it has to be transparent
for i in range(6):
    for j in range(2):
        x = 2560/6
        y = 853/2
        sprite = pygame.Surface((x, y), pygame.SRCALPHA)
        sprite.blit(spriteSheet, (0, 0), (x * i, y * j, x, y))
        pygame.image.save(sprite, "./sprites/" + str(i) + str(j) + ".png")
        

