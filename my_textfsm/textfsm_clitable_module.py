from textfsm import clitable
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor,as_completed
from pprint import pprint
import yaml


def get_command_output_from_device(device_dict,command):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        cmd_out = ssh.send_command(command)
    return cmd_out

def parse_command_to_dict(device_dict,arg,index='index',vendor='cisco_ios'):
    command,template_path = arg
    host_ip = device_dict['host']
    show_output = get_command_output_from_device(device_dict,command)
    cli_table = clitable.CliTable(index, template_path)
    attributes = {'Command': command, 'Vendor': vendor}
    cli_table.ParseCmd(show_output, attributes)
    #print('CLI Table output:\n', cli_table)
    #print('Formatted Table:\n', cli_table.FormattedTable())
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    out_dict = [dict(zip(header,row)) for row in data_rows]
    return {host_ip:out_dict}

def send_and_parse_command_parallel(devices,command,template_path,limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        thread_func = parse_command_to_dict
        thread_arg = (command,template_path)
        func_dict = {}
        future_list = [executor.submit(thread_func,device,thread_arg) for device in devices]
        for f in as_completed(future_list):
            thread_result = f.result()
            func_dict.update(thread_result)
    return func_dict

if __name__ == "__main__":
    devices = yaml.safe_load(open('/root/Desktop/PYNENG-FOLDER/devices.yml'))
    command = 'show ip int brief'
    template_path = 'templates'
    pprint( send_and_parse_command_parallel(devices,command,template_path))




