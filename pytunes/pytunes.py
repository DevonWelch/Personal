import pygame
import time
import random
import eyed3
import os
import csv
import ctypes
from pygame.locals import *
from pygame_mods import scrollbar, gradient, rnbw_gradient, initialize_screen
import getpass
import sys
import unicodedata
from Tkinter import Tk
from tkFileDialog import askdirectory

class playlst:
    
    def __init__(self, library, name, type_playlst = 'new'):
        
        # different values and meanings for type_playlst are:
        
        # library is generally the library, but for creating the library 
        # (and importing playlists?) the value of library is a temporary dict
        # of the songs that will be contained in the playlst
        self.list = []
        self.dict = {}
        self.name = name
        song_number = ''
        if type_playlst == 'import':
            int_list = []
            final_list = []
            temp_list = library.keys()
            for item in temp_list:
                int_list.append(int(item))
            int_list.sort()
            for item in int_list:
                final_list.append(str(item))            
            for item in final_list:
                self.dict[item] = library[item]
                rec_song = [item]
                for info in library[item]:
                    rec_song.append(info)
                self.list.append(rec_song) 
            song_number = 'cancel'            
        elif type_playlst == 'copy':
            for item in library.list:
                self.list.append(item)
            for key in library.dict.keys():
                self.dict[key] = library.dict[key]
            self.name = name
            song_number = 'done'
        elif type_playlst == 'sort_or_filter':
            for item in library.list:
                self.list.append(item)
            for key in library.dict.keys():
                self.dict[key] = library.dict[key]
            self.name = name
            song_number = 'cancel'
        while song_number != 'done' and song_number != 'cancel' and \
              song_number != 'all':
            song_number = raw_input('Choose which song you want to add to the \
playlist. \rDuplicates will not be added. If you want to view the library,\r\
type "library" (no quotes). If you want to see the playlist so \rfar, type \
"playlist" (no quotes). Type "done" to finish \rcreation of the playlist. Type \
"cancel" to cancel creation of the playlist. ')
            if song_number == 'library':
                library.display()
            elif song_number == 'playlist':
                self.display()
            elif song_number.isdigit():
                if library.dict.has_key(song_number):
                    if self.dict.has_key(song_number):
                        print \
                            'You have already added that song to the playlist.'
                    else:
                        self.dict[song_number] = library.dict[song_number]
                        rec_song = [song_number]
                        for item in library.dict[song_number]:
                            rec_song.append(item)
                        self.list.append(rec_song)
                        print 'Song successfully added.'
                else:
                    print 'There is no song corresponding to that number. '
            elif song_number == 'all':
                int_list = []
                final_list = []
                temp_list = library.dict.keys()
                for item in temp_list:
                    int_list.append(int(item))
                int_list.sort()
                for item in int_list:
                    final_list.append(str(item))                 
                for item in final_list:
                    if not self.dict.has_key(item):
                        self.dict[item] = library.dict[item]
                        rec_song = [item]
                        for info in library.dict[item]:
                            rec_song.append(info)
                        self.list.append(rec_song)                        
                break
            elif song_number != 'done' and song_number != 'cancel' and \
                 song_number != 'all':
                print 'Invalid input' + ': ' + song_number
        if (type_playlst == 'new' and song_number == 'done') or \
           (type_playlst == 'copy' and song_number == 'done'):
            save_playlist(self.list, self.name)
            f = open('playlists.txt', 'a')
            f.write('%s\n' % name)
            f.close()
        # above four lines are here instead of in save_playlist because then
        # they would add library to playlists (even worse, it would be added 
        # every time the library is reconstructed)  
    
    def filter(self, restriction, filter_type = 'all'):
        # problem with filter and song: want to return them as new playlsts,
        # how do i do that? also, now that uids are being saved as strings....
        # arrrrrgggggghhhhhhhhh
        new_playlst = playlst(self, 'filtered%s' % self.name, 'sort_or_filter')
        restriction = restriction.lower()
        if filter_type == 'all':
            new_playlst.list = new_playlst._filter_guts(restriction, 'all')
        elif filter_type == 'name':
            new_playlst.list = new_playlst._filter_guts(restriction, 1)    
        elif filter_type == 'artist':
            new_playlst.list = new_playlst._filter_guts(restriction, 2) 
        elif filter_type == 'album':
            new_playlst.list = new_playlst._filter_guts(restriction, 3)    
        elif filter_type == 'genre':
            new_playlst.list = new_playlst._filter_guts(restriction, 4)     
        # new_playlst.display()
        return new_playlst
    
    def _filter_guts(self, restriction, position):
        
        filtered_library = []
        if position == 'all':
            for song in self.list:
                    if song[1].lower().find(restriction) != -1 or \
                       song[2].lower().find(restriction) != -1 or \
                       song[3].lower().find(restriction) != -1 or \
                       song[4].lower().find(restriction) != -1:
                        filtered_library.append(song)
        else:
            for song in self.list:
                if song[position].lower().find(restriction) != -1:
                    filtered_library.append(song)
        return filtered_library    
    
    def shuffle(self):
        
        new_playlst = playlst(self, 'shuffled %s' % self.name, 'sort_or_filter')
        random.shuffle(new_playlst.list)
        # new_playlst.display()
        return new_playlst
        
    def sort(self, sort_type):
        
        new_playlst = playlst(self, 'sorted %s' % self.name, 'sort_or_filter')
        if sort_type == 'name':
            place = 1
        elif sort_type == 'artist':
            place = 2
        elif sort_type == 'album':
            place = 3
        elif sort_type == 'genre':
            place = 4
        elif sort_type == 'length':
            place = 5
        elif sort_type == 'uid':
            place = 0
        elif sort_type == 'reverse':
            place = 'reverse'
        if place != 0 and place != 'reverse':
            for song in new_playlst.list:
                song[0], song[place] = song[place], song[0]
            new_playlst.list.sort()
            for song in new_playlst.list:
                song[0], song[place] = song[place], song[0] 
        elif place == 'reverse':
            new_playlst.list.reverse()
        else:
            for song in new_playlst.list:
                song[0] = int(song[0])
            new_playlst.list.sort()
            for song in new_playlst.list:
                song[0] = str(song[0])                                  
        # new_playlst.display()
        return new_playlst
    
    def add_song(self):
        
        pass
    
    def delete_song_from_playlist(self, song):
        
        pass    
    
    def display(self):
        
        song_width = 0
        artist_width = 0
        album_width = 0
        for song in self.list:
            if len(song[1]) > song_width:
                song_width = len(song[1])
            if len(song[2]) > artist_width:
                artist_width = len(song[2])  
            if len(song[3]) > album_width:
                album_width = len(song[3])   
        song_width += 4
        artist_width += 4
        album_width += 4
        for song in self.list:
            print song[0] + '\t' + song[5] + '\t' + song[1].ljust(song_width)+\
                  song[2].ljust(artist_width) + song[3].ljust(album_width) + \
                  song[4]   
    
