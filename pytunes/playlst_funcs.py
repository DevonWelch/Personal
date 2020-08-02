import os
import sys

from song_funcs import make_song_info

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
    
    print(playlist)

    f = open('%s.txt' % playlist_name, 'w')
    f.write('Name, Artist, Album, Genre, Length, Path, UID\n')
    if os.name == 'posix':
        for song in playlist[0]:
            for item in song:
                f.write(item + ';><;')
            f.write('\n')    
    else:
        for song in playlist:
            print(song)
            for item in song:
                f.write(item + ';><;')
            f.write('\n')
    f.close()    
    
def go_back(current_index, playing_playlst):
    
    return play(current_index - 2, playing_playlst)

def filter_everything(current_playlst, typing_dict, typing):
    
    for key in typing_dict:
        if key == typing:
            current_playlst = current_playlst.filter(typing_dict[key][1:-1], \
                                                     key)
        elif typing_dict[key] != '>':
            current_playlst = current_playlst.filter(typing_dict[key][1:], key)
    return current_playlst