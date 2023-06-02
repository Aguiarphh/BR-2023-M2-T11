import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, DEFAULT_TYPE, HEART
from dino_runner.utils.text_tools import draw_message_component
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud_speed = 10 
        self.cloud_x1 = 200 
        self.cloud_y1 = 100  
        self.cloud_x2 = 600  
        self.cloud_y2 = 50
        self.score = 0
        self.death_count = 0
        self.paused = False
        self.game_over = False
        self.lives = 3
        self.heart = 3
        self.collisor = 0
        self.power = ""

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.reset_game()

        while self.playing:
            self.events()
            if self.paused:
                self.clock.tick(FPS)
                continue
            self.update()
            self.draw()

    def reset_game(self):
        self.score = 0
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.player.reset_dinosaur()
        self.heart = 3
        if self.lives == 0:
            self.game_over = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_c:
                    self.paused = False

    def add_Heart(self):
        if self.heart == 3:
            self.screen.blit(HEART, (10, 10))
            self.screen.blit(HEART, (40, 10))
            self.screen.blit(HEART, (70, 10))
        elif self.heart == 2:
            self.screen.blit(HEART, (10, 10))
            self.screen.blit(HEART, (40, 10))
        elif self.heart == 1:
            self.screen.blit(HEART, (10, 10))
            
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_power_up_time()    
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        self.add_Heart()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

        self.screen.blit(CLOUD, (self.cloud_x1, self.cloud_y1))  # desenho da primeira nuvem
        self.screen.blit(CLOUD, (self.cloud_x2, self.cloud_y2))  # desenho da segunda nuvem
        if self.cloud_x1 < -64: #largura da nuvem
            self.cloud_x1 = SCREEN_WIDTH
        if self.cloud_x2 < -64: 
            self.cloud_x2 = SCREEN_WIDTH
        self.cloud_x1 -= self.cloud_speed # movendo a nuvem para a esquerda
        self.cloud_x2 -= self.cloud_speed 

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text2 = font.render(f"Lives: {self.lives}", True, (0,255,0))
        
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, (960, 100))

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks())/1000,2)
            
            if time_to_show >= 0:
                FONT_STYLE = "freesansbold.ttf"
                font = pygame.font.Font(FONT_STYLE, 22)
                text = font.render(f"{time_to_show}", True, (255,255,0))
                
                text_rect = text.get_rect()
                text_rect.x = 500
                text_rect.y = 50
                
                self.screen.blit(text, text_rect)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
                self.collisor = 0
                self.power = ""
                velocity = round(self.score / 55)
                self.game_speed = 20 + velocity

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
             draw_message_component("Press any key to start", self.screen)
        elif self.death_count >= 1 and self.death_count <= 3:
            draw_message_component("Press any key to restart", self.screen, pos_y_center=half_screen_height + 140)
            draw_message_component(
                f"Your Score: {self.score}",
                self.screen,
                pos_y_center = half_screen_height - 150
            )          
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center = half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 40))
        else:
            draw_message_component("Game Over", self.screen)

        pygame.display.flip() 
        self.handle_events_on_menu()
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN and self.game_over == False:
                self.run()
            
