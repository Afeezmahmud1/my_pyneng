with open("/root/Desktop/PYNENG-FOLDER/exercises/07_files/ospf.txt") as f:
    for line in f:
        d,pfx,ad_met,via,next_hop,last_update,out_intf = line.rstrip().split()
        ad_met = ad_met.strip('[]')
        last_update = last_update.rstrip(',')
        code_out = f'''
        Prefix                 {pfx}
        AD Metric              {ad_met}
        Next hop               {next_hop}
        Last update            {last_update}
        Outbound Interface     {out_intf}
        '''
        print(code_out)

print("Thank you")

