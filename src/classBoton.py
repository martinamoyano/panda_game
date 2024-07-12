import pygame
class Boton:
    def __init__(self, origen: tuple, dimesion: tuple, path: str, path_colision: str) -> None:
        self.imagen_no_colision = path
        self.imagen = path
        self.imagen_surface = pygame.image.load(path).convert_alpha()
        self.imagen_surface = pygame.transform.scale(self.imagen_surface, dimesion)
        self.imagen_colision = path_colision
        self.colision = False
        self.origen = origen
        self.dimension = dimesion
        self.rect = self.imagen_surface.get_rect()
        self.rect.center = origen


    # Getters
    def get_imagen(self) -> str:
        return self.imagen

    def get_imagen_colision(self) -> str:
        return self.imagen_colision
    
    def get_imagen_no_colision(self) -> str:
        return self.imagen_no_colision
    
    def get_imagen_surface(self) -> str:
        return self.imagen_surface

    def get_colision(self) -> bool:
        return self.colision

    def get_origen(self) -> tuple:
        return self.origen

    def get_dimension(self) -> tuple:
        return self.dimension

    def get_rect(self) -> pygame.Rect:
        return self.rect

    # Setters
    def set_imagen(self, imagen: str) -> None:
       
        self.imagen = imagen
        self.imagen_surface = pygame.image.load(imagen)
        self.imagen_surface = pygame.transform.scale(self.imagen_surface, self.dimension)

    def set_imagen_colision(self, imagen_colision: str) -> None:
        self.imagen_colision = imagen_colision

    def set_colision(self, colision: bool) -> None:
        self.colision = colision
        if colision:
            self.imagen_surface = pygame.image.load(self.imagen_colision)
        else:
            self.imagen_surface = pygame.image.load(self.imagen_no_colision)
        self.imagen_surface = pygame.transform.scale(self.imagen_surface, self.dimension)

    def set_origen(self, origen: tuple) -> None:
        self.origen = origen
        self.rect.center = origen

    def set_dimension(self, dimension: tuple) -> None:
        self.dimension = dimension
        self.imagen_surface = pygame.transform.scale(self.imagen_surface, dimension)
        self.rect = self.imagen_surface.get_rect()
        self.rect.center = self.origen

    def quitar_colision (self) -> None:
        
        self.colision = False
        self.set_imagen (self.imagen_no_colision)

    def colisionar (self) -> None:
        
        self.colision = True
        self.set_imagen (self.imagen_colision)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)