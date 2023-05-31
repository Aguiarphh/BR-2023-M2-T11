import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import OBSTACLE_Y_POS, BIRD


class Bird(Obstacle):
    def __init__(self,image):
        super().__init__(image) 

        self.ini_y_pos = random.randint(150,170)
        self.images = image #array de images
        self.rect.y = self.ini_y_pos #desenhando no ar
        self.flying_index = 0 #usado para mudar a imagen

        self.touched_ground = False
        self.moving = True

    def update(self, game_speed,obstacles):
        self.fly()

        if self.flying_index > 9:
            self.flying_index = 0

        super().update(game_speed,obstacles)#esta encarregado de atualizar o movimento em base ao game_speed

    def fly(self):
        self.image = BIRD[self.flying_index//5]
        self.flying_index+=1

        if self.moving:
            if not self.touched_ground:
                self.rect.y +=10
                if self.rect.y > OBSTACLE_Y_POS:
                    self.touched_ground = True
            else:
                self.rect.y -=10
                if self.rect.y < self.ini_y_pos:
                    self.touched_ground = False