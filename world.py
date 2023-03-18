import pygame
import os
from states import State
from pygame.math import Vector2 as vec

# Begin MainGame class
class main_game(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.player = Player(self.game)

    def update(self, delta_time, actions):
        self.player.update(delta_time, actions)

    def render(self, display):
        display.fill('red')
        self.player.render(display)

# Begin Player class
class Player():
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.rect = self.curr_anim_list[0].get_rect()
        self.position = vec(0, 0)
        self.speed = 6
        self.gravity = 4
        self.jump_speed = -20
        self.direction = vec(0, 0)
        self.current_frame, self.last_frame_update = 0, 0
        self.is_jumping = False
        self.jump_start_time = 0
        self.jump_duration = 5
        self.jump_height = 25
        self.clock = pygame.time.Clock()

    def get_input(self, actions):
        self.direction.x = actions['right'] - actions['left']

        if actions['up'] and not self.is_jumping:
            self.is_jumping = True
            self.direction.y = self.jump_speed
            self.jump_start_time = pygame.time.get_ticks()

    def apply_gravity(self, delta_time):
        self.direction.y += self.gravity * delta_time
        self.rect.bottom += self.direction.y * delta_time

    def update(self, delta_time, actions):
        self.get_input(actions)
        self.apply_gravity(delta_time)
        self.position += self.direction * self.speed * delta_time
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y
        self.animate(delta_time,actions)

    def render(self, display):
        display.blit(self.curr_image, self.rect)

    def animate(self, delta_time,actions):
        is_idle = not (self.direction.x or self.direction.y)

        if self.is_jumping:
            elapsed_time = (pygame.time.get_ticks() - self.jump_start_time) / 1000
            if elapsed_time <= self.jump_duration:
                d = self.jump_speed * elapsed_time + self.gravity * elapsed_time ** 2 / 2
                self.rect.bottom -= int(d)
            else:
                self.is_jumping = False
                self.direction.y = 0

        if actions['up']:
             # Character is jumping or falling
            self.curr_anim_list = self.jump_sprites
        else:

            if self.direction.x > 0:
                self.curr_anim_list = self.run_right_sprites
            elif self.direction.x < 0:
                self.curr_anim_list = self.run_left_sprites
            else:
                self.curr_anim_list = self.idle_sprites

       
    
        if is_idle:
                self.current_frame = 0
                self.curr_image = self.idle_sprites[self.current_frame]
        else:
                if self.last_frame_update > .15:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
                    self.curr_image = self.curr_anim_list[self.current_frame]
        
        self.curr_anim_list = self.idle_sprites if is_idle else self.curr_anim_list

        self.last_frame_update += delta_time

    def load_sprites(self): 
        self.sprite_dir = os.path.join(os.getcwd(), "graphics", "sprites","bunny")

        self.jump_sprites = []
        for i in range(1, 6):
            self.jump_sprites.append(
                pygame.image.load(os.path.join(self.sprite_dir, "jump" + str(i) + ".png")))
      
        self.idle_sprites, self.run_right_sprites, self.run_left_sprites = [],[],[]

        for i in range(1, 7):
            self.run_right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "run" + str(i) + ".png")))
        for i in range(1, 4):
            self.idle_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "idle" + str(i) + ".png")))
            
        self.run_left_sprites = [pygame.transform.flip(img, True, False) for img in self.run_right_sprites]       
       

        self.curr_image = self.idle_sprites[0]
        self.curr_anim_list = self.idle_sprites      


    
        #  # Compute how much time has passed since the frame last updated
        # self.last_frame_update += delta_time
        # # If no direction is pressed, set image to idle and return
        # if not (self.direction.x or self.direction.y):
        #     self.curr_image = self.curr_anim_list[0]
        #     return 
        
        # if self.is_jumping:
        #     elapsed_time = (pygame.time.get_ticks() - self.jump_start_time) / 1000
        #     if elapsed_time <= self.jump_duration:
        #         d = self.jump_speed * elapsed_time + self.gravity * elapsed_time**2 / 2
        #         self.rect.y = self.rect.bottom - self.rect.height - int(d)
        #     else:
        #         self.is_jumping = False
        #         self.direction.y = 0
        #         self.rect.bottom = self.rect.bottom
       
        #  # If an image was pressed, use the appropriate list of frames according to direction
        # if self.direction.x > 0: 
        #       self.curr_anim_list = self.run_right_sprites
        # elif self.direction.x < 0:
        #       self.curr_anim_list = self.run_left_sprites
        # else:
        #       self.curr_anim_list = self.idle_sprites
        #     # Playing run animation if enough time has elapsed
        # if self.curr_anim_list != self.idle_sprites:
        #       if self.last_frame_update > .15:
        #           self.last_frame_update = 0
        #           self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
        #           self.curr_image = self.curr_anim_list[self.current_frame]
        # else:
        #     self.curr_image = self.idle_sprites[self.current_frame]
       
    #  self.last_frame_update += delta_time
        
    #     if not (direction_x or direction_y):
    #         self.curr_image = self.idle_sprites[0]
    #         return
      
    #     if self.direction.y > 0:
    #         self.curr_anim_list = self.jump_sprites
    #         self.jump_start_time = pygame.time.get_ticks()  
    #     elif self.direction.y < 0:
    #         self.curr_anim_list = self.idle_sprites
    #         self.is_jumping = False

    #     if not self.is_jumping:
    #         if direction_x > 0: 
    #             self.curr_anim_list = self.run_right_sprites
    #         elif direction_x < 0:
    #             self.curr_anim_list = self.run_left_sprites
    #         else:
    #             self.curr_anim_list = self.idle_sprites
      
    #         if self.curr_anim_list != self.idle_sprites:
    #             if self.last_frame_update > .15:
    #                 self.last_frame_update = 0
    #                 self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
    #                 self.curr_image = self.curr_anim_list[self.current_frame]




            
# if self.is_jumping:
#             elapsed_time = (pygame.time.get_ticks() - self.jump_start_time) / 1000
#             if elapsed_time <= self.jump_duration:
#                 d = self.jump_speed * elapsed_time + self.gravity * elapsed_time**2 / 2
#                 self.rect.y = self.rect.bottom - self.rect.height - int(d)
#             else:
#                 self.is_jumping = False
#                 self.direction.y = 0