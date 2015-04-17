import pygame
import time
import math

class character:
    
    def __init__(self, sprites, name, mass):
        '''sprites is a dict mapping lists to strings; acceptable strings are
        'walk', 'run', 'attack', 'idle', 'jump', and 'die'. the list is an 
        ordered list of which sprites to use for the particular cycle, in order,
        represented by their filepath. sprites should be right facing.'''
        
        self.name = name
        self.sprites = sprites
        self.count = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.abs_x_velocity = 0
        self.abs_y_velocity = 0
        self.mass = mass
        self.momentum = 0
        self.action = 'idle'
        self.sprite_delay = 0.5
        self.bounciness = 0
        
    def walk(self):
        
        global prev_time
        if self.sprites.has_key('run') and velocity > 20:
            if self.action == 'run':
                if time.time() - prev_time >= self.sprite_delay:
                    self.count += 1
                    prev_time = time.time()
            else:
                self.count = 0            
            self.run_count += 1
            if self.count >= len(self.sprites['run']):
                # once knowledge of the run cycle improves, probably better to
                # reset to some intermediate value
                self.count = 0
            self.action = 'run'            
        else:    
            if self.action == 'walk':
                if time.time() - prev_time >= self.sprite_delay:
                    self.count += 1
                    prev_time = time.time()
            else:
                self.count = 0            
            if self.count >= len(self.sprites['walk']):
                # once knowledge of the walk cycle improves, probably better to
                # reset to some intermediate value
                self.count = 0
            self.action = 'walk'
        
    def idle(self):
        
        global prev_time
        if self.action == 'idle':
            if time.time() - prev_time >= self.sprite_delay:
                self.count += 1
                prev_time = time.time()
        else:
            self.count = 0
        if self.count >= len(self.sprites['idle']):
            # once knowledge of the idle cycle improves, probably better to
            # reset to some intermediate value
            self.count = 0
        self.action = 'idle'    
        
    def display(self, x, y):
        
        temp_img = pygame.image.load(self.sprites[self.action][self.count])
        temp_img = temp_img.convert()
        screen.blit(temp_img, (x, y))
        
    def change_delay(self):
        
        self.sprite_delay = min(0.5, 1 - 0.5 * abs(self.x_velocity))
        
    def update(self, x, y):
        
        self.display(x, y)
        try:
            self.x_velocity = math.log(abs(self.abs_x_velocity), 100) * \
                (self.abs_x_velocity / abs(self.abs_x_velocity))
        except:
            self.x_velocity = 0
        try:
            self.y_velocity = math.log(abs(self.abs_y_velocity), 100) * \
                (self.abs_y_velocity / abs(self.abs_y_velocity))
        except:
            self.y_velocity = 0
        self.change_delay()
        self.momentum = self.mass * self.x_velocity
        
def initialize_screen(screen_width=0, screen_height=0):
        
    import ctypes
    pygame.display.init()
    if screen_width < 1 or screen_height < 1:
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0) / 2 
        screen_height = user32.GetSystemMetrics(1) / 2
    screen = pygame.display.set_mode([screen_width, screen_height], \
                                     pygame.RESIZABLE)
    return [screen, screen_width, screen_height]

dict_1 = {'walk':['.\sprite_1.png',\
                  '.\sprite_2.png',\
                  '.\sprite_3.png',\
                  '.\sprite_4.png',\
                  '.\sprite_5.png',\
                  '.\sprite_6.png',\
                  '.\sprite_7.png',\
                  '.\sprite_8.png'],
          'idle':['.\sprite_1.png',\
                  '.\sprite_2.png',\
                  '.\sprite_3.png',\
                  '.\sprite_4.png',\
                  '.\sprite_5.png',\
                  '.\sprite_6.png',\
                  '.\sprite_7.png',\
                  '.\sprite_8.png']}

pc = character(dict_1, 'pc', 10)

quit = False
pygame.display.init()
screen_info = initialize_screen(1000, 750)
screen, width, height = screen_info[0], screen_info[1], screen_info[2]
keys_down = []
#sprite_delay = 0.5
prev_time = time.time()

while not quit:
    pygame.display.flip()
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            quit = True  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pc.walk()
                pc.abs_x_velocity -= 1
            elif event.key == pygame.K_RIGHT:
                pc.walk()
                pc.abs_x_velocity += 1
            keys_down.append(event.key)
        elif event.type == pygame.KEYUP:
            keys_down.remove(event.key)
    for item in keys_down:
        if item == pygame.K_LEFT:
            pc.walk()
            pc.abs_x_velocity -= 1
        elif item == pygame.K_RIGHT:
            pc.walk()
            pc.abs_x_velocity += 1  
    if keys_down.count(276) == 0 and keys_down.count(275) == 0 and \
       pc.abs_x_velocity != 0:
        if abs(pc.abs_x_velocity) <= 1800:
            temp_val = max(abs(pc.abs_x_velocity) - 50, 0)
            if temp_val == 0:
                pc.abs_x_velocity = 0
                pc.count = 0
            else:
                pc.abs_x_velocity = temp_val * \
                    (pc.abs_x_velocity / abs(pc.abs_x_velocity))
        else:
            pc.abs_x_velocity = (abs(pc.abs_x_velocity) - \
                                 (abs(pc.abs_x_velocity)/5000.0)) * \
                (pc.abs_x_velocity / abs(pc.abs_x_velocity))
            pc.walk()
    screen.fill((255,255,255))
    pc.update(500, 325)
    
pygame.quit()