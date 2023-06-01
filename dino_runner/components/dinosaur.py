import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, SCREEN_WIDTH, DEFAULT_TYPE

RUN_IMG = {DEFAULT_TYPE: RUNNING}
DUCK_IMG = {DEFAULT_TYPE: DUCKING}
JUMP_IMG = {DEFAULT_TYPE: JUMPING}

X_POS = 80
Y_POS = 310
Y_POS_DUCK = 340
JUMP_VEL = 8.5


class Dinosaur(Sprite):

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[DEFAULT_TYPE][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.jump_vel = JUMP_VEL
        self.dino_jump = False
        self.dino_duck = False
        self.dino_run = True

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP]:
            self.dino_jump = True
            self.dino_run = False
        elif user_input[pygame.K_DOWN]:
            self.dino_duck = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_run = True

        if user_input[pygame.K_LEFT]:
            self.x_vel = -5  # mover para a direita
        elif user_input[pygame.K_RIGHT]:
            self.x_vel = 5  # mover para a esquerda
        else:
            self.x_vel = 0  # para de se mover
        
        if self.dino_rect.x < 0:
            self.dino_rect.x = 0   #  limitando o dino de acordo com a largura da tela
        elif self.dino_rect.x + self.dino_rect.width > SCREEN_WIDTH:
            self.dino_rect.x = SCREEN_WIDTH - self.dino_rect.width

        self.dino_rect.x += self.x_vel
        
        if self.step_index > 9:
            self.step_index = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index//5]
 
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index//5]
        self.dino_rect.y = Y_POS_DUCK
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def reset_dinosaur(self):
        self.dino_rect.x = X_POS