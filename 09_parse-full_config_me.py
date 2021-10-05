ignore = ['duplex','alias','Current configuration']
def ignore_check(cmd,*ignore_list):
    ignore_status = False
    for word in ignore_list:
        if word in cmd:
            ignore_status = True
    return ignore_status
def parse_full_cfg(filename="sw_config2.txt"):
    with open (filename) as f:
        parse_dict = {}
        check_child = True
        for line in f:
            if ignore_check(line,*ignore):
                continue
            else:
                check_child = False
                if not line.startswith(' '):
                    key = line.rstrip()
                    parse_dict[key] = []
            while not check_child:
                if line.startswith(' '):
                    parse_dict[key].append(line.rstrip())
                    break
                elif line.startswith('!'):
                    check_child = True
                else:
                    break
    final_parse = {}
    for key,value in parse_dict.items():
        if key is '!':
            continue
        else:
            final_parse[key] = value
    return final_parse


config_output = parse_full_cfg()

for key,value in config_output.items():
    print("{} {}".format(key,value))




