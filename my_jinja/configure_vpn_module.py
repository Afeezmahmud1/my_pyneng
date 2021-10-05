import yaml
from  generate_config_module import generate_config
from jinja2 import Environment,FileSystemLoader
from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoTimeoutException
import re

def get_tun_num (tun_str_set):
    tun_set = {int (x) for x in tun_str_set}
    if not tun_set: 
        return 0
    x = 0
    for element in tun_set:
        if x == element:
            x = x+1
        else:
            return x
    return x
def get_tunnel_id_list (device_dict):
     with ConnectHandler(**device_dict) as ssh:
         ssh.enable()
         show_out = ssh.send_command('show ip int brief | in Tunnel')
     if not show_out:
         return set(show_out)
     tun_intf_list = re.findall(r'Tunnel(\d+)',show_out)
     return set(tun_intf_list)   

def configure_device(device_dict,cfg_str):
    cfg_list = cfg_str.splitlines()
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        device_out = ssh.send_config_set(cfg_list)
    return device_out

def configure_vpn(src_device_params,dst_device_params,src_template,dst_template,vpn_data_dict):
    src_tunnel_set = get_tunnel_id_list(src_device_params)
    dst_tunnel_set = get_tunnel_id_list(dst_device_params)
    func_set = src_tunnel_set.union(dst_tunnel_set)
    tun_num_id = get_tun_num(func_set)
    vpn_data_dict.update({'tun_num': tun_num_id})
    src_cfg = generate_config(src_template,vpn_data_dict)
    dst_cfg = generate_config(dst_template,vpn_data_dict)
    src_configured = configure_device(src_device_params,src_cfg)
    dst_configured = configure_device(dst_device_params,dst_cfg)
    return src_configured,dst_configured
if __name__ == '__main__':
    router1_dict = cisco_router = {
            'device_type': 'cisco_ios',
            'host': '10.2.2.11',
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco',
            }
    router2_dict = {
            'device_type': 'cisco_ios',
            'host': '10.2.2.13',
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco',
            }

    router1_template = 'templates/gre_src_template.txt'
    router2_template = 'templates/gre_dst_template.txt'
    with open ('data_files/gre_ipsec_vpn.yml') as f:
        routers_data_dict = yaml.safe_load(f)
    a,b = configure_vpn(router1_dict,router2_dict,router1_template,router2_template,routers_data_dict)
    print (a)
    print(b)
    
