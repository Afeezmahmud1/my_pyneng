from netmiko import CiscoIosSSH

class Mynetmiko(CiscoIosSSH):
    def __init__(self,host,username,password,secret):
        super().__init__(host,username,password,secret)

