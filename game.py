import pygame
import os
#from button import Button

WIDTH, HEIGHT = 700, 700 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad-Mania") #game name displayed on window

#----CONSTANTS----
BACKGROUND = (38, 50, 70) #background color
FPS = 30 #caps the refresh rate so the game is consistent
SIZE = 4 #board dimensions
TRACK_SIZE = 128
GRID_THICKNESS = 2
CAR_SPEED = 10

#----IMAGES-------
STRAIGHT_IMG = pygame.image.load(os.path.join('Assets', 'straight.png'))
VERTICAL = pygame.transform.scale(STRAIGHT_IMG, (TRACK_SIZE, TRACK_SIZE))
HORIZONTAL = pygame.transform.rotate(VERTICAL, 90)

CURVE_IMG = pygame.image.load(os.path.join('Assets', 'curve.png'))
LD = pygame.transform.scale(CURVE_IMG, (TRACK_SIZE, TRACK_SIZE))
DR = pygame.transform.rotate(LD, 90)
UR = pygame.transform.rotate(DR, 90)
LU = pygame.transform.rotate(UR, 90)

CAR_IMG = pygame.image.load(os.path.join('Assets', 'car.png'))
VERTICAL_CAR = pygame.transform.scale(CAR_IMG, (TRACK_SIZE, TRACK_SIZE))
HORIZONTAL_CAR = pygame.transform.rotate(VERTICAL_CAR, -90)
EMPTY = pygame.image.load(os.path.join('Assets', 'empty.png'))

#----BUTTONS----

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        #WINDOW.blit(self.image (self.rect.x, self.rect.y))
        return action


#Railroad track initialization
#The different tracks are represented by a 4 digit number
#each bit represents a direction LUDR
#ex: 1001 represents a horizontal track because it has an opening at Left and Right
tracks = [[0000 for i in range(SIZE)] for i in range(SIZE)]
tracks[0][0] = '1010'
tracks[0][1] = '1001'
tracks[0][2] = '0110'
tracks[0][3] = '1001'
tracks[1][0] = '0011'
tracks[1][1] = '1001'
tracks[1][2] = '0110'
tracks[1][3] = '1001'
tracks[2][0] = '0101'
tracks[2][1] = '1100'
tracks[2][2] = '1001'
tracks[2][3] = '1001'
tracks[3][0] = '0110'
tracks[3][1] = '0110'
tracks[3][2] = '0101'
tracks[3][3] = '1001'

car = {'trackPos': (0,0), 'boxPos': 500, 'dir': 'U'} #all the different possible directions are LUDR

def getDigit(s, i):
    return int(s[i])

def makeGridButtons():
    return [[Button(j * TRACK_SIZE, i * TRACK_SIZE, EMPTY, 1) for j in range(TRACK_SIZE)] for i in range(TRACK_SIZE)]

def rotateTrack(tracks, i, j):
    if tracks[i][j] == '0011':
        tracks[i][j] = '0101'
    elif tracks[i][j] == '0101':
        tracks[i][j] = '1100'
    elif tracks[i][j] == '0110':
        tracks[i][j] = '1001'
    elif tracks[i][j] == '1001':
        tracks[i][j] = '0110'
    elif tracks[i][j] == '1010':
        tracks[i][j] = '0011'
    elif tracks[i][j] == '1100':
        tracks[i][j]= '1010'


def handleTrackClicks(buttons):
    for i in range(SIZE):
        for j in range(SIZE):
            if buttons[i][j].draw():
                rotateTrack(tracks, i, j)


def updateCar():
    if(car['direction'] == 'U'):
        car['position'] += (0, -CAR_SPEED)
    elif(car['direction'] == 'L'):
        car

def drawGrid():
    for i in range(SIZE):
        for j in range(SIZE):
            pygame.draw.rect(WINDOW, (47, 35, 158), (j * TRACK_SIZE, i * TRACK_SIZE, TRACK_SIZE, TRACK_SIZE), GRID_THICKNESS)
            if tracks[i][j] == '1001':
                WINDOW.blit(HORIZONTAL, (j * TRACK_SIZE, i * TRACK_SIZE))
            elif tracks[i][j] == '0110':
                WINDOW.blit(VERTICAL, (j * TRACK_SIZE, i * TRACK_SIZE))
            elif tracks[i][j] == '1010':
                WINDOW.blit(LD, (j * TRACK_SIZE, i * TRACK_SIZE))
            elif tracks[i][j] == '0011':
                WINDOW.blit(DR, (j * TRACK_SIZE, i * TRACK_SIZE))
            elif tracks[i][j] == '0101':
                WINDOW.blit(UR, (j * TRACK_SIZE, i * TRACK_SIZE))
            elif tracks[i][j] == '1100':
                WINDOW.blit(LU, (j * TRACK_SIZE, i * TRACK_SIZE))

def draw():
    WINDOW.fill(BACKGROUND)
    drawGrid()
    WINDOW.blit(VERTICAL_CAR, (3 * TRACK_SIZE, 3 * TRACK_SIZE))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    gridButtons = makeGridButtons()
    #startButton = Button()

    

    while run: #Game Loop
        clock.tick(FPS)
        for event in pygame.event.get(): #Ends game when user quits
            if event.type == pygame.QUIT:
                run = False
        #Handle game loops here
        handleTrackClicks(gridButtons)
        draw() #the game is constantly drawing and updating the screen
    pygame.quit()

if __name__ == "__main__": #only runs the game if this specific file is run
    main()