import os

import eyed3
import pygame

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
    except Exception as e:
        print(e)
        raise e
        return ['Unknown', 'Unknown', 'Unknown', 'Unknown', '0:00', filepath, \
                str(uid)]
    name = _make_try(song, 'name', filepath, -1)
    artist = _make_try(song, 'artist', filepath, -3)      
    album = _make_try(song, 'album', filepath, -2)  
    try:
        print(song)
        print(song.tag)
        print(song.tag.genre)
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

def play(song_num, playlst, start_pos = 0.0):
    
    pygame.mixer.init()
    if playlst.name == 'library':
        pygame.mixer.music.load('%s' % playlst.dict[song_num][5])    
    else:
        pygame.mixer.music.load('%s' % playlst.list[int(song_num)][6])
    pygame.mixer.music.play(0, start_pos)    
    return [str(int(song_num) + 1), start_pos]

def pause(song_selected):
    
    if song_selected:
        pygame.mixer.music.pause()
    
def unpause(song_selected):
    
    if song_selected:
        pygame.mixer.music.unpause()
        
def rewind():
            
    pygame.mixer.music.rewind()        