import re
import json
import os

def load_and_convert():
    
    s = open('/Users/Devon/Dropbox/programming/wiki_json_win.txt', 'r')
    y = json.load(s)
    x = convert_json(y)
    cont_conv(x)    

def stringify_l(l):
    
    pass

def cont_conv(l_list):
    x = l_list
    #b = open('/Users/Devon/Dropbox/programming/bulk_json_mac.json', 'w')
    i = 0
    b = open('/Users/Devon/Desktop/batch_json/wiki'+str(i)+'.json', 'w')
    for j in range(len(x)):
        if (j + 1) % 10000 == 0:
            i += 1
            b.close()
            b = open('/Users/Devon/Desktop/batch_json/wiki'+str(i)+'.json', 'w')
        b.write('{"index":{"_index":"wiki", "_type":"wiki", "_id":"%s"}}\n' % str(j))   
        if x[j]['geo']:
            if x[j]['geo']['lat'] and x[j]['geo']['lon']:
                temp_str = '{"geo":{"lat":' + x[j]['geo']['lat'] + ',"lon":' + \
                    x[j]['geo']['lon'] + '},'
            #elif x[j]['geo']['lat']:
                #temp_str = '{"geo":{"lat":' + x[j]['geo']['lat'] + \
                    #',"lon":null},'             
            #elif x[j]['geo']['lon']:
                #temp_str = '{"geo":{"lat":null,"lon":' + \
                    #x[j]['geo']['lon'] + '},'      
            else:
                #temp_str = '{"geo":{"lat":null, "lon":null},'    
                temp_str = '{"geo":null,'
        else:
            #temp_str = '{"geo":{"lat":null, "lon":null},'
            temp_str = '{"geo":null,'
        
        if x[j]['r_geo']:
            if x[j]['r_geo']['lat'] and x[j]['r_geo']['lon']:
                temp_str += '"r_geo":{"lat":' + x[j]['r_geo']['lat'] + ',"lon":' + \
                    x[j]['r_geo']['lon'] + '},'
            #elif x[j]['r_geo']['lat']:
                #temp_str = '{"r_geo":{"lat":' + x[j]['r_geo']['lat'] + \
                    #',"lon":null},'             
            #elif x[j]['r_geo']['lon']:
                #temp_str = '{"r_geo":{"lat":null,"lon":' + \
                    #x[j]['r_geo']['lon'] + '},'  
            else:
                #temp_str += '"r_geo":{"lat":null, "lon":null},'            
                temp_str += '"r_geo":null,'
        else:
            #temp_str += '"r_geo":{"lat":null, "lon":null},'
            temp_str += '"r_geo":null,'
        
        if x[j]['river_geo']['source']:
            if x[j]['river_geo']['source']['lat'] and x[j]['river_geo']['source']['lon']:
                temp_str += '"river_source":{"lat":' + x[j]['river_geo']['source']['lat'] + ',"lon":' + \
                    x[j]['river_geo']['source']['lon'] + '},'   
            else:       
                temp_str += '"river_source":null,'        
        else:
            temp_str += '"river_source":null,'
            
        if x[j]['river_geo']['source_confluence']:
            if x[j]['river_geo']['source_confluence']['lat'] and x[j]['river_geo']['source_confluence']['lon']:
                temp_str += '"river_source_confluence":{"lat":' + x[j]['river_geo']['source_confluence']['lat'] + ',"lon":' + \
                    x[j]['river_geo']['source_confluence']['lon'] + '},'   
            else:       
                temp_str += '"river_source_confluence":null,'        
        else:
            temp_str += '"river_source_confluence":null,'  
            
        if x[j]['river_geo']['mouth']:
            if x[j]['river_geo']['mouth']['lat'] and x[j]['river_geo']['mouth']['lon']:
                temp_str += '"river_mouth":{"lat":' + x[j]['river_geo']['mouth']['lat'] + ',"lon":' + \
                    x[j]['river_geo']['mouth']['lon'] + '},'   
            else:       
                temp_str += '"river_mouth":null,'        
        else:
            temp_str += '"river_mouth":null,'        
        
        if x[j]['e_geo']['lowest']:
            if x[j]['e_geo']['lowest']['lat'] and x[j]['e_geo']['lowest']['lon']:
                temp_str += '"elevation_lowest":{"lat":' + x[j]['e_geo']['lowest']['lat'] + ',"lon":' + \
                    x[j]['e_geo']['lowest']['lon'] + '},'   
            else:       
                temp_str += '"elevation_lowest":null,'        
        else:
            temp_str += '"elevation_lowest":null,'      
            
        if x[j]['e_geo']['highest']:
            if x[j]['e_geo']['highest']['lat'] and x[j]['e_geo']['highest']['lon']:
                temp_str += '"elevation_highest":{"lat":' + x[j]['e_geo']['highest']['lat'] + ',"lon":' + \
                    x[j]['e_geo']['highest']['lon'] + '},'   
            else:       
                temp_str += '"elevation_highest":null,'        
        else:
            temp_str += '"elevation_highest":null,'        
        
        #if x[j]['river_geo'] == {}:
            ##temp_str+= '"river_geo":{"lat":null, "lon":null},'
            #temp_str += '"river_geo":{"source":null, "source_confluence":null, "mouth":null},'
        #else:
            #temp_str+= '"river_geo":{'
            #if x[j]['river_geo']['source']:
                ##temp_str += '"source":{"lat":"' + \
                    ##x[j]['river_geo']['source']['lat'] + '","lon":"' + \
                    ##x[j]['river_geo']['source']['lon'] + '"},'
                #if x[j]['river_geo']['source']['lat'] and x[j]['river_geo']['source']['lon']:
                    #temp_str = '{"source":{"lat":' + x[j]['river_geo']['source']['lat'] + ',"lon":' + \
                        #x[j]['river_geo']['source']['lon'] + '},'
                ##elif x[j]['river_geo']['source']['lat']:
                    ##temp_str = '{"source":{"lat":' + x[j]['river_geo']['source']['lat'] + \
                        ##',"lon":null},'             
                ##elif x[j]['river_geo']['source']['lon']:
                    ##temp_str = '{"source":{"lat":null,"lon":' + \
                        ##x[j]['river_geo']['source']['lon'] + '},'    
                #else:
                    ##temp_str += '"source":{"lat":null, "lon":null},'          
                    #temp_str += '"source":null,'
            #else:
                ##temp_str += '"source":{"lat":null, "lon":null},'
                #temp_str += '"source":null,'
            #if x[j]['river_geo']['source_confluence']:
                ##temp_str += '"source_confluence":{"lat":"' + \
                    ##x[j]['river_geo']['source_confluence']['lat'] + '","lon":"' + \
                    ##x[j]['river_geo']['source_confluence']['lon'] + '"},'
                #if x[j]['river_geo']['source_confluence']['lat'] and \
                   #x[j]['river_geo']['source_confluence']['lon']:
                    #temp_str = '{"source_confluence":{"lat":' + \
                        #x[j]['river_geo']['source_confluence']['lat'] + ',"lon":' + \
                        #x[j]['river_geo']['source_confluence']['lon'] + '},'
                ##elif x[j]['river_geo']['source_confluence']['lat']:
                    ##temp_str = '{"source_confluence":{"lat":' + \
                        ##x[j]['river_geo']['source_confluence']['lat'] + \
                        ##',"lon":null},'             
                ##elif x[j]['river_geo']['source_confluence']['lon']:
                    ##temp_str = '{"source_confluence":{"lat":null,"lon":' + \
                        ##x[j]['river_geo']['source_confluence']['lon'] + '},'  
                #else:
                    ##temp_str += '"source_confluence":{"lat":null, "lon":null},'   
                    #temp_str += '"source_confluence":null,'  
            #else:
                ##temp_str += '"source_confluence":{"lat":null, "lon":null},'     
                #temp_str += '"source_confluence":null,'  
            #if x[j]['river_geo']['mouth']:
                ##temp_str += '"mouth":{"lat":"' + \
                    ##x[j]['river_geo']['mouth']['lat'] + '","lon":"' + \
                    ##x[j]['river_geo']['mouth']['lon'] + '"}},'
                #if x[j]['river_geo']['mouth']['lat'] and x[j]['river_geo']['mouth']['lon']:
                    #temp_str = '{"mouth":{"lat":' + x[j]['river_geo']['mouth']['lat'] + ',"lon":' + \
                        #x[j]['river_geo']['mouth']['lon'] + '}},'
                ##elif x[j]['river_geo']['mouth']['lat']:
                    ##temp_str = '{"mouth":{"lat":' + x[j]['river_geo']['mouth']['lat'] + \
                        ##',"lon":null},'             
                ##elif x[j]['river_geo']['mouth']['lon']:
                    ##temp_str = '{"mouth":{"lat":null,"lon":' + \
                        ##x[j]['river_geo']['mouth']['lon'] + '},'  
                #else:
                    ##temp_str += '"mouth":{"lat":null, "lon":null},'      
                    #temp_str += '"mouth":null},' 
            #else:
                ##temp_str += '"mouth":{"lat":null, "lon":null}},'  
                #temp_str += '"mouth":null},'  
            
        #if x[j]['e_geo'] == {}:
            ##temp_str+= '"e_geo":{"lat":null, "lon":null},'
            #temp_str += '"e_geo":{"lowest":null, "highest":null},'
        #else:
            #temp_str+= '"e_geo":{'
            #if x[j]['e_geo']['highest']:
                ##temp_str += '"highest":{"lat":"' + \
                    ##x[j]['e_geo']['highest']['lat'] + '","lon":"' + \
                    ##x[j]['e_geo']['highest']['lon'] + '"},'
                #if x[j]['e_geo']['highest']['lat'] and x[j]['e_geo']['highest']['lon']:
                    #temp_str = '{"highest":{"lat":' + x[j]['e_geo']['highest']['lat'] + ',"lon":' + \
                        #x[j]['e_geo']['highest']['lon'] + '},'
                ##elif x[j]['e_geo']['highest']['lat']:
                    ##temp_str = '{"highest":{"lat":' + x[j]['e_geo']['highest']['lat'] + \
                        ##',"lon":null},'             
                ##elif x[j]['e_geo']['highest']['lon']:
                    ##temp_str = '{"highest":{"lat":null,"lon":' + \
                        ##x[j]['e_geo']['highest']['lon'] + '},'  
                #else:
                    ##temp_str += '"highest":{"lat":null, "lon":null},'                
                    #temp_str += '"highest":null,' 
            #else:
                ##temp_str += '"highest":{"lat":null, "lon":null},'   
                #temp_str += '"highest":null,' 
            #if x[j]['e_geo']['lowest']:
                ##temp_str += '"lowest":{"lat":"' + \
                    ##x[j]['e_geo']['lowest']['lat'] + '","lon":"' + \
                    ##x[j]['e_geo']['lowest']['lon'] + '"}},'
                #if x[j]['e_geo']['lowest']['lat'] and x[j]['e_geo']['lowest']['lon']:
                    #temp_str = '{"lowest":{"lat":' + x[j]['e_geo']['lowest']['lat'] + ',"lon":' + \
                        #x[j]['e_geo']['lowest']['lon'] + '}},'
                ##elif x[j]['e_geo']['lowest']['lat']:
                    ##temp_str = '{"lowest":{"lat":' + x[j]['e_geo']['lowest']['lat'] + \
                        ##',"lon":null},'             
                ##elif x[j]['e_geo']['lowest']['lon']:
                    ##temp_str = '{"lowest":{"lat":null,"lon":' + \
                        ##x[j]['e_geo']['lowest']['lon'] + '},'  
                #else:
                    ##temp_str += '"lowest":{"lat":null, "lon":null},'                         
                    #temp_str += '"lowest":null},'   
            #else:
                ##temp_str += '"lowest":{"lat":null, "lon":null}},'       
                #temp_str += '"lowest":null},'   
        temp_str += '"info":"' + \
            x[j]['first_para'][:-1].replace('"', "'").replace('\t', '').replace('\n','')\
            + '",'
            
        temp_str += '"title":"' + x[j]['title'].strip() + '"}\n'
        
        if j == 169912:
            print j
            print temp_str
        b.write(temp_str.encode('utf8'))
    b.write('\n')
    b.close()

    #{"geo":null,"r_geo":null,"river_source":null,"river_source_confluence":null,"river_mouth":null,"elevation_lowest":null,"elevation_highest":null,"first_para":"''' Pudur	'''({{lang-ta|  புதூர் }}) is a village in the [[Annavasal block|Annavasal]][[revenue block]] of [[Pudukkottai district]],&lt;ref&gt;http://tnmaps.tn.nic.in/pr_villages.php?dc=22&amp;tlkname=Annavasal&amp;region=1&amp;lvl=block&amp;size=1200&lt;/ref&gt; [[Tamil Nadu]], [[India]].","title":"Pudur, Pudukkottai"}


