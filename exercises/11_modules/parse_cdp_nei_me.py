def parse_cdp_neighbors(f_read_str):
    out_line = f_read_str.splitlines()
    for line in out_line[:3]:#Look at the first three lines for hostname
        if '>' in line:
            hostname = line.split('>')[0]
        elif '#' in line and '(' in line:
            hostname = line.split('#')[0].split('(')[0]
        elif '#' in line:
            hostname = line.split('#')[0]
#Get table header and the index in order to know where the main display start from
    for index,header in enumerate(out_line):
        if header.startswith('Device ID'):
            cdp_header = header
            header_index = index
    cdp_main = out_line[(header_index+1):] # Main data starts from index header plus one

#List comprehension to get list of local and remote parameters
    local_intf_list =   [''.join(x.split()[1:3]) for x in cdp_main]
    local_name_list =   [hostname]*len(local_intf_list)
    remote_name_list =  [x.split()[0] for x in cdp_main]
    remote_intf_list = [''.join(x.split()[-2:]) for x in cdp_main]

#Combine the list together to get the desired dictionary
    '''
    cdp_out_dict = {}
    for x in  range((len(local_intf_list))):
            key = (local_name_list[x],local_intf_list[x])
            value = (remote_name_list[x],remote_intf_list[x])
            cdp_out_dict[key] = value
    '''
    #dictionary comprehension
    cdp_out_dict = {(local_name_list[x],local_intf_list[x]):(remote_name_list[x],remote_intf_list[x]) for x in range((len(local_intf_list)))}

#other ways to combine the list using zip function
    '''
    key_local_device_name_int_tuple_list = list(zip(local_name_list,local_intf_list))
    value_remote_device_name_int_tuple_list = list(zip(remote_name_list,remote_intf_list))
    cdp_out_dict = dict(zip(key_local_device_name_int_tuple_list,value_remote_device_name_int_tuple_list))
    '''

    cdp_out_dict = dict(zip(list(zip(local_name_list,local_intf_list)),list(zip(remote_name_list,remote_intf_list))))

#Return the final dictionary  output
    return cdp_out_dict

#Separate exportable from non export able code

if __name__ == "__main__":
    var1 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r1.txt'
    var2 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r2.txt'
    var3 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r3.txt'
    var4 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_sw1.txt'
    with open (var4) as cdp_file:
        print(parse_cdp_neighbors(cdp_file.read()))



