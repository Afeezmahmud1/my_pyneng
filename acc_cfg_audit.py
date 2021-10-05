from pprint import pprint
from concurrent.futures import ThreadPoolExecutor,as_completed
import re
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException)
from paramiko.ssh_exception import SSHException
import yaml
import json
import stdiomask
from datetime import datetime
from telnet_module import CiscoTelnet

start_time = datetime.now()

def string_to_file(filename,input_string,prompt=False):
    split_input_string = input_string.splitlines()
    split_input_string_plus_newline= [element+'\n' for element in split_input_string]
    with open (filename,'a') as f_write:
        if prompt:
            f_write.write(prompt)
        f_write.write('\n')
        f_write.writelines(split_input_string_plus_newline)
    return

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

def send_telnet_show_commands (device,commands):
    result = {}
    host = device['ip']
    try:
        with CiscoTelnet(**device) as telnet:
            #ssh.enable()
            if type(commands) == str:
                commands = [commands]
            for command in commands:
                rsa_key = telnet.send_show_command(command,parse=False)
                match = re.search('% Key pair was generated',rsa_key)
                err,state = check_for_error(rsa_key)
                if state:
                    status = "ssh not supported"
                    result[host] = status
                    return result
                elif match:                                   #'Key type: RSA KEYS' in out_list:
                    config_cmd = ['ip ssh version 2','line vty 0 15','transport input ssh']
                    status = "ssh enabled_disabling telnet..."
                    cfg_status = telnet.send_config_command(config_cmd,strict=True)
                    result[host] = status
                    return result
                else:
                    status = "ssh not enabled"
                    result[host] = status
                    return  result

    except:
        #print(f"Unknown Error occur while Attempting to login to {device['host']}")
        #return device['host']
        return {host:'unable to Login'}

def send_commands(R1,**command):
    Raise_Value_Exception_Error(command)
    for key,value in command.items():
        if key == 'show':
            show_out =  send_telnet_show_commands(R1,command['show'])
            return show_out
        elif key == 'config':
            config_out = send_config_commands(R1,command['config'])
            return config_out
        else:
            print("Unkown function parameter")

def thread_command(devices,filename,limit=3,**kwarg):
    Raise_Value_Exception_Error (kwarg)
    show_worker = False
    config_worker = False
    for key,value in kwarg.items():
        if key == 'show':
            thread_func = send_telnet_show_commands
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
        all_dict = {}
        future_list = [executor.submit(thread_func,device,thread_arg) for device in devices]
        for f in as_completed(future_list):
            thread_result = f.result()
            if show_worker:
                all_dict.update(thread_result)
        with open(filename,'a') as f:
            json.dump(all_dict,f,sort_keys=True,indent=2)
    return


if __name__ == "__main__":
    admin_user = input("Login Username: ")
    admin_password = stdiomask.getpass(prompt='password: ')
    admin_enable = stdiomask.getpass(prompt='enable password: ')
    show_cmds = ["sh crypto key mypubkey rsa"]
    with open("telnet_devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        dev.update({'username':admin_user,'password' : admin_password,'secret' : admin_enable})
    out_file = 'acc_file.json'
    thread_command(devices,out_file,show=show_cmds)

    #all_devices = {}
    #for dev in devices:
    #    dev.update({'username':admin_user,'password' : admin_password,'secret' : admin_enable})
    #    per_device = send_commands(dev,show=show_cmds)
    #    all_devices[dev['ip']]=per_device
    #pprint(all_devices,width=200)
    #pprint(per_device,width=200)
    #print(datetime.now()-start_time)
