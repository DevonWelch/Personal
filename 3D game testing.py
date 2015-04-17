import pygame
from pygame_mods import initialize_screen, gradient, two_gradient, rnbw_gradient
import math
import time

# x is left/right, y is forward/backward, z is up/down

# this is going to be a test type thing, to see how it feels to make a game
# in pygame in 3D

black = (0, 0, 0)
white = (255, 255, 255)

screen, width, height = initialize_screen()
quit = False
rotation = [0, 0]
focal_point = 'self'
current_point = [0, 0, 20]
light_source = [0, 15, 1000]
view_angle_dict = {}
light_angle_dict = {}
light_dict = {}
item_list = []

# general order of pygame:
# 1. pygame.display.flip()
# 2. get events, change variables, etc.
# 3. fill background
# 4. draw other things - sprites, etc.

class viewable_object:
    
    # contains three lists:
    
    # a list of [x, y, z] coordinates that describes the surface of a 3D object
    
    # a list of [x, y, z] coordinates of the edges of the 3D object
    
    # a list of [x, y, z] coordinates the vertices of the 3D object.
    
    # all coordinates of vertices will also be coordinates of edges, and all
    # coordinates of edges will be coordinates of the surface   
    
    # viewable_object itself is not suable; use on the children classes for the 
    # specific object you want (including cube, rectangular prism, cylinder, 
    # sphere, tetrahedron, square_pyramid, cone)
    
    def __init__(self):
        
        pass
    
    def move(self, x, y, z):
        
        for item in self.surface:
            item[0] += x
            item[1] += y
            item[2] += z
        self.center = (self.center[0] + x, self.center[1] + y, self.center[2] + z)
        self.calc_view()
        self.calc_light()
    
    def update_view_angle_dict(self):
        
        for item in self.surface:
            temp_angle = get_double_angle(item, current_point)
            if view_angle_dict.has_key(temp_angle):
                view_angle_dict[temp_angle].append(item)
            else:
                view_angle_dict[temp_angle] = [item]
                
    def update_light_angle_dict(self):
        
        for item in self.surface:
            temp_angle = get_double_angle(item, light_source)
            if light_angle_dict.has_key(temp_angle):
                light_angle_dict[temp_angle].append(item)
            else:
                light_angle_dict[temp_angle] = [item]          
    
    def calc_view(self):
        
        self.viewable = []
        self.light = {}
        for coord in self.surface:
            #if not_obstructed(coord, current_point, 'observer'):
                #light_dict[tuple(coord)] = 0.01
                #self.viewable.append(coord)
            self.light[tuple(coord)] = 0.2
            self.viewable.append(coord)            
    
    def calc_light(self):
        
        #self.light = {}
        for coord in self.viewable:
            #if not_obstructed(coord, light_source, 'light'):
            self.light[tuple(coord)] = \
                max(2000 - get_len(coord, light_source), 200) / 1000.0
        #light_dict[(self.name, self.center)] = self.light
    
class sphere(viewable_object):
    
    def __init__(self, radius, x_off, y_off, z_off, name):
        
        step = radius / 10.0
        self.surface = get_sphere_surface(radius, step, \
                                          {0:x_off, 1:y_off, 2:z_off})
        self.center = (x_off, y_off, z_off)
        self.name = name
        self.update_view_angle_dict()
        self.update_light_angle_dict()
        self.calc_view()
        self.calc_light()   
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        #self.momentum = 0
        item_list.append(self)

def get_sphere_surface(radius, step, off_dict):
    
    coords = []
    temp_val_1 = -radius + off_dict[2]
    coords.append([off_dict[0], off_dict[1], temp_val_1])
    while temp_val_1 < radius + off_dict[2]:
        temp_val_1 += step
        temp_val_2 = reverse_len(radius, temp_val_1 - off_dict[2])
        count = 0
        temp_val_3 = 0
        temp_step = temp_val_2 / 10.0
        while count <= 10:
            coords.append([off_dict[0] + temp_val_2, off_dict[1] + temp_val_3, \
                           temp_val_1])
            coords.append([off_dict[0] - temp_val_2, off_dict[1] + temp_val_3, \
                           temp_val_1])
            coords.append([off_dict[0] + temp_val_2, off_dict[1] - temp_val_3, \
                           temp_val_1])
            coords.append([off_dict[0] - temp_val_2, off_dict[1] - temp_val_3, \
                                    temp_val_1])
            temp_val_2 -= temp_step
            temp_val_3 = reverse_trip_len(radius, temp_val_1 - off_dict[2], temp_val_2)
            count += 1
    coords.append([off_dict[0], off_dict[1], radius + off_dict[2]])
    return coords
        
