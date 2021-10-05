from textfsm import clitable
import yaml
from netmiko import ConnectHandler
from pprint import pprint
from tabulate import tabulate

def get_command_output_from_device(device_dict,command):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        cmd_out = ssh.send_command(command)
    return cmd_out

def parse_command_to_dict(cmd,raw_out):
    cli_table = clitable.CliTable('index','templates')
    attributes = {'Command': cmd, 'Vendor': 'cisco_ios'}
    cli_table.ParseCmd(raw_out, attributes)
    #print('CLI Table output:\n', cli_table)
    #print('Formatted Table:\n', cli_table.FormattedTable())
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    out_dict = [dict(zip(header,row)) for row in data_rows]
    return out_dict

cmd= 'sh ip int br'
device_dict = {
            "device_type": "cisco_ios",
            "host": "10.2.2.11",
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
}
if __name__ == "__main__":
    cmd_out = get_command_output_from_device(device_dict,cmd)
    print(cmd_out)
    print('\n')
    pc = parse_command_to_dict('show ip int br', cmd_out)
    pprint(pc,width=200)

