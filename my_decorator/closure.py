from netmiko import ConnectHandler
def netmiko_closure_func (**device_param):
    ssh = ConnectHandler(**device_param)
    ssh.enable()
    def send_show_command(command):
        return ssh.send_command(command)
    def send_config_command(command):
        return ssh.send_config_set(command)
    def cli():
        pass
    cli.show = send_show_command
    cli.config = send_config_command
    return cli
if __name__ == "__main__":
    dev_dict = {'device_type' : 'cisco_ios',
                 'host':'10.2.2.11',
                 'username':'cisco',
                 'password':'cisco',
                 'secret':'cisco'
                 }
    r1 = netmiko_closure_func(**dev_dict) # =  cli function and it remembers ssh state
    print(r1.config('logging 10.2.2.12')) #= send_show_command('show clock')