class cube(viewable_object):
    
    def __init__(self, size, x_off, y_off, z_off, name):
        
        #self = rectangular_prism(size, size, size)
        self.vertices = \
            [[-size/2.0 + x_off, -size/2.0 + y_off, -size/2.0 + z_off], \
             [size/2.0 + x_off, -size/2.0 + y_off, 0-size/2.0 + z_off], \
             [-size/2.0 + x_off, size/2.0 + y_off, -size/2.0 + z_off], \
             [-size/2.0 + x_off, -size/2.0 + y_off, size/2.0 + z_off], \
             [size/2.0 + x_off, size/2.0 + y_off, -size/2.0 + z_off], \
             [size/2.0 + x_off, -size/2.0 + y_off, size/2.0 + z_off], \
             [-size/2.0 + x_off, size/2.0 + y_off, size/2.0 + z_off], \
             [size/2.0 + x_off, size/2.0 + y_off, size/2.0 + z_off]]
        step = size / 10.0
        self.edges = self.vertices + explore_edges([-size/2.0 + x_off, \
                            -size/2.0 + y_off, -size/2.0 + z_off], size,\
                            step, [-size/2.0 + x_off, -size/2.0 + y_off, \
                            -size/2.0 + z_off], {0:x_off, 1:y_off, 2:z_off})[0]
        self.surface = explore_all_faces(size,step,{0:x_off, 1:y_off, 2:z_off})\
            + self.edges    
        self.center = (x_off, y_off, z_off)
        self.name = name
        self.update_view_angle_dict()
        self.update_light_angle_dict()
        self.calc_view()
        self.calc_light()
        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0
        item_list.append(self)

def get_len(xyz_1, xyz_2):
    
    temp_len = float(abs(xyz_1[0] - xyz_2[0])**2 + abs(xyz_1[1] - xyz_2[1])**2)
    length = math.sqrt(temp_len + abs(xyz_1[2] - xyz_2[2])**2)
    return length

def reverse_len(length, known_val):
    
    return math.sqrt(length**2 - known_val**2)

def reverse_trip_len(length, known_val_1, known_val_2):
    
    temp_val = math.sqrt(abs(length**2 - known_val_1**2))
    temp_val_2 = math.sqrt(abs(temp_val**2 - known_val_2**2))
    return temp_val_2

def get_double_angle(xyz, viewed_from, correct=True):
    
    x_angle = get_angle(xyz[0] - viewed_from[0], xyz[1] - viewed_from[1], correct)
    z_angle = get_angle(xyz[2] - viewed_from[2], xyz[1] - viewed_from[1], correct)
    return (x_angle, z_angle)

def get_angle(x, y, correct=True):
    try:
        angle = math.degrees(math.atan(float(x)/y))
        #if correct and abs(rotation[0]) < 90:
            #if y < 0 and x < 0:
                #angle = angle - 180
            #elif y < 0:
                #angle = angle + 180          
        #elif correct and abs(rotation[0]) >= 90:
            #angle = -angle
        if correct:
            if y < 0 and x < 0:
                angle = angle - 180
            elif y < 0:
                angle = angle + 180         
    except:
        if x < 0:
            angle = -90
        elif x > 0:
            angle = 90
        else:
            angle = 0
    return int(angle*10)/10.0

def not_obstructed(xyz, viewed_from, source):
    
    if source == 'observer':
        if max(view_angle_dict[get_double_angle(xyz, viewed_from)]) == xyz:
            return True
    elif source == 'light':
        if max(light_angle_dict[get_double_angle(xyz, viewed_from)]) == xyz:
            return True      
    return False

def explore_all_faces(size, step, off_dict):
    
    coords = []
    coords += explore_face([-size/2.0 + off_dict[0], -size/2.0 + off_dict[1], \
                             -size/2.0 + off_dict[2]], 0, size, \
                           step, off_dict)
    coords += explore_face([-size/2.0 + off_dict[0], -size/2.0 + off_dict[1], \
                             size/2.0 + off_dict[2]], 1, \
                           size, step, off_dict)
    coords += explore_face\
        ([size/2.0 + off_dict[0], size/2.0 + off_dict[1], \
                             -size/2.0 + off_dict[2]], 2, size, step, \
         off_dict)
    return coords


