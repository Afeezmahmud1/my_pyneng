from textfsm import clitable
import yaml
from pprint import pprint
from tabulate import tabulate
def parse_command_to_dict(cmd,raw_out):
    cmd_out = open('output/sh_ip_int_br.txt').read()
    cli_table = clitable.CliTable('index','templates')
    attributes = {'Command': cmd, 'Vendor': 'cisco_ios'}
    cli_table.ParseCmd(cmd_out, attributes)
    #print('CLI Table output:\n', cli_table)
    #print('Formatted Table:\n', cli_table.FormattedTable())
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    out_dict = [dict(zip(header,row)) for row in data_rows]
    return out_dict

pc = parse_command_to_dict('show ip int br','output/sh_ip_int_br.txt')
pprint(pc,width=200)

