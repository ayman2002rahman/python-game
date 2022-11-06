import pygame
import os
from pygame import mixer
#from button import Button

mixer.init()
mixer.music.load(os.path.join('Assets', 'winsound.mp3'))
mixer.music.set_volume(0.5)

WIDTH, HEIGHT = 700, 700 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miner Mania") #game name displayed on window

#----CONSTANTS----
BACKGROUND = (98, 163, 60) #background color
MAIN_MENU_BACKGROUND = (196, 195, 186)
WIN_BACKGROUND = (255, 153, 0)

TITLE_SCALE = 0.85
END_SCALE = 0.7
FPS = 10 #caps the refresh rate so the game is consistent
SIZE = 5 #board dimensions
TRACK_SIZE = 128
GRID_THICKNESS = 2
CAR_SPEED = 7

#----IMAGES-------
STRAIGHT_IMG = pygame.image.load(os.path.join('Assets', 'straight.png'))
VERTICAL = pygame.transform.scale(STRAIGHT_IMG, (TRACK_SIZE, TRACK_SIZE))
HORIZONTAL = pygame.transform.rotate(VERTICAL, 90)

CURVE_IMG = pygame.image.load(os.path.join('Assets', 'curve.png'))
LD = pygame.transform.scale(CURVE_IMG, (TRACK_SIZE, TRACK_SIZE))
DR = pygame.transform.rotate(LD, 90)
UR = pygame.transform.rotate(DR, 90)
LU = pygame.transform.rotate(UR, 90)

CAVE = pygame.image.load(os.path.join('Assets', 'cave.png'))
ENTRANCE = pygame.transform.scale(CAVE, (TRACK_SIZE, TRACK_SIZE))
EXIT = pygame.transform.rotate(ENTRANCE, 90)

CAR_IMG = pygame.image.load(os.path.join('Assets', 'car.png'))
VERTICAL_CAR = pygame.transform.scale(CAR_IMG, (TRACK_SIZE, TRACK_SIZE))
HORIZONTAL_CAR = pygame.transform.rotate(VERTICAL_CAR, -90)

EMPTY = pygame.image.load(os.path.join('Assets', 'empty.png'))
TITLE_IMG = pygame.image.load(os.path.join('Assets', 'title.png'))
TITLE = pygame.transform.scale(TITLE_IMG, (int(TITLE_SCALE * TITLE_IMG.get_width()), int(TITLE_SCALE * TITLE_IMG.get_height())))
START_IMG = pygame.image.load(os.path.join('Assets', 'startButton.png'))
RESTART_IMG = pygame.image.load(os.path.join('Assets', 'restart.png'))
END_IMG = pygame.image.load(os.path.join('Assets', 'end.png'))
WIN = pygame.transform.scale(END_IMG, (int(END_SCALE * END_IMG.get_width()), int(END_SCALE * END_IMG.get_height())))

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
        WINDOW.blit(self.image, (self.rect.topleft[0], self.rect.topleft[1]))
        return action


#Railroad track initialization
#The different tracks are represented by a 4 digit number
#each bit represents a direction LUDR
#ex: 1001 represents a horizontal track because it has an opening at Left and Right
tracks = [[0000 for i in range(SIZE)] for i in range(SIZE)]
tracks[0][0] = '1010'
tracks[0][1] = '1001'
tracks[0][2] = '0011'
tracks[0][3] = '1001'
tracks[1][0] = '0011'
tracks[1][1] = '0101'
tracks[1][2] = '1100'
tracks[1][3] = '1001'
tracks[2][0] = '0101'
tracks[2][1] = '1100'
tracks[2][2] = '0101'
tracks[2][3] = '1001'
tracks[3][0] = '1100'
tracks[3][1] = '0011'
tracks[3][2] = '0101'
tracks[3][3] = '1001'
tracks[0][4] = '0110'
tracks[1][4] = '1100'
tracks[2][4] = '0110'
tracks[3][4] = '0101'
tracks[4][0] = '1001'
tracks[4][1] = '0011'
tracks[4][2] = '1010'
tracks[4][3] = '0101'
tracks[4][4] = '1001'

playingSolution = False

def getDigit(s, i):
    return int(s[i])

def makeGridButtons():
    return [[Button(j * TRACK_SIZE, i * TRACK_SIZE, EMPTY, 1) for j in range(TRACK_SIZE)] for i in range(TRACK_SIZE)]

