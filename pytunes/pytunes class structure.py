import pygame
import time
import random
import eyed3
import os
import csv

class playlist:
    
    def __init__(self, name):
        
        pass
    
class sng:
    
    def __init__(self, name, artist, album, genre, length, path, uid):
        
        self.name = name
        self.album = album
        self.artist = artist
        self.genre = genre
        self.length = length
        self.path = path
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
        info = temp_info.rsplit('\\')[num]   
    info = info.strip()
    return info

def make_song_info(filepath, uid):
    '''Given the file path of a song, returns the information of the song in 
    the format [name, artist, album, genre, length, path, uid]. '''
    
    song = eyed3.core.load('%s' % filepath)
    name = _make_try(song, 'name', filepath, -1)
    artist = _make_try(song, 'artist', filepath, -3)      
    album = _make_try(song, 'album', filepath, -2)  
    try:
        genre = str(song.tag.genre.name)
    except:
        genre = 'Unknown'
    if genre == '<not-set>':
        genre = 'Unknown'
    temp_length = song.info.time_secs
    num_min = temp_length / 60
    num_sec = str(temp_length - (num_min * 60))
    if len(num_sec) == 1:
        num_sec = '0' + num_sec
    length = str(num_min) + ':' + num_sec
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

def import_songs():
    '''Make the library from the text file.'''
    
    library_dict = {}
    library_list = []
    #with open('song_list.csv', 'rb') as csvfile:
        #filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #for row in filereader:
            #print row[6]
            #library_dict[row[6]] = [row[0], row[1], row[2], row[3], row[4],\
                                    #row[5]]
    f = open('library.txt', 'r')
    line = f.readline()
    line = f.readline()
    while line != '':
        temp_list = line.split(';><;')
        library_dict[temp_list[6]] = sng(temp_list[0], temp_list[1], \
                                           temp_list[2], temp_list[3], \
                                           temp_list[4], temp_list[5], \
                                           temp_list[6])
        library_list.append(sng(temp_list[0], temp_list[1], temp_list[2], \
                        temp_list[3], temp_list[4], temp_list[5], temp_list[6]))
        line = f.readline()
    f.close()
    return [library_dict, library_list]

def make_playlist(library_dict, library_list, playlist_name):
    
    playlist = []
    playlist_dict = {}
    song_number = ''
    while song_number != 'done' and song_number != 'cancel':
        song_number = raw_input('Choose which song you want to add to the \
playlist. \rDuplicates will not be added. If you want to view the library,\r\
type "library" (no quotes). If you wnat to see the playlist so far, type in \
"playlist" (no quotes). ')
        if song_number == 'library':
            display_library(library_list)
        elif song_number == 'playlist':
            display_library(playlist)
        elif song_number.isdigit():
            if library_dict.has_key(song_number):
                if playlist_dict.has_key(song_number):
                    print 'You have already added that song to the playlist.'
                else:
                    playlist_dict[song_number] = library_dict[song_number]
                    rec_song = [song_number]
                    for item in library_dict[song_number]:
                        rec_song.append(item)
                    playlist.append(rec_song)
                    print 'Song successfully added.'
            else:
                print 'There is no song corresponding to that number. '
        elif song_number != 'done' and song_number != 'cancel':
            print 'Invalid input'
    save_playlist(playlist, playlist_name)
    f = open('playlists.txt', 'a')
    f.write('%s\n' % playlist_name)
    f.close()
    # above three lines are here instead of in save_playlist because then they
    # would add library to playlists (even worse, it would be added every time 
    # the library is reconstructed)
    return playlist

def save_playlist(playlist, playlist_name):
    
    f = open('%s.txt' % playlist_name, 'w')
    f.write('Name, Artist, Album, Genre, Length, Path, UID\n')
    for song in playlist:
        for item in song:
            f.write(item + ';><;')
        f.write('\n')
    f.close()    

def display_library(library_list):
    
    song_width = 0
    artist_width = 0
    album_width = 0
    for song in library_list:
        if len(song.name) > song_width:
            song_width = len(song[1])
        if len(song.artist) > artist_width:
            artist_width = len(song[2])  
        if len(song.album) > album_width:
            album_width = len(song[3])   
    song_width += 4
    artist_width += 4
    album_width += 4
    for song in library_list:
        print song.uid + '\t' + song.length + '\t' + \
              song.name.ljust(song_width) + song.artist.ljust(artist_width) + \
              song.album.ljust(album_width) + song.genre

def sort_library(type, song_list):
    
    if type == 'name':
        place = 1
    elif type == 'artist':
        place = 2
    elif type == 'album':
        place = 3
    elif type == 'genre':
        place = 4
    elif type == 'length':
        place = 5
    else:
        place = 0
    for song in song_list:
        song[0], song[place] = song[place], song[0]
    song_list.sort()
    for song in song_list:
        song[0], song[place] = song[place], song[0]    
    return song_list