def explore_face(xyz, val_1, size, step, off_dict):
    '''Makes an edge (not including the vertices) and returns a list of all the
    points on the two adjacent faces (not including the edges or verices)'''
    
    edge = explore_one_edge(xyz, val_1, size, step, off_dict)[0]
    coords = []
    for num_1 in range(3):
        if num_1 != val_1:
            for coord in edge:
                temp_xyz = []
                for item in coord:
                    temp_xyz.append(item)
                temp_xyz[num_1] = 0
                temp_num = len(coords)
                coords += explore_one_edge(temp_xyz, num_1, size, step, off_dict)[0]
    return coords
    #while count < 100:
        #temp_xyz_2 = []
        #for item in temp_xyz:
            #temp_xyz_2.append(item)        
        #coords.append(temp_xyz_2)
        #count += 1
        #temp_xyz[val] = count * step
    #for item in range(3):
        #if temp_xyz[item] > size:
            #temp_xyz[item] = size
    #if temp_xyz[0] < size or temp_xyz[1] < size or temp_xyz[2] < size:
        #explore = temp_xyz
    #print len(coords)
    #return [coords, explore]    
    
    
def explore_edges(xyz, size, step, explored, off_dict={0:0, 1:0, 2:0}):
    
    temp_xyz = []
    for item in xyz:
        temp_xyz.append(item) 
    coords = []
    explore = []
    for num in range(3):
        if xyz[num] < size/2.0 + off_dict[num]:
            temp_coords, temp_explore = explore_one_edge(temp_xyz, num, size, step, off_dict)
            coords += temp_coords
            if len(temp_explore) > 0:
                explore.append(temp_explore)
    if len(explore) > 0:
        for item in explore:
            if explored.count(item) == 0:
                explored.append(item)
                temp_coords, explored = explore_edges(item, size, step, \
                                                      explored, off_dict)
                coords += temp_coords
    return [coords, explored]

def explore_one_edge(xyz, val, size, step, off_dict={0:0, 1:0, 2:0}):
    
    temp_xyz = []
    for item in xyz:
        temp_xyz.append(item)
    coords = []
    explore = []
    count = 1
    temp_xyz[val] = count * step + off_dict[val] - size/2.0
    while count < 10:
        temp_xyz_2 = []
        for item in temp_xyz:
            temp_xyz_2.append(item)        
        coords.append(temp_xyz_2)
        count += 1
        temp_xyz[val] = count * step + off_dict[val] - size/2.0
    for item in range(3):
        if temp_xyz[item] > size/2.0 + off_dict[item]:
            temp_xyz[item] = size + off_dict[item]
    if temp_xyz[0] < size/2.0 + off_dict[0] or temp_xyz[1] < size/2.0 + \
       off_dict[1] or temp_xyz[2] < size/2.0 + off_dict[2]:
        explore = temp_xyz
    return [coords, explore]

