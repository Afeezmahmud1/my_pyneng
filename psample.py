from pprint import pprint
import re
import pexpect
def send_show_commands(ip,username,password,enable,commands,prompt='#'):
    with pexpect.spawn( f'ssh {username}@{ip}',timeout = 10, encoding="utf-8") as ssh:
        ssh.expect('[Pp]assword')
        ssh.sendline(password)
        enable_status = ssh.expect(['>','#'])
        if enable_status == 0:
            ssh.sendline('enable')
            ssh.expect('[Pp]assword')
            ssh.sendline(enable)
            ssh.expect(prompt)
        ssh.sendline('terminal len 0')
        ssh.expect(prompt)
        result = {}
        for command in commands:
            ssh.sendline(command)
            match = ssh.expect([prompt,pexpect.TIMEOUT,pexpect.EOF])
            if match == 1:
                print(f"Symbol {prompt} is not found in output result output is written to dictionary")
            if match == 2:
                print("Connection has been terminated by Server")
                return result
            else:
                output = ssh.before
                result[command] = output.replace("\r\n","\n")
        return result
if __name__  == "__main__":
    devices = ['192.168.10.2','192.168.10.3']
    commands = ['show clock','sh cdp nei']
    for ip in devices:
        output = send_show_commands(ip,'cisco','cisco','cisco',commands)
        pprint(output, width=120)


