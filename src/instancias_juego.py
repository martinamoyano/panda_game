import pygame, sys
from random import randint
from enemy import Enemy
from player import Panda
from classItem import *
from funciones import *
from pantallas import *
from settings import *
from classBoton import *
from classTextbox import *


def menu_screen(screen, boton_play: Boton, boton_score: Boton, boton_options: Boton, boton_salir: Boton) -> None: 
    """
    Función para mostrar la pantalla de menú con botones y imagen de fondo.

    Args:
        screen (Surface de Pygame): Objeto que representa la pantalla del juego.
        boton_play (Botón): Objeto del botón de comenzar.
        boton_score (Botón): Objeto del botón de puntuación.
        boton_options (Botón): Objeto del botón de opciones.

    Devuelve:
        None
    """
    best_player = parser_csv (r"src\jugadores.csv")
    
    blitear_imagen(screen, r"src\AC Fat Bamboo.png", (WIDTH, HEIGHT),(0, 0))
    
    #Botones
    screen.blit(boton_play.get_imagen_surface(), boton_play.get_rect())
    screen.blit(boton_score.get_imagen_surface(), boton_score.get_rect())
    screen.blit(boton_options.get_imagen_surface(), boton_options.get_rect())
    screen.blit(boton_salir.get_imagen_surface(), boton_salir.get_rect())

    blitear_textos (screen, fuente(20, "Emulogic"), f"Best player: {best_player['name']}", (20, 20))
    #Actualizamos pantalla
    pygame.display.update()

def scores_screen(screen, boton_return: Boton) -> None:
  
    #Fondo
    blitear_imagen(screen, r"src\fondo.png", (WIDTH, HEIGHT),(0, 0))

    #Botones
    screen.blit(boton_return.get_imagen_surface(), boton_return.get_rect())
    

    player_list = parser_json (r"src\jugadores.json", "jugadores")
    x = 100
    y = 50
    for player in player_list:
        blitear_textos(screen, fuente(30, "arial"), f"{player["name"]:20}{player["score"]}", (x,y))
        y += 50
        if y > 500:
            break

    #Actualizamos pantalla
    pygame.display.update()

def colisionar_boton (boton: Boton, boton_a: Boton) -> None:
    if boton_a.get_colision() == True:
        boton_a.quitar_colision()

    boton.colisionar()

def colisiones_botones_menu (event, boton_play: Boton, boton_score: Boton, boton_options: Boton, boton_salir: Boton) -> None:
    if (boton_play.get_rect().collidepoint(event.pos)):
        colisionar_boton (boton_play, boton_score)
    elif (boton_score.get_rect().collidepoint(event.pos)):
        colisionar_boton (boton_score, boton_play)
    elif (boton_options.get_rect().collidepoint(event.pos)):
        colisionar_boton (boton_options, boton_play)
    elif (boton_salir.get_rect().collidepoint(event.pos)):
        colisionar_boton (boton_salir, boton_play)
    else:
        boton_play.quitar_colision()
        boton_score.quitar_colision()
        boton_options.quitar_colision()
        boton_salir.quitar_colision()
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

def click_botones_menu (event, run: bool, scores: bool, options: bool, boton_play: Boton, boton_score: Boton, boton_options: Boton, boton_salir: Boton) -> bool:
    
    if (boton_play.get_rect().collidepoint(event.pos)):
        run = False

    elif (boton_score.get_rect().collidepoint(event.pos)):
        scores = True

    elif (boton_options.get_rect().collidepoint(event.pos)):
        options = True
    
    elif (boton_salir.get_rect().collidepoint(event.pos)):
        pygame.quit()
        sys.exit()

    return run, scores, options

def menu (screen):
    boton_play =  Boton ((155,430), (220,55), r"src\buttons\boton_comenzar.png", r"src\buttons\boton_comenzar_activo.png")
    boton_score =  Boton ((410,430), (220,55), r"src\buttons\boton_puntajes.png", r"src\buttons\boton_opciones_activo.png")
    boton_options =  Boton ((670,430), (215,50), r"src\buttons\boton_opciones.png", r"src\buttons\boton_opciones_activo.png")
    boton_salir =  Boton ((410, 510), (215,50), r"src\buttons\boton_salir.png", r"src\buttons\boton_salir_activo.png")
    
    run = True
    scores = False
    options = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                colisiones_botones_menu (event, boton_play, boton_score, boton_options, boton_salir)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                run, scores, options = click_botones_menu (event, run, scores, options, boton_play, boton_score, boton_options, boton_salir)

        if scores == True:
            run_scores (screen)
            scores = False
        elif options == True:
            run_scores (screen)
            options = False

        menu_screen (screen, boton_play, boton_score, boton_options, boton_salir)
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