def rotateTrack(tracks, i, j):
    if not playingSolution:
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
    
def checkSolution(): #constantly being checked if the player has found the solution
    i, j = (4, 0)
    dir = 'U'
    while(True):
        if(i == 0 and j == SIZE):
            return True
        if dir == 'U':
            if i == 0:
                return False
            if not getDigit(tracks[i - 1][j], 2):
                return False
            i -= 1
            if getDigit(tracks[i][j], 0):
                dir = 'L'
            elif getDigit(tracks[i][j], 3):
                dir = 'R'
        if dir == 'L':
            if j == 0:
                return False
            if not getDigit(tracks[i - 1][j], 3):
                return False
            j -= 1
            if getDigit(tracks[i][j], 1):
                dir = 'U'
            elif getDigit(tracks[i][j], 2):
                dir = 'D'
        if dir == 'D':
            if i == SIZE - 1:
                return False
            if not getDigit(tracks[i + 1][j], 1):
                return False
            i += 1
            if getDigit(tracks[i][j], 0):
                dir = 'L'
            elif getDigit(tracks[i][j], 3):
                dir = 'R'
        if dir == 'R':
            if i == 0 and j ==  SIZE - 1:
                return True
            if j == SIZE - 1:
                return False
            if not getDigit(tracks[i][j + 1], 0):
                return False
            j += 1
            if getDigit(tracks[i][j], 1):
                dir = 'U'
            elif getDigit(tracks[i][j], 2):
                dir = 'D'
    
    
def drawGrid():
    for i in range(SIZE):
        for j in range(SIZE):
            #pygame.draw.rect(WINDOW, (47, 35, 158), (j * TRACK_SIZE, i * TRACK_SIZE, TRACK_SIZE, TRACK_SIZE), GRID_THICKNESS)
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
    WINDOW.blit(ENTRANCE, (0, 5 * TRACK_SIZE))
    WINDOW.blit(EXIT, (5 * TRACK_SIZE, 0))
    pygame.display.update()

def mainMenu(startButton):
    WINDOW.fill(MAIN_MENU_BACKGROUND)
    WINDOW.blit(TITLE, (40, 200))
    if startButton.draw():
        return True
    pygame.display.update()
    return False

def drawWinScreen(resetButton):
    WINDOW.fill(WIN_BACKGROUND)
    WINDOW.blit(WIN, (200, 200))
    if resetButton.draw():
        return True
    pygame.display.update()
    return False

def resetGame():
    tracks[0][0] = '1010'
    tracks[0][1] = '1001'
    tracks[0][2] = '0011'
    tracks[0][3] = '1001'
    tracks[1][0] = '0011'
    tracks[1][1] = '0101'
    tracks[1][2] = '1100'
    tracks[1][3] = '1001'
    tracks[2][0] = '0101'
    tracks[2][1] = '1100'
    tracks[2][2] = '0101'
    tracks[2][3] = '1001'
    tracks[3][0] = '1100'
    tracks[3][1] = '0011'
    tracks[3][2] = '0101'
    tracks[3][3] = '1001'
    tracks[0][4] = '0110'
    tracks[1][4] = '1100'
    tracks[2][4] = '0110'
    tracks[3][4] = '0101'
    tracks[4][0] = '1001'
    tracks[4][1] = '0011'
    tracks[4][2] = '1010'
    tracks[4][3] = '0101'
    tracks[4][4] = '1001'


def main():
    clock = pygame.time.Clock()
    run = True
    gridButtons = makeGridButtons()
    startButton = Button(300, 450, START_IMG, 1)
    resetButton = Button(300, 450, RESTART_IMG, 1)


    mainMenuScreen = True
    startGame = False


    while run: #Game Loop
        clock.tick(FPS)
        for event in pygame.event.get(): #Ends game when user quits
            if event.type == pygame.QUIT:
                run = False
        #Handle game loops here
        if startGame:
            handleTrackClicks(gridButtons)
            draw() #the game is constantly drawing and updating the screen
            if checkSolution():
                mixer.music.play()
                pygame.time.delay(2000)
                startGame = False
                winScreen = True
        elif mainMenuScreen:
            if mainMenu(startButton):
                startGame = True
                mainMenuScreen = False
        elif winScreen:
            if drawWinScreen(resetButton):
                startGame = True
                winScreen = False
                resetGame()
    pygame.quit()

if __name__ == "__main__": #only runs the game if this specific file is run
    main()