height = 10
width = 10
import pygame
import unicodedata
pygame.display.init()
screen = pygame.display.set_mode([width, height])
semi_colour = (125, 125, 125)
line_colour = (0, 0, 0)

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

class scrollbar:
    
    #height = 1000
    #width = 1000
    #import pygame
    #pygame.display.init()
    #screen = pygame.display.set_mode([width, height])    
    
    # does it make sense for this to be a class? 
    
    # need methods to scroll, determine the size of the draggable part of the 
    # scrollbar (both of these in turn need the information of how much is
    # currently displayed out of the total information)
    
    # should clicking on the non-scrollable part jump to that location or
    # fast-scroll?
    
    # should there be arrow buttons on the top and bottom?    
    
    def __init__(self, disp_ratio, max_scroll, screen, current_scroll = 0,\
                 top = 0, bottom = height, left = width-10):
        '''disp_ratio is how much of the total information is currently 
        displayed, max scroll is what the maximum value of current_scroll can 
        be, current_scroll is the value that determines what information is 
        currently being displayed, top is the y value that the scrollbar should 
        be drawn from, bottom is the y value that the scrollbar should be drawn 
        to, left is the x value that the scrollbar should be drawn from, right 
        is the x value that the scrollbar should be drawn to. The default values
        of top, bottom, left and right make the scrollbar drawn to the right 
        side of the screen, from top to bottom, as you would usually see.'''
    
        import pygame
        
        self.top = top
        self.bottom = bottom
        self.height = bottom - top
        self.left = left
        self.rect = pygame.Rect(self.left, self.top, 15, self.height)
        self.disp_ratio = disp_ratio
        if max_scroll > 0:
            self.max_scroll = max_scroll
        else:
            self.max_scroll = 1
        self.current_scroll = current_scroll
        self.scroller_height = int(self.disp_ratio * self.height)
        if self.scroller_height < 6:
            self.scroller_height = 6
        if self.scroller_height % 2 == 1:
            self.scroller_height += 1
        if self.scroller_height > self.height - 2:
            self.scroller_height = self.height - 2
        self.scrollable_height = self.height - self.scroller_height - 2
        if (self.height - self.scrollable_height) % 2 == 0:
            self.scrollable_height += 1
        elif self.scrollable_height == 0:
            self.scrollable_height = self.height      
        # self.scroller_display is what y value the scroller will be centered on
        self.scroller_display = int((float(self.current_scroll) / \
                                    float(self.max_scroll)) * self.scrollable_height) + \
                                    self.top + int(self.scroller_height/2)
        if self.scroller_display < self.top + \
           int(self.scroller_height / 2) + 1:
            self.scroller_display = self.top + \
                int(self.scroller_height / 2) + 1
        elif self.scroller_display > self.bottom - \
             int(self.scroller_height / 2) - 1:
            self.scroller_display = self.bottom - \
                int(self.scroller_height / 2) - 1
        # self.scroller_rect is the area that will be covered by the scroller
        self.scroller_rect = pygame.Rect(self.left + 1,\
                                         self.scroller_display - \
                                         int((self.scroller_height / 2)), \
                                         13, self.scroller_height)
        self.screen = screen
        #self.scroll_height = (self.bottom - int(self.scroller_height / 2)) \
            #- (self.top + int(self.scroller_height / 2))
    
    def drag_scroll(self, y_value):
        
        pass
    
    def jump(self, y_value):
        
        temp_y = y_value - self.top - int(self.scroller_height/2)
        ratio = float(temp_y) / float(self.scrollable_height)
        if ratio >= 0:
            self.current_scroll = int(self.max_scroll * ratio)
        else:
            self.current_scroll = 0
        # self.self_display()
        return self.current_scroll
    
    def click_scroll(self, y_value):
        
        if y_value < (self.top + self.bottom) / 2 and self.current_scroll != 0:
            self.current_scroll -= 1
        elif y_value > (self.top + self.bottom) / 2 and \
             self.current_scroll != self.max_scroll:
            self.current_scroll += 1
        # self.self_display()
        return self.current_scroll
    
    def self_display(self):
        
        import pygame
        
        grdnt = gradient(screen, (255, 194, 14), (77, 109, 243), self.left, \
                         self.top, self.left + 20, self.bottom)
        grdnt.draw()
        # pygame.draw.rect(self.screen, (200, 220, 255), self.rect, 0)
        self.scroller_display = int((float(self.current_scroll) / \
                                    float(self.max_scroll)) * self.scrollable_height) + \
                                    self.top + int(self.scroller_height/2)
        if self.scroller_display < self.top + \
           int(self.scroller_height / 2) + 1:
            self.scroller_display = self.top + \
                int(self.scroller_height / 2) + 1
        elif self.scroller_display > self.bottom - \
             int(self.scroller_height / 2) - 1:
            self.scroller_display = self.bottom - \
                int(self.scroller_height / 2) - 1
        #print self.scroller_display
        #print self.scroller_height
        #print self.current_scroll
        #print ''
        # self.scroller_rect is the area that will be covered by the scroller
        self.scroller_rect = pygame.Rect(self.left + 1,\
                                         self.scroller_display - \
                                         int((self.scroller_height / 2)), \
                                         13, self.scroller_height)
        pygame.draw.rect(self.screen, (100, 255, 100), self.scroller_rect, 0)
        pygame.draw.line(self.screen, (0, 175, 0), \
           (self.left + 1, self.scroller_display - (self.scroller_height / 2)),\
           (self.left + 1, self.scroller_display - (self.scroller_height / 2) \
            + self.scroller_height - 1)) 
        pygame.draw.line(self.screen, (0, 175, 0), \
           (self.left + 13, self.scroller_display -(self.scroller_height / 2)),\
           (self.left + 13, self.scroller_display - (self.scroller_height / 2) \
            + self.scroller_height - 1))
        pygame.draw.line(self.screen, (0, 175, 0), \
           (self.left + 1, self.scroller_display - (self.scroller_height / 2)),\
           (self.left + 13, self.scroller_display - (self.scroller_height / 2)))
        pygame.draw.line(self.screen, (0, 175, 0), \
           (self.left + 1, self.scroller_display - (self.scroller_height / 2) \
            + self.scroller_height-1), (self.left + 13, self.scroller_display -\
            (self.scroller_height / 2) + self.scroller_height - 1))         
        pygame.draw.line(screen, semi_colour, (self.left - 2, self.top), \
                         (self.left - 2, self.bottom - 1), 2)
    
    # first three methods just need to change the value of scroll? 
    
# need to add stuff so that it can be a horizontal scroll bar

class gradient:
    
    # can handle vertical/horizontal lines and rects
    
    def __init__(self, screen, start_col, end_col, start_x, start_y, end_x, \
                 end_y, orientation = None, line_width = 0):
        
        self.screen = screen
        self.start_col = start_col
        self.end_col = end_col
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.line_width = line_width
        self.bigger = None
        self.alpha = 255.0
        if orientation:
            if orientation == 'vertical':
                self.bigger = 'y'
                self.num_steps = end_y - start_y  
            elif orientation == 'horizontal':
                self.bigger= 'x'
                self.num_steps = end_x - start_x   
        if not self.bigger:
            if end_x - start_x > end_y - start_y:
                self.bigger= 'x'
                self.num_steps = end_x - start_x
            else:
                self.bigger = 'y'
                self.num_steps = end_y - start_y
        self.alpha_step = 255.0 / self.num_steps
        self.r_step = float(end_col[0] - start_col[0]) / self.num_steps
        self.g_step = float(end_col[1] - start_col[1]) / self.num_steps
        self.b_step = float(end_col[2] - start_col[2]) / self.num_steps
    
    def draw(self):
        
        import pygame
        
        temp_col = self.start_col
        self.count = 0
        if self.bigger == 'x':
            temp_x = self.start_x
            while self.count < self.num_steps:
                draw_col = (temp_col[0], temp_col[1], temp_col[2], self.alpha)
                pygame.draw.line(screen, draw_col, (temp_x, self.start_y), \
                                 (temp_x, self.end_y), 1)
                temp_x += 1
                self.count += 1
                temp_col = self._inc_col(temp_col)  
                #self.alpha = max(self.alpha - self.alpha_step, 0)
        elif self.bigger == 'y':
            temp_y = self.start_y
            while self.count < self.num_steps:
                draw_col = (temp_col[0], temp_col[1], temp_col[2], self.alpha)
                pygame.draw.line(screen, draw_col, (self.start_x, temp_y), \
                                 (self.end_x, temp_y), 1)
                temp_y += 1
                self.count += 1
                temp_col = self._inc_col(temp_col)   
                #self.alpha = max(self.alpha - self.alpha_step, 0)
                    
    def _inc_col(self, temp_col):
        
        temp_col = (temp_col[0] + self.r_step, \
                    temp_col[1] + self.g_step, \
                    temp_col[2] + self.b_step)   
        return temp_col

class two_gradient(gradient):
    
    def __init__(self, screen, start_col, mid_col, end_col, start_x, start_y, \
                 end_x, end_y, orientation = None, line_width = 0):
        
        self.screen = screen
        self.start_col = start_col
        self.mid_col = mid_col
        self.end_col = end_col
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.line_width = line_width
        self.bigger = None
        if orientation:
            if orientation == 'vertical':
                self.bigger = 'y'
                self.num_steps = end_y - start_y  
            elif orientation == 'horizontal':
                self.bigger= 'x'
                self.num_steps = end_x - start_x   
        if not self.bigger:
            if end_x - start_x > end_y - start_y:
                self.bigger= 'x'
                self.num_steps = end_x - start_x
            else:
                self.bigger = 'y'
                self.num_steps = end_y - start_y 
        self.r_step_1 = float(mid_col[0] - start_col[0]) / (self.num_steps / 2)
        self.g_step_1 = float(mid_col[1] - start_col[1]) / (self.num_steps / 2)
        self.b_step_1 = float(mid_col[2] - start_col[2]) / (self.num_steps / 2)
        self.r_step_2 = float(end_col[0] - mid_col[0]) / (self.num_steps / 2)
        self.g_step_2 = float(end_col[1] - mid_col[1]) / (self.num_steps / 2)
        self.b_step_2 = float(end_col[2] - mid_col[2]) / (self.num_steps / 2)        
    
    
    def _inc_col(self, temp_col):
        
        if self.count < (self.num_steps / 2):        
            temp_col = (temp_col[0] + self.r_step_1, \
                        temp_col[1] + self.g_step_1, \
                        temp_col[2] + self.b_step_1)   
        else:
            temp_col = (temp_col[0] + self.r_step_2, \
                        temp_col[1] + self.g_step_2, \
                        temp_col[2] + self.b_step_2)              
        return temp_col           

class rnbw_gradient(gradient):
    
    # to make a rainbow gradient, start at (255, 0, 0), then go to (255, 255, 0)
    # then (0, 255, 0) the (0, 255, 255) then (0, 0, 255) then (255, 0, 255) 
    # then (255, 0, 0)    
    
    # for this class to work, 1 of the values of start_col must be 255 and one 
    # value must be 0; the third value can be anything between 0 and 255
    
    def __init__(self, screen, start_col, end_col, start_x, start_y, end_x, \
                 end_y, orientation = None, line_width = 0):
        
        self.screen = screen
        self.start_col = start_col
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.line_width = line_width
        self.bigger = None
        if orientation:
            if orientation == 'vertical':
                self.bigger = 'y'
                self.num_steps = end_y - start_y  
            elif orientation == 'horizontal':
                self.bigger= 'x'
                self.num_steps = end_x - start_x   
        if not self.bigger:
            if end_x - start_x > end_y - start_y:
                self.bigger= 'x'
                self.num_steps = end_x - start_x
            else:
                self.bigger = 'y'
                self.num_steps = end_y - start_y   
        self.step_size = 1530.0 / self.num_steps
                
    def _inc_col(self, temp_col):
        
        # if block is laid out in the order that they would be activated 
        # assuming start_col is (255, 0, 0)
        
        if temp_col[0] == 255 and 0 <= temp_col[1] < 255 and temp_col[2] == 0:
            temp_col = (temp_col[0], min((temp_col[1] + self.step_size), 255), \
                        temp_col[2])
        elif 0 < temp_col[0] <= 255 and temp_col[1] == 255 and temp_col[2] == 0:
            temp_col = (max((temp_col[0] - self.step_size), 0), temp_col[1], \
                        temp_col[2])    
        elif 0 == temp_col[0] and temp_col[1] == 255 and 0 <= temp_col[2] < 255:
            temp_col = (temp_col[0], temp_col[1], \
                        min((temp_col[2] + self.step_size), 255))  
        elif 0 == temp_col[0] and 0 < temp_col[1] <= 255 and temp_col[2] == 255:
            temp_col = (temp_col[0], max((temp_col[1] - self.step_size), 0), \
                        temp_col[2])     
        elif 0 <= temp_col[0] < 255 and 0 == temp_col[1] and temp_col[2] == 255:
            temp_col = (min((temp_col[0] + self.step_size), 255), temp_col[1], \
                        temp_col[2])  
        elif temp_col[0] == 255 and 0 == temp_col[1] and 0 < temp_col[2] <= 255:
            temp_col = (temp_col[0], temp_col[1], \
                        max((temp_col[2] - self.step_size), 0))         
        return temp_col   
    
