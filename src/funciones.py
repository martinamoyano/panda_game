import pygame, json, re
from random import randint
from classItem import Coin
from classBoton import Boton

pygame.mixer.init()
coin_sound = pygame.mixer.Sound(r"src\sounds\coin.mp3")
energy_sound = pygame.mixer.Sound(r"src\sounds\energy.mp3")
live_sound = pygame.mixer.Sound(r"src\sounds\live_pickup.wav")



'''------------------------ LIMITES MOVIMIENTO EN PANTALLA ------------------------------'''

def limites(player, width, height):
    """
    Limita el movimiento de un jugador dentro de un ancho y alto específicos.

    Args:
        player (pygame.sprite.Sprite): El objeto de jugador para limitar el movimiento.
        width (int): El ancho máximo del área del juego.
        height (int): La altura máxima del área del juego.

    Returns:
        None

    Esta función verifica la posición del rectángulo del jugador y lo ajusta si excede los límites del área del juego. El rectángulo del jugador se ajusta a la parte derecha del área del juego si su borde derecho es mayor que el ancho. El rectángulo del jugador se ajusta a la parte izquierda del área del juego si su borde izquierdo es menor que 0. El rectángulo del jugador se ajusta a la parte inferior del área del juego menos 10 píxeles si su borde inferior es mayor que la altura menos 10. El rectángulo del jugador se ajusta a la parte superior del área del juego más 60 píxeles si su borde superior es menor que 60.
    """
    try:
        if player.rect.right > width:
            player.rect.right = width
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.bottom > height - 10:
            player.rect.bottom = height - 10
        if player.rect.top < 60:
            player.rect.top = 60
    except AttributeError:
        print("El objeto 'player' debe tener un atributo 'rect'.")

'''------------------------ CARGAR LISTAS ------------------------------'''

def cargar_coins (cantidad: int, width, height) -> list:
    coin_list = []
    for i in range (cantidad):
        coin = Coin ((20,20), (randint(25,width-25),randint(68,height-25)), r"src\coin.png")
        coin_list.append(coin)
    return coin_list

def cargar_coins(cantidad: int, width, height) -> list:
    """
    Crea una lista de monedas con posiciones aleatorias.

    Args:
        cantidad (int): Cantidad de monedas a crear.
        width (int): Ancho del área del juego.
        height (int): Altura del área del juego.

    Returns:
        list: Lista de objetos Coin.
    """
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad de monedas debe ser un entero positivo")

    coin_list = []
    for i in range(cantidad):
        coin = Coin((20, 20), (randint(25, width-25), randint(68, height-25)), r"src\coin.png")
        coin_list.append(coin)
    return coin_list

'''---------------------------- FUENTE --------------------------------------'''

def fuente(tamaño_fuente: int, nombre_fuente : str = None) -> pygame.font.Font:
    """
    Crea y devuelve una fuente de Pygame con el tamaño especificado.

    Args:
        tamaño_fuente (int): El tamaño de la fuente a crear.
        nombre_fuente (str): Nombre de la fuente que se va a utilizar, si no se especifica se establece en None.

    Returns:
        pygame.font.Font: Una instancia de la fuente con el tamaño especificado.
    """
    font = pygame.font.SysFont(nombre_fuente, tamaño_fuente)
    return font

'''---------------------------- BLITEO --------------------------------------'''

def blitear_textos(screen, font, texto: str, posicion: tuple , color = (0, 0 ,0)) -> None:
    """
    Dibuja texto en pantalla en la posición especificada con la fuente y color dados.

    Args:
        screen (pygame.Surface): La superficie de la pantalla donde se dibujará el texto.
        font (pygame.font.Font): La fuente utilizada para dibujar el texto.
        texto (str): El texto que se desea dibujar.
        posicion (tuple): Coordenadas donde comenzará a dibujar el texto.
    """
    if type (texto) != str:
        texto = str(texto)
    textos = font.render (texto, True, color)
    screen.blit (textos, posicion)

def blitear_imagen(screen, path, dimension: tuple, posicion: tuple) -> None :
    """
    Dibuja una imagen en pantalla en la posición especificada con el tamaño dado.

    Args:
        screen (pygame.Surface): La superficie de la pantalla donde se dibujará la imagen.
        path (str): La ruta del archivo de imagen que se desea dibujar.
        dimension (tuple): Dimensión de la imagen después de ser escalada.
        posicion (tuple): Coordenadas donde se dibujará la imagen.
    """
    imagen_surface = pygame.image.load (path)
    imagen_surface = pygame.transform.scale (imagen_surface, dimension)
    screen.blit (imagen_surface, posicion)

def blitear_cant_projectiles(screen, player):
    blitear_imagen(screen, r'src\panda_projectile.png', (27, 27), (140, 18))
    # if player.projectiles >= 0:
    #     blitear_textos(screen, fuente(30), f'x{player.projectiles}', (170,33))
    # else:
    blitear_textos(screen, fuente(30), f'x{player.projectiles}', (170,23))

