import re
import yaml
import csv
from pprint import pprint
from tabulate import tabulate
import draw_network_topology
def create_unique_dict(param_dict):
    uniq_dict = {}
    dup_key_value =[]
    for dict_key in param_dict.keys():
        if dict_key in param_dict.values():
            dup_key_value.append(param_dict[dict_key])
        if dict_key not in dup_key_value:
            uniq_dict[dict_key] = param_dict[dict_key]
    return uniq_dict
def parse_sh_cdp_neighbors(file_str):
    regex = re.compile(r'(\S+) +(\D+ \d/\d) +\d+ +[RSI ]+ +\S+ +(\D+ \d/\d)')
    hostname = re.search('(\S+)>show cdp neighbors',file_str).group(1)
    full_list = regex.findall(file_str)
    full_dict = {}
    full_dict[hostname] = {}
    for entry in full_list:
        full_dict[hostname][entry[1]] = {}
        full_dict[hostname][entry[1]][entry[0]] = entry[2]
    return full_dict
def generate_topology_from_cdp (list_of_files,save_to_filename=None):
    cdp_dict = {}
    for file_ in list_of_files:
        with open(file_) as f:
            one_dict = parse_sh_cdp_neighbors(f.read())
        cdp_dict.update(one_dict)
    formatted_dict = {}
    for x,y in cdp_dict.items():
        for x1,y1 in y.items():
            value = (list(y1.keys())[0],list(y1.values())[0])
            key = (x,x1)
            formatted_dict[key]=value
    graph_dict = create_unique_dict(formatted_dict)
    if save_to_filename:
        with open (save_to_filename,'w') as file_write:
            yaml.dump(cdp_dict,file_write, default_flow_style=False)
            print ("File suucesfully save to {}".format(save_to_filename))
        return graph_dict
    else:
        return graph_dict


if __name__ == "__main__":
    files = ['sh_cdp_n_sw1.txt','sh_cdp_n_r1.txt','sh_cdp_n_r2.txt','sh_cdp_n_r3.txt',
            'sh_cdp_n_r4.txt','sh_cdp_n_r5.txt','sh_cdp_n_r6.txt']
    path = '/root/Desktop/PYNENG-FOLDER/exercises/17_serialization/'
    filenames = [path + x for x in files]
    out_file = 'cdp_nei.yaml'
    topo_dict = generate_topology_from_cdp(filenames,out_file)
    draw_network_topology.draw_topology(topo_dict,'img/topo_2')