class sng:
    # maybe don't do this one? having it a list is REALLY useful for sorting
    def __init__(self, name, album, artist, genre, length, uid):
        
        self.name = name
        self.album = album
        self.artist = artist
        self.genre = genre
        self.length = length
        self.uid = uid

def _make_try(song, info_type, filepath, num):
    
    try:
        if info_type == 'name':
            info = str(song.tag.title)
        elif info_type == 'artist':
            info = str(song.tag.artist)
        elif info_type == 'album':
            info = str(song.tag.album)            
    except:
        info = None
    if info == None or info == 'None' or info == '':
        temp_info = filepath.split('.mp3')[0]
        if os.name == 'posix':
            info = temp_info.rsplit('/')[num]
        else:
            info = temp_info.rsplit('\\')[num]   
    info = info.strip()
    return info

def make_song_info(filepath, uid):
    '''Given the file path of a song, returns the information of the song in 
    the format [name, artist, album, genre, length, path, uid]. '''
    
    try:
        song = eyed3.core.load('%s' % filepath)
    except:
        return ['Unknown', 'Unknown', 'Unknown', 'Unknown', '0:00', filepath, \
                str(uid)]
    name = _make_try(song, 'name', filepath, -1)
    artist = _make_try(song, 'artist', filepath, -3)      
    album = _make_try(song, 'album', filepath, -2)  
    try:
        genre = str(song.tag.genre.name)
    except:
        genre = 'Unknown'
    if genre == '<not-set>':
        genre = 'Unknown'
    try:
        temp_length = song.info.time_secs
        num_min = temp_length / 60
        num_sec = str(temp_length - (num_min * 60))
        if len(num_sec) == 1:
            num_sec = '0' + num_sec
        length = str(num_min) + ':' + num_sec
    except:
        length = '0:00'
    return [name, artist, album, genre, length, filepath, str(uid)]

# potentially playcount (x.tag.play_count), rating?


def get_songs(dir, uid = 0):
    '''Gets all the songs form the current directory and all subdirectories,
    recursively; returns a list of the deatils of a song in the format 
    [name, artist, album, genre, length, path, uid].'''
    
    if len(os.listdir(dir)) == 0:
        return []
    half_list = []
    for item in os.listdir(dir):
        if os.name == 'posix':
            path = dir + '/' + item
        else:
            path = dir + '\\' + item
        if os.path.isdir(path):
            temp_list = get_songs(path, uid)
            if temp_list != []:
                quarter_list, uid = temp_list[0], temp_list[1]
            else:
                quarter_list = []
            for song in quarter_list:
                half_list.append(song)
        elif item.endswith('.mp3'):
            half_list.append(make_song_info(path, uid))
            uid += 1
    return [half_list, uid]

def import_playlst(playlst_name, list_type='library'):
    '''Make a playlst from the text file.'''
    
    playlst_dict = {}
    #with open('song_list.csv', 'rb') as csvfile:
        #filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #for row in filereader:
            #print row[6]
            #library_dict[row[6]] = [row[0], row[1], row[2], row[3], row[4],\
                                    #row[5]]
    if os.name == 'posix':
        folder = sys.path[-1] + '/'
    else:
        folder = sys.path[0] + '\\'
    f = open('%s%s.txt' % (folder, playlst_name), 'r')
    line = f.readline()
    line = f.readline()
    while line != '':
        temp_list = line.split(';><;')
        if list_type == 'library':
            playlst_dict[temp_list[6]] = [temp_list[0], temp_list[1], \
                                           temp_list[2], temp_list[3], \
                                           temp_list[4], temp_list[5]]
        else:
            playlst_dict[temp_list[0]] = [temp_list[1], temp_list[2], \
                                           temp_list[3], temp_list[4], \
                                           temp_list[5], temp_list[6]]           
        #library_list.append([temp_list[6], temp_list[0], temp_list[1],\
                        #temp_list[2], temp_list[3], temp_list[4], temp_list[5]])
        line = f.readline()
    f.close()
    return playlst_dict

