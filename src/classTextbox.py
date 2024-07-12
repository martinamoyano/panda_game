import pygame
class Textbox:
    def __init__(self, origen: tuple, dimension: tuple, color: tuple) -> None:
        self.width = dimension[0]
        self.height = dimension[1]
        self.origen = origen
        self.x = origen[0]
        self.y = origen[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.text = ""
   
    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_color(self) -> tuple:
        return self.color

    
    def get_text (self) -> str:
        return self.text

    def set_x(self, x) -> int:
        self.x = x
        self.rect.x = x
    
    def set_y(self, y) -> int:
        self.y = y
        self.rect.y = y
    
    def set_width(self, width: int) -> None:
        self.width = width
        self.rect.width = width 

    def set_height(self, height: int) -> None:
        self.height = height
        self.rect.height = height
    def set_rect(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def set_color(self, color: tuple) -> None:
        self.color = color

    def set_text (self, text: str) -> None:
        self.text = text