def blitear_lives(screen, player):#MODULARIZAR
    lives_x = 25 
    for i in range(player.lives):
        blitear_imagen(screen, r'src\live_heart.png', (35,35), (lives_x,15))
        lives_x += 30

def blitear_coins(screen, coin_list):
    for coin in coin_list:
        if coin.get_activo() == True:
            screen.blit(coin.get_imagen(), coin.get_rect()) ##

def blitear_disparos(screen, projectiles_list, height, width):
    for projectil in projectiles_list:
        if projectil.get_activo() == True:
            projectil.movimiento(height, width)
            screen.blit(projectil.get_imagen(), projectil.get_rect())
        else:
            projectiles_list.remove(projectil)

'''------------------------ COLISIONES ----------------------------'''

def punto_en_rectangulo(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def detectar_colision(rect_1, rect_2):
    for r1, r2 in [(rect_1,rect_2),(rect_2,rect_1)]:
        if punto_en_rectangulo(r1.topleft,r2) or \
            punto_en_rectangulo(r1.topright,r2) or \
            punto_en_rectangulo(rect_1.bottomleft, r2) or\
            punto_en_rectangulo(rect_1.bottomright, r2):
            return True
        else:
            return False

def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int]) -> float :
    base = pto_1[0] - pto_2[0]
    altura = pto_1[1] - pto_2[1]
    return (base ** 2 + altura ** 2) ** 0.5

def calcular_radio(rect):
    return rect.width // 2

def detectar_colision_circulo(rect_1, rect_2) -> bool :
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    base = rect_1.centerx - rect_2.centerx
    altura = rect_1.centery - rect_2.centery
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

def coin_colision(coin_list, player):
    for coin in coin_list:
        if detectar_colision_circulo(coin.get_rect(), player.rect):
            coin.set_activo(False)
            player.score += 100
            coin_list.remove(coin)
            
            coin_sound.play()

def projectil_colision_enemy(projectiles_list, enemy, player):
    for projectile in projectiles_list:
        if detectar_colision_circulo (projectile.get_rect(), enemy.rect):
            projectile.set_activo (False)
            projectiles_list.remove(projectile)
            enemy.activo = False
            player.score += 200

def booster_colision (booster, player, current_time, next_booster_spawn_time, booster_end_time):
    if detectar_colision_circulo (booster.get_rect(), player.rect) and booster.get_activo():
        booster.set_activo (False)
        player.speed += 10
        booster_end_time = current_time + 8000
        next_booster_spawn_time = current_time + 10000 

        energy_sound.play()
    
    return next_booster_spawn_time, booster_end_time

def live_colision(extra_lives_list, player):
    for live in extra_lives_list:
        if detectar_colision_circulo(live.get_rect(), player.rect):
            live.set_activo(False)
            player.lives += 1
            extra_lives_list.remove(live)
            
            live_sound.play()


def projectil_extra_colision(extra_projectiles_list, player):
    for proyectil in extra_projectiles_list:
        if detectar_colision_circulo(proyectil.get_rect(), player.rect):
            proyectil.set_activo(False)
            extra_projectiles_list.remove(proyectil)
            player.projectiles = 10
            
def colision_enemy(enemy, player):
    if detectar_colision_circulo(enemy.rect, player.rect):
        if player.get_activo():
            player.lives -= 1
            player.set_activo(False)

def colision_botones_scores (event, boton_return: Boton) -> None: #########
    if (boton_return.get_rect().collidepoint(event.pos)):
        boton_return.colisionar()
    else:
        boton_return.quitar_colision()
        pygame.mouse.set_system_cursor (pygame.SYSTEM_CURSOR_ARROW)

def click_botones_scores (event, run, boton_return: Boton) -> bool: 
    if (boton_return.get_rect().collidepoint(event.pos)): #inicia juego
        run = False
        boton_return.quitar_colision()
    
    return run

'''---------------------------- JSON Y CSV -------------------------------'''

def parser_json (path: str, clave: str) -> list | dict:
    retorno = []

    try:
        with open (path, "r", encoding= "utf8") as archivo:
            diccionario = json.load(archivo)
        
        retorno = diccionario[clave]
    except FileNotFoundError:
        print ("El archivo no existe o la ruta es incorrecta")

    return retorno

def parser_csv (path: str)-> dict:
    try:
        with open (path, "r", encoding= "utf8") as archivo:
            clave = re.split (",|\n", archivo.readline())
            
            for lineas in archivo:
                registro = re.split (",|\n", lineas)
                
                diccionario = {}
                diccionario = {
                clave[0]: registro [0],
                clave[1]: registro [1]
                }
    except FileNotFoundError:
        print ("El archivo no existe o la ruta es incorrecta")
    
    return diccionario

def actualizar_json(path: str, clave: str, elemento):
    try:
        diccionario = {}
        diccionario[clave] = elemento

        with open(path, "w", encoding="utf8") as archivo:
            json.dump(diccionario, archivo, indent=4)
    except KeyError:
        print("La clave no existe en el diccionario")
    except FileNotFoundError:
        print("El archivo no existe o la ruta es incorrecta")