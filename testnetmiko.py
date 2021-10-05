from pprint import pprint
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException)
#from netmiko import ConnectHandler
#from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
#from netmiko.ssh_exception import AuthenticationException
import yaml

def Raise_Value_Exception_Error(command):
    key_arg = ['show','config']
    if (all( key in command.keys() for key in key_arg)):
        raise ValueError ('Either "Show" or "Config" params and not both')


def check_for_error(config_out):
    status = False
    error_list = ['Invalidinput detected', 'Incomplete command', 'Ambiguous command']
    for error in error_list:
        if error in config_out:
            status = True
            return error,status
def send_config_commands (dev,cmd_list,log=True):
    ssh = ConnectHandler(**dev)
    output_with_error = {}
    output_without_error = {}
    if log:
        print(f"Connectng to device.... {dev['host']}")
        if type(cmd_list) == str:
            cmd_list = [cmd_list]
        ssh.enable()
        for command in cmd_list:
            result = ssh.send_config_set(command)
            err,state = check_for_error(result)
            if state:
                print(f'"{command}" command is executed with error: {err}  on the device {dev["host"]}')
                output_with_error[command] = result
                decider = input("Continue execution of remaining commands? [y]/n: ").lower() or 'y'
                if decider.startswith('n'):
                    break
                else:
                    output_without_error[command] = result
        return output_with_error,output_without_error
dev_dict = {
        'device_type': 'cisco_ios',
        'host': '10.2.2.13'
        'username': 'isco'
        'password': 'cisco'
        'secret': 'cisco',
        'timeout': 5,
        'fast_cli': True
        }

