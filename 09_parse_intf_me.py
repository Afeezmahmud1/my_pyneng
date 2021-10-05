def parse_config(filename="/root/Desktop/PYNENG-FOLDER/exercises/09_functions/config_sw1.txt"):
    '''
    Docstring:
    input : Cisco switch running/Startup config file.txt
    output: Tuple of dictioanry with interface as key and vlan as value
    '''
    with open (filename) as f:
        parse_dict = {}
        check = True
        for line in f:
            if line.startswith('interface Fast'):
                check = False
                intf = line.rstrip().split()[1]
                parse_dict[intf] = []
            while not check:
                if line.startswith(' '):
                    parse_dict[intf].append(line.rstrip())
                    break
                if line.startswith('!'):
                    check = True
                else:
                    break
    final_out = {'access':{},'trunk' :{}}
    for intf,cmd_list in parse_dict.items():
        if ' switchport mode access' in cmd_list:
            vlan ={}
            for cmd in cmd_list:
                if 'access vlan' in cmd:
                    vlan = cmd.lstrip().split()[3]
            if vlan:
                final_out['access'][intf] = int(vlan)
            else:
                vlan = 1
                final_out['access'][intf] = int(vlan)
        if ' switchport mode trunk' in cmd_list:
            vlan =''
            for cmd in cmd_list:
                if 'allowed vlan' in cmd:
                    vlan = cmd.lstrip().split()[4]
            if vlan:
                vl_trk = vlan.split(',') # String to list
                vl_list = [int(vl_trk) for vl_trk in vlan.split(',')] #list element from str to int
                final_out['trunk'][intf] = vl_list
            else:
                vlan = 'all'
                final_out['trunk'][intf] = vlan
    return(final_out['access'],final_out['trunk'])
access_func,trunk_func = parse_config("sw_config2.txt") #Function call
print(access_func)
print(trunk_func)

