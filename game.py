import pygame
import os
#from button import Button

WIDTH, HEIGHT = 700, 700 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miner Mania") #game name displayed on window

#----CONSTANTS----
BACKGROUND = (38, 50, 70) #background color
MAIN_MENU_BACKGROUND = (196, 195, 186)
GAMEOVER_BACKGROUND = (247, 81, 81)
TITLE_SCALE = 0.85
GAMEOVER_SCALE = 0.7
FPS = 10 #caps the refresh rate so the game is consistent
SIZE = 4 #board dimensions
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

CAR_IMG = pygame.image.load(os.path.join('Assets', 'car.png'))
VERTICAL_CAR = pygame.transform.scale(CAR_IMG, (TRACK_SIZE, TRACK_SIZE))
HORIZONTAL_CAR = pygame.transform.rotate(VERTICAL_CAR, -90)

EMPTY = pygame.image.load(os.path.join('Assets', 'empty.png'))
TITLE_IMG = pygame.image.load(os.path.join('Assets', 'title.png'))
TITLE = pygame.transform.scale(TITLE_IMG, (int(TITLE_SCALE * TITLE_IMG.get_width()), int(TITLE_SCALE * TITLE_IMG.get_height())))
START_IMG = pygame.image.load(os.path.join('Assets', 'startButton.png'))
RESTART_IMG = pygame.image.load(os.path.join('Assets', 'restart.png'))
GAMEOVER_IMG = pygame.image.load(os.path.join('Assets', 'gameover.png'))
GAMEOVER_MESSAGE = pygame.transform.scale(GAMEOVER_IMG, (int(GAMEOVER_SCALE * GAMEOVER_IMG.get_width()), int(GAMEOVER_SCALE * GAMEOVER_IMG.get_height())))

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
tracks[2][2] = '1001'
tracks[2][3] = '1001'
tracks[3][0] = '0110'
tracks[3][1] = '0110'
tracks[3][2] = '0101'
tracks[3][3] = '1001'

car = {'trackPos': (3, 0), 'pixPos': (0, 4 * TRACK_SIZE), 'dir': 'U'} #all the different possible directions are LUDR

def getDigit(s, i):
    return int(s[i])

def makeGridButtons():
    return [[Button(j * TRACK_SIZE, i * TRACK_SIZE, EMPTY, 1) for j in range(TRACK_SIZE)] for i in range(TRACK_SIZE)]

def rotateTrack(tracks, i, j):
    if car['trackPos'] != (1, j):
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
    pixPosList = list(car['pixPos'])
    if car['dir'] == 'L':
        pixPosList[0] -= CAR_SPEED
    elif car['dir'] == 'U':
        pixPosList[1] -= CAR_SPEED
    elif car['dir'] == 'D':
        pixPosList[1] += CAR_SPEED
    elif car['dir'] == 'R':
        pixPosList[0] += CAR_SPEED
    car['pixPos'] = tuple(pixPosList)
    

