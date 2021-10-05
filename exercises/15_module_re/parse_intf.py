import re
from pprint import pprint
file2 = 'config_r2.txt'
filename = '/root/Desktop/PYNENG-FOLDER/exercises/15_module_re/config_r2.txt'
with open(filename) as f:
    desc_check = False
    ip_check = False
    dict_intf = {}
    for line in f:
        if re.search('^interface \S+',line):
            key = re.search('^interface (\S+)',line).group(1)
            dict_intf[key] = []
            #desc_check = True
            ip_check = True
        '''while desc_check:
            if re.search('description .*',line):
                dict_intf[key] = line
                desc_check = False
            elif re.search('!',line):
                desc_check = False
            else:
                break'''
        while ip_check:
            if re.search(' ip address \S+ \S+',line):
                dict_intf[key].append(line)
                break
            if re.search(' ip unnumbered \S+',line):
                dict_intf[key].append(line)
                break
            if re.search('!',line):
                ip_check = False
            else:
                break
pprint(dict_intf)