def make_ground(view_type, ground_type, convert, correct=True, altern=False):
    
    # cool floor effect if you change x_angle to y/x instead of x/y
    
    if view_type == 'wide':
        x_view = 160
        y_view = 120
    elif view_type == 'normal':
        x_view = 120
        y_view = 90
    elif view_type == 'super_wide':
        x_view = 180
        y_view = 130
    elif view_type == 'hyper_wide':
        x_view = 270
        y_view = 150
    elif view_type == 'narrow':
        x_view = 90
        y_view = 60
    elif view_type == 'omega_wide':
        x_view = 360
        y_view = 180 
        
    if not altern:
        x = range(-145, 145, 6)
        for item in x:
            y = range(-150, 150, 6)
            for second_item in y:
                if ground_type == 'plane':
                    xyz = convert_xyz((item + \
                                (int(current_point[0])/6) * 6, second_item + \
                                (int(current_point[1])/6)*6, 0), convert)
                    x_angle, z_angle = get_double_angle(xyz, current_point, True)
                    if convert == 'neither' or convert == 'x':
                        z_angle += rotation[1]
                    if convert == 'neither' or convert == 'z':
                        x_angle+= rotation[0]
                elif ground_type == 'receding':
                    if convert == 'both' or convert == 'z':
                        convert = 'z'
                    else:
                        convert = 'neither'
                    xyz = convert_xyz((item + \
                            (int(current_point[0])/6) * 6, second_item + \
                            (int(current_point[1])/6)*6, 0), convert)
                    x_angle, z_angle = get_double_angle(xyz, current_point, True)
                    #x_angle, z_angle = get_double_angle((item + \
                            #(int(current_point[0])/4) * 4, second_item + \
                            #(int(current_point[1])/4)*4, 0), current_point, True)
                    x_angle += rotation[0]
                    if convert == 'neither' or convert == 'x':
                        z_angle += rotation[1]                    
                if abs(rotation[0]) > 90:
                    if abs(z_angle) > 90:
                        try:
                            z_angle = (180 - abs(z_angle)) * (z_angle/abs(z_angle))
                        except:
                            z_angle = 180
                    if abs(x_angle) > 180:
                        x_angle = (360 - abs(x_angle)) * (x_angle/abs(x_angle)) * -1
                #z_angle += rotation[1]
                temp_x = (((x_angle + x_view/2.0) / x_view)) * width
                temp_y = height - (((z_angle + y_view/2.0) / y_view) * height)   
                if 0 <= temp_x <= width and 0 <= temp_y <= height:  
                    temp_col = (255.0 , 255.0, 255.0)
                    pygame.draw.line(screen, temp_col,(temp_x, temp_y),\
                                     (temp_x, temp_y))          
    else:
        x = range(-145, 145, 6)
        for item in x:
            if ground_type == 'plane':
                xyz_1 = convert_xyz((item + \
                            (int(current_point[0])/6) * 6, 150 + \
                            (int(current_point[1])/6)*6, 0), convert)
                x_angle_1, z_angle_1 = get_double_angle(xyz_1, current_point, True)
                if convert == 'neither' or convert == 'x':
                    z_angle_1 += rotation[1]
                if convert == 'neither' or convert == 'z':
                    x_angle_1 += rotation[0]
                xyz_2 = convert_xyz((item + \
                            (int(current_point[0])/6) * 6, -150 + \
                            (int(current_point[1])/6)*6, 0), convert)
                x_angle_2, z_angle_2 = get_double_angle(xyz_2, current_point, True)
                if convert == 'neither' or convert == 'x':
                    z_angle_2 += rotation[1]
                if convert == 'neither' or convert == 'z':
                    x_angle_2 += rotation[0]                    
            elif ground_type == 'receding':
                if convert == 'both' or convert == 'z':
                    convert = 'z'
                else:
                    convert = 'neither'
                xyz_1 = convert_xyz((item + \
                        (int(current_point[0])/6) * 6, -150 + \
                        (int(current_point[1])/6)*6, 0), 'z')
                x_angle_1, z_angle_1 = get_double_angle(xyz_1, current_point, True)
                #x_angle, z_angle = get_double_angle((item + \
                        #(int(current_point[0])/4) * 4, second_item + \
                        #(int(current_point[1])/4)*4, 0), current_point, True)
                x_angle_1 += rotation[0]
                xyz_2 = convert_xyz((item + \
                        (int(current_point[0])/6) * 6, 150 + \
                        (int(current_point[1])/6)*6, 0), 'z')
                x_angle_2, z_angle_2 = get_double_angle(xyz_2, current_point, True)
                #x_angle, z_angle = get_double_angle((item + \
                        #(int(current_point[0])/4) * 4, second_item + \
                        #(int(current_point[1])/4)*4, 0), current_point, True)  
                x_angle_2 += rotation[0]
            if abs(rotation[0]) > 90:
                if abs(z_angle_1) > 90:
                    try:
                        z_angle_1 = (180 - abs(z_angle_1)) * (z_angle_1/abs(z_angle_1))
                    except:
                        z_angle_1 = 180
                if abs(z_angle_2) > 90:
                    try:
                        z_angle_2 = (180 - abs(z_angle_2)) * (z_angle_2/abs(z_angle_2))
                    except:
                        z_angle_2 = 180                
                if abs(x_angle_1) > 180:
                    x_angle_1 = (360 - abs(x_angle_1)) * (x_angle_1/abs(x_angle_1)) * -1
                if abs(x_angle_2) > 180:
                    x_angle_2 = (360 - abs(x_angle_2)) * (x_angle_2/abs(x_angle_2)) * -1
            #z_angle += rotation[1]
            temp_x_1 = (((x_angle_1 + x_view/2.0) / x_view)) * width
            temp_y_1 = height - (((z_angle_1 + y_view/2.0) / y_view) * height)     
            #temp_x_2 = (((x_angle_2 + x_view/2.0) / x_view)) * width
            #temp_y_2 = height - (((z_angle_2 + y_view/2.0) / y_view) * height)
            temp_x_2 = ((((x_angle_1/abs(x_angle_1))*90 + x_view/2.0) / x_view)) * width
            temp_y_2 = height 
            temp_col = (255.0 , 255.0, 255.0)
            pygame.draw.line(screen, temp_col,(temp_x_1, temp_y_1),\
                (temp_x_2, temp_y_2)) 
        y = range(-150, 150, 6)    
        for second_item in y:        
            if ground_type == 'plane':
                xyz_1 = convert_xyz((-145 + \
                            (int(current_point[0])/6) * 6, item + \
                            (int(current_point[1])/6)*6, 0), convert)
                x_angle_1, z_angle_1 = get_double_angle(xyz_1, current_point, True)
                if convert == 'neither' or convert == 'x':
                    z_angle_1 += rotation[1]
                if convert == 'neither' or convert == 'z':
                    x_angle_1 += rotation[0]
                xyz_2 = convert_xyz((145 + \
                            (int(current_point[0])/6) * 6, item + \
                            (int(current_point[1])/6)*6, 0), convert)
                x_angle_2, z_angle_2 = get_double_angle(xyz_2, current_point, True)
                if convert == 'neither' or convert == 'x':
                    z_angle_2 += rotation[1]
                if convert == 'neither' or convert == 'z':
                    x_angle_2 += rotation[0]                    
            elif ground_type == 'receding':
                if convert == 'both' or convert == 'z':
                    convert = 'z'
                else:
                    convert = 'neither'
                xyz_1 = convert_xyz((-150 + \
                        (int(current_point[0])/6) * 6, item + \
                        (int(current_point[1])/6)*6, 0), 'z')
                x_angle_1, z_angle_1 = get_double_angle(xyz_1, current_point, True)
                #x_angle, z_angle = get_double_angle((item + \
                        #(int(current_point[0])/4) * 4, second_item + \
                        #(int(current_point[1])/4)*4, 0), current_point, True)
                x_angle_1 += rotation[0]
                xyz_2 = convert_xyz((150 + \
                        (int(current_point[0])/6) * 6, item + \
                        (int(current_point[1])/6)*6, 0), 'z')
                x_angle_2, z_angle_2 = get_double_angle(xyz_2, current_point, True)
                #x_angle, z_angle = get_double_angle((item + \
                        #(int(current_point[0])/4) * 4, second_item + \
                        #(int(current_point[1])/4)*4, 0), current_point, True)
                x_angle_2 += rotation[0]
            if abs(rotation[0]) > 90:
                if abs(z_angle_1) > 90:
                    try:
                        z_angle_1 = (180 - abs(z_angle_1)) * (z_angle_1/abs(z_angle_1))
                    except:
                        z_angle_1 = 180
                if abs(z_angle_2) > 90:
                    try:
                        z_angle_2 = (180 - abs(z_angle_2)) * (z_angle_2/abs(z_angle_2))
                    except:
                        z_angle_2 = 180                
                if abs(x_angle_1) > 180:
                    x_angle_1 = (360 - abs(x_angle_1)) * (x_angle_1/abs(x_angle_1)) * -1
                if abs(x_angle_2) > 180:
                    x_angle_2 = (360 - abs(x_angle_2)) * (x_angle_2/abs(x_angle_2)) * -1
            #z_angle += rotation[1]
            temp_x_1 = (((x_angle_1 + x_view/2.0) / x_view)) * width
            temp_y_1 = height - (((z_angle_1 + y_view/2.0) / y_view) * height)     
            temp_x_2 = (((x_angle_2 + x_view/2.0) / x_view)) * width
            temp_y_2 = height - (((z_angle_2 + y_view/2.0) / y_view) * height)
            temp_col = (255.0 , 255.0, 255.0)
            pygame.draw.line(screen, temp_col,(temp_x_1, temp_y_1),\
                (temp_x_2, temp_y_2))         