def conv_line(line):
    
    new_line = line.replace("'geo'", '"geo"')
    new_line = new_line.replace("'title'", '"title"')

def convert_json(l_dict):
    '''dict->list
    converts l_dict in two ways:
    changes the key to an index number and makes the title anotehr value,
    and reformats the latitude and longitude.
    '''
    ret_list = []
    for key in l_dict.keys():
        temp_dict = {}
        temp_dict['title'] = key
        if l_dict[key]['geo']:
            temp_dict['geo'] = convert_lat_long(l_dict[key]['geo'])
        else:
            temp_dict['geo'] = {"lat":None, "lon":None}
        if l_dict[key]['r_geo']:
            temp_dict['r_geo'] = convert_lat_long(l_dict[key]['r_geo'])        
        else:
            temp_dict['r_geo'] = {"lat":None, "lon":None}
        if l_dict[key]['river_geo']:
            temp_dict['river_geo'] = {}
            if l_dict[key]['river_geo']['source']:
                temp_dict['river_geo']['source'] = \
                    convert_lat_long(l_dict[key]['river_geo']['source'])
            else:
                temp_dict['river_geo']['source'] = {"lat":None, "lon":None}
            if l_dict[key]['river_geo']['source_confluence']:
                temp_dict['river_geo']['source_confluence'] = \
                    convert_lat_long(l_dict[key]['river_geo']['source_confluence'])
            else:
                temp_dict['river_geo']['source_confluence'] = {"lat":None, "lon":None}            
            if l_dict[key]['river_geo']['mouth']:
                temp_dict['river_geo']['mouth'] = \
                    convert_lat_long(l_dict[key]['river_geo']['mouth'])
            else:
                temp_dict['river_geo']['mouth'] = {"lat":None, "lon":None}      
        else:
            temp_dict['river_geo'] = {'source':{"lat":None, "lon":None}, \
                                      'source_confluence':{"lat":None, "lon":None},\
                                      'mouth':{"lat":None, "lon":None}}
        if l_dict[key]['e_geo']:
            temp_dict['e_geo'] = {"lat":None, "lon":None}
            if l_dict[key]['e_geo']['highest']:
                temp_dict['e_geo']['highest'] = \
                    convert_lat_long(l_dict[key]['e_geo']['highest'])
            else:
                temp_dict['e_geo']['highest'] = {"lat":None, "lon":None}            
            if l_dict[key]['e_geo']['lowest']:
                temp_dict['e_geo']['lowest'] = \
                    convert_lat_long(l_dict[key]['e_geo']['lowest'])          
            else:
                temp_dict['e_geo']['lowest'] = {"lat":None, "lon":None}           
        else:
            temp_dict['e_geo'] = {'lowest':{"lat":None, "lon":None}, \
                                  'highest':{"lat":None, "lon":None}}
        temp_dict['first_para'] = l_dict[key]['first_para']
        ret_list.append(temp_dict)
    return ret_list

