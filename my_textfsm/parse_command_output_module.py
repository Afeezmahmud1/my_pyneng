from netmiko import ConnectHandler
import textfsm
from pprint import pprint
from tabulate import tabulate

def parse_command_output(cmd_template,cmd_output):
    with open(cmd_template) as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(cmd_output)
    return fsm.header,result
if __name__ == '__main__':
    r1_params = {
            "device_type": "cisco_ios",
            "host": "10.2.2.11",
            "username": "cisco",
            "password": "cisco",
            "secret": "cisco",
            }
    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")
    #with open ('output/port-channel1.txt') as f:
    #output= f.read()
    header,result = parse_command_output("templates/sh_ip_int_br.template", output)
    print(tabulate(result,headers=header))
