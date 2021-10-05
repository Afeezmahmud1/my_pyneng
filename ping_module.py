import ipaddress
import subprocess
from tabulate import tabulate

def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False
def convert_ranges_to_ip_list(ip_list):
    expanded_ip_list = []
    for ip in ip_list:
        if check_ip(ip):
           expanded_ip_list.append(ip)
        elif ip.split('-')[1].isdigit():
            start_ip = int(ip.split('-')[0].split('.')[-1])
            stop_ip = int(ip.split('-')[1]) + 1
            for x in range(start_ip,stop_ip):
                *ip_first_three_octet,last_octet = ip.split('-')[0].split('.')
                derived_ip = f"{'.'.join(ip_first_three_octet)}.{str(x)}"
                expanded_ip_list.append(derived_ip)
        elif check_ip(ip.split('-')[0]) and check_ip(ip.split('-')[1]):
            *ip_first_three_octet,last_octet_start = ip.split('-')[0].split('.')
            _,_,_,last_octet_stop = ip.split('-')[1].split('.')
            for x in range((int(last_octet_start)),(int(last_octet_stop)+1)):
                derived_ip = f"{'.'.join(ip_first_three_octet)}.{str(x)}"
                expanded_ip_list.append(derived_ip)
    return expanded_ip_list
def print_ip_table(tuple_of_ip_status_list):
    reachable_list,unreachable_list = tuple_of_ip_status_list
    dict_of_list = {'Reachable':reachable_list ,'Unreachable':unreachable_list}
    print(tabulate(dict_of_list,headers='keys',tablefmt="grid"))


def ping_ip_address(raw_ip_list):
    ip_list = convert_ranges_to_ip_list(raw_ip_list)
    available_ip_list = []
    unavailable_ip_list = []
    for ip in ip_list:
        if check_ip(ip):
            ping = subprocess.run(['ping','-c','2',ip],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            if ping.returncode == 0:
                available_ip_list.append(ip)
            else:
                unavailable_ip_list.append(ip)
        else:
            bad_ip_list.append(ip)
    print_input =  (available_ip_list,unavailable_ip_list)
    print_ip_table(print_input)

if __name__ == "__main__":
    my_ip_list = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132','4.2.2.2','127.0.0.1']
    ip_list = ['10.2.2.1','10.2.2.2','127.0.0.1','4.2.2.2','8.8.8.8']
    ping_ip_address(ip_list)


