from base_connect_class import BaseSSH
import stdiomask
import time
class CiscoSSH(BaseSSH):
    def __init__(self,device_type,host,username=False,password=False,secret=False):
        if not username:
            username = input("Enter username: ")
        if not password:
            password = stdiomask.getpass(prompt="Enter Login passowrd: ")
        if not secret:
            secret= stdiomask.getpass(prompt="Enter enable password: ")
        #device_param = {'host':host,'username':username,'password':password,'secret':secret}
        #super().__init__(**device_param)
        self.host = host
        self.device_type= device_type
        self.username = username
        self.password = password
        self.secret = secret
        super().__init__(device_type=self.device_type,host=self.host,username=self.username,password=self.password,secret=self.secret)
        self.ssh.enable()
    def close(self):
        self.ssh.disconnect()

if __name__ == "__main__":
    dev_dict = {
            'device_type': 'cisco_ios',
            'host': '10.2.2.11',
            'username':'cisco',
            'password':'cisco',
            }

    r1 = CiscoSSH(**dev_dict)
    r1_out = r1.send_show_command('show ip int br')
    r1.close()
    print(r1_out)
