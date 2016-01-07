import random

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
    