import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
class Game (Env):
    def __init__(self):
        self.x_pos = 0
        self.HIGHT = 100
        self.y_pos = 100
        self.z_rot = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_rot_way = 0
        self.GRAVITY_ACCELERATION = -3
        self.STARSHIP_Z_ROT_VELOCITY = 12
        self.STARSHIP_NORMAL_ACCELARATION = 5
        self.DT = 1/24
        self.enigine_state = 0
        self.done = 0
        self.dict = {1:[0,-1],2:[0,0],3:[0,1],4:[1,-1],5:[1,0],0:[1,1]}

    def observation(self):
        return [self.x_pos,self.y_pos,self.z_rot,self.x_velocity, self.y_velocity]
    def reward(self):
        rew = - 0.005  - ((np.abs(self.y_pos)/1000)**2)*0.1
        return rew
    def end_reward(self):
        if abs(self.x_pos)<= 200:
            return  100*np.cos(np.radians(self.z_rot)) - np.min([np.sqrt(self.x_velocity**2 + self.y_velocity**2 )*2,100]) 
        else:
            return 220 +100*np.cos(np.radians(self.z_rot)) - np.min([np.sqrt(self.x_velocity**2 + self.y_velocity**2 )*2,100])
    def step(self,action_discrit):
        info = {}
        if np.isscalar(action_discrit):
            action = self.dict[action_discrit]
        else:
            action = action_discrit
    
        if self.y_pos < 0:
            self.done = False
            return self.observation(),self.end_reward(), self.done,info
        else:

            self.x_pos = self.x_pos + self.x_velocity*self.DT
            self.y_pos = self.y_pos + self.y_velocity*self.DT
           
            self.z_rot =self.z_rot + action[1]*self.STARSHIP_Z_ROT_VELOCITY/3.1415 * self.DT
            if self.y_pos <= 0 :
                self.y_pos = 1
                self.y_velocity = 0
            else:
                self.y_velocity = 0.999*self.y_velocity + np.cos(np.radians(self.z_rot))*self.STARSHIP_NORMAL_ACCELARATION*self.DT*action[0] + self.GRAVITY_ACCELERATION *self.DT 
            if self.x_pos <= -500:
                self.x_pos = -499
                self.x_velocity = - 0.4*self.x_velocity
            elif self.x_pos >= 500:
                self.x_pos = 499
                self.x_velocity = - 0.4*self.x_velocity
            else:
                self.x_velocity = (0.998*self.x_velocity + np.sin(np.radians(self.z_rot))*self.STARSHIP_NORMAL_ACCELARATION*self.DT*action[0])
             
            return self.observation(),self.reward(), self.done,info


    def reset(self):
        self.x_pos = 0
        self.y_pos = self.HIGHT
        self.z_rot = np.random.randint(-90,90)
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_rot_way = 0
        self.enigine_state = 0
        self.done = 0
        return  self.observation()

