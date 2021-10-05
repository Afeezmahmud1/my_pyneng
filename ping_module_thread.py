from pprint import pprint
import ipaddress
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tabulate import tabulate
from datetime import datetime

def check_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return True
    except:
        return False

def ping_ip(ip):
    logging.basicConfig(format = '%(threadName)s %(name)s %(levelname)s: %(message)s',level=logging.INFO)
    start_msg = '===> {} ping start for: {}'
    received_msg = '<=== {} ping end for: {}'
    if check_ip(ip):
        #logging.info(start_msg.format(datetime.now().time(), ip))
        ping = subprocess.run(['ping','-c','3',ip],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        #logging.info(received_msg.format(datetime.now().time(), ip))
        if ping.returncode == 0:
            return ip,'reachable'
        else:
            return ip,'unreachable'
    else:
        return ip,'bad ip'
def print_ip_table(tuple_of_ip_status_list):
    reachable_list,unreachable_list,bad_ip = tuple_of_ip_status_list
    dict_of_list = {'Reachable':reachable_list ,'Unreachable':unreachable_list,'Bad Ip':bad_ip}
    print(tabulate(dict_of_list,headers='keys',tablefmt="grid"))



def ping_ip_address(ip_list,thread_limit=5):
    with ThreadPoolExecutor(max_workers=thread_limit) as executor:
        reachable_list = []
        unreachable_list = []
        bad_ip = []
        future_list = [executor.submit(ping_ip,ip) for ip in ip_list]
        for f in as_completed(future_list):
            func_ip,func_status = f.result()
            if func_status == 'reachable':
                reachable_list.append(func_ip)
            elif func_status == 'unreachable':
                unreachable_list.append(func_ip)
            else:
                bad_ip.append(func_ip)
    return reachable_list,unreachable_list,bad_ip

if __name__ == '__main__':
    ip_list = ['10.2.2.1','10.2.2.2','127.0.0.1','4.2.2.2','8.8.8.8']
    output = ping_ip_address(ip_list)
    print_ip_table(output)