def convert_xyz(xyz, x_or_z='x'):
    '''returns a copy of xyz such that x and y are adjusted with regards to
    rotation[0].'''
    
    # 0 returns xyz
    # 90 return -yxz
    # -90 returns y-xz
    # +/-180 returns -x-yz
    
    if x_or_z == 'x':    
        temp_length = math.sqrt((xyz[0] - current_point[0])**2 + \
                                (xyz[1] - current_point[1])**2)
        temp_angle = get_double_angle(xyz, current_point)[0]
        temp_new_angle = temp_angle + rotation[0]
        return (math.sin(math.radians(temp_new_angle))*temp_length + \
                current_point[0], \
                math.cos(math.radians(temp_new_angle))*temp_length + \
                current_point[1], xyz[2])
    elif x_or_z == 'z':
        temp_length = math.sqrt((xyz[2] - current_point[2])**2 + \
                                (xyz[1] - current_point[1])**2)
        temp_angle = get_double_angle(xyz, current_point)[1]
        temp_new_angle = temp_angle + rotation[1]
        return (xyz[0], math.cos(math.radians(temp_new_angle))*temp_length + \
                current_point[1], \
                math.sin(math.radians(temp_new_angle))*temp_length + \
                current_point[2])  
    elif x_or_z == 'both':
        return convert_xyz(convert_xyz(xyz, 'x'), 'z')
    elif x_or_z == 'neither':
        return xyz
    
    
