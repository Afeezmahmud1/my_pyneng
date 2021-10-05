import csv
import re
from tabulate import tabulate
def write_inventory_to_csv(List_of_file_with_sh_version, sh_version_csv_file):
    out_list = []
    for file_ in List_of_file_with_sh_version:
        with open (file_) as f:
            filename = file_.split('/')[-1]
            *ignore,hostname,_=re.split('[/_.]',file_)#use list unpacking to get hostname from filepath
            regex = re.compile(r'Cisco IOS Software, \d+ \D+ \S+, Version +(\S+), RELEASE.+?'
                    r'router uptime is (\d+ days, \d+ hours, \d+ minutes).+?'
                    r'System image file is "(\S+)"',re.DOTALL)
            sample_out = regex.search(f.read()).groups()
            list_sample_out = [[hostname] + list(sample_out)]
            out_list += list_sample_out
    with open (sh_version_csv_file,'w') as f:
            csv_write = csv.writer(f)
            column = ['hostname','ios','uptime','image']
            csv_write.writerow(column)
            csv_write.writerows(out_list)
            print(tabulate(out_list,headers=column, tablefmt="grid"))
if __name__ == "__main__":
    path = '/root/Desktop/PYNENG-FOLDER/exercises/17_serialization/'
    list_x = ['sh_version_r1.txt', 'sh_version_r2.txt','sh_version_r3.txt']
    sh_version_file_list = [path+x for x in list_x]
    write_inventory_to_csv(sh_version_file_list,'sh_version.csv')




