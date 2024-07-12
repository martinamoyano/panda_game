import pygame
from funciones import *
from classTextbox import *

fondo = pygame.image.load(r'src\fondo.png')
marco = pygame.image.load(r'src\marco_bambu.png')

#BLITEO PANTALLA GAME OVER
def gameover_screen(screen, score, textbox: Textbox) -> None:

    fondo_game_over = pygame.image.load(r'src\fondo_game_over.png')
    
    screen.blit(fondo_game_over, (0,0))

    pygame.draw.rect(screen, textbox.color, textbox.get_rect(), 2)

    blitear_textos(screen, fuente(25, 'Emulogic'), textbox.get_text(), (textbox.get_x() + 5, textbox.get_y() + 3))
    blitear_textos(screen, fuente(25, 'Emulogic'), f"Score: {score}", (280, 380))
    blitear_textos(screen, fuente(20, 'Emulogic'), f"Ingresa tu nombre: ", (215, 435))
    
    pygame.display.flip()

#BLITEO PANTALLA GAME
def game_screen(screen, player, fondo, enemies_list, coin_list, projectiles_list, extra_projectiles_list, extra_lives_list, width, height, booster) -> None:
    
    screen.blit(fondo, (0,0))

    for enemy in enemies_list:
        if enemy.activo == True:
            enemy.enemy_sprites.draw(screen)

    screen.blit(marco, (0,0))
    
    if player.speed > 5:  #no es correcto seria mejor el atributo player.booster
        screen.blit(booster.get_imagen(), (200,12))

    blitear_lives(screen, player)
    
    blitear_cant_projectiles(screen, player)

    blitear_textos(screen, fuente(35), f"Score: {player.score}", (600, 20))
    blitear_coins(screen, coin_list)

    
    if player.get_activo():
        screen.blit(player.image, player.rect)
    
    for vidas in extra_lives_list:
        if vidas.get_activo() == True:
            screen.blit(vidas.get_imagen(), vidas.get_rect()) #####

    if booster.get_activo():
        screen.blit(booster.get_imagen(), booster.get_rect())

    for proyectil in extra_projectiles_list:
        if proyectil.get_activo() == True:
            screen.blit(proyectil.get_imagen(), proyectil.get_rect())

    if len(projectiles_list) > 0:
        blitear_disparos(screen, projectiles_list, height, width)

    pygame.display.update()