def print_status():
    
    print current_point
    print rotation

def reset():
    
    reset_current()
    reset_rotation()

def reset_current():
    
    global current_point
    current_point = [0, 0, 20]

def reset_rotation():
    
    global rotation
    rotation = [0, 0]
    #global rotate_dict
    #rotate_dict = {}
    #for key in light_dict:
        #rotate_dict[key] = key    

def view(view_type, convert, correct):
    
    if view_type == 'wide':
        x_view = 160
        y_view = 120
    elif view_type == 'normal':
        x_view = 120
        y_view = 90
    elif view_type == 'super_wide':
        x_view = 180
        y_view = 130
    elif view_type == 'hyper_wide':
        x_view = 270
        y_view = 150
    elif view_type == 'narrow':
        x_view = 90
        y_view = 60
    elif view_type == 'omega_wide':
        x_view = 360
        y_view = 180    
    
    #min_x = 0
    #max_x = 0
    #min_y = 0
    #max_y = 0    
    for shape in item_list:  
        if get_len(shape.center, current_point) < 1000:
            for point in shape.light:
                xyz = convert_xyz(point, convert)
                x_angle, z_angle = get_double_angle(xyz, current_point, correct)
                if convert == 'neither' or convert == 'z':
                    x_angle += rotation[0]
                if abs(z_angle) > 90:
                    try:
                        z_angle = (180 - abs(z_angle)) * (z_angle/abs(z_angle))
                    except:
                        z_angle = 180        
                if abs(rotation[0]) > 90:
                    if abs(x_angle) > 180:
                        x_angle = (360 - abs(x_angle)) * \
                            (x_angle/abs(x_angle)) * -1    
                if convert == 'neither' or convert == 'x':
                    z_angle += rotation[1]
                temp_x = (((x_angle + x_view/2.0) / x_view)) * width
                temp_y = height - (((z_angle + y_view/2.0) / y_view) * height)
                #print temp_x
                #print temp_y
                if 0 <= temp_x <= width and 0 <= temp_y <= height:   
                    if shape.light[point] <= 1.0:
                        temp_col = (255.0*shape.light[point], \
                                    255.0*shape.light[point], \
                                    255.0*shape.light[point])
                        pygame.draw.line(screen, temp_col,(temp_x, temp_y),\
                                         (temp_x, temp_y))
                    else:
                        temp_col = 255*(shape.light[point] - int(shape.light[point]))
                        pygame.draw.line(screen, (temp_col,temp_col,temp_col),\
                                    (temp_x, temp_y),(temp_x, temp_y))
                        for item in range(int(shape.light[point])):
                            pygame.draw.line(screen, (255,255,255),\
                                             (temp_x, temp_y),(temp_x, temp_y))
    #return max_x, min_x, max_y, min_y   

def draw_one_pixel(xyz, view_type, color):
    
    if view_type == 'wide':
        x_view = 160
        y_view = 120
    elif view_type == 'normal':
        x_view = 120
        y_view = 90
    elif view_type == 'super_wide':
        x_view = 180
        y_view = 130
    elif view_type == 'hyper_wide':
        x_view = 270
        y_view = 150
    elif view_type == 'narrow':
        x_view = 90
        y_view = 60
    elif view_type == 'omega_wide':
        x_view = 360
        y_view = 180 
        
    x_angle, z_angle = get_double_angle(xyz, current_point, True)    
    x_angle += rotation[0]
    z_angle += rotation[1]
    temp_x = (((x_angle + x_view/2.0) / x_view)) * width
    temp_y = height - (((z_angle + y_view/2.0) / y_view) * height)    
    pygame.draw.line(screen, color,(temp_x, temp_y),(temp_x, temp_y))    
    

def draw_origin(view_type):
    
    if view_type == 'wide':
        x_view = 160
        y_view = 120
    elif view_type == 'normal':
        x_view = 120
        y_view = 90
    elif view_type == 'super_wide':
        x_view = 180
        y_view = 130
    elif view_type == 'hyper_wide':
        x_view = 270
        y_view = 150
    elif view_type == 'narrow':
        x_view = 90
        y_view = 60
    elif view_type == 'omega_wide':
        x_view = 360
        y_view = 180    
    
    x_angle, z_angle = get_double_angle((0,0,0), current_point)
    temp_x = (((x_angle + x_view/2.0) / x_view)) * width
    temp_y = height - (((z_angle + y_view/2.0) / y_view) * height)   
    pygame.draw.line(screen, (0,0,255),(temp_x, temp_y),(temp_x, temp_y))

