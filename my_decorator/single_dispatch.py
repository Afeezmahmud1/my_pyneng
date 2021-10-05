from netmiko import ConnectHandler
import yaml
from pprint import pprint
from functools import singledispatch
from collections.abc import Iterable, Sequence

@singledispatch
def send_commands (command, device):
    print ( 'original func' )
    raise NotImplementedError ( 'Only list or string supported' )
@send_commands . register ( str )
def _ (show_command, device):
    print ( 'Execute show' )
    with ConnectHandler ( ** device) as ssh:
        ssh . enable ()
        result = ssh . send_command (show_command)
    return result
@send_commands . register (Iterable)
def _(config_commands, device):
    print ( 'Executing config' )
    with ConnectHandler ( ** device) as ssh:
        ssh . enable ()
        result = ssh . send_config_set (config_commands)
    return result
if __name__ == '__main__':
    r1= {'device_type' : 'cisco_ios',
                 'host':'10.2.2.11',
                 'username':'cisco',
                 'password':'cisco',
                 'secret':'cisco'
                 }

    commands = [ 'logging 10.255.255.1' ,'logging buffered 20010' ,'no logging console' ]
    show_command = "sh ip int br"
    unknown = 1
    #print (send_commands ( commands, r1))
    print (send_commands (unknown, r1))
