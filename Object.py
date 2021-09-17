import pygame
import Player
import Consts
import numpy as np
class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,v_x,v_y):
        pygame.sprite.Sprite.__init__(self)
        self.consts = Consts.consts()
        self.image = pygame.image.load(self.consts.get_rainbow_image())
        self.showed_image = self.image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*50/self.image.get_height()),50))
        self.mask= pygame.mask.from_surface(self.image)
        self.x_pos = x
        self.y_pos = y
        self.z_rot =0
        self.x_velocity = v_x
        self.y_velocity = v_y
        self.shooting_tactic = Player.Player.add_bullet_rainbow

        self.out = 0

        self.rect = self.showed_image.get_rect(center = self.image.get_rect().center)
        self.rect.center = (500+self.x_pos, 900-self.y_pos)


    def update(self, dt):
        
        self.step(dt)
        
        self.showed_image = pygame.transform.rotate(self.image,- self.z_rot)
        self.rect = self.showed_image.get_rect(center = self.image.get_rect().center)
            
        self.rect.center = (self.rect.center[0]+500+self.x_pos,self.rect.center[1]+900-self.y_pos)
        self.mask= pygame.mask.from_surface(self.image)

    def step(self,dt):
        

            self.x_pos = self.x_pos + self.x_velocity*dt
            self.y_pos = self.y_pos + self.y_velocity*dt
           

            if self.x_pos <= -700:
                self.out = 1
            elif self.x_pos >= 800:
                self.out = 1

            if self.y_pos <= -200:
                self.out = 1
            elif self.y_pos >= 1200:
                self.out = 1
    def __del__(self):
        return

    def draw(self,surface):
        surface.blit(self.showed_image,self.rect)