def move(key):
    
    move_1 = math.cos(math.radians(abs(float(rotation[0]))))
    move_2 = math.sin(math.radians(abs(float(rotation[0]))))
    #if -10 < look_angle < 10:
        #move_1 = 1
    #elif 170 < look_angle or -170 > look_angle:
        #move_1 = -1
    #elif 85 < look_angle < 95 or -85 > look_angle > -95:
        #move_1 = 0
    #move_1 = math.cos(math.radians(look_angle))
    #print move_1
    #move_2 = 1 - abs(move_1)
    #if move_1 < 0:
        #move_2 = move_2 * -1
    #move_2 = 1 - abs(move_1)
    #if abs(rotation[0]) > 90:
        #move_2 = move_2 * -1
    if rotation[0] > 0:
        move_2 = -move_2    
    if key == 'a':
        current_point[1] += 2*move_2
        current_point[0] -= 2*move_1
    elif key == 'w':
        up = math.sin(math.radians(-rotation[1]))
        current_point[1] += 2*(move_1 * (1 - abs(up)))
        current_point[0] += 2*(move_2 * (1 - abs(up)))
        current_point[2] += 2*up
    elif key == 's':
        down = math.sin(math.radians(-rotation[1]))
        current_point[1] -= 2*(move_1 * (1 - abs(down)))
        current_point[0] -= 2*(move_2 * (1 - abs(down)))
        current_point[2] -= 2*down
    elif key == 'd': 
        current_point[1] -= 2*move_2
        current_point[0] += 2*move_1
    elif key == 'i':
        current_point[1] += 2
    elif key == 'j':
        current_point[0] -= 2
    elif key == 'k':
        current_point[1] -= 2
    elif key == 'l':
        current_point[0] += 2

def draw_reticle():
    
    pygame.draw.line(screen, (0,0,255),(width/2.0, height/2.0),\
                     (width/2.0, height/2.0))
        
def draw_everything(view_type, ground, convert, correct):
    
    view(view_type, convert, correct)
    #draw_origin(view_type)        
    make_ground(view_type, ground, convert, correct, False)  
    draw_reticle()

def print_fps(current_time):
    
    temp_rect = pygame.Rect(0, 0, 120, 25)
    pygame.draw.rect(screen, (0,0,0), temp_rect, 0)
    pygame.draw.line(screen, (255,255,255), (0, 15),\
                             (115, 15),2)
    pygame.draw.line(screen, (255,255,255), (115, 0),\
                                 (115, 15),2)       
    font = pygame.font.SysFont(None, 21) 
    try:
        text = font.render(str(1.0/(time.time()-current_time)), 1, \
                           (255, 255, 255))
    except:
        text = font.render('1000', 1, (255,255,255))
    screen.blit(text, (0, 0))
    return time.time()

def help_move(item, key):
    
    if key == 't':
        item.move(0,1,0)
    elif key == 'f':
        item.move(-1,0,0)   
    elif key == 'g':
        item.move(0,-1,0)  
    elif key == 'h':
        item.move(1,0,0)
    elif key == 'y':
        item.move(0,0,1)
    elif key == 'r':
        item.move(0,0,-1)    
    
        
x = cube(20,20,30,20,'x')
y = sphere(10, -20, 40, 30, 'y')
z = cube(5, -10, 70,25, 'z')
q = sphere(5, 40,10, 45, 'q')
p = sphere(5, 1000, 1000, 20, 'p')
change = True
key_down = False
min_x = 0
max_x = 0
min_y = 0
max_y = 0
view_list = ['narrow', 'normal', 'wide', 'super_wide', 'hyper_wide', \
             'omega_wide']
ground_list = ['plane', 'receding']
convert_list = ['both', 'x', 'z', 'neither']
correct_list = [True, False]
view_num = 0
ground_num = 0
convert_num = 0
item_num = 0
correct_num = 0
keys_down = []
#origin = [0, 0, 0]
#rotate_dict = {}
#for key in light_dict:
    #rotate_dict[key] = key