def _filter_guts(library_list, restriction, position):
    
    filtered_library = []
    if position == 'all':
        for song in library_list:
                if song[1].lower().find(restriction) != -1 or \
                   song[2].lower().find(restriction) != -1 or \
                   song[3].lower().find(restriction) != -1 or \
                   song[4].lower().find(restriction) != -1:
                    filtered_library.append(song)
    else:
        for song in library_list:
            if song[position].lower().find(restriction) != -1:
                filtered_library.append(song)
    return filtered_library

def filter(library_list, restriction, filter_type = 'all'):
    # does it return a new, filtered library_list? and then input remove_filter
    # to go back to normal
    # implement reverse filter?
    # can implement some but not all
    restriction = restriction.lower()
    if filter_type == 'all':
        filtered_library = _filter_guts(library_list, restriction, 'all')
    elif filter_type == 'name':
        filtered_library = _filter_guts(library_list, restriction, 1)    
    elif filter_type == 'artist':
        filtered_library = _filter_guts(library_list, restriction, 2) 
    elif filter_type == 'album':
        filtered_library = _filter_guts(library_list, restriction, 3)    
    elif filter_type == 'genre':
        filtered_library = _filter_guts(library_list, restriction, 4)     
    return filtered_library

def play(song_num, library_dict):
    
    pygame.mixer.init()
    pygame.mixer.music.load('%s' % library_dict[song_num][5])    
    pygame.mixer.music.play()    

def play_playlist(playlist, song = ''):
    # have to say which song to start from
    pass

def queue_next():
    
    pass

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
    
    pass

def stop():
    
    pass

def skip():
    
    pass

def rewind():
    
    pass

def go_back():
    
    pass

input = ''
while input != 'no' and input != 'n' and input != 'y' and input != 'yes':
    input = raw_input("Have you obtained any new music since last starting\
 pytunes? \rScanning for new music takes a while, so don't waste time if you\
 \rdon't have to. (input y/n/yes/no) ")
    input = input.lower()

if input == 'y' or input == 'yes':
    print 'Now scanning...'
    temp_songs = get_songs\
        ('C:\Users\Devon Welch\Music\iTunes\iTunes Media\Music')
    music_songs, uid = temp_songs[0], temp_songs[1]
    download_songs = get_songs('C:\Users\Devon Welch\Downloads', uid)[0]

    song_list = []
    for item in music_songs:
        song_list.append(item)
    for item in download_songs:
        song_list.append(item)  

    #with open('song_list.csv', 'w') as csvfile:
        #sl_csv = csv.writer(csvfile)  
        #sl_csv.writerow(['Name','Artist','Album','Genre','Length', 'Path', \
                         #'UID'])
        #for item in song_list:
            #sl_csv.writerow(item)    
    save_playlist(song_list, 'Library')
    #f = open('Library.txt', 'w')
    #f.write('Name, Artist, Album, Genre, Length, Path, UID\n')
    #for song in song_list:
        #for item in song:
            #f.write(item + ';><;')
        #f.write('\n')
    #f.close()

print 'Welcome to pytunes!'

temp_library = import_songs()
library_dict, library_list = temp_library[0], temp_library[1]

# what functionality do i want? 

# playlists (long ones); when deleting a song from a shuffled playlist, simply
# goes to the next song, playlist doesn't get reshuffled. can skip and go back
# in shuffled playlists

# gui? maybe after everything else

# pause, change volume, queue all in pygame already

# option to use a playlist for deleting - so, maybe only goes to next song after
# current one is removed form the playlist (and would either play once or 
# indefinitely) 

# some kinda machine learning by seeing which songs i play one after the other?

# remember where i am in a playlist when i switch to another?

# if text/graphical display, sorting by name, artist, album

# shuffle option

# display upcoming songs in shuffle (and normal)

# move a song to the bottom of a shuffled playlist

# to play a playlist, as soon as a song starts playing, need to queue up the 
# next song, as there is no multi-queueing. same goes for shuffle

# need to make a way to create library for computers that are not mine - 
# probably manual selection/text input... only other way would be to go 
# through EVERY director on the computer

# have to worry about polling? have to determine when a song ends, then play 
# the next one, then add anotehr to the queue

# want to get 'now scanning' to print right away (if i make a gui eventually,
# probably don't have to worry)

# for better time, shouldn't I just add the songs to the file as soon as
# they're created, rather than making lists?

# personal settings for different preferences (that stay between sessions)

# shuffled playlists stay shuffled the same?

# copy playlist

# check to make sure there is not already a playlist with the same name

# restructure under class structure? -> song (play, make_song_info), playlist
# (filter, sort, delete_song_from_playlist, play_playlist, sort_library,
# display_library)

# until visual NEED to be able to loop more than two songs while still
# accepting text input - if possible. 

# maybe play should be under library_dict?