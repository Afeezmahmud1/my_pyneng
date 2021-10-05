from sys import argv
print(argv)
interface = argv[1]
int_id = f'interface {interface} '
command_template = ['switchport mode trunk',
                   'switchport nonegotiate',
                   'switchport trunk allowed vlan {}',
                   'spanning-tree guard root'
                   ]
print(int_id)
print('\n'.join(command_template).format(argv[2]) )