current_time = time.time()
pygame.font.init()
while not quit:
    pygame.display.flip()
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            quit = True    
        elif event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_LEFT:
                #rotation[0] += 5
                #if rotation[0] > 180:
                    #rotation[0] = -180
            #elif event.key == pygame.K_RIGHT:
                #rotation[0] -= 5
                #if rotation[0] < -180:
                    #rotation[0] = 180
            #elif event.key == pygame.K_DOWN:
                #rotation[1] += 5
                #if rotation[1] > 90:
                    #rotation[1] = 90
            #elif event.key == pygame.K_UP:
                #rotation[1] -= 5
                #if rotation[1] < -90:
                    #rotation[1] = -90              
            #elif event.key == 32:
                #current_point[2] += 1
            #elif event.key == 304:
                #current_point[2] -= 1    
            if event.key == 13:
                print_status()
            elif event.key == 49:
                reset_current()
            elif event.key == 50:
                reset_rotation()
            elif event.key == 51:
                reset()
            elif event.key == 52:
                view_num += 1
                if view_num >= len(view_list):
                    view_num = 0
            elif event.key == 53:
                ground_num += 1
                if ground_num >= len(ground_list):
                    ground_num = 0   
            elif event.key == 54:
                convert_num += 1
                if convert_num >= len(convert_list):
                    convert_num = 0     
            elif event.key == 55:
                item_num += 1
                if item_num >= len(item_list):
                    item_num = 0       
            elif event.key == 56:
                correct_num += 1
                if correct_num >= len(correct_list):
                    correct_num = 0               
            keys_down.append(event.key)
            #view_angle_dict = {}   
            #light_dict = {}
            #x.update_view_angle_dict()
            #x.calc_view()
            #x.calc_light()      
            change = True
        elif event.type == pygame.KEYUP:
            keys_down.remove(event.key)
    if len(keys_down) > 0:
        if keys_down.count(97):
            move('a')
            #current_point[0] -= 0.2
        elif keys_down.count(100):
            move('d')
            #current_point[0] += 0.2
        if keys_down.count(276):
            rotation[0] += 5
            if rotation[0] > 180:
                rotation[0] = -180
            #for key in rotate_dict:
                #rotate_dict[key] = convert_xyz(key, 'both')            
        elif keys_down.count(275):
            rotation[0] -= 5
            if rotation[0] < -180:
                rotation[0] = 180
            #for key in rotate_dict:
                #rotate_dict[key] = convert_xyz(key, 'both')            
        if keys_down.count(119):
            move('w')
        elif keys_down.count(115):
            move('s')
        if keys_down.count(274):
            rotation[1] += 5
            if rotation[1] > 90:
                rotation[1] = 90
            #else:
                #for key in rotate_dict:
                    #rotate_dict[key] = convert_xyz(key, 'both')            
        elif keys_down.count(273):
            rotation[1] -= 5
            if rotation[1] < -90:
                rotation[1] = -90 
            #else:
                #for key in rotate_dict:
                    #rotate_dict[key] = convert_xyz(key, 'both')
        if keys_down.count(32):
            current_point[2] += 1
        elif keys_down.count(304):
            current_point[2] -= 1    
        if keys_down.count(105):
            move('i')
        elif keys_down.count(107):
            move('k')
        if keys_down.count(106):
            move('j')
        elif keys_down.count(108):
            move('l')
        if keys_down.count(116):
            help_move(item_list[item_num], ('t'))
        elif keys_down.count(103):
            help_move(item_list[item_num], ('g'))
        if keys_down.count(102):
            help_move(item_list[item_num], ('f'))
        elif keys_down.count(104):
            help_move(item_list[item_num], ('h'))
        if keys_down.count(121):
            help_move(item_list[item_num], ('y'))
        elif keys_down.count(114):
            help_move(item_list[item_num], ('r'))
        #view_angle_dict = {}   
        #for item in item_list:
            #item.update_view_angle_dict()
        #light_dict = {}
        #x.update_view_angle_dict()
        #x.calc_view()
        #x.calc_light()         
        change = True
    if change:
        screen.fill(black)
        #update(item_list)
        #temp_max_x, temp_min_x, temp_max_y, temp_min_y = view('hyper_wide')
        #max_y = max(max_y, temp_max_y)
        #max_x = max(max_x, temp_max_x)
        #min_y = min(min_y, temp_min_y)
        #min_x = min(min_x, temp_min_x)
        draw_everything(view_list[view_num], ground_list[ground_num], \
                        convert_list[convert_num], correct_list[correct_num])
    current_time = print_fps(current_time)
    change = False
    
pygame.quit()

#print max_x
#print min_x
#print max_y
#print min_y   