class text_input:
    
    def __init__(self, x, y, prompt = '>>>', font_size = 21, \
                 font = 'arabictypesetting', col = (255, 255, 255)):
        
        self.prompt = prompt
        self.current_disp = prompt
        self.x = x
        self.y = y
        self.col = col
        pygame.font.init()
        try:
            self.font = pygame.font.SysFont(font, font_size)
        except:
            self.font = pygame.font.SysFont(None, font_size)    
        self.display()
        
        
    def display(self, end = -1):
        
        if end == -1:
            end = len(self.current_disp)
        screen.blit(self.font.render(self.current_disp[:end], 1, self.col), \
                    (self.x, self.y))
        pygame.display.flip()
    
    def process_input(self, event):
        
        cmd = None
        if event.key == 13:
            cmd = self.current_disp[len(self.prompt):]
            self.current_disp = self.prompt
        elif event.key == 8:
            if len(self.current_disp) > len(self.prompt):
                self.current_disp = self.current_disp[:-1]
                # if you don't want the bleed effect, comment out the for loop
                # (one extra call of self.display is needed for final character)
                for num in range(len(self.current_disp) - len(self.prompt))[1:]:
                    self.display(-num)
        else:
            self.current_disp = self.current_disp + \
                unicodedata.normalize('NFKD', event.unicode).\
                encode('ascii','ignore')     
        return cmd
    
class fade(gradient):
    
    def __init__(self, screen, col, start_x, start_y, end_x, \
                 end_y, orientation = None, line_width = 0):
        
        self.screen = screen
        self.start_col = (col[0], col[1], col[2], 0)
        self.end_col = (col[0], col[1], col[2], 255)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.line_width = line_width
        self.bigger = None
        self.alpha = 0
        if orientation:
            if orientation == 'vertical':
                self.bigger = 'y'
                self.num_steps = end_y - start_y  
            elif orientation == 'horizontal':
                self.bigger= 'x'
                self.num_steps = end_x - start_x   
        if not self.bigger:
            if end_x - start_x > end_y - start_y:
                self.bigger= 'x'
                self.num_steps = end_x - start_x
            else:
                self.bigger = 'y'
                self.num_steps = end_y - start_y
        try:
            self.alpha_step = 255.0 / self.num_steps
        except:
            self.alpha_step = 0
        
    def _inc_col(self, temp_col):
        
        temp_col = (temp_col[0], temp_col[1], temp_col[2], \
                    temp_col[3] + self.alpha_step)
        return temp_col    
    
    def draw(self):
        
        import pygame
        
        temp_col = self.start_col
        self.count = 0
        if self.bigger == 'x':
            temp_x = self.start_x
            while self.count < self.num_steps:
                #draw_col = pygame.Color(temp_col[0], temp_col[1], temp_col[2], \
                                        #int(temp_col[3]))
                temp_img = pygame.Surface((1, int(self.end_y - self.start_y)))
                temp_img.fill(temp_col)
                temp_img.set_alpha(temp_col[3])
                screen.blit(temp_img, (temp_x, self.start_y))
                #pygame.draw.line(screen, draw_col, (temp_x, self.start_y), \
                                 #(temp_x, self.end_y), 1)
                temp_x += 1
                self.count += 1
                temp_col = self._inc_col(temp_col)  
                #self.alpha = max(self.alpha - self.alpha_step, 0)
        elif self.bigger == 'y':
            temp_y = self.start_y
            while self.count < self.num_steps:
                print temp_col
                temp_img = pygame.Surface((int(self.end_x - self.start_x), 1))
                temp_img.fill(temp_col)
                temp_img.set_alpha(temp_col[3])
                #draw_col = pygame.Color(temp_col[0], temp_col[1], temp_col[2], \
                                        #int(temp_col[3]))
                #pygame.draw.line(screen, draw_col, (self.start_x, temp_y), \
                                 #(self.end_x, temp_y), 1)
                screen.blit(temp_img, (self.start_x, temp_y))
                temp_y += 1
                self.count += 1
                temp_col = self._inc_col(temp_col)   
                #self.alpha = max(self.alpha - self.alpha_step, 0)    