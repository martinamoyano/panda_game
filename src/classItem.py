import pygame

class Item:
    def __init__(self, dimension: tuple, centro: tuple, imagen: str) -> None:
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, dimension)
        self.dimension = dimension
        self.rect = self.imagen.get_rect()
        self.rect.center = centro
        self.activo = True
    
    def get_imagen(self):
        return self.imagen

    def set_imagen(self, value: str):
        self.imagen = pygame.image.load(value)
        self.imagen = pygame.transform.scale(self.imagen, self.dimension)
        self.rect = self.imagen.get_rect() 

    def get_rect(self):
        return self.rect

    def set_rect(self, value: pygame.Rect):
        self.rect = value

    def get_activo(self):
        return self.activo

    def set_activo(self, value: bool):
        self.activo = value

    def get_dimension(self):
        return self.imagen.get_size()

    def set_dimension(self, value: tuple):
        self.imagen = pygame.transform.scale(self.imagen, value)
        self.rect = self.imagen.get_rect() #actualizo

    def get_centro(self):
        return self.rect.center

    def set_centro(self, value: tuple):
        self.rect.center = value

class Coin (Item):
    def __init__(self, dimension: tuple, centro: tuple, imagen: str) -> None:
        super().__init__(dimension, centro, imagen)

class Live (Item):
    def __init__(self, dimension: tuple, centro: tuple, imagen: str) -> None:
        super().__init__(dimension, centro, imagen)

class Booster (Item):
    def __init__(self, dimension: tuple, centro: tuple, imagen: str) -> None:
        super().__init__(dimension, centro, imagen)

#################################QUITAR ESTA BASURA

class Projectile (Item):
    def __init__(self, dimension: tuple, centro: tuple, imagen: str, movement: int ) -> None:
        super().__init__(dimension, centro, imagen)
        self.movement = movement
        self.speed = 15

    def movimiento(self, height, width):
        match self.movement:
            case 1:
                if self.rect.top <= height: #down
                    self.rect.y += self.speed
                else:
                    self.activo = False
            
            case 2:
                if self.rect.left <= width: #right
                    self.rect.x += self.speed
                else:
                    self.activo = False
            
            case 3: 
                if self.rect.left >= 0: #left
                    self.rect.x -= self.speed 
                else:
                    self.activo = False

            case 4: 
                if self.rect.bottom >= 75: #up / 75 = borde bambu
                    self.rect.y -= self.speed 
                else:
                    self.activo = False