def carCollision():
    if car['pixPos'][0] < 0 or car['pixPos'][0] > (SIZE - 1) * TRACK_SIZE + 30:
        return True
    if car['pixPos'][1] < 0 or car['pixPos'][1] > SIZE * TRACK_SIZE:
        return True
    if car['dir'] == 'L':
        if car['trackPos'][1] == 0:
            return False
        if car['pixPos'][0] < car['trackPos'][1] * TRACK_SIZE + 20:
            if not getDigit(tracks[car['trackPos'][0], car['trackPos'][1] - 1], 3):
                return False
            elif getDigit(tracks[car['trackPos'][0], car['trackPos'][1] - 1], 1):
                car['dir'] = 'U'
                pixPosList = list(car['pixPos'])
                pixPosList[0] = (car['trackPos'][1] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
                trackPosList = list(car['trackPos'])
                trackPosList[1] = car['trackPos'][1] - 1
                car['trackPos'] = tuple(trackPosList)
            elif getDigit(tracks[car['trackPos'][0], car['trackPos'][1] - 1], 2):
                car['dir'] = 'D'
                pixPosList = list(car['pixPos'])
                pixPosList[0] = (car['trackPos'][1] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
                trackPosList = list(car['trackPos'])
                trackPosList[1] = car['trackPos'][1] + 1
                car['trackPos'] = tuple(trackPosList)
    elif car['dir'] == 'U':
        if car['trackPos'][0] == 0:
            return False
        if car['pixPos'][1] < car['trackPos'][0] * TRACK_SIZE + 20:
            if not getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 2):
                return False
            elif getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 0):
                car['dir'] = 'L'
                pixPosList = list(car['pixPos'])
                pixPosList[1] = (car['trackPos'][0] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
            elif getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 3):
                car['dir'] = 'R'
                pixPosList = list(car['pixPos'])
                pixPosList[1] = (car['trackPos'][0] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
    elif car['dir'] == 'D':
        if car['trackPos'][0] == 0:
            return False
        if car['pixPos'][1] < car['trackPos'][0] * TRACK_SIZE + 20:
            if not getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 2):
                return False
            elif getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 0):
                car['dir'] = 'L'
                pixPosList = list(car['pixPos'])
                pixPosList[1] = (car['trackPos'][0] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
            elif getDigit(tracks[car['trackPos'][0] - 1, car['trackPos'][1]], 3):
                car['dir'] = 'R'
                pixPosList = list(car['pixPos'])
                pixPosList[1] = (car['trackPos'][0] - 1) * TRACK_SIZE
                car['pixPos'] = tuple(pixPosList)
    elif car['dir'] == 'R':
        pass
    return False

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
    if car['dir'] == 'U' or car['dire'] == 'D':
        WINDOW.blit(VERTICAL_CAR, (car['pixPos'][0] , car['pixPos'][1]))
    else:
        WINDOW.blit(HORIZONTAL_CAR, (car['pixPos'][0] , car['pixPos'][1]))
    updateCar()
    pygame.display.update()

def mainMenu(startButton):
    WINDOW.fill(MAIN_MENU_BACKGROUND)
    WINDOW.blit(TITLE, (40, 200))
    if startButton.draw():
        return True
    pygame.display.update()
    return False

def gameOver(restartButton):
    WINDOW.fill(GAMEOVER_BACKGROUND)
    WINDOW.blit(GAMEOVER_MESSAGE, (65, 200))
    if restartButton.draw():
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
    tracks[2][2] = '1001'
    tracks[2][3] = '1001'
    tracks[3][0] = '0110'
    tracks[3][1] = '0110'
    tracks[3][2] = '0101'
    tracks[3][3] = '1001'
    car['trackPos'] = (3, 0)
    car['pixPos'] = (0, 4 * TRACK_SIZE)
    car['dir'] = 'U'


def main():
    clock = pygame.time.Clock()
    run = True
    gridButtons = makeGridButtons()
    startButton = Button(300, 450, START_IMG, 1)
    restartButton = Button(300, 450, RESTART_IMG, 1)

    wait = True

    mainMenuScreen = True
    startGame = False
    gameOverScreen = False


    while run: #Game Loop
        clock.tick(FPS)
        for event in pygame.event.get(): #Ends game when user quits
            if event.type == pygame.QUIT:
                run = False
        #Handle game loops here
        if startGame:
            #if wait:
            #    pygame.time.delay(1000)
            #    wait = False
            handleTrackClicks(gridButtons)
            draw() #the game is constantly drawing and updating the screen
            if carCollision():
                gameOverScreen = True
                startGame = False
        elif mainMenuScreen:
            if mainMenu(startButton):
                startGame = True
                mainMenuScreen = False
        elif gameOverScreen:
            if gameOver(restartButton):
                resetGame()
                startGame = True
                gameOverScreen = False
    pygame.quit()

if __name__ == "__main__": #only runs the game if this specific file is run
    main()