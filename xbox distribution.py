import pygame
import elementtree
import re
import urllib2
import time
import math
#import sys
#import os

#def restart_program():
    #"""Restarts the current program.
    #Note: this function does not return. Any cleanup action (like
    #saving data) must be done before calling this function."""
    #python = sys.executable
    #os.execl(python, python, * sys.argv)

def _html_to_mini_str(url):
    
    html_file = urllib2.urlopen(url)
    html_file.readline()
    html_file.readline()
    html_file.readline()
    html_file.readline()
    html_file.readline()
    html_file.readline()
    return html_file.readline()

def make_int(num):
    
    temp_num = num.split(',')
    num = ''
    for item in temp_num:
        num += item
    return int(num)

def get_rank(num):
    
    temp_num = highest - num
    #temp_num = num
    temp_num /= step_size
    return highest - (temp_num * step_size)

def update_all():

    for item in \
        re.findall('href=\'/profile/.*?"table-gs">(.*?)</li></ul></div>', \
                     current_page):
        if not item.startswith('updating'):
            rank = get_rank(make_int(item))
            if score_dict.has_key(rank):
                score_dict[rank] = score_dict[rank] + 1
            else:
                score_dict[rank] = 1  
	    score_list.append(make_int(item))
	    append_list.append(make_int(item))

def update_score_dict():
    
    for item in \
        re.findall('href=\'/profile/.*?"table-gs">(.*?)</li></ul></div>', \
                     current_page):
        if not item.startswith('updating'):
            rank = get_rank(make_int(item))
            if score_dict.has_key(rank):
                score_dict[rank] = score_dict[rank] + 1
            else:
                score_dict[rank] = 1	    

def update_score_list():
    
    for item in \
        re.findall('href=\'/profile/.*?"table-gs">(.*?)</li></ul></div>', \
                     current_page):
	if not item.startswith('updating'):
	    score_list.append(make_int(item))
	    append_list.append(make_int(item))

def save_info():
    
    f = open('xbox distribution info.txt', 'w')
    f.write('%s\n' % url)
    for item in score_dict.keys():
	if type(item) == int:
	    f.write('%i:%i\n' % (item, score_dict[item]))
	else:
	    f.write('%s:%i\n' % (item, score_dict[item]))
    #f.write('list\n')
    #for item in score_list:
	#f.write('%s\n' % item)
    f.close()
    f = open('xbox distribution list.txt', 'a')
    for item in append_list:
	f.write('%s\n' % item)
    f.close()

def get_display_dict(low, high, width, final_dict):
    
    display_dict = {}
    step_size = (high - low) / width
    if step_size < 1:
	step_size = 1
    for item in final_dict:
	if low <= item <= high:
	    if display_dict.has_key((item-low)/step_size):
		display_dict[(item-low)/step_size] = display_dict[(item-low)/step_size] + \
		    final_dict[item]
	    else:
		display_dict[(item-low)/step_size] = final_dict[item]
    return [display_dict, step_size]
	

def first_stat_get():
    
    global score_list
    global mean
    global final_dict
    score_list.sort()
    median = get_list_median(score_list)
    rewrite()
    final_dict = get_final_dict()
    mean = get_dict_mean(final_dict)
    mode, sd, var = get_dict_mode_sd_var(final_dict)
    save_stats(mean, median, mode, sd, var)
    return [mean, median, mode, sd, var]

def get_final_dict():
    
    f = open('xbox final distribution.txt', 'r')
    score_dict = {}
    line = f.readline()
    while line != '':
	temp_info = line.split(':')
	score_dict[int(temp_info[0])] = int(temp_info[1][:-1])
	line = f.readline()
    f.close()
    return score_dict

def rewrite():
    
    f = open('xbox distribution list.txt', 'r')
    final_dict = {}
    line = f.readline()
    while line != '':
	if line[:-1] != 'unknown':
	    if final_dict.has_key(int(line[:-1])):
		final_dict[int(line[:-1])] = final_dict[int(line[:-1])] + 1
	    else:
		final_dict[int(line[:-1])] = 1
	line = f.readline()
    f.close()
    f = open('xbox final distribution.txt', 'w')
    for item in final_dict:
	f.write('%i:%i\n' % (item,final_dict[item]))
    f.close()

def get_stats():
    
    f = open('xbox distribution stats.txt', 'r')
    mean = int(f.readline()[:-1])
    median = int(f.readline()[:-1])
    mode = int(f.readline()[:-1])
    sd = int(f.readline()[:-1])
    var = int(f.readline()[:-1])
    f.close()
    return [mean, median, mode, sd, var]

def save_stats(mean, median, mode, sd, var):
    
    f = open('xbox distribution stats.txt', 'w')
    f.write('%i\n' % mean)
    f.write('%i\n' % median)
    f.write('%i\n' % mode)
    f.write('%i\n' % sd)
    f.write('%i\n' % var)
    f.close()

def get_info():
    
    global url
    global current_page
    global score_dict
    global score_list
    global append_list
    f = open('xbox distribution info.txt', 'r')
    url = f.readline()[:-1]
    current_page = _html_to_mini_str(url)
    line = f.readline()
    score_dict = {}
    score_list = []
    append_list = []
    while line != '':
	temp_info = line.split(':')
	if temp_info[0] == 'unknown':
	    #score_dict[temp_info[0]] = int(temp_info[1][:-1])
	    pass
	else:
	    score_dict[int(temp_info[0])] = int(temp_info[1][:-1])
	line = f.readline()
    #line = f.readline()
    #while line != '':
	#score_list.append(line[:-1])
	#line = f.readline()
    f.close()
    f = open('xbox distribution list.txt', 'r')
    line = f.readline()
    while line != '' and line != '\n':
	if line[:-1] == 'unknown':
	    #score_list.append(line[:-1])
	    pass
	else:
	    score_list.append(int(line[:-1]))
	line = f.readline()    
    f.close()

def get_page(url):
    
    return url[51:]

def get_approx_mean():
    
    total = 0.0
    num = 0.0
    for key in score_dict:
	total += key * score_dict[key]
	num += score_dict[key]
    return total / num


def get_dict_mean(dct):
    
    total = 0.0
    amount = 0
    for item in dct:
	total += dct[item]*item
	amount += dct[item]
    return total / amount

def get_dict_mode(dct):
    
    current = 1
    for item in dct:
	if dct[item] > dct[current]:
	    current = item
    return current

def get_dict_sd(dct):
    
    total = 0.0
    amount = 0
    for item in dct:
	total += ((item - mean)**2)*dct[item]
	amount += dct[item]
    return math.sqrt(total/amount)

def get_dict_var(dct):
    
    total = 0.0
    amount = 0
    for item in dct:
	total += ((item)**2)*dct[item]
	amount += dct[item]
    return (total/amount) - (mean**2)

def get_dict_mode_sd_var(dct):
    
    current = 0
    sd_total = 0.0
    var_total = 0.0
    amount = 0
    for item in dct:
	sd_total += ((item - mean)*dct[item])**2
	var_total += (item*dct[item])**2
	if dct[item] > current:
	    current = item
	amount += dct[item]
    return [current, math.sqrt(sd_total/amount), \
	        (var_total/amount)-(mean**2)]

def get_list_mean(lst):
    
    total = 0.0
    for item in lst:
	total += item
    return total / len(lst)

def get_list_mode(lst):
    '''requires a sorted list'''
    
    current = 0
    prev = 0
    count_1 = 0
    count_2 = 0
    for item in lst:
	if item == current:
	    count_1 += 1
	else:
	    if count_1 > count_2:
		prev = current
		count_2 = count_1
	    current = item
	    count_1 = 1
    if count_1 > count_2:
	return current   
    else:
	return prev

def get_list_median(lst):
    '''requires a sorted list'''
    
    if len(lst) % 2 == 1:
	return lst[len(lst)/2]
    else:
	return (lst[len(lst)/2] + lst[(len(lst)/2)-1])/2.0

def get_list_sd(lst):
    '''requires a sorted list and the global variable mean'''
    
    total = 0.0
    for item in lst:
	total += (item - mean)**2
    return math.sqrt(total/len(lst))

def get_list_var(lst):
    '''requires a sorted list and the global variable mean'''
    
    total = 0.0
    for item in lst:
	total += item**2
    return (total/len(lst)) - (mean**2)

def get_list_mode_sd_var(lst):
    '''requires a sorted list and the global variable mean'''
    
    current = 0
    prev = -1
    count_1 = 0
    count_2 = 0
    sd_total = 0.0
    var_total = 0.0
    for item in lst:
	sd_total += (item - mean)**2
	var_total += item**2
	if item == current:
	    count_1 += 1
	else:
	    if count_1 > count_2:
		prev = current
		count_2 = count_1
	    current = item
	    count_1 = 1
    if count_1 > count_2:
	return [current, math.sqrt(sd_total/len(lst)), \
	        (var_total/len(lst))-(mean**2)]
    else:
	return [prev, math.sqrt(sd_total/len(lst)), \
	        (var_total/len(lst))-(mean**2)]

