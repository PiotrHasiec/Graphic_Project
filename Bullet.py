import pygame
import numpy as np
from Object import Object
class Bullet(pygame.sprite.Sprite):
    color_counter = 0
    def __init__(self,x,y,z_rotation,v_x,v_y,damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((9,9))
        self.radius = 4
        self.x_pos = x
        self.y_pos = y
        self.z_rotation = z_rotation
        self.x_velocity = 15*np.sin(np.radians(self.z_rotation)) + v_x
        self.y_velocity = 15*np.cos(np.radians(self.z_rotation)) +v_y
        self.z_rot_way = 0
        self.z_velocity = 0
        self.out = 0
        self.rect = self.image.get_rect()
        self.damage = damage
        self.color = color
        
    def update(self,dt):
        self.x_pos += self.x_velocity*dt
        self.y_pos += self.y_velocity*dt
        self.rect.center= (500+self.x_pos,900-self.y_pos)
        self.z_rotation += self.z_rot_way*self.z_velocity*dt
        if self.x_pos <= -700:
                self.out = 1
        elif self.x_pos >= 800:
                self.out = 1

        if self.y_pos <= -200:
                self.out = 1
        elif self.y_pos >= 1200:
                self.out = 1
    def draw(self, surface):
            pygame.draw.circle(surface,self.color,(500+self.x_pos,900-self.y_pos),self.radius)