def convert_lat_long(lat_dict):
    '''dict->dict
    Converts the l_dict of form
    
    {lat_d: str, lat_m: str, lat_s: str, lat_dir: str,
    long_d: str, long_m: str, long_s: str, long_dir: str}
    
    to 
    
    {latitude: str, longitude: str}
    
    for ease of use with ElasticSearch.
    '''
    ret_dict = {}
    if 'lat_d' in lat_dict.keys() and lat_dict['lat_d']:
        lat = float(lat_dict['lat_d'])
    else:
        lat = 0
    if 'lat_m' in lat_dict.keys() and lat_dict['lat_m']:
        lat += float(lat_dict['lat_m']) / 60  
    if 'lat_s' in lat_dict.keys() and lat_dict['lat_s']:
        lat += float(lat_dict['lat_s']) / 3600     
    if 'lat_dir' in lat_dict.keys() and lat_dict['lat_dir'] == "S":
        lat = lat * -1   
    lat = str(lat)
        
    if 'long_d' in lat_dict.keys() and lat_dict['long_d']:
        try:
            lon = float(lat_dict['long_d'])
        except:
            print lat_dict
            lon = 0
    else:
        lon = 0
    if 'long_m' in lat_dict.keys() and lat_dict['long_m']:
        lon += float(lat_dict['long_m']) / 60  
    if 'long_s' in lat_dict.keys() and lat_dict['long_s']:
        lon += float(lat_dict['long_s']) / 3600     
    if 'long_dir' in lat_dict.keys() and lat_dict['long_dir'] == "W":
        lon = lon * -1   
    lon = str(lon)
    #try:
        #lat = lat_dict['lat_d'].lstrip('0')
    #except:
        #lat = ''
    #if 'lat_m' in lat_dict.keys():
        #if lat.count('.'):
            #lat += lat_dict['lat_m'].replace('.', '')
        #else:
            #lat += '.' + lat_dict['lat_m'].replace('.', '')
    #elif 'lat_s' in lat_dict.keys():
        #if lat.count('.'):
            #lat += '00'
        #else:
            #lat += '.00'
    #if 'lat_s' in lat_dict.keys():
        #lat += lat_dict['lat_s'].replace('.', '')
    ##else:
        ##lat += '00'  
    #if 'lat_dir' in lat_dict.keys() and lat_dict['lat_dir'] == 'S':
        #lat = '-' + lat
    #try:
        #lon = lat_dict['long_d'].lstrip('0')
    #except:
        #lon = ''
    #if 'long_m' in lat_dict.keys():
        #if lon.count('.'):
            #lon += lat_dict['long_m'].replace('.', '')
        #else:
            #lon += '.' + lat_dict['long_m'].replace('.', '')
    #elif 'long_s' in lat_dict.keys():
        #if lat.count('.'):
            #lon += '00'
        #else:
            #lon += '.00'
    #if 'long_s' in lat_dict.keys():
        #lon += lat_dict['long_s'].replace('.', '')
    ##else:
        ##lon += '00'  
    #if 'long_dir' in lat_dict.keys() and lat_dict['long_dir'] == 'W':
        #lon = '-' + lon  
    #if lat.startswith('--') or lat == '-':
        #lat = lat[1:]
    #if lon.startswith('--') or lon == '-':
        #lon = lon[1:]        
    #if lat.startswith('.'):
        #lat = '0' + lat
    #if lon.startswith('.'):
        #lon = '0' + lon
    #if lat.startswith('-.'):
        #lat = '-0' + lat[1:]
    #if lon.startswith('-.'):
        #lon = '-0' + lon[1:]    
    ret_dict['lat'] = lat
    ret_dict['lon'] = lon
    if lat.count('.') > 1:
        print lat 
        print lat_dict['lat_d']
        print lat_dict['lat_m']
        print lat_dict['lat_s']
        print '\n'
    if lon.count('.') > 1:
        print lon
        print lat_dict['long_d']
        print lat_dict['long_m']
        print lat_dict['long_s'] 
        print '\n'
    return ret_dict

