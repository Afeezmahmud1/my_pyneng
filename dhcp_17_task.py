import csv
import re
from tabulate import tabulate
def write_dhcp_snooping_to_csv(List_of_file_with_sh_dhcp, dhcp_csv_file):
    out_list = []
    for file_ in List_of_file_with_sh_dhcp:
        with open (file_) as f:
            filename = file_.split('/')[-1]
            hostname = re.search('(.*?)_.*',filename).group(1)#disable greedy behaviour of * with ?
            regex = re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d{1,4}) +(\S+)')
            sample_out = regex.findall(f.read())
            list_sample_out = [[hostname] + list(sample_out[x]) for x in range(0,len(sample_out))]
            out_list += list_sample_out
    with open (dhcp_csv_file,'w') as f:
            csv_write = csv.writer(f)
            column = ['switch','mac','ip','vlan','interface']
            csv_write.writerow(column)
            csv_write.writerows(out_list)
            print(tabulate(out_list,headers=column, tablefmt="grid"))
if __name__ == "__main__":
    path = '/root/Desktop/PYNENG-FOLDER/exercises/17_serialization/'
    list_x = ['sw1_dhcp_snooping.txt','sw2_dhcp_snooping.txt','sw3_dhcp_snooping.txt']
    dhcp_snooping_file_list = [path+x for x in list_x]
    write_dhcp_snooping_to_csv(dhcp_snooping_file_list,'dhcp_snooping.csv')




