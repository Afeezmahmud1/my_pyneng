'''
###############################################################################
 VERSION 2 with DICTIONARY
 out_dict = {} ### take note

with open ("/root/Desktop/PYNENG-FOLDER/exercises/07_files/CAM_table.txt") as f:

     for line in f:

         if 'Gi0/' in line.rstrip():

             vlan_id = line.rstrip().split()[0]

             out_dict[vlan_id] ={} ### take note

             out_dict[vlan_id]['id'] =  line.rstrip().split()[0]

             out_dict[vlan_id]['mac_add']  =  line.rstrip().split()[1]

             out_dict[vlan_id]['dyn'] = line.rstrip().split()[2]

             out_dict[vlan_id]['intf']  =  line.rstrip().split()
####################################################################################
'''
out_list = []
out_dict = {}
vlan_db = []
with open ("/root/Desktop/PYNENG-FOLDER/exercises/07_files/CAM_table.txt") as f:
    for line in f:
        try:
            vlan_id = line.rstrip().split()[0]
            i_d = int(vlan_id)
        except (ValueError,IndexError):
            continue
        else:
            vlan_id=line.rstrip().split()[0]
            mac_add = line.rstrip().split()[1]
            intf = line.rstrip().split()[3]
            out_list.append((int(vlan_id),mac_add,intf))
            vlan_db.append(int(vlan_id))

out_list.sort()

for line in out_list:
    print(f"{line[0]:<8}{line[1]:<18}{line[2]}")

vlan_in_db = False
while not vlan_in_db:
    vlan_is_digit = False
    while not vlan_is_digit:
        id_vlan = input(" Enter the vlan to diplay in MAC DB: ")
        try:
            id_vlan = int(id_vlan)
        except ValueError:
            print("The VLAN You've Entered is not a Number")
            continue
        else:
            vlan_is_digit = True
    if id_vlan not in vlan_db:
        print("The VLAN You've Entered does not Have Host/Interface in IT")
        continue
    else:
        vlan_in_db = True
for line in out_list:
    if id_vlan in line:
        print(f"{line[0]}    {line[1]}    {line[2]}")