def run_scores (screen):
    boton_return = Boton ((50,50), (75,60), r"src\back-158491_640.webp", r"src\check-markimage-search-results-picture-icon-boton-check-115533860879whjy7sk3g.png")
    
    run = True
    while run:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                colision_botones_scores (event, boton_return)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                run = click_botones_scores (event, run, boton_return)

        scores_screen (screen, boton_return)
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
def game (screen):
    pygame.mixer.init()
    clock = pygame.time.Clock()
    player = Panda(SCREEN_CENTER, 3,0, 5, 10, r"src\panda.png") 
    initial_speed = player.speed

    enemies_list = []
    enemy = Enemy(((WIDTH // 2), 25))
    enemies_list.append(enemy)

    booster = Booster((60, 40), (randint(25,WIDTH-25),randint(66,HEIGHT-25)), r'src\energy_booster.png')
    booster.set_activo(False)

    player.image = player.sheet.subsurface(player.sheet.get_clip())

    pygame.mixer.music.load(r'src\Y2meta.app - Donkey Kong Country Music SNES - DK Island Swing (128 kbps).mp3') 
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1) 

    cantidad_monedas = 10
    coin_list = cargar_coins (cantidad_monedas, WIDTH, HEIGHT)
    projectiles_list = []
    extra_lives_list = []
    extra_projectiles_list = []

    next_projectile_spawn_time = pygame.time.get_ticks() + randint(10000, 30000)
    next_life_spawn_time = pygame.time.get_ticks() + randint(10000, 30000)  
    next_booster_spawn_time = pygame.time.get_ticks() + 20000
    booster_end_time = 0

    is_running = True

    tiempo_reaparicion = 20000
    next_enemie_spawn_time = pygame.time.get_ticks() + tiempo_reaparicion

    velocidad_enemigos = 5

    inmune = False
    while is_running:

        if player.get_activo() == False and inmune == False:
            pygame.time.set_timer(pygame.USEREVENT, 400)
            inmune = True
        
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                inmune = False
                player.set_activo(True)
            player.handle_event(event, projectiles_list)

        coin_colision(coin_list, player)

        for enemy in enemies_list:
            if enemy.activo == True:
                colision_enemy(enemy, player)
                projectil_colision_enemy(projectiles_list, enemy, player)
            else:
                enemies_list.remove(enemy)

        projectil_extra_colision(extra_projectiles_list, player)

        next_booster_spawn_time, booster_end_time = booster_colision(booster, player, current_time, next_booster_spawn_time, booster_end_time)

        if booster_end_time <= current_time and initial_speed < player.speed:
            player.speed -= 10

            next_booster_spawn_time = current_time + 20000  

            booster_end_time = current_time + 5000
            booster.set_centro((randint(25,WIDTH-25),randint(25,HEIGHT-25)))
        
        live_colision(extra_lives_list, player)

        if player.lives == 0:
            is_running = False  
                
        player.update()
        for enemy in enemies_list:
            enemy.enemy_sprites.update()
            enemy.movimiento(HEIGHT, WIDTH)
        
        limites(player, WIDTH, HEIGHT)

        hay_monedas = False
        for coin in coin_list:
            if coin.get_activo() == True:
                hay_monedas = True
                break
        
        if hay_monedas == False:
            if tiempo_reaparicion > 5000:
                tiempo_reaparicion -= 5000
            else:
                tiempo_reaparicion = 2000
            
            velocidad_enemigos += 1
            for enemigo in enemies_list:
                enemigo.speed = velocidad_enemigos

            cantidad_monedas += 5

            coin_list = cargar_coins (cantidad_monedas, WIDTH, HEIGHT)

        if player.lives < 3 and current_time >= next_life_spawn_time: #### MODULO
            vida = Live((30, 30), (randint(10, WIDTH - 10), randint(66, HEIGHT - 10)), r"src\live_heart.png")
            extra_lives_list.append(vida)
            next_life_spawn_time = current_time + randint(10000, 30000)  
        
        if player.projectiles == 0 and current_time >= next_projectile_spawn_time:
            proyectil = Projectile((15, 15), (randint(10, WIDTH - 10), randint(10, HEIGHT - 10)), r"src\panda_projectile.png", 0)
            extra_projectiles_list.append(proyectil)
            next_projectile_spawn_time = current_time + randint(10000, 30000)

        if current_time >= next_enemie_spawn_time:
            enemy = Enemy((randint(10, WIDTH - 10), -10))
            enemies_list.append(enemy)

            next_enemie_spawn_time = pygame.time.get_ticks() + tiempo_reaparicion

        if booster.get_activo() == False and current_time >= next_booster_spawn_time:
            booster.set_activo(True)

        game_screen(screen, player, fondo, enemies_list, coin_list, projectiles_list, extra_projectiles_list, extra_lives_list, WIDTH, HEIGHT, booster)
        clock.tick(30)
    scores = player.score
    return scores

def actualizar_csv (path, player):
        with open(path, "w", encoding="utf-8") as file:
            file.write("name,score\n")
            file.write(player["name"] + "," + str(player["score"]))

def game_over (screen, score):
    alto = fuente(60).size("W" * 10)[1]
    textbox = Textbox ((290, 490), (250, alto), (80, 142, 17))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    textbox.text = textbox.text[:-1]
                else:
                    if event.unicode.isalpha() and len (textbox.text) <= 12:
                        textbox.text += event.unicode.upper()

                textbox.set_width (max (fuente(60).size(textbox.text)[0] + 10, 250))

        gameover_screen (screen, score, textbox)
    
    ###################################### EXPORTAR ############################################
    player = {
        "score": score,
        "name": textbox.text
    }

    player_list = parser_json (r"src\jugadores.json", "jugadores")
    player_list.append (player)
    player_list.sort(key=lambda x: x["score"], reverse=True)
    best_player = player_list[0]
    actualizar_csv (r"src\jugadores.csv", best_player)
    actualizar_json (r"src\jugadores.json", "jugadores", player_list)

    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)