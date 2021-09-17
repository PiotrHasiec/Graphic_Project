import pygame,sys
from Object import Object
from Player import Player
from  Bullet import Bullet
import numpy as np
import tensorflow as tf
import keras
from Meteor import Meteor

class GameControler:

    def __init__(self, screen_size ):

        self.screen = pygame.display.set_mode(screen_size)
        self.time = 0
        self.background = pygame.image.load("stars.png")
        self.background = pygame.transform.scale(self.background,(1000,1000))
        self.reward = 0
        self.steps = 0
        self.done = 0
        self.players = []
        self.objects = []
        self.clock = pygame.time.Clock()
        self.points = 0
        self.font = pygame.font.SysFont("dejavusans", 40)
        self.done = 0
        text = "GAME OVER"

        self.text_render = self.font.render(text,1, (250, 250, 50))
    def run(self):
        self.init_player()
        self.objects.clear()     
        self.done = self.points = 0
        while True:
            if len(self.players) >=1:
                self.col_obj  = self.players[0].bullets +self.players+ self.objects
                prev_time = self.time
                self.time = pygame.time.get_ticks()
                dt = self.time - prev_time
            
                
                self.render()
                
                self.update(dt/15)
                
                if self.steps %130 == 0:
                    self.add_meteor()
                    self.points +=1
                if self.steps %180 == 0:
                    self.add_bonus()
                self.check_collisions()
            else:
                self.render_end_screen()
            self.display()
            self.event_handle()
            
            self.steps+=1
            self.clock.tick(60)
    def init_player(self):
        
        
        player = Player(0,0,0)
        self.players.append( player)
 
    def event_handle(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                

    def display(self):
        pygame.display.flip()
        

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background,(0,0))
        
        for obj in self.col_obj:
            obj.draw(self.screen)
        points = self.font.render(str(self.points), 1, (250, 250, 50))
        self.screen.blit(points,self.text_render.get_rect())

    def render_end_screen(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            
            self.run() 
        self.screen.blit(self.background,(0,0))

        
        self.screen.blit(self.text_render,(400,450))
        
            


    def update(self,dt):
       
        for player in self.players:
            player.update(dt)
        for obj in self.objects:
            obj.update(dt)
            if obj.out:
                self.objects.remove(obj)
    def add_meteor(self):
        x = np.random.randint(-600,600)
        y = np.random.randint(1000,1100)
        self.objects.append(Meteor(x,y,(-x+self.players[0].x_pos)/160,(-y+self.players[0].y_pos)/160))
    def add_bonus(self):
        x = np.random.randint(-500,500)
        self.objects.append(Object(x,1100,0,(-1000+self.players[0].y_pos)/160))
        
    def check_collisions(self):
        to_remove = []
        for player in self.players:
            for obj_iterator_1 in range(len(self.objects)):
                obj_iter_1 = self.objects[obj_iterator_1]
                if pygame.sprite.collide_mask(player,obj_iter_1):
                    if type(obj_iter_1) == Meteor:
                        self.players.remove(player)
                       
                        return
                    if type(obj_iter_1) == Object:
                        player.shooting_tactic = obj_iter_1.shooting_tactic
                        Player.color_counter =0
                        self.points += 1
                        to_remove.append(obj_iter_1)
                for bullet in player.bullets:
                    if pygame.sprite.collide_mask(bullet,obj_iter_1):
                        if type(obj_iter_1) == Meteor :
                            if obj_iter_1.hit(bullet.damage):
                                to_remove.append(obj_iter_1)
                            
                        else:
                            to_remove.append(obj_iter_1)
                            
                        player.bullets.remove(bullet)
                        

                    
        for obj in to_remove:
            if obj in self.objects:
                self.objects.remove(obj)
                
                        
                   
        


            