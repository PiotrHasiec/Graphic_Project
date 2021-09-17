import pygame
import Consts
import Object
import numpy as np
from Bullet import Bullet
pygame.mixer.init()
pygame.mixer.music.load(Consts.consts().get_rocket_wav())
class Controller:
    def __init__(self, up,  left, right, shoot):
        self.up = up
        self.left = left
        self.right = right
        self.shoot = shoot

class Player(pygame.sprite.Sprite):
    color_counter = 0
    def __init__(self,x,y,z_rot):
        pygame.sprite.Sprite.__init__(self)
        self.consts = Consts.consts()
        self.controller = Controller(pygame.K_SPACE,pygame.K_LEFT,pygame.K_RIGHT, pygame.K_z)
        self.image = pygame.image.load(self.consts.get_player_image())
        self.active_image = pygame.image.load(self.consts.get_player_active_image())
        self.showed_image = self.image
        self.active_image = pygame.transform.scale(self.active_image, (int(self.active_image.get_width()*150/self.active_image.get_height()),150))
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*150/self.image.get_height()),150))
        self.showed_image = pygame.transform.rotate(self.image,- z_rot)
        self.mask= pygame.mask.from_surface(self.image)
        self.bullets = []
        self.x_pos = x
        self.y_pos = y
        self.z_rot = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_rot_way = 0
        self.z_rot_velocity = 2
        self.shooting_mode = 0
        self.GRAVITY_ACCELERATION = -0.3
        self.STARSHIP_NORMAL_ACCELARATION = 0.5
        self.shooting_tactic = Player.add_bullet
        
        

        self.rect = self.showed_image.get_rect(center = self.image.get_rect().center)
    def update(self,dt):
        pressed = pygame.key.get_pressed()
        engine_state = 0
        rotation_way = 0
        if pressed[self.controller.up]: engine_state = 1 
        if pressed[self.controller.left]: rotation_way = -1
        elif pressed[self.controller.right]: rotation_way = 1
        if pressed[self.controller.shoot]: self.shooting_tactic(self)
        self.step([engine_state,rotation_way],dt)
        if not engine_state:
            self.showed_image = pygame.transform.rotate(self.image,- self.z_rot)
            self.rect = self.showed_image.get_rect(center = self.image.get_rect().center)
            pygame.mixer.music.stop()
        else:
            self.showed_image = pygame.transform.rotate(self.active_image,- self.z_rot)
            self.rect = self.showed_image.get_rect(center = self.image.get_rect().center)
            pygame.mixer.music.play(-1)
        self.rect.center = (self.rect.center[0]+500+self.x_pos,self.rect.center[1]+900-self.y_pos)
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.out:
                self.bullets.remove(bullet)
        self.mask= pygame.mask.from_surface(self.image)


    def step(self,action_discrit,dt):
        
            action = action_discrit
            self.x_pos = self.x_pos + self.x_velocity*dt
            self.y_pos = self.y_pos + self.y_velocity*dt
    
            self.z_rot =self.z_rot + action[1]*self.z_rot_velocity/3.1415 
            if self.y_pos <= 0 :
                self.y_pos = 1
                self.y_velocity = 0
            else:
                self.y_velocity = 0.99*self.y_velocity + np.cos(np.radians(self.z_rot))*self.STARSHIP_NORMAL_ACCELARATION*action[0]*dt + self.GRAVITY_ACCELERATION*dt  
            if self.x_pos <= -500:
                self.x_pos = -499
                self.x_velocity = - 0.4*self.x_velocity
            elif self.x_pos >= 500:
                self.x_pos = 499
                self.x_velocity = - 0.4*self.x_velocity
            else:
                self.x_velocity = (0.98*self.x_velocity + np.sin(np.radians(self.z_rot))*self.STARSHIP_NORMAL_ACCELARATION*action[0]*dt)
    def add_bullet_rainbow(self):
        if Player.color_counter%768 <256:
            color = (255 -Player.color_counter%768 ,Player.color_counter%768,0)
        elif Player.color_counter%768 <512:
            color =(0 ,255 -(Player.color_counter%768-256),(Player.color_counter%768-256))
        else:
            color =((Player.color_counter%768-512),0 ,255 -(Player.color_counter%768-512))
        Player.color_counter+=3
        if Player.color_counter > 1400:
            Player.color_counter = 0
            self.shooting_tactic = Player.add_bullet
        self.bullets.append(Bullet(self.x_pos + self.active_image.get_rect().width/2,self.y_pos-self.active_image.get_rect().height/2,self.z_rot-0.6,self.x_velocity,self.y_velocity,4,color))
        self.bullets.append(Bullet(self.x_pos + self.active_image.get_rect().width/2,self.y_pos-self.active_image.get_rect().height/2,self.z_rot,self.x_velocity,self.y_velocity,4,color))
        self.bullets.append(Bullet(self.x_pos + self.active_image.get_rect().width/2,self.y_pos-self.active_image.get_rect().height/2,self.z_rot+0.6,self.x_velocity,self.y_velocity,4,color))
    def add_bullet(self):
        self.bullets.append(Bullet(self.x_pos + self.active_image.get_rect().width/2,self.y_pos-self.active_image.get_rect().height/2,self.z_rot,self.x_velocity,self.y_velocity,1.5,(255,10,10)))
    def draw(self,surface):
        
        for bullet in self.bullets:
            bullet.draw(surface)
         
            if bullet.out:
                self.bullets.remove(bullet)
        surface.blit(self.showed_image,self.rect)
    def __del__(self):
        pygame.mixer.init()
        pygame.mixer.music.stop()
        return

    

