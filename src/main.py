import pygame
from instancias_juego import *
from settings import *

def main():
    pygame.init()
	
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PANDA'S JUNGLE RUN")
    pygame.display.set_icon(pygame.image.load(r"src\icon.png"))
        
    menu (SCREEN)
    score = game(SCREEN)
    game_over (SCREEN, score)
    pygame.quit()

if __name__ == "__main__":
    main() 
