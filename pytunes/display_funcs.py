import pygame
from pygame_mods import gradient #scrollbar, gradient, rnbw_gradient, initialize_screen

def _disp_sort_help(screen, old_sort_by, new_sort_by, current_playlst, playing_playlst,\
                    start_x, end_x):
    
    yellow = (255, 194, 14)
    blue = (77, 109, 243)  
    green = (200, 240, 200)
    if new_sort_by == 'random':
        playing_playlst = current_playlst
        current_playlst = current_playlst.shuffle()
        grdnt = gradient(screen, blue, yellow, start_x, 79, end_x, 99, \
                         'vertical') 
        new_sort_by = 'random'
    elif old_sort_by == new_sort_by:
        playing_playlst = current_playlst
        current_playlst = current_playlst.sort('reverse')
        grdnt = gradient(screen, blue, yellow, start_x, 79, end_x, 99, \
                         'vertical') 
        new_sort_by = 'back_' + old_sort_by
    else:
        playing_playlst = current_playlst
        current_playlst = current_playlst.sort('%s' % new_sort_by)      
        grdnt = gradient(screen, yellow, blue, start_x, 79, end_x, 99, \
                         'vertical')  
    return [current_playlst, playing_playlst, new_sort_by, grdnt]

def display_sort(screen, x_value, sort_by, current_playlst, playing_playlst, width):
    
    if x_value > width - 15:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(screen, sort_by, 'random', current_playlst, \
                            playing_playlst, width - 15, width)          
    elif 142 < x_value < 185:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(screen, sort_by, 'uid', current_playlst, playing_playlst,\
                            143, 184)                
    elif 185 < x_value < 230:
        current_playlst, playing_playlst, sort_by, grdnt = \
           _disp_sort_help(screen, sort_by, 'length', current_playlst, playing_playlst,\
                            186, 229)         
    elif 230 < x_value < 455:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(screen, sort_by, 'name', current_playlst, playing_playlst,\
                            231, 454)                           
    elif 455 < x_value < 608:
        current_playlst, playing_playlst, sort_by, grdnt = \
           _disp_sort_help(screen, sort_by, 'artist', current_playlst, playing_playlst,\
                            456, 607)                           
    elif 608 < x_value < 761:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(screen, sort_by, 'album', current_playlst, playing_playlst,\
                            609, 760)                           
    elif 761 < x_value:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(screen, sort_by, 'genre', current_playlst, playing_playlst,\
                            762, width - 18)    
    return [current_playlst, playing_playlst, sort_by, grdnt]

def _adjust(info, width):
    
    # works somewhat well, but ultimately i'll have to blit each component of 
    # each song seperately due to difference in charcater size
    
    width = width / 9
    diff = width - len(info)
    if diff < 0:
        info = info[:diff-3] + '...'
    return info

def pygm_txt_disp(song, font, uid_width=45, len_width=45, name_width=225, \
                  artist_width=153, album_width=153, genre_width=63):
    
    if type(song) == list:
        text = [font.render(_adjust(song[0], uid_width), 1, (0, 0, 0)), \
                font.render(_adjust(song[5], len_width), 1, (0, 0, 0)), \
                font.render(_adjust(song[1], name_width), 1, (0, 0, 0)), \
                font.render(_adjust(song[2], artist_width), 1, (0, 0, 0)), \
                font.render(_adjust(song[3], album_width), 1, (0, 0, 0)), \
                font.render(_adjust(song[4], genre_width), 1, (0, 0, 0))] 
    else:
        text = font.render(song, 1, (0, 0, 0))
    return text

def draw_basics(screen, width, height, background_colour, semi_colour, \
                line_colour, uid_width=45, len_width=45, name_width=225, \
                artist_width=153, album_width=153, genre_width=63):
    # draws background, filters, columns, rows, and lines
    
    # background
    screen.fill(background_colour)
    # filter boxes
    filter_rect = pygame.Rect(0, 103, width, 15)
    pygame.draw.rect(screen, (255, 255, 255), filter_rect) 
    # columns
    temp_x = 140 + uid_width
    pygame.draw.line(screen, semi_colour, (temp_x, 16), (temp_x, height))
    temp_x += len_width
    pygame.draw.line(screen, semi_colour, (temp_x, 16), (temp_x, height))
    temp_x += name_width
    pygame.draw.line(screen, semi_colour, (temp_x, 16), (temp_x, height))
    temp_x += artist_width
    pygame.draw.line(screen, semi_colour, (temp_x, 16), (temp_x, height))
    temp_x += album_width
    pygame.draw.line(screen, semi_colour, (temp_x, 16), (temp_x, height)) 
    temp_x = width - 17
    pygame.draw.line(screen, semi_colour, (temp_x, 77), (temp_x, 102), 2) 
    # rows
    row_height = 139
    while row_height < height - 16:
        pygame.draw.line(screen, semi_colour, \
            (143, row_height),(width, row_height),1)  
        row_height += 18
    # instead of grouping to be vertical/horizontal, grouping in main/border
    # because the cross section of the border lines looks nice.
    # middle (black) lines
    pygame.draw.line(screen, line_colour, (140, 16),(140, height - 16),3)
    pygame.draw.line(screen, line_colour, (0, 120),(width, 120),3)
    pygame.draw.line(screen, line_colour, (0, 101), (width, 101), 3)
    pygame.draw.line(screen, line_colour, (0, 77), (width, 77), 2)
    # border (grey) lines
    pygame.draw.line(screen, semi_colour, (142, 15), (142, height - 16))
    pygame.draw.line(screen, semi_colour, (138, 15), (138, height - 16))       
    pygame.draw.line(screen, semi_colour, (0, 118), (width, 118))
    pygame.draw.line(screen, semi_colour, (0, 122), (width, 122))
    pygame.draw.line(screen, semi_colour, (0, 103), (width, 103))
    pygame.draw.line(screen, semi_colour, (0, 99), (width, 99))