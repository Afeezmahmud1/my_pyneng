from pprint import pprint
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException)
#from netmiko import ConnectHandler
#from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
#from netmiko.ssh_exception import AuthenticationException
import yaml
import stdiomask
from datetime import datetime
start_time = datetime.now()
def Raise_Value_Exception_Error(command):
    key_arg = ['show','config']
    if (all( key in command.keys() for key in key_arg)):
        raise ValueError ('Either "Show" or "Config" params and not both')


def check_for_error(config_out):
    status = False
    err1 = ''
    error_list = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']
    for error in error_list:
        if error in config_out:
            status = True
            err1 = error
            break
    return error,status

def send_show_commands (device,commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            if type(commands) == str:
                commands = [commands]
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
            return result
    except (NetmikoAuthenticationException):
        print(f"Authentication Error:Incorrect Username/Password while Attempt to login {device['host']}")
    except (NetmikoTimeoutException):
        print(f"Session Timout while attempting to login to {device['host']}")
    except (EOFError):
        print("End of file Error")
    except (SSHException):
        print(f"Unknown Error occur while Attempting to login to {device['host']}")
    except Exception as unknown_error:
        print("Unknown Error")

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
                print("Aborting execution of the remaining commands.....")
                break
        else:
            output_without_error[command] = result
    return output_with_error,output_without_error

def send_commands(R1,**command):
    Raise_Value_Exception_Error(command)
    for key,value in command.items():
        if key == 'show':
            show_out =  send_show_commands(R1,command['show'])
            return show_out
        elif key == 'config':
            config_out = send_config_commands(R1,command['config'])
            return config_out
        else:
            print("Unkown function parameter")

if __name__ == "__main__":
    #admin_user = stdiomask.getpass(prompt='username:  ')
    #admin_password = stdiomask.getpass(prompt='password:  ')
    #admin_enable = stdiomask.getpass(prompt='enable password:  ')
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    cfg_cmds = commands_with_errors + correct_commands
    #cfg_cmds = ['router ospf 10','a']
    show_cmds = ["sh clock","sh version | in uptime"]
    all_devices = {}
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        #dev.update({'user':admin_user,'password' : admin_password,'secret' : admin_enable})
        per_device = send_commands(dev, show = show_cmds)
        all_devices[dev['host']] = per_device
    pprint(all_devices,width=200)
    #pprint(per_device,width=200)
    print(datetime.now()-start_time)