def update_file():
    
    f = open('xbox distribution.py', 'a')
    #x = open('xbox distribution change template.py', 'r')
    #line = x.readline()
    #while line != '':
        #f.write(line)
    #x.close()
    f.write('\nscore_dict = {}\n')
    for item in score_dict.keys():
        f.write('score_dict[%i] = %i\n' % (item, score_dict[item]))
    f.write('url = "%s"\n' % url)
    f.write('current_page = _html_to_mini_str(url)\n\n')
    f.write('if decision == "y":\n\n')
    f.write('    quit = False\n')
    f.write('    pygame.display.init()\n')
    f.write('    screen_info = initialize_screen(1600, 800)\n')
    f.write('    screen, width, height = screen_info[0], screen_info[1], screen_info[2]\n')
    f.write('    x_val = 0\n')
    f.write('    max_value = float(max(score_dict.values()))\n')
    f.write('    pygame.font.init()\n\n')
    f.write('    while url != last and not quit:\n')
    f.write('\turl = \'http://www.xboxlivescore.com\' + \\\n')
    f.write('\t    re.findall(\'href="(/xbox-live-leaderboard/.*?)">\', current_page)[-2]\n')
    f.write('\tcurrent_page = _html_to_mini_str(url)\n')
    f.write('\tupdate_score_dict()\n')
    f.write('\tmax_value = float(max(score_dict.values()))\n')
    f.write('\tevent_list = pygame.event.get()\n')
    f.write('\tfor event in event_list:\n')
    f.write('\t    if event.type == pygame.QUIT:\n')
    f.write('\t\tquit = True\n')    
    f.write('\t    elif event.type == pygame.MOUSEMOTION:\n')
    f.write('\t\tx_val = event.pos[0]\n')
    f.write('\tscreen.fill((0,0,0))\n')
    f.write('\tfor item in score_dict:\n')
    f.write('\t    temp_y = (score_dict[item] / max_value) * height\n')
    f.write('\t    pygame.draw.line(screen, (255,255,255), (item/step_size, height), \\\n')
    f.write('\t\t(item/step_size, height - temp_y))\n')
    f.write('\tfont = pygame.font.SysFont(None, 21)\n')
    f.write('\ttext = font.render(str((x_val*step_size) + (highest % step_size)), 1, \\\n')
    f.write('\t\t(255,255,255))\n')
    f.write('\tscreen.blit(text, (0,0))\n\n')
    f.write('else:\n\n')
    f.write('    quit = False\n')
    f.write('    pygame.display.init()\n')
    f.write('    initialize_screen(1600, 800)\n\n')
    f.write('    while url != last and not quit:\n')
    f.write('\turl = \'http://www.xboxlivescore.com\' + \\\n')
    f.write('\t    re.findall(\'href="(/xbox-live-leaderboard/.*?)">\', current_page)[-2]\n')
    f.write('\tcurrent_page = _html_to_mini_str(url)\n')
    f.write('\tupdate_score_dict()\n')
    f.write('\tevent_list = pygame.event.get()\n')
    f.write('\tfor event in event_list:\n')
    f.write('\t    if event.type == pygame.QUIT:\n')
    f.write('\t\tquit = True\n\n')
    f.write('pygame.quit()\n')
    f.write('update_file()\n\n')
    f.close()

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

url = 'http://www.xboxlivescore.com/xbox-live-leaderboard/'
current_page = _html_to_mini_str(url)
last = 'http://www.xboxlivescore.com' + \
    re.findall('&nbsp;&nbsp;<a href="(.*?)">Last', current_page)[0]
highest = re.findall('href=\'/profile/.*?"table-gs">(.*?)</li></ul></div>', \
                     current_page)[0]
highest = make_int(highest)
step_size = highest / 1800


reset = ''
while reset != 'y' and reset != 'n' and reset != 'd':
    reset = raw_input('Do you want to reset your info? (y/n) \
\nOr have you finished collecting information? (d) ')
    
if reset == 'y':
    
    score_dict = {}
    score_list = []
    append_list = []
    update_score_dict()
    update_score_list()
    f = open('xbox distribution list.txt', 'w')
    f.close()
    
elif reset == 'n':
    
    get_info()
    
else:
    
    #get_info()
    last = url
    decision = 'd'
    do_save = False


#quit = False
#pygame.display.init()
#initialize_screen(1600, 800)