def save_playlist(playlist, playlist_name):
    
    f = open('%s.txt' % playlist_name, 'w')
    f.write('Name, Artist, Album, Genre, Length, Path, UID\n')
    for song in playlist[0]:
        for item in song:
            f.write(item + ';><;')
        f.write('\n')
    f.close()    

def play(song_num, playlst, start_pos = 0.0):
    
    pygame.mixer.init()
    if playlst.name == 'library':
        pygame.mixer.music.load('%s' % playlst.dict[song_num][5])    
    else:
        pygame.mixer.music.load('%s' % playlst.list[int(song_num)][6])
    pygame.mixer.music.play(0, start_pos)    
    return [str(int(song_num) + 1), start_pos]

def play_playlist(playlist, song = ''):
    # have to say which song to start from
    pass

def queue_next(playlst, index):
    
    pygame.mixer.music.queue('%s' % playlst.list[int(index)][6])
    return str(int(index) + 1)

def delete_playlist(playlist_name):
    # remember, HAS to delete from playlists.txt
    pass

def display_all_playlists():
    
    pass

def delete_song_from_playlist(playlist, song):
    
    pass

def add_all_to_playlist(filtered_library, playlist):
    # rather than having to add every song individually, once a filter has been
    # done you can add them all to a playlist
    
    pass

def pause():
    
    if song_selected:
        pygame.mixer.music.pause()
    
def unpause():
    
    if song_selected:
        pygame.mixer.music.unpause()

def skip():
    # should be able to just use play?
    pass

def rewind():
    
    pygame.mixer.music.rewind()

def go_back(current_index, playing_playlst):
    
    return play(current_index - 2, playing_playlst)

def import_all_playlists():
    
    pass

#def initialize_screen(screen_width=0, screen_height=0):
    
    #pygame.display.init()
    #if screen_width < 1 or screen_height < 1:
        #user32 = ctypes.windll.user32
        #screen_width = user32.GetSystemMetrics(0) / 2 
        #screen_height = user32.GetSystemMetrics(1) / 2
    #screen = pygame.display.set_mode([screen_width, screen_height], \
                                     #pygame.RESIZABLE)
    #return [screen, screen_width, screen_height]

def _disp_sort_help(old_sort_by, new_sort_by, current_playlst, playing_playlst,\
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

def display_sort(x_value, sort_by, current_playlst, playing_playlst, width):
    
    if x_value > width - 15:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(sort_by, 'random', current_playlst, \
                            playing_playlst, width - 15, width)          
    elif 142 < x_value < 185:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(sort_by, 'uid', current_playlst, playing_playlst,\
                            143, 184)                
    elif 185 < x_value < 230:
        current_playlst, playing_playlst, sort_by, grdnt = \
           _disp_sort_help(sort_by, 'length', current_playlst, playing_playlst,\
                            186, 229)         
    elif 230 < x_value < 455:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(sort_by, 'name', current_playlst, playing_playlst,\
                            231, 454)                           
    elif 455 < x_value < 608:
        current_playlst, playing_playlst, sort_by, grdnt = \
           _disp_sort_help(sort_by, 'artist', current_playlst, playing_playlst,\
                            456, 607)                           
    elif 608 < x_value < 761:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(sort_by, 'album', current_playlst, playing_playlst,\
                            609, 760)                           
    elif 761 < x_value:
        current_playlst, playing_playlst, sort_by, grdnt = \
            _disp_sort_help(sort_by, 'genre', current_playlst, playing_playlst,\
                            762, width - 18)    
    return [current_playlst, playing_playlst, sort_by, grdnt]

# def filtering(x_value, 

#def _adjust(info, width):
    
    ## works somewhat well, but ultimately i'll have to blit each component of 
    ## each song seperately due to difference in charcater size
    
    #width = width / 9
    #diff = width - len(info)
    #if diff > 0:
        #info = info + ' ' * diff
    #elif diff < 0:
        #info = info[:diff]
    #return info

#def pygm_txt_disp(song, font, uid_width=45, len_width=45, name_width=198, \
                  #artist_width=153, album_width=153, genre_width=63):
    
    #if type(song) == list:
        #text = font.render(_adjust(song[0], uid_width) + '  ' + \
                           #_adjust(song[5], len_width) + '    '+ \
                           #_adjust(song[1], name_width) + '    ' + \
                           #_adjust(song[2], artist_width) + '    ' + \
                           #_adjust(song[3], album_width) + '    ' + \
                           #_adjust(song[4], genre_width), 1, (0, 0, 0))  
    #else:
        #text = font.render(song, 1, (0, 0, 0))
    #return text

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

def draw_basics(screen, width, height, uid_width=45, len_width=45, \
            name_width=225, artist_width=153, album_width=153, genre_width=63):
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
    
   
def import_playlsts():
    # not sure if this will, in fact, work
    pass

def filter_everything(current_playlst, typing_dict, typing):
    
    for key in typing_dict:
        if key == typing:
            current_playlst = current_playlst.filter(typing_dict[key][1:-1], \
                                                     key)
        elif typing_dict[key] != '>':
            current_playlst = current_playlst.filter(typing_dict[key][1:], key)
    return current_playlst

# what functionality do i want? 

# playlists (long ones); when deleting a song from a shuffled playlist, simply
# goes to the next song, playlist doesn't get reshuffled. can skip and go back
# in shuffled playlists

# pause, change volume, queue all in pygame already

# option to use a playlist for deleting - so, maybe only goes to next song after
# current one is removed form the playlist (and would either play once or 
# indefinitely) 

# some kinda machine learning by seeing which songs i play one after the other?

# remember where i am in a playlist when i switch to another?

# display upcoming songs in shuffle (and normal)

# move a song to the bottom of a shuffled playlist

# need to make a way to create library for computers that are not mine - 
# probably manual selection/text input... only other way would be to go 
# through EVERY director on the computer

# for better time, shouldn't I just add the songs to the file as soon as
# they're created, rather than making lists?

# personal settings for different preferences (that stay between sessions)

# shuffled playlists stay shuffled the same?

# copy playlist

# check to make sure there is not already a playlist with the same name

# maybe play should be under library_dict?

# make _add_all helper function

# approximate gui design: upper right: current song info (name, album, artist, 
# genre, time); upper left: all filter; above each column a filter; below 
# those, sort boxes; below filter box, playlists;at bottom, comment input place;
# songs marked as 'favourites' written in red; at bottom a console so you can
# input commands and get more control? could be something like when you press 
# enter the console accepts a text input? red or blue and yellow colour scheme?
# or, banner along teh top/bottom with info of currentl playing song and upper 
# left is just the control panel. also, optional tab/window/whatever of 
# upcoming songs and recently played songs. 

# category (name, artist, etc.) columns need to be resizable

# make a convert seconds to time helper function.

# clean up the whole main block. really, really messy and repetitive.

# need an import feature in teh gui

# get all playlists

# display all playlists, songs, with scrollbars

# filter boxes, console

# buttons

# graphical time in additon to textual? (progress bar so you can click on a 
# time)

# playlst.init() is pretty messy. should clean that up too

# in general, defining a new playlst should add it to playlst_list and 
# playlst_dict?

# details of teh next queued song could be displayed in the appropriate 
# columns above the line

# should probably attempt to get the making of teh display song dict to be 
# faster - could it maybe be done straight from the playlst dict? should really,
# REALLY do this. very noticable pause upon staring since implementing this. 

# need to get the columns to remain equal sizes, and be able to cutoff at a 
# certain point. columns still need to be resizable. need to add faint outlines
# to columns.

# need a volume controller! durrrrr

# shuffle with shift, double python volume controller icon.

# rewind/return button: clicking if song is more than 2.0 seconds in: rewinds
# to beginning of song. clicking if before: goes to previous song played that 
# does not naturally precede the current song (naturally meaning it is the
# previous song in the playest to the nth degree, that ended naturally, playing 
# the next song, that eded naturally, and so on until the current song)

# reowrk functionw ith the knowledge that global variable can just be called 
# instead of passing them in a arguments



if __name__ == '__main__':
    
    input = ''
    while input != 'no' and input != 'n' and input != 'y' and input != 'yes':
        input = raw_input("Have you obtained any new music since last starting \
pytunes? \rScanning for new music takes a while, so don't waste time if you\
\rdon't have to. (input y/n/yes/no) ")
        input = input.lower()
    
    if input == 'y' or input == 'yes':
        input = ''
        while input != 'd' and input != 'c':
            input = raw_input("Would you like to choose a directory to add music from, or \
do the default? (c/d) ")
            input = input.lower()
            
        if input == 'd':
            print 'Now scanning...'
            user = getpass.getuser()
            if sys.platform.startswith('win'):
                temp_songs = get_songs\
                    ('C:\Users\%s\Music' % user)
                music_songs, uid = temp_songs[0], temp_songs[1]
                download_songs = get_songs('C:\Users\%s\Downloads' % user, uid)[0]
            elif sys.platform == 'darwin':
                temp_songs = get_songs\
                    ('/Users/%s/Music' % user)
                music_songs, uid = temp_songs[0], temp_songs[1]
                download_songs = get_songs('/Users/%s/Downloads' % user, uid)[0]   
            # elif sys.platform.startswith('linux'):
                
            song_list = []
            for item in music_songs:
                song_list.append(item)
            for item in download_songs:
                song_list.append(item)   
            save_playlist(song_list, 'Library')
        else:
            Tk().withdraw()
            filename = askdirectory() 
            temp_songs = get_songs(filename)
            song_list = []
            for item in temp_songs:
                song_list.append(item)
            save_playlist(song_list, 'Library')
    
    print 'Welcome to pytunes!\n'
    
    temp_dict = import_playlst('library')
    library = playlst(temp_dict, 'library', 'import')
    temp_dict = None
    playlst_list = []
    playlst_dict = {}
    try:
        f = open('playlists.txt', 'r')
        line = f.readline()
        while line != '':
            playlst_list.append(line[:-1])
            line = f.readline()
        playlst_list.sort()
        for item in playlst_list:
            playlst_dict[item] = import_playlst(item, 'playlst')
        for item in playlst_dict.keys():
            playlst_dict[item] = playlst(playlst_dict[item], item, 'import')
    except:
        f = open('playlists.txt', 'w')
    f.close()
    pygame.display.init()
    screen_info = initialize_screen()
    screen, width, height = screen_info[0], screen_info[1], screen_info[2]
    quit = False
    pygame.mixer.music.set_endevent(31)
    playlist_index = 0
    playing_playlst = library
    current_playlst = library
    prev_playlst = library
    #current_info = play('0', library, 0.0)
    #playing_next = True
    #current_index, start_pos = current_info[0], current_info[1]
    #current_song = current_playlst.list[int(current_index) - 1]
    #prev_index = current_index
    background_colour = pygame.Color(200, 240, 200)
    line_colour = (20, 20, 20)
    semi_colour = (125, 125, 125)
    white = (255, 255, 255)
    top_rect = pygame.Rect(0, 0, width, 15)
    bot_rect = pygame.Rect(0, height - 15, width, 15)
    play_button = pygame.image.load\
       ('.\Pytunes play button small.png')
    play_button = play_button.convert()
    paused = False
    pygame.font.init()  
    playlst_display_dict = {}
    song_display_dict = {}
    try:
        font = pygame.font.SysFont('daunpenh', 21)
    except:
        font = pygame.font.SysFont(None, 21)    
    try:
        bot_font = pygame.font.SysFont('arabictypesetting', 21)
    except:
        bot_font = pygame.font.SysFont(None, 21)    
    for item in range(len(current_playlst.list)):
        song_display_dict[item] = pygm_txt_disp(current_playlst.list[item],\
                                                font)
    playing_len = len(song_display_dict)
    library_display_dict = song_display_dict
    playlst_display_dict = {}
    for item in range(len(playlst_list)):
        playlst_display_dict[item] = pygm_txt_disp(playlst_list[item], font)    
    scroll = 0
    keydown = ''
    song_selected = False
    songs_displayed = (height - 137) / 18
    disp_ratio = songs_displayed / float(len(library.list))
    scrl_bar = scrollbar(disp_ratio, len(library.list) - (height - 137)/18 - 1,\
                         screen, 0, 123, height - 17, width - 15)
    scrolling = False
    scroll_start = time.time()
    scroll_count = 0
    bottom_text = ' >>> '
    typing = False
    sort_by = None
    filtered_playlst = library
    original_playlst = library
    extra_grdnt = None
    typing_dict = {}
    typing_dict['all'] = '>'
    typing_dict['uid'] = '>'
    typing_dict['length'] = '>'
    typing_dict['artist'] = '>'
    typing_dict['album'] = '>'
    typing_dict['genre'] = '>'
    typing_dict['name'] = '>'
    while not quit:
        pygame.display.flip()
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                quit = True
            # plays the next queued song
            elif event.type == 31 and not playing_next and not \
                 pygame.mixer.music.get_busy():
                if int(current_index) >= playing_len:
                    current_index = '0'
                current_index, start_pos = \
                    play(current_index, playing_playlst, 0.0)
                current_song = playing_playlst.list[int(current_index) - 1]
                playing_next = True
            elif event.type == pygame.VIDEORESIZE:
                height = event.h
                width = event.w
                top_rect = pygame.Rect(0, 0, width, 15)
                screen = pygame.display.set_mode([width, height], \
                                     pygame.RESIZABLE)
                bot_rect = pygame.Rect(0, height - 15, width, 15)
                songs_displayed = (height - 137) / 18
                disp_ratio = songs_displayed / float(len(current_playlst.list))
                scroll_ratio = scrl_bar.current_scroll / \
                    float(scrl_bar.max_scroll)
                scroll = int(scroll_ratio * \
                    (len(current_playlst.list) - (height - 137)/18))          
                scrl_bar = scrollbar(disp_ratio, len(current_playlst.list) \
                        - (height - 137)/18 - 1, screen, scroll, \
                        123, height - 17, width - 15)
                if sort_by == 'random':
                    yellow = (255, 194, 14)
                    blue = (77, 109, 243)                    
                    extra_grdnt = gradient(screen, (77, 109, 243), \
                                           (255, 194, 14), width - 15, \
                                           79, width, 99, 'vertical')                     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll -= 3
                    scrl_bar.current_scroll -= 3
                elif event.button == 5:
                    scroll += 3
                    scrl_bar.current_scroll += 3
                elif event.button == 2 or event.button == 3:
                    print 'right'
                elif event.pos[1] < 15:
                    if not paused:
                        pause()
                        paused = True
                    else:
                        unpause()
                        paused = False
                elif 50 <= event.pos[0] <= 85 and \
                     19 <= event.pos[1] <= 65:
                    if not paused:
                        pause()
                        paused = True
                    else:
                        unpause()
                        paused = False
                # select a song from the current playlist
                elif width - 17 > event.pos[0] > 143 and \
                     height - 15 > event.pos[1] > 121 and \
                     (event.pos[1] - 121)/18 < len(current_playlst.list):
                    current_index, start_pos = \
                        play(str((event.pos[1] - 121)/18 + scroll), \
                                        current_playlst, 0.0)
                    playing_len = len(song_display_dict)
                    playing_playlst = current_playlst
                    prev_index = current_index
                    current_song = playing_playlst.list[int(current_index) - 1]
                    playing_next = True
                    song_selected = True
                elif width - 18 < event.pos[0] and \
                     height - 15 > event.pos[1] > 122:
                    scroll = scrl_bar.jump(event.pos[1])
                    scrolling = True
                # elif change playlist:
                #     prev_playlst = current_playlst
                # elif reverse:
                #     current_info = play(str(int(current_index) - 1), 
                #                         playing_playlst, 0.0)
                #     current_index, start_pos = current_info[0], current_info[1
                # elif return:
                #    return to previous playlst
                #    play song at prev_index in prev_playlst 
                #    current_index = prev_index
                elif event.pos[1] > height - 15:
                    bottom_text = ' >>>_'
                    typing = 'bot'
                # go to a playlist
                elif event.pos[0] < 141 and height - 15 > event.pos[1] > 121:
                    if 0 <= (event.pos[1] - 121)/18 <= len(playlst_list) - 1:
                        sort_by = None
                        extra_grdnt = None                      
                        current_playlst = \
                            playlst_dict[playlst_list[(event.pos[1] - 121)/18]]
                        filtered_playlst = current_playlst                        
                        if original_playlst != current_playlst:
                            for key in typing_dict:
                                typing_dict[key] = '>'
                            typing = False
                            original_playlst = current_playlst
                        else:
                            current_playlst = \
                                filter_everything(filtered_playlst, \
                                                  typing_dict, typing)                          
                        song_display_dict = {}
                        for item in range(len(current_playlst.list)):
                            #song_display_dict[item] = \
                                #pygm_txt_disp(current_playlst.list[item], font)      
                            song_display_dict[item] = \
                                library_display_dict\
                                [int(current_playlst.list[item][0])]     
                        songs_displayed = min(((height - 137) / 18), \
                                              len(current_playlst.list))
                        disp_ratio = songs_displayed / \
                            float(len(current_playlst.list))
                        scrl_bar = scrollbar(disp_ratio, \
                                        len(current_playlst.list) \
                                        - (height - 137)/18 - 1, \
                                        screen, 0, 123, height - 17, width - 15)
                        scroll = 0
                        scrolling = False
                        scroll_start = time.time()
                        scroll_count = 0  
                # go to library
                elif event.pos[0] < 141 and 77 < event.pos[1] < 99:
                    sort_by = None
                    extra_grdnt = None                                    
                    if original_playlst != library:
                        for key in typing_dict:
                            typing_dict[key] = '>'
                        typing = False
                        original_playlst = library
                        current_playlst = library
                        song_display_dict = library_display_dict
                        filtered_playlst = library
                    else:
                        filtered_playlst = library
                        current_playlst = \
                            filter_everything(filtered_playlst, \
                                              typing_dict, typing) 
                        for item in range(len(current_playlst.list)):
                            #song_display_dict[item] = \
                                #pygm_txt_disp(current_playlst.list[item], font)      
                            song_display_dict[item] = \
                                library_display_dict\
                                [int(current_playlst.list[item][0])]                             
                    songs_displayed = min(((height - 137) / 18), \
                                          len(current_playlst.list))
                    disp_ratio = songs_displayed / \
                        float(len(current_playlst.list))
                    scrl_bar = scrollbar(disp_ratio, \
                                    len(current_playlst.list) \
                                    - (height - 137)/18 - 1,\
                                    screen, 0, 123, height - 17, width - 15)
                    scroll = 0
                    scrolling = False
                    scroll_start = time.time()
                    scroll_count = 0    
                # determine which filter is currently being typed in
                elif 99 < event.pos[1] < 118:
                    if event.pos[0] < 137:
                        typing = 'all'
                        #if typing_dict['all'] != '>_':
                            #typing_dict['all'] = '>_'
                    elif 142 < event.pos[0] < 185:
                        typing = 'uid'
                        #if typing_dict['uid'] != '>_':
                            #typing_dict['uid'] = '>_'                        
                    elif 185 < event.pos[0] < 230:
                        typing = 'length'  
                        #if typing_dict['length'] != '>_':
                            #typing_dict['length'] = '>_'                        
                    elif 230 < event.pos[0] < 455:
                        typing = 'name' 
                        #if typing_dict['name'] != '>_':
                            #typing_dict['name'] = '>_'                        
                    elif 455 < event.pos[0] < 608:
                        typing = 'artist' 
                        #if typing_dict['artist'] != '>_':
                            #typing_dict['artist'] = '>_'                        
                    elif 608 < event.pos[0] < 761:
                        typing = 'album' 
                        #if typing_dict['album'] != '>_':
                            #typing_dict['album'] = '>_'                        
                    elif 761 < event.pos[0]:
                        typing = 'genre'   
                        #if typing_dict['genre'] != '>_':
                            #typing_dict['genre'] = '>_'    
                    for key in typing_dict:
                        if key == typing:
                            if not typing_dict[key].endswith('_'):
                                typing_dict[key] = typing_dict[key] + '_'
                        else:
                            if typing_dict[key].endswith('_'):
                                typing_dict[key] = typing_dict[key][:-1]
                # sorts the playlist
                # need to ahve  aprevious elif so that column widths can be
                # adjustable
                elif event.pos[0] > 142 and 77 < event.pos[1] < 120:
                    filtered_playlst = display_sort(event.pos[0], sort_by, \
                                    filtered_playlst, playing_playlst, width)[0]                    
                    current_playlst, playing_playlst, sort_by, extra_grdnt = \
                        display_sort(event.pos[0], sort_by, current_playlst, \
                                     playing_playlst, width)
                    song_display_dict = {}
                    for item in range(len(current_playlst.list)):
                        #song_display_dict[item] = \
                            #pygm_txt_disp(current_playlst.list[item], font)      
                        song_display_dict[item] = \
                            library_display_dict\
                            [int(current_playlst.list[item][0])]                        
                else:
                    print event.pos                
            elif event.type == pygame.MOUSEBUTTONUP:
                scrolling = False
            elif event.type == MOUSEMOTION:
                if scrolling and height - 15 > event.pos[1] > 120:
                    scroll = scrl_bar.jump(event.pos[1])
            elif event.type == pygame.KEYDOWN and typing == False:
                if event.key == pygame.K_DOWN:
                    scroll += 1
                    scrl_bar.current_scroll += 1
                    scroll_start = time.time()
                    keydown = 'down'
                elif event.key == pygame.K_UP:
                    scroll -= 1
                    scroll_start = time.time()
                    scrl_bar.current_scroll -= 1
                    keydown = 'up'
                elif event.key == pygame.K_LEFT:
                    if song_selected:
                        if current_index == '1':
                            current_index = str(len(playing_playlst.list) + 1)
                        current_index, start_pos = \
                            play(str(int(current_index) - 2), \
                                 playing_playlst, 0.0)
                        current_song = \
                            playing_playlst.list[int(current_index) - 1]
                        playing_next = True
                elif event.key == pygame.K_RIGHT:
                    if song_selected:
                        if int(current_index) >= playing_len:
                            current_index = '0'
                        current_index, start_pos = \
                            play(current_index, playing_playlst, 0.0)
                        current_song = \
                            playing_playlst.list[int(current_index) - 1]
                        playing_next = True     
                elif event.key == pygame.K_SPACE:
                    if not paused:
                        pause()
                        paused = True
                    else:
                        unpause()
                        paused = False      
                elif event.key == 304 or event.key == 303:
                    filtered_playlst = display_sort(width - 5, sort_by, \
                                    filtered_playlst, playing_playlst, width)[0]                    
                    current_playlst, playing_playlst, sort_by, extra_grdnt = \
                        display_sort(width - 5, sort_by, current_playlst, \
                                     playing_playlst, width)
                    song_display_dict = {}
                    for item in range(len(current_playlst.list)):
                        #song_display_dict[item] = \
                            #pygm_txt_disp(current_playlst.list[item], font)      
                        song_display_dict[item] = \
                            library_display_dict\
                            [int(current_playlst.list[item][0])]                     
            elif event.type == pygame.KEYDOWN and typing:
                if typing == 'bot':
                    if event.key == 13:
                        command = bottom_text[4:-1]
                    elif event.key == K_ESCAPE:
                        typing = False
                        bottom_text = ' >>> '
                    elif event.key == K_BACKSPACE:
                        if len(bottom_text) > 5:
                            bottom_text = bottom_text[:-2] + '_'
                    else:
                        bottom_text = bottom_text[:-1] + \
                            unicodedata.normalize('NFKD', event.unicode).\
                            encode('ascii','ignore') + '_'
                else:
                    # filters the playlist
                    if event.key == K_ESCAPE:
                        typing_dict[typing] = typing_dict[typing][:-1]
                        typing = False
                    elif event.key == K_BACKSPACE:
                        if len(typing_dict[typing]) > 2:
                            typing_dict[typing] = typing_dict[typing][:-2] + '_'                    
                    else:
                        typing_dict[typing] = typing_dict[typing][:-1] + \
                            unicodedata.normalize('NFKD', event.unicode).\
                            encode('ascii','ignore') + '_'  
                    scroll_ratio = scrl_bar.current_scroll / \
                            float(scrl_bar.max_scroll)                     
                    current_playlst = \
                        filter_everything(filtered_playlst, typing_dict, typing) 
                    scroll = int(scroll_ratio * \
                        (len(current_playlst.list) - (height - 137)/18)) 
                    song_display_dict = {}
                    for item in range(len(current_playlst.list)):
                        #song_display_dict[item] = \
                            #pygm_txt_disp(current_playlst.list[item], font)      
                        song_display_dict[item] = \
                            library_display_dict\
                            [int(current_playlst.list[item][0])]
                    songs_displayed = min(((height - 137) / 18), \
                                              len(current_playlst.list))
                    if len(current_playlst.list) > (height - 137)/18:
                        disp_ratio = songs_displayed / \
                            float(len(current_playlst.list))
                        scrl_bar = scrollbar(disp_ratio, \
                                len(current_playlst.list) \
                                - (height - 137)/18,\
                                screen, scroll, 123, height - 17, width - 15)
                    else:
                        scrl_bar = scrollbar(1, \
                                len(current_playlst.list) \
                                - (height - 137)/18 - 1,\
                                screen, scroll, 123, height - 17, width - 15)
                    scrolling = False
                    scroll_start = time.time()
                    scroll_count = 0                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    keydown = ''
                    scroll_count = 0
        if keydown == 'down':
            time_diff = 12 - int(time.time() - scroll_start)
            if time_diff > 0:
                if scroll_count % time_diff == 0:
                    scroll += 1
                    scrl_bar.current_scroll += 1
                scroll_count += 1          
            else:
                scroll += 1
                scrl_bar.current_scroll += 1
        elif keydown == 'up':
            time_diff = 12 - int(time.time() - scroll_start)
            if time_diff > 0:
                if scroll_count % time_diff == 0:
                    scroll -= 1
                    scrl_bar.current_scroll -= 1
                scroll_count += 1          
            else:
                scroll -= 1
                scrl_bar.current_scroll -= 1
        if scroll > len(song_display_dict) - (height - 137)/18:
            scroll = len(song_display_dict) - (height - 137)/18
            scrl_bar.current_scroll = len(song_display_dict) - (height - 137)/18        
        if len(song_display_dict) < (height - 137)/18 or scroll < 0:
            scroll = 0
            scrl_bar.current_scroll = 0            
        draw_basics(screen, width, height)
        # turns the current song into teh text viewable at the top 
        if song_selected:
            temp_time = int((pygame.mixer.music.get_pos() + start_pos) / 1000)
            num_min = temp_time / 60
            num_sec = str(temp_time - (num_min * 60))
            if len(num_sec) == 1:
                num_sec = '0' + num_sec
            play_time = str(num_min) + ':' + num_sec        
            text = font.render(current_song[1] + '; ' + current_song[2] + '; ' \
                               + current_song[3] + '; ' + play_time + '/' + \
                               current_song[5] , 1, (0, 0, 0)) 
        # display 6 columns: uid, length, name, artist, album, genre; this 
        # displays all of the currently viewable songs of the viewed playlst
        for item in range(len(song_display_dict)):
            if height - 144 >= 18 * (item - scroll) >= 0:
                screen.blit(song_display_dict[item][0], (145, 121 + \
                                                  18 * (item - scroll)))
                screen.blit(song_display_dict[item][1], (190, 121 + \
                                                  18 * (item - scroll)))
                screen.blit(song_display_dict[item][2], (235, 121 + \
                                                  18 * (item - scroll)))
                screen.blit(song_display_dict[item][3], (460, 121 + \
                                                  18 * (item - scroll)))
                screen.blit(song_display_dict[item][4], (613, 121 + \
                                                  18 * (item - scroll)))
                screen.blit(song_display_dict[item][5], (766, 121 + \
                                                  18 * (item - scroll)))   
        # displays all playlsts in the bottom left quadrant
        for item in range(len(playlst_display_dict)):
            if height - 144 >= 18 * item >= 0:
                screen.blit(playlst_display_dict[item], (0, 121 + \
                                                  18 * item))     
        # displays the library in the upper left quadrant
        screen.blit(font.render('library', 1, (0, 0, 0)), (45, 78))
        # displays sort gradient
        if extra_grdnt:
            extra_grdnt.draw()
        # displays all the filters
        all_text = font.render(typing_dict['all'], 1, (0, 0, 0)) 
        uid_text = font.render(typing_dict['uid'], 1, (0, 0, 0)) 
        length_text = font.render(typing_dict['length'], 1, (0, 0, 0)) 
        name_text = font.render(typing_dict['name'], 1, (0, 0, 0)) 
        artist_text = font.render(typing_dict['artist'], 1, (0, 0, 0)) 
        album_text = font.render(typing_dict['album'], 1, (0, 0, 0)) 
        genre_text = font.render(typing_dict['genre'], 1, (0, 0, 0)) 
        screen.blit(all_text, (0, 99))
        screen.blit(uid_text, (143, 99))
        screen.blit(length_text, (186, 99))
        screen.blit(name_text, (231, 99))
        screen.blit(artist_text, (456, 99))
        screen.blit(album_text, (609, 99))
        screen.blit(genre_text, (763, 99))
        # this is done here instead of above because this will cover 
        # any excess songs
        # top white area and horizontal line
        pygame.draw.line(screen, line_colour, (0, 15),(width, 15),3)
        pygame.draw.rect(screen, white, top_rect, 0) 
        # bottom white area and horizontal line 
        pygame.draw.line(screen, line_colour, (0, height - 16),\
                         (width, height - 16),3)
        pygame.draw.rect(screen, white, bot_rect, 0)
        # puts the text, buttons, and text input boxes on the screen
        if song_selected:
            screen.blit(text, (1, -2))    
            temp_index = int(current_index)
            for item in range(4):
                if temp_index >= len(playing_playlst.list):
                    temp_index = 0
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][0], \
                              (145, 14 + 15 * item))
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][1], \
                              (190, 14 + 15 * item))
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][2], \
                              (235, 14 + 15 * item))   
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][3], \
                              (460, 14 + 15 * item))   
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][4], \
                              (613, 14 + 15 * item))                
                screen.blit(library_display_dict\
                              [int(playing_playlst.list[temp_index][0])][5], \
                              (766, 14 + 15 * item))
                temp_index += 1
        else:
            paused = False
        bot_text = bot_font.render(bottom_text, 1, (0, 0, 0)) 
        screen.blit(bot_text, (0, height - 18))
        screen.blit(play_button, (55, 20))
        scrl_bar.self_display()
        playing_next = False
    pygame.quit()
    print 'Thank you for using pytunes.'


