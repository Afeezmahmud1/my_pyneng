trunk_template = [
"switchport trunk encapsulation dot1q",
"switchport mode trunk",
"switchport trunk allowed vlan"
]
access_template = ["switchport mode access",
                    "switchport access vlan",
                    "spanning-tree portfast"
                 ]
template_var =  {"access":
                 {'0/12':"10",'0/14':"11",'0/16':"17",'0/17':"150"},
                "trunk":
                 {"0/1": ["add", "10", "20"], "0/2": ["only", "11", "30"], "0/4": ["del","17"]}
                 }
for intf,action_vlan in template_var["trunk"].items():
    print(f"Interface GigabitEthernet{intf}")
    if action_vlan[0] == "add":
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                print(f" {command} add {','.join(action_vlan[1:])}")
            else:
                print(f" {command}")
    elif action_vlan[0] == "only":
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                print(f" {command} {','.join(action_vlan[1:])}")
            else:
                print(f" {command}")
    elif action_vlan[0] == "del":
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                print(f" {command} remove {','.join(action_vlan[1:])}")
            else:
                print(f" {command}")
    else:
        print("UNKNOWN TRUNK COMMAND")

for intf,vlan in template_var["access"].items():
    print(f"interface Fastinterface{intf}")
    for command in access_template:
        if command.endswith("access vlan"):
            print(f" {command} {vlan}")
        else:
            print(f" {command}")



                    


