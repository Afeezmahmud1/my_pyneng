import telnetlib
#from my_clitable import parse_command_to_dict
from tabulate import tabulate
import time
#import textfsm
from textfsm import clitable
from pprint import pprint

class CiscoTelnet():
    def __init__ (self,ip,username,password,secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self._telnet = telnetlib.Telnet(ip)
        self._telnet.read_until(b"Username")
        self._telnet.write(f"{username}\n".encode("utf-8"))
        self._telnet.read_until(b"Password")
        self._telnet.write(f"{password}\n".encode("utf-8"))
        index, m, output = self._telnet.expect([b">", b"#"])
        if index == 0:
            self._telnet.write("enable\n".encode("utf-8"))
            self._telnet.read_until(b"Password")
            self._telnet.write(f"{secret}\n".encode("utf-8"))
            self._telnet.read_until(b"#", timeout=5)
        self._telnet.write(b"terminal length 0\n")
        self._telnet.read_until(b"#", timeout=5)
        time.sleep(3)
        self._telnet.read_very_eager()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self._telnet.close()
    def close(self):
        self._telnet.close()
    def _write_command(self,cmd_str):
        cmd_byte =  f"{cmd_str}\n".encode("utf-8")
        self._telnet.write(cmd_byte)
    def _parse_command_output(self,cli_command,unstructured_output):
        cli_table = clitable.CliTable('index','templates')
        attributes = {'Command':cli_command,'Vendor': 'cisco_ios'}
        cli_table.ParseCmd(unstructured_output,attributes)
        data_rows = [list(row) for row in cli_table]
        header = list(cli_table.header)
        structured_output = [dict(zip(header,row)) for row in data_rows]
        return structured_output
    def send_show_command(self,commands,parse=True):
        if type(commands) == str:
            commands = [commands]
        result = ''
        for command in commands:
            self._write_command(command)
            output = self._telnet.read_until(b"#", timeout=5).decode("utf-8")
            result += output.replace("\r\n", "\n")
        if parse and len(commands) == 1:
            cmd_str,*z = commands
            parse_out = self._parse_command_output(cmd_str,result)
            return parse_out
        else:
            return result
    def config_mode(self):
        self._write_command('config t')
        output = self._telnet.read_until(b"#", timeout=5).decode("utf-8")
        return output.replace("\r\n", "\n")
    def exit_config_mode(self):
        self._write_command('end')
        output = self._telnet.read_until(b"#", timeout=5).decode("utf-8")
        return output.replace("\r\n", "\n")
    def _check_for_error(self,config_out):
        status = False
        err1 = ''
        error_list = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']
        for error in error_list:
            if error in config_out:
                status = True
                err1 = error
                break
        return error,status
    def _get_error_message(self,func_out):
        out_list = func_out.splitlines()
        for element in out_list:
            if '%' in element:
                error_mark = element
                break
        return error_mark

    def send_config_command(self,commands,strict=True):
        if isinstance(commands,str):
            commands = [commands]
        result = ''
        err_str=''
        result += self.config_mode()
        for command in commands:
            self._write_command(command)
            output= self._telnet.read_until(b"#", timeout=5).decode("utf-8")
            refined_output = output.replace("\r\n", "\n")
            error,state = self._check_for_error(output)
            if strict:
                if state:
                    error_msg = self._get_error_message(refined_output)
                    raise ValueError(f'When executing the command {command} on device: {self.ip} an error occurred -> {error_msg}')
            else:
                if state:
                    error_msg = self._get_error_message(refined_output)
                    print( f'When executing the command {command} on device: {self.ip} an error occurred -> {error_msg}')
            result += refined_output
        result += self.exit_config_mode()
        return result
    
if __name__ == "__main__":
    device_dict = {'ip': '10.2.2.11',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    show_command = ['show cdp nei det']
    config_cmd = ['router eigrp 100','ntwork 10.0.0.0 0.0.0.0','r']
    with CiscoTelnet(**device_dict) as telnet:
        command_out = telnet.send_config_command(config_cmd,strict=True)
    print ("Unstructured Output")
    print(command_out)
    