def l_in_line(line):
    
    return (line.count('latd') or line.count('latm') or line.count('lats') or \
        line.count('latNS') or line.count('lat_deg') or line.count('lat_min')\
        or line.count('lat_sec') or line.count('latitude') or \
        line.count('lat_d') or line.count('lat_m') or line.count('lat_s') or \
        line.count('lat_degrees') or line.count('lat_minutes') or \
        line.count('lat_seconds') or line.count('lat_direction') or \
        line.count('lat_hem') or line.count('longd') or line.count('longm') \
        or line.count('longs') or line.count('longEW') or \
        line.count('long_deg') or line.count('long_min') or \
        line.count('long_sec') or line.count('longitude') or \
        line.count('long_d') or line.count('long_m') or line.count('long_s') \
        or line.count('long_degrees') or line.count('long_minutes') or \
        line.count('long_seconds') or line.count('long_direction') or \
        line.count('long_hem') or line.count('Coord') or \
        line.count('Coord') or line.count('Location map') or line.count('map_locator'))

def get_lat_or_long(line, l={}):
    '''file line, dict? -> dict
    Starts, continues, or finishes the creation of a lat/long dict.
    The variable naming of latitude and longitude, along with the 
    completeness of the data and potential line separation is quite 
    inconsistent in the Wikipedia dump, so this function will be called on 
    all the lines of an articles identified as having lat/long variables in 
    them, and combining them into one variable.
    
    Uses regex, whereas the initial detection uses string funcitons, so this
    will be more fine tuned and may determine that the line passed in does
    not actually contain useful information.
    
    Format is {lat_d: str, lat_m: str, lat_s: str, lat_dir: str,
               long_d: str, long_m: str, long_s: str, long_dir: str}
    '''
    
    lat_d = \
        re.findall('^lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)|\s*lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)|\|lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    lat_m = \
        re.findall('^lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)|\s*lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)|\|lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    lat_s = \
        re.findall('^lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)|\s*lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)|\|lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        l['lat_s'] = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    long_d = \
        re.findall('^long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)|\s*long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)|\|long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
    long_m = \
        re.findall('^long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)|\s*long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)|\|long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
    long_s = \
        re.findall('^long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)|\s*long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)|\|long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        l['long_s'] = long_s[0][0] + long_s[0][1] + long_s[0][2]
    latitude = \
        re.findall('^latitude\s*?=\s*?(\d+\.?\d*)|\s*latitude\s*?=\s*?(\d+\.?\d*)|\|latitude\s*?=\s*?(\d+\.?\d*)', line)
    if latitude:
        latitude = latitude[0][0] + latitude[0][1] + latitude[0][2]
        l['lat_d'] = latitude.split('.')[0]
        if len(latitude.split('.')) > 1:
            if len(latitude.split('.')[1]) > 2:
                l['lat_m'] = latitude.split('.')[1][:2]
                l['lat_s'] = latitude.split('.')[1][2:]
            else:
                l['lat_m'] = latitude.split('.')[1]
    longitude = \
        re.findall('^longitude\s*?=\s*?(\d+\.?\d*)|\s*longitude\s*?=\s*?(\d+\.?\d*)|\|longitude\s*?=\s*?(\d+\.?\d*)', line)
    if longitude:
        longitude = longitude[0][0] + longitude[0][1] + longitude[0][2]
        l['long_d'] = longitude.split('.')[0]
        if len(longitude.split('.')) > 1:
            if len(longitude.split('.')[1]) > 2:
                l['long_m'] = longitude.split('.')[1][:2]
                l['long_s'] = longitude.split('.')[1][2:]
            else:
                l['long_m'] = longitude.split('.')[1]    
                longitude = \
                    re.findall('^longitude\s*?=\s*?(\d+\.?\d*)|\s*longitude\s*?=\s*?(\d+\.?\d*)|\|longitude\s*?=\s*?(\d+\.?\d*)', line)
    coords = re.findall('\{\{[Cc]oord\|([\d\.]*)\|([NEWS])\|([\d\.]*)\|([NEWS])|\{\{[Cc]oord\|([\d]*)\|([\d\.]*)\|([NEWS])\|([\d]*)\|([\d\.]*)\|([NEWS])|\{\{[Cc]oord\|([\d]*)\|([\d]*)\|([\d\.]*)\|([NEWS])\|([\d]*)\|([\d]*)\|([\d\.]*)\|([NEWS])|\{\{[Cc]oord\|(-?[\d\.]*)\|(-?[\d\.]*)', line)                
    if coords:
        if coords[0][0]:
            temp_lat = coords[0][0].split('.')
            if len(temp_lat) > 1:
                l['lat_m'] = temp_lat[1]
            l['lat_d'] = temp_lat[0]
            l['lat_dir'] = coords[0][1]
            temp_long = coords[0][2].split('.')
            if len(temp_long) > 1:
                l['long_m'] = temp_long[1]
            l['long_d'] = temp_long[0]
            l['long_dir'] = coords[0][3]            
        elif coords[0][4]:
            l['lat_d'] = coords[0][4]
            temp_lat = coords[0][5].split('.')
            if len(temp_lat) > 1:
                l['lat_s'] = temp_lat[1]
            l['lat_m'] = temp_lat[0]
            l['lat_dir'] = coords[0][6]
            l['long_d'] = coords[0][7]
            temp_long = coords[0][8].split('.')
            if len(temp_long) > 1:
                l['long_m'] = temp_long[1]
            l['long_d'] = temp_long[0]
            l['long_dir'] = coords[0][9]             
        elif coords[0][10]:
            l['lat_d'] = coords[0][10]
            l['lat_m'] = coords[0][11]
            l['lat_s'] = coords[0][12]
            l['lat_dir'] = coords[0][13]
            l['long_d'] = coords[0][14]
            l['long_m'] = coords[0][15]
            l['long_s'] = coords[0][16]
            l['long_dir'] = coords[0][17]             
        else:
            if coords[0][18].startswith('-'):
                l['lat_dir'] = 'S'
            else:
                l['lat_dir'] = 'N'
            temp_lat = coords[0][18].split('.')
            if len(temp_lat) > 1:
                l['lat_m'] = temp_lat[1]
            l['lat_d'] = temp_lat[0]       
            if coords[0][19].startswith('-'):
                l['long_dir'] = 'S'
            else:
                l['long_dir'] = 'N'
            temp_long = coords[0][19].split('.')
            if len(temp_long) > 1:
                l['long_m'] = temp_long[1]
            l['long_d'] = temp_long[0]        
    coords_2 = re.compile(ur'coordinates.*?=.*?(\d*)\u00B0(\d*?)\'(\d*)([NS]).*?(\d*)\u00B0(\d*?)\'(\d*)([EW])', re.UNICODE)
    try:
        coords_2 = coords_2.findall(unicode(line))
    except:
        coords_2 = ''
    if coords_2:
        l['lat_d'] = str(coords_2[0][0])
        l['lat_m'] = str(coords_2[0][1])
        l['lat_s'] = str(coords_2[0][2])
        l['lat_dir'] = str(coords_2[0][3])
        l['long_d'] = str(coords_2[0][4])
        l['long_m'] = str(coords_2[0][5])
        l['long_s'] = str(coords_2[0][6])
        l['long_dir'] = str(coords_2[0][7])
    lat_dir = \
        re.findall('^lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)|\s*lat_?(?:NW|direction|hem)?\s*?=\s*?(N|S)|\|lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['lat_dir'] = lat_dir    
    long_dir = \
        re.findall('^long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)|\s*long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)|\|long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['long_dir'] = long_dir
    return l

def get_river_lat_or_long(line, l={}):
    '''file line, dict? -> dict
    Starts, continues, or finishes the creation of a lat/long dict.
    The variable naming of latitude and longitude, along with the 
    completeness of the data and potential line separation is quite 
    inconsistent in the Wikipedia dump, so this function will be called on 
    all the lines of an articles identified as having lat/long variables in 
    them, and combining them into one variable.
     
    Uses regex, whereas the initial detection uses string funcitons, so this
    will be more fine tuned and may determine that the line passed in does
    not actually contain useful information.
     
    Format is {lat_d: str, lat_m: str, lat_s: str, lat_dir: str,
               long_d: str, long_m: str, long_s: str, long_dir: str}
    '''
     
    l['source'] = {}
    lat_d = \
        re.findall('source_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['source']['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('source_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['source']['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('source_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['source']['lat_s'] = lat_s
    long_d = \
        re.findall('source_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['source']['long_d'] = long_d[0]
    long_m = \
        re.findall('source_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['source']['long_m'] = long_m[0]
    long_s = \
        re.findall('source_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['source']['long_s'] = long_s
    lat_dir = \
        re.findall('source_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['source']['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('source_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['source']['long_dir'] = long_dir[0]
         
    l['source_confluence'] = {}
    lat_d = \
        re.findall('source_confluence_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['source_confluence']['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('source_confluence_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['source_confluence']['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('source_confluence_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['source_confluence']['lat_s'] = lat_s
    long_d = \
        re.findall('source_confluence_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['source_confluence']['long_d'] = long_d[0]
    long_m = \
        re.findall('source_confluence_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['source_confluence']['long_m'] = long_m[0]
    long_s = \
        re.findall('source_confluence_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['source_confluence']['long_s'] = long_s
    lat_dir = \
        re.findall('source_confluence_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['source_confluence']['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('source_confluence_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['source_confluence']['long_dir'] = long_dir[0]    
         
    l['mouth'] = {}
    lat_d = \
        re.findall('mouth_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['mouth']['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('mouth_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['mouth']['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('mouth_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['mouth']['lat_s'] = lat_s
    long_d = \
        re.findall('mouth_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['mouth']['long_d'] = long_d[0]
    long_m = \
        re.findall('mouth_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['mouth']['long_m'] = long_m[0]
    long_s = \
        re.findall('mouth_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['mouth']['long_s'] = long_s
    lat_dir = \
        re.findall('mouth_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['mouth']['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('mouth_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['mouth']['long_dir'] = long_dir[0]      
    if l['mouth'] == {} and l['source'] == {} and l['source_confluence'] == {}:
        l = {}    
    return l
 
def get_r_lat_or_long(line, l={}):
    '''file line, dict? -> dict
    Starts, continues, or finishes the creation of a lat/long dict.
    The variable naming of latitude and longitude, along with the 
    completeness of the data and potential line separation is quite 
    inconsistent in the Wikipedia dump, so this function will be called on 
    all the lines of an articles identified as having lat/long variables in 
    them, and combining them into one variable.
     
    Uses regex, whereas the initial detection uses string funcitons, so this
    will be more fine tuned and may determine that the line passed in does
    not actually contain useful information.
     
    Format is {lat_d: str, lat_m: str, lat_s: str, lat_dir: str,
               long_d: str, long_m: str, long_s: str, long_dir: str}
    '''
     
    lat_d = \
        re.findall('range_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('range_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('range_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['lat_s'] = lat_s
    long_d = \
        re.findall('range_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['long_d'] = long_d[0]
    long_m = \
        re.findall('range_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['long_m'] = long_m[0]
    long_s = \
        re.findall('range_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['long_s'] = long_s
    lat_dir = \
        re.findall('range_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('range_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['long_dir'] = long_dir[0]
    return l
 
def get_e_lat_or_long(line, l={}):
    '''file line, dict? -> dict
    Starts, continues, or finishes the creation of a lat/long dict.
    The variable naming of latitude and longitude, along with the 
    completeness of the data and potential line separation is quite 
    inconsistent in the Wikipedia dump, so this function will be called on 
    all the lines of an articles identified as having lat/long variables in 
    them, and combining them into one variable.
     
    Uses regex, whereas the initial detection uses string funcitons, so this
    will be more fine tuned and may determine that the line passed in does
    not actually contain useful information.
     
    Format is {lat_d: str, lat_m: str, lat_s: str, lat_dir: str,
               long_d: str, long_m: str, long_s: str, long_dir: str}
    '''
     
    l['lowest'] = {}
    lat_d = \
        re.findall('lowest_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['lowest']['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('lowest_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['lowest']['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('lowest_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['lowest']['lat_s'] = lat_s
    long_d = \
        re.findall('lowest_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['lowest']['long_d'] = long_d[0]
    long_m = \
        re.findall('lowest_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['lowest']['long_m'] = long_m[0]
    long_s = \
        re.findall('lowest_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['lowest']['long_s'] = long_s
    lat_dir = \
        re.findall('lowest_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['lowest']['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('lowest_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['lowest']['long_dir'] = long_dir[0]
         
    l['highest'] = {}
    lat_d = \
        re.findall('highest_lat_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_d = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
    if lat_d:
        #l['lat_d'] = lat_d[0][0] + lat_d[0][1] + lat_d[0][2]
        l['highest']['lat_d'] = lat_d[0]
    lat_m = \
        re.findall('highest_lat_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_m = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
    if lat_m:
        #l['lat_m'] = lat_m[0][0] + lat_m[0][1] + lat_m[0][2]
        l['highest']['lat_m'] = lat_m[0]
    lat_s = \
        re.findall('highest_lat_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
    if lat_s:
        #lat_s = lat_s[0][0] + lat_s[0][1] + lat_s[0][2]
        lat_s = lat_s[0]
        if lat_s.count('.'):
            lat_s = lat_s.split('.')[0] + lat_s.split('.')[1]
        l['highest']['lat_s'] = lat_s
    long_d = \
        re.findall('highest_long_?d(?:eg)?(?:rees)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_d = long_d[0][0] + long_d[0][1] + long_d[0][2]
    if long_d:
        #l['long_d'] = long_d[0][0] + long_d[0][1] + long_d[0][2]
        l['highest']['long_d'] = long_d[0]
    long_m = \
        re.findall('highest_long_?m(?:in)?(?:utes)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_m = long_m[0][0] + long_m[0][1] + long_m[0][2]
    if long_m:
        #l['long_m'] = long_m[0][0] + long_m[0][1] + long_m[0][2]
        l['highest']['long_m'] = long_m[0]
    long_s = \
        re.findall('highest_long_?s(?:ec)?(?:onds)?\s*?=\s*?(\d+\.?\d*)', line)
    #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
    if long_s:
        #long_s = long_s[0][0] + long_s[0][1] + long_s[0][2]
        long_s = long_s[0]
        if long_s.count('.'):
            long_s = long_s.split('.')[0] + long_s.split('.')[1]
        l['highest']['long_s'] = long_s
    lat_dir = \
        re.findall('highest_lat_?(?:NS|direction|hem)?\s*?=\s*?(N|S)', line)                
    if lat_dir:
        #lat_dir = lat_dir[0][0] + lat_dir[0][1] + lat_dir[0][2]
        l['highest']['lat_dir'] = lat_dir[0]
    long_dir = \
        re.findall('highest_long_?(?:EW|direction|hem)?\s*?=\s*?(E|W)', line)                
    if long_dir:
        #long_dir = long_dir[0][0] + long_dir[0][1] + long_dir[0][2]
        l['highest']['long_dir'] = long_dir[0]    
        
    if l['highest'] == {} and l['lowest'] == {}:
        l = {}
    return l

#if os.name == 'posix':
    #f = open('/Users/Devon/Desktop/enwiki-20151201-pages-articles.xml', 'r')
#else:
    #f=open('C:\Users\Devon\Desktop\enwiki-20151201-pages-articles.xml', 'r')
#line = f.readline()
done_printing = False
start_printing = False
prev_line = ''
title = ''
#while line != '' and not done_printing:
    ##if line.count('Coordinates') > 0 and not start_printing and not line.count('Tranquillitatis')\
    ##   and not line.count('Leslie'):
    #if title.startswith('    <title>Assassination of'):
        ##print title
        ##print prev_line
        #start_printing = True
    #if line.startswith('    <title>'):
        #title = line
    #if line.startswith('    <title>') and start_printing == True:
        #done_printing = True
        #start_printing = False
    #if start_printing == True:
        #print line
        #prev_line = line
    #line = f.readline()

checking = False
lat_list = []
next_stop = False

i = 0

#while line != '' and i < 1000000:
    ##if line.count('Coordinates') > 0 and not start_printing and not line.count('Tranquillitatis')\
    ##   and not line.count('Leslie'):
    #if next_stop:
        #next_stop = False
        #checking = False
    ##if title.startswith('    <title>Assassination of Martin Luther King, Jr.'):
        ##print title
        ##print prev_line
        ##start_printing = True
    #if line.startswith('    <title>'):
        #title = line[11:-8]
        ##print line
    #if line.count('Infobox'):
        #checking = True
        ##print line
    #if line.count('}'):
        #if line.count('Infobox'):
            #next_stop = True
        #else:
            #checking = False
    ##if line.count('long') and checking:
        ##split_line = line.split()
        ##for item in split_line:
            ##if item.count('long') and not item in lat_list: # and not item.count('population'):
                ##lat_list += [item]
                ##print line
                ##break
    #if line.count('geo') and checking:
        #print line
    #line = f.readline()
    #i += 1

l_dict = {}
was_l = False
next_stop = False
one_more = False
adding = False
countdown = -1

#while line != '' and i < 100000:
    ##if line.count('Coordinates') > 0 and not start_printing and not line.count('Tranquillitatis')\
    ##   and not line.count('Leslie'):
    #if was_l and (one_more or next_stop) and not line == '\n':
        #this_info = line
        #one_more = False
        #next_stop = False
        #checking = False
        #was_l = False
        #l_dict[title] = {'geo': l, 'first_para': this_info}
    #if next_stop and not was_l:
        #next_stop = False
        #checking = False 
    #if one_more and not was_l:
        #one_more = False
        #checking = False
    ##if title.startswith('    <title>Assassination of Martin Luther King, Jr.'):
        ##print title
        ##print prev_line
        ##start_printing = True
    #if line.startswith('    <title>'):
        #title = line[11:-9]
        #adding = True
        ##print line
    #if line.count('Infobox'):
        #checking = True
        ##print line
    #if line.count('}'):
        #adding = False
        #if line.count('Infobox'):
            #next_stop = True
        #elif not line.count('{'):
            #checking = False
            #one_more = True
    #if checking and (line.count('latd') or line.count('latm') or line.count('lats') or \
                     #line.count('latNS') or line.count('lat_deg') or \
                     #line.count('lat_min') or line.count('lat_sec') or \
                     #line.count('latitude') or line.count('lat_d') or \
                     #line.count('lat_m') or line.count('lat_s') or \
                     #line.count('lat_degrees') or line.count('lat_minutes') or\
                     #line.count('lat_seconds') or line.count('lat_direction') or \
                     #line.count('lat_hem') or line.count('longd') or \
                     #line.count('longm') or line.count('longs') or \
                     #line.count('longEW') or line.count('long_deg') or \
                     #line.count('long_min') or line.count('long_sec') or \
                     #line.count('longitude') or line.count('long_d') or \
                     #line.count('long_m') or line.count('long_s') or \
                     #line.count('long_degrees') or line.count('long_minutes') or\
                     #line.count('long_seconds') or line.count('long_direction') or \
                     #line.count('long_hem')):
        #print line
        ##if adding:
            ##l = get_lat_or_long(line, l)
        ##else:    
            ##l = get_lat_or_long(line)
        #l = line
        #was_l = True
    #line = f.readline()
    #i += 1
    ##countdown -= 1

nested = 0
l = {}
l = {}
r_l = {}
river_l = {}
e_l = {}
bloomsbury_printed = False
got_first_line = False
#with open('/Users/Devon/Desktop/enwiki-20151201-pages-articles.xml', 'r') as f:

    ##while line != '':
    #for line in f:
        ##if i >100000:
            ##print l_dict
            ##print len(l_dict.keys())
            ##raw_input('')
    ##if line.count('Coordinates') > 0 and not start_printing and not line.count('Tranquillitatis')\
    ##   and not line.count('Leslie'):
        ##if was_l and (one_more or next_stop) and not line == '\n':
            ##print title
            ##this_info = line
            ##one_more = False
            ##next_stop = False
            ##checking = False
            ##was_l = False
            
            ##if l != {}:
                ##l_dict[title] = {'geo': l, 'first_para': this_info}
            ##l = {}
        #if line.count("==Overview=="):
            #got_first_line = True
        #if line.startswith("'''") and not got_first_line:
            #this_info = line
            ##checking = False            
        ##if next_stop and not was_l:
            ##next_stop = False
            ##checking = False 
        ##if one_more and not was_l:
            ##one_more = False
            ##checking = False
        ##if title.startswith('    <title>Assassination of Martin Luther King, Jr.'):
            ##print title
            ##print prev_line
            ##start_printing = True
        ##if line.startswith('    <title>'):
        #t = re.findall('^\s*<title>(.*?)</title>', line)
        #if t:
            ##checking = True
            ##title = line[11:-9]
            #if was_l:
                #was_l = False
                #if l != {} or r_l != {} or river_l != {} or e_l != {}:
                    #l_dict[title] = {'geo': l, 'r_geo': r_l, 'river_geo': river_l,\
                                     #'e_geo': e_l,'first_para': this_info}  
                    #print title
                    #l = {}
                    #r_l = {}
                    #river_l = {}
                    #e_l = {}        
            #got_first_line = False            
            #title = t[0]
            #adding = True
            ##print line
        ##if line.count('Infobox'):
            ##checking = True
            ##print line
        #if line.startswith('    <title>Bloomsbury Theatre'):
            #bloomsbury_printed = True
        #if bloomsbury_printed == True:
            #print line
        ##if checking:
            ##nested += line.count('{') - line.count('}')
            ##if nested > 0:
                ##adding = True
        ##if checking and line.count('{') + line.count('}') > 0:
            ##print title
            ##print line
            ##print nested
        ##if line.count('}'):
            ##if nested == 0:
                ##adding = False
                ##checking = False
                ##one_more = True
        ##if checking and (line.count('coord') or line.count('latmax') or \
                         ##line.count('Resting') or line.count('government_lat') or \
                         ##line.count('resting_place') or line.count('latmin') or \
                         ##line.count('geo')):
            ##print title
            ##print line
        ##if checking and l_in_line(line):
        #if l_in_line(line):
            ##print title
            ##print line
            #l = get_lat_or_long(line, l)
            #r_l = get_r_lat_or_long(line, r_l)
            #river_l = get_river_lat_or_long(line, river_l)
            #e_l = get_e_lat_or_long(line, e_l)            
            ##if adding:
                ##l = get_lat_or_long(line, l)
                ###print 'adding'
            ##else:    
                ##l = get_lat_or_long(line, {})
            ##l = line
            #if l != {} or r_l != {} or river_l != {} or e_l != {}:
                #was_l = True
        ##line = f.readline()
        #i += 1
        ##countdown -= 1

#if os.name == 'posix':
    #w = open('/Users/Devon/Dropbox/programming/wiki_json_mac.json', 'w')
#else:
    #w = open('C:\Users\Devon\Desktop\wiki_json_win', 'w')

#json.dump(l_dict, w)

#w.close()