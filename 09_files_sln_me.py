access_mode_template = [
"switchport mode access",
"switchport access vlan",
"switchport nonegotiate",
"spanning-tree portfast",
"spanning-tree bpduguard enable",
]

access_config = {"FastEthernet0/12": 10, "FastEthernet0/14": 11, "FastEthernet0/16": 17}

access_config_2 = {
"FastEthernet0/3": 100,
"FastEthernet0/7": 101,
"FastEthernet0/9": 107,
}

'''port_security_template = [
"switchport port-security maximum 2",
"switchport port-security violation restrict",
"switchport port-security"
]
'''
port_security_template = []
config_template_access = [access_mode_template,port_security_template] 
trunk_mode_template = [
"switchport mode trunk",
"switchport trunk native vlan 999",
"switchport trunk allowed vlan",
]

trunk_config = {
"FastEthernet0/1": [10, 20, 30],
"FastEthernet0/2": [11, 30],
"FastEthernet0/4": [17],
}

trunk_config_2 = {
"FastEthernet0/11": [120, 131],
"FastEthernet0/15": [111, 130],
"FastEthernet0/14": [117],
}
config_template_trunk = [trunk_mode_template]

def generate_access_config(*command_template,**intf_vlan_mapping):
    cmd_line = []
    cmd_dict = {}
    for intf,vlan in intf_vlan_mapping.items():
        cmd_dict[intf] = []
        cmd_line.append(f"interface {intf}")
        for command_part1 in command_template:
            if command_part1:
                for command in command_part1:
                    if command.endswith("access vlan"):
                        cmd_line.append(f' {command} {vlan}')
                        cmd_dict[intf].append(f' {command} {vlan}')
                    elif command.endswith("allowed vlan"):
                        vlan = str(vlan).strip('[]')
                        cmd_line.append(f' {command} {vlan}')
                        cmd_dict[intf].append(f' {command} {vlan}')
                    else:
                        cmd_line.append(f' {command}')
                        cmd_dict[intf].append(f' {command}')
    return(cmd_line,cmd_dict)
#send_list,send_dict = generate_access_config(*config_template_access,**access_config)
send_list,send_dict = generate_access_config(*config_template_trunk,**trunk_config)

'''  The output below print list in config style
for element in send_list:
    if element.startswith('s'):
        print("  {}".format(element))
    else:
        print("{}".format(element))
'''
for intf,command_list in send_dict.items():
    print(f"interface {intf}")
    for command in command_list:
        print(f" {command}")