# lucinda williams song (uid: 2) causing the program to crash? just lucinda 
# williams in general????

# either way, get some error catching for songs that cause pytunes to crash

# no longer getting songs with weird characters - fix in the future

# highlight songs?

# blinking cursor in text box currently selected - and, when text box selected,
# no other key presses should work

# for making the columns, probably makes most sense to have max width per 
# column embedded into the library/playlist file (as the last line, probably).
# also have a max default size; if max size of a column is bigger than that,
# truncate that column's width (but allow resizing)

# need to autocorrect the numbers in playlsts when the uid of that song changes

# if music is from??? a zip file, it doesn't want to load. still doesn't explain 
# lucinda williams.

# pretty sure it has something to do with the bit rate; converting one of the
# lucinda williams songs from 159 to 128 kbps allowed it to be played; 
# however, there are some songs that are irregular bitrates that will play, so
# i'm not sure exactly what the rule is

# that one did get fixed, but one of the cowboy bebop songs that is 192 kbps
# aborted the program...

# makes a lot more sense to have column data stored as where the column begins 
# and ends rather tahn the width of it

# doesn't sort properly by length

# add a playlist toolbar at teh bottom of the playlist quadrant (add, delete, 
# edit) (with buttons)

# need cursor to blink, very easy to miss

# butoons that are animated when you hover over them? (mimic snake movements)