from pprint import pprint
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException)
from paramiko.ssh_exception import SSHException
import yaml
import stdiomask
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor,as_completed
def Raise_Value_Exception_Error(command):
    key_arg = ['show','config']
    if (all( key in command.keys() for key in key_arg)):
        raise ValueError ('Either "Show" or "Config" params and not both')
    return


def string_to_file(filename,input_string,prompt=False):
    split_input_string = input_string.splitlines()
    split_input_string_plus_newline= [element+'\n' for element in split_input_string]
    with open (filename,'a') as f_write:
        if prompt:
            f_write.write(prompt)
        f_write.write('\n')
        f_write.writelines(split_input_string_plus_newline)
    return

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

def send_show_command (device,func_cmd):
     result = {}
     if type(func_cmd) == dict:
         for host_ip,host_command in func_cmd.items():
             if device['host'] == host_ip:
                 commands = host_command
                 if type(commands) == str:
                     commands = [commands]
     elif type(func_cmd) == str:
         commands = [func_cmd]
     else:
         commands = func_cmd
     with ConnectHandler(**device) as ssh:
         ssh.enable()
         prompt = ssh.base_prompt
         for command in commands:
             output = ssh.send_command(command)
             expected = f'{prompt}#{command}'
             result[expected] = output
     return result

def send_config_command (device,func_cmd,log=True):
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    logging.basicConfig(format = '%(threadName)s %(name)s %(levelname)s: %(message)s',level=logging.INFO)
    ssh_msg = 'Connecting to ip :{} . . . . . . '
    err_msg ='Error occurent while Executing the command on device : {}'
    if type(func_cmd) == dict:
        for host_ip,host_command in func_cmd.items():
            if device['host'] == host_ip:
                commands = host_command
                if type(commands) == str:
                    commands = [commands]
    elif type(func_cmd) == str:
        commands = [func_cmd]
    else:
        commands = func_cmd
    with ConnectHandler(**device) as ssh:
        if log:
            logging.info(ssh_msg.format(device['host']))
        ssh.enable()
        result = ssh.send_config_set(commands)
        err,state = check_for_error(result)
        if state:
            logging.info(err_msg.format(device['host']))
    return result

def thread_command(devices,filename,limit=3,**kwarg):
    Raise_Value_Exception_Error (kwarg)
    show_worker = False
    config_worker = False
    for key,value in kwarg.items():
        if key == 'show':
            thread_func = send_show_command
            thread_arg = value
            show_worker = True
            break
        elif key == 'config':
            thread_func = send_config_command
            thread_arg = value
            config_worker = True
            break
        else:
            out_error = 'Function Action is not acceptable'
            print(out_error)
            return
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = [executor.submit(thread_func,device,thread_arg) for device in devices]
        for f in as_completed(future_list):
            thread_result = f.result()
            if show_worker:
                for thread_command,command_result in thread_result.items():
                    string_to_file (filename,command_result,prompt=thread_command)
            else:
                string_to_file(filename,thread_result)
    return
if __name__ == "__main__":
    config_command_dict = {'10.2.2.11':['vlan 11','name VLAN-11'],'10.2.2.13':['ip acess-list extended DEVNET','permit ip any any']}
    config_command_list = ['ip routing','router ospf 100','network 0.0.0.0 0.0.0.0 area 0']
    config_command_str = 'ip http server'
    show_command_str = 'show clock'
    show_command_list = ["sh clock","sh cdp nei"]
    show_command_dict = {"10.2.2.11":[ "sh ip int br","show clock"],"10.2.2.13": "sh cdp nei"}
    out_file = 'netmiko_1_thread.txt'
    with open ('/root/Desktop/PYNENG-FOLDER/devices.yml') as f:
        devices = yaml.safe_load(f)
    admin_user = stdiomask.getpass(prompt= 'Admin_user: ',mask='*')# default mask is '*'
    admin_password = stdiomask.getpass (prompt= 'Admin_password: ',mask='')# to remove mask set it to empty string
    enable_secret = stdiomask.getpass (prompt= 'Enable Secret: ',mask='#')
    for device in devices:
        device.update({'username':admin_user,'password':admin_password,'secret':enable_secret})
    thread_command(devices,out_file,config=config_command_dict)    