#while url != last and not quit:
    #url = 'http://www.xboxlivescore.com' + \
        #re.findall('href="(/xbox-live-leaderboard/.*?)">', current_page)[-2]
    #current_page = _html_to_mini_str(url)
    #update_score_dict()
    #event_list = pygame.event.get()
    #for event in event_list:
        #if event.type == pygame.QUIT:
            #quit = True 

#pygame.quit()
#update_file()

#quit = False
#pygame.display.init()
#screen_info = initialize_screen(1600, 800)
#screen, width, height = screen_info[0], screen_info[1], screen_info[2]
#x_val = 0
#max_value = float(max(score_dict.values()))
#pygame.font.init()

#while not quit:
    #pygame.display.flip()
    #event_list = pygame.event.get()
    #for event in event_list:
        #if event.type == pygame.QUIT:
            #quit = True    
        #elif event.type == pygame.MOUSEMOTION:
            #x_val = event.pos[0]
    #screen.fill((0,0,0))
    #for item in score_dict:
        #temp_y = (score_dict[item] / max_value) * height
        #pygame.draw.line(screen, (255,255,255), (item/step_size, height), \
                         #(item/step_size, height - temp_y))
    #font = pygame.font.SysFont(None, 21) 
    #text = font.render(str((x_val*step_size) + (highest % step_size)), 1, \
                               #(255, 255, 255))
    #screen.blit(text, (0, 0))    

if reset != 'd':
    
    mean = 0
    decision = ''
    while decision != 'y' and decision != 'n':
	decision = raw_input('Do you want to see the graph as it is updated? (y/n) ')
    
    page_num = get_page(url)
    last_page = re.findall('href="/xbox-live-leaderboard/(.*?)">', current_page)[-1]
    
    prev_time = time.time()
    im_prev_time = prev_time
    save_for_exception = current_page

    do_save = True

if decision == 'y':
    
    quit = False
    pygame.display.init()
    screen_info = initialize_screen(1800, 250)
    screen, width, height = screen_info[0], screen_info[1], screen_info[2]
    x_val = 0
    max_value = float(max(score_dict.values()))
    changed = False
    pygame.font.init()    
    font = pygame.font.SysFont(None, 21) 
    
    while url != last and not quit:
	pygame.display.flip()
	changed_one = False
	while not changed_one:
	    try:
		url = 'http://www.xboxlivescore.com' + \
		    re.findall('href="(/xbox-live-leaderboard/.*?)">', current_page)[-2]
		changed_one = True
	    except:
		#print re.findall('href="(/xbox-live-leaderboard/.*?)">', current_page)
		#print current_page
		#print save_for_exception
		#print url
		#do_save = False
		#quit = True
		#break
		changed_two = False
		while not changed_two:
		    try:
			url = 'http://www.xboxlivescore.com/xbox-live-leaderboard/' + \
			    str(int(get_page(url))+25)
			current_page = _html_to_mini_str(url)
			changed_two = True
		    except:
			text = font.render('trouble connecting to the internet', 1, \
				                   (255, 255, 255))
			screen.blit(text, (1400, 30))
			pygame.display.flip()
			changed = False	
		if score_dict.has_key('unknown'):
		    score_dict['unknown'] = score_dict['unknown'] + 25
		else:
		    score_dict['unknown'] = 25
		score_list += ['unknown'] * 25
		append_list += ['unknown'] * 25
	page_num = get_page(url)
	save_for_exception = current_page
	while not changed:
	    try:
		current_page = _html_to_mini_str(url)
		changed = True
	    except:
		text = font.render('trouble connecting to the internet', 1, \
			                   (255, 255, 255))
		screen.blit(text, (1400, 30))
		pygame.display.flip()
		changed = False
	update_all()
	max_value = float(max(score_dict.values()))
	event_list = pygame.event.get()
	for event in event_list:
	    if event.type == pygame.QUIT:
		quit = True
	    elif event.type == pygame.MOUSEMOTION:
		x_val = event.pos[0]	
	    elif event.type == pygame.VIDEORESIZE:
		height = event.h
		width = event.w
		screen = pygame.display.set_mode([width, height], \
	                             pygame.RESIZABLE)	 
	changed = False
	screen.fill((0,0,0))
	for item in score_dict:
	    if item != 'unknown':
		temp_y = (score_dict[item] / max_value) * height
		pygame.draw.line(screen, (255,255,255), (item/step_size, height), \
		                 (item/step_size, height - temp_y))
	text = font.render(str((x_val*step_size) + (highest % step_size)), 1, \
                                   (255, 255, 255))
	percentage = (float(page_num) / float(last_page))*100
	second_text = font.render("%s/%s, %f%%" % (page_num, last_page, percentage), 1, (255, 255, 255))
	screen.blit(text, (0, 0))  
	screen.blit(second_text, (1400, 0))  
	time_diff = time.time() - im_prev_time
	pages_left = (int(last_page) - int(page_num))/25
	eta = time_diff * pages_left
	eta_days = int(eta / 86400)
	eta_hours = int((eta - (eta_days * 86400)) / 3600)
	eta_mins = int((eta - (eta_days * 86400) - (eta_hours * 3600)) / 60)
	eta_secs = int((eta - (eta_days * 86400) - (eta_hours * 3600) - (eta_mins * 60)))
	if eta_hours < 10:
	    eta_hours = '0' + str(eta_hours)
	else:
	    eta_hours = str(eta_hours)
	if eta_mins < 10:
	    eta_mins = '0' + str(eta_mins)
	else:
	    eta_mins = str(eta_mins)	
	if eta_secs < 10:
	    eta_secs = '0' + str(eta_secs)
	else:
	    eta_secs = str(eta_secs)	
	second_text = font.render("ETA: %i:%s:%s:%s:%f" % (eta_days, eta_hours, eta_mins, eta_secs, eta), 1, (255, 255, 255))
	screen.blit(second_text, (1100, 0))  
	im_prev_time = time.time()
	if time.time() - prev_time > 60:
	    text = font.render('saving...', 1, (255, 255, 255))
	    screen.blit(text, (1400, 30))
	    pygame.display.flip()	    
	    save_info()
	    prev_time = time.time()
	    append_list = []

