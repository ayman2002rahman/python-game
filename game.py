import pygame
#import os

WIDTH, HEIGHT = 900, 500 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Railroad-Mania") #game name displayed on window

#----CONSTANTS----
BACKGROUND = (38, 50, 70) #background color
FPS = 60 #caps the refresh rate so the game is consistent

#----IMAGES-------
#RAILROAD_IMG = pygame.image.load(os.path.join('Assets', 'straight.png'))

def draw():
    WINDOW.fill(BACKGROUND)
    #WINDOW.blit(RAILROAD_IMG, (550, 950))
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