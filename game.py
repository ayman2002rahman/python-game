import pygame
import os
from rail import Rail

WIDTH, HEIGHT = 700, 700 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad-Mania") #game name displayed on window

#----CONSTANTS----
BACKGROUND = (38, 50, 70) #background color
FPS = 60 #caps the refresh rate so the game is consistent
SIZE = 4 #board dimensions
TRACK_SIZE = 125
GRID_THICKNESS = 2

#----IMAGES-------
STRAIGHT_IMG = pygame.image.load(os.path.join('Assets', 'straight.png'))
STRAIGHT = pygame.transform.scale(STRAIGHT_IMG, (40, 40))

#Railroad track initialization
#The different tracks are represented by a 4 digit number
#each bit represents a direction LUDR
#ex: 1001 represents a horizontal track because it has an opening at Left and Right
tracks = [[0000 for i in range(SIZE)] for i in range(SIZE)]
tracks[0][0] = '1001'
tracks[0][1] = '1001'
tracks[0][2] = '1001'
tracks[0][3] = '1001'
tracks[1][0] = '1001'
tracks[1][1] = '1001'
tracks[1][2] = '1001'
tracks[1][3] = '1001'
tracks[2][0] = '1001'
tracks[2][1] = '1001'
tracks[2][2] = '1001'
tracks[2][3] = '1001'
tracks[3][0] = '1001'
tracks[3][1] = '1001'
tracks[3][2] = '1001'
tracks[3][3] = '1001'

def getDigit(s, i):
    return int(s[i])

def drawGrid():
    for i in range(SIZE):
        for j in range(SIZE):
            pygame.draw.rect(WINDOW, (47, 35, 158), (i * TRACK_SIZE, j * TRACK_SIZE, TRACK_SIZE, TRACK_SIZE), GRID_THICKNESS)

def draw():
    WINDOW.fill(BACKGROUND)
    WINDOW.blit(STRAIGHT, (100, 50))
    drawGrid()
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run: #Game Loop
        clock.tick(FPS)
        for event in pygame.event.get(): #Ends game when user quits
            if event.type == pygame.QUIT:
                run = False
        #Handle game loops here
        draw() #the game is constantly drawing and updating the screen
    pygame.quit()

if __name__ == "__main__": #only runs the game if this specific file is run
    main()