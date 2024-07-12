import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.orientacion = randint(1,2)
        self.speed = 5
        self.activo = True

        self.right_images = [
            pygame.image.load(r'src\enemigo_bolita\enemigo_bolita_0.png').convert_alpha(),
            pygame.image.load(r'src\enemigo_bolita\enemigo_bolita_1.png').convert_alpha(),
            pygame.image.load(r'src\enemigo_bolita\enemigo_bolita_2.png').convert_alpha(),
            pygame.image.load(r'src\enemigo_bolita\enemigo_bolita_3.png').convert_alpha()
        ]

        self.left_images = []
        for image in self.right_images:
            rotated_image = pygame.transform.rotate(image, 180)
            self.left_images.append(rotated_image)
            
        self.down_images = []
        for image in self.right_images:
            rotated_image = pygame.transform.rotate(image, 270)
            self.down_images.append(rotated_image)

        self.up_images = []
        for image in self.right_images:
            rotated_image = pygame.transform.rotate(image, 90)
            self.up_images.append(rotated_image)

        self.image = self.right_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame = 0

        self.set_colorkey_images((75, 125, 125))  

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_sprites.add(self)

    def set_colorkey_images(self, color):
        for image_list in [self.right_images, self.left_images, self.down_images, self.up_images]:
            for image in image_list:
                image.set_colorkey(color)

    def get_frame(self, images):
        self.frame += 1
        if self.frame >= len(images):
            self.frame = 0
        return images[self.frame]
    
    def update(self):
        if self.moving_left:
            self.image = self.get_frame(self.left_images)
        if self.moving_right:
            self.image = self.get_frame(self.right_images)
        if self.moving_up:
            self.image = self.get_frame(self.up_images)
        if self.moving_down:
            self.image = self.get_frame(self.down_images)

    def seleccionador_movimiento (self, height, width):
        self.orientacion = randint (1,4)
        match self.orientacion:
            case 1:
                self.rect.x = randint (50, width-50) #down
                self.rect.bottom = 75 #limite bambu
            case 2:
                self.rect.topright = (0, randint(55,height-50)) #right
            case 3:
                self.rect.y = randint(50, height - 50)  #left
                self.rect.left = width  
            case 4:
                self.rect.x = randint (50, width-50) #up
                self.rect.top = height

    def movimiento(self, height, width):
        match self.orientacion:
            case 1:
                if self.rect.top <= height:
                    self.moving_right, self.moving_left, self.moving_up = False, False, False
                    self.moving_down = True
                    self.rect.y += self.speed
                else:
                    self.seleccionador_movimiento(height, width)
            
            case 2:
                if self.rect.left <= width:
                    self.moving_down, self.moving_left, self.moving_up = False, False, False
                    self.moving_right = True
                    self.rect.x += self.speed
                else:
                    self.seleccionador_movimiento(height, width)
            
            case 3: 
                if self.rect.left >= 0:
                    self.moving_down, self.moving_up, self.moving_right = False, False, False
                    self.moving_left = True
                    self.rect.x -= self.speed 
                else:
                    self.seleccionador_movimiento(height, width)

            case 4: 
                if self.rect.bottom >= 0:
                    self.moving_down, self.moving_left, self.moving_right = False, False, False
                    self.moving_up = True
                    self.rect.y -= self.speed 
                else:
                    self.seleccionador_movimiento(height, width)

    
        


