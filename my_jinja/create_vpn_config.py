import yaml
from  generate_config_module import generate_config
from jinja2 import Environment,FileSystemLoader

def create_vpn_config(template1,template2,data_dict):
    return generate_config(template1,data_dict),generate_config(template2,data_dict)

if __name__ == '__main__':
    src_template = 'templates/gre_src_template.txt'
    dst_template = 'templates/gre_dst_template.txt'
    with open('data_files/gre_ipsec_vpn.yml') as f:
        tunnel_data = yaml.safe_load(f)
    src_gre_config,dst_gre_config = create_vpn_config(src_template,dst_template,tunnel_data)
    print (src_gre_config)
    print(dst_gre_config)


