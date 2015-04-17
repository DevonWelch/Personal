import pygame
import os
from pygame_mods import initialize_screen

def get_average(image):
    '''takes an image as a pygame surface type and returns the average RGB of 
    the image, weighted for transparency (i.e. if a pixel in the original image
    is transparent, it does not contribute to the average).'''
    
    average = [0,0,0]
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            temp_col = image.get_at((x, y))
            average[0] += temp_col[0] * (temp_col[3]/255.0)
            average[1] += temp_col[1] * (temp_col[3]/255.0)
            average[2] += temp_col[2] * (temp_col[3]/255.0)
    average[0] = average[0] / (x*y)
    average[1] = average[1] / (x*y)
    average[2] = average[2] / (x*y)
    return average

def get_average_alt(image):
    '''takes an image as a pygame surface type and returns the average RGB of 
    the image, weighted for transparency (i.e. if a pixel in the original image
    is transparent, it does not contribute to the average).'''
    
    most_dict = {}
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            temp_col = (image.get_at((x,y))[0], image.get_at((x,y))[1], \
                        image.get_at((x,y))[2])
            if most_dict.has_key(temp_col):
                most_dict[temp_col] += image.get_at((x,y))[3]/255.0
            else:
                most_dict[temp_col] = image.get_at((x,y))[3]/255.0
    most = [(0,0,0), 0]
    for item in most_dict.keys():
        if most_dict[item] > most[1]:
            most = [item, most_dict[item]]
    return most[0]

def make_spread(dir, y):
    '''makes an x wide and y high display, where x is the number of pictures in
    dir; each picture contributes one y high column of pixels that is the 
    average colour of that image.'''
    
    temp_list = []
    for item in os.listdir(dir):
        if item.endswith('JPG') or item.endswith('PNG') or item.endswith('jpg')\
           or item.endswith('png'):
            temp_list.append(item)
    new_surf = initialize_screen(len(temp_list), y)[0]
    for item in range(len(temp_list)):
        pygame.draw.line(new_surf, \
                         get_average(pygame.image.load(dir+temp_list[item])), \
                         (item, 0), (item, y))
        print '%i/%i' % (item + 1, len(temp_list))
    pygame.display.flip()
    quit = False
    while not quit:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                quit = True        
    pygame.quit()
    
def make_movie_spread(vid, screen):
    
    vid.set_display(screen)
    vid.play()
    vid.pause()
    quit = False
    temp_surface = pygame.Surface((screen.get_width(), screen.get_height()), 0, screen)
    spread_dict = {}
    frame = 1
    count = 1
    while frame != 0:
        try:
            vid.render_frame(frame)
            spread_dict[count] = get_average(screen)
            pygame.display.flip()
            frame += 60 
            event_list = pygame.event.get()
            for event in event_list:
                #print mov.get_busy()
                #print mov.get_length()
                if event.type == pygame.QUIT:
                    frame = 0           
            count += 1
        except:
            frame = 0    
    
    pygame.quit()
    pygame.init()
    print spread_dict
    print len(spread_dict)
    new_surf = initialize_screen(len(spread_dict), 500)[0]
    for item in spread_dict:
        pygame.draw.line(new_surf, spread_dict[item], (item, 0), (item, 500)) 
    pygame.display.flip()
        
    while not quit:
        #pygame.display.flip()
        event_list = pygame.event.get()
        for event in event_list:
            #print mov.get_busy()
            #print mov.get_length()
            if event.type == pygame.QUIT:
                quit = True    
    pygame.quit()    
    return spread_dict

pygame.display.init()
mov = pygame.movie.Movie('C:\Users\Devon\Desktop\lms\LMS3.mpg')
#w, h = mov.get_size()
#w = int(w * 1.3 + 0.5)
#h = int(h * 1.3 + 0.5)
#wsize = (w+10, h+10)
#msize = (w, h)
#screen = pygame.display.set_mode(wsize)
#mov.set_display(screen, Rect((5, 5), msize))

#pygame.event.set_allowed((QUIT, KEYDOWN))
#pygame.time.set_timer(USEREVENT, 1000)
#mov.play()
x,y = mov.get_size()
screen = initialize_screen(x, y)[0]    
spread_dict = make_movie_spread(mov, screen)

#FPS = 60

#pygame.init()
#clock = pygame.time.Clock()
#movie = pygame.movie.Movie('C:\Users\Devon\Desktop\lms\LMS2.mpg')
#screen = pygame.display.set_mode(movie.get_size())
#movie_screen = pygame.Surface(movie.get_size()).convert()

#movie.set_display(movie_screen)
#movie.play()


#playing = True
#while playing:
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #movie.stop()
            #playing = False

    #screen.blit(movie_screen,(0,0))
    #pygame.display.update()
    #clock.tick(FPS)

#pygame.quit()

#make_spread('C:\Users\Devon\Pictures\Pictures\DSLR\Mexico\\', 600)