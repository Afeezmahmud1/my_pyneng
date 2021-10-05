#!/usr/bin/env python3
switchport_cmd = ['switchport mode access',
                  'switchport access vlan {}',
                  'spanning-tree portfast'
                  ]
print( '\n'.join(switchport_cmd).format(5))