elif reset == 'd':
    
    quit = False
    pygame.display.init()
    initialize_screen(1600, 800)
    
    while url != last and not quit:
	url = 'http://www.xboxlivescore.com' + \
            re.findall('href="(/xbox-live-leaderboard/.*?)">', current_page)[-2]
	current_page = _html_to_mini_str(url)
	update_all()
	event_list = pygame.event.get()
	for event in event_list:
	    if event.type == pygame.QUIT:
		quit = True     
	if time.time() - prev_time > 60:
	    save_info()
	    prev_time = time.time()
	    append_list = []
		
pygame.quit()
#update_file()
if do_save:
    save_info()
append_list = []

if url == last:
    #first
    #final_dict = {}
    #mean, median, mode, sd, var = first_stat_get()
    #subsequent
    final_dict = get_final_dict()
    mean, median, mode,sd,var = get_stats()
    pygame.display.init()
    screen_info = initialize_screen(1800, 250)
    screen, width, height = screen_info[0], screen_info[1], screen_info[2]
    display_dict, step_size = get_display_dict(0, 1000000, width, final_dict)
    high = 1000000
    low = 0
    x_val = 0
    pygame.font.init()    
    font = pygame.font.SysFont(None, 21)     
    quit = False
    while not quit:
	pygame.display.flip()
	screen.fill((0,0,0))
	event_list = pygame.event.get()
	for event in event_list:
	    if event.type == pygame.QUIT:
		quit = True
	    elif event.type == pygame.MOUSEMOTION:
		x_val = event.pos[0]	
	    elif event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 1:
		    low = (x_val*step_size) + (high % step_size) +low
		elif event.button == 3:
		    high = (x_val*step_size) + (high % step_size) +low
		elif event.button == 2:
		    low = 0
		    high = 1000000
		if high < low + width:
		    high = low + width		    
		display_dict, step_size = \
		    get_display_dict(low, high, width, final_dict)
	    elif event.type == pygame.VIDEORESIZE:
		height = event.h
		width = event.w
		screen = pygame.display.set_mode([width, height], \
		                     pygame.RESIZABLE)	
		screen.fill((0,0,0))
	try:
	    max_value = float(max(display_dict.values()))
	except:
	    pass
	for item in display_dict:
	    temp_y = (display_dict[item] / float(max_value)) * height
	    pygame.draw.line(screen, (255,255,255), ((item), height), \
		                     ((item), height - temp_y))  
	text = font.render(str((x_val*step_size) + (high % step_size) +low), 1,\
	                               (255, 255, 255))    
	screen.blit(text, (1400, 0)) 
	second_text = font.render("%i - %i" % (low, high), 1, (255, 255, 255))
	screen.blit(second_text, (1400, 20))

pygame.quit()

# once done, redo with highest ~= 105000. or 3 sd away from mean
