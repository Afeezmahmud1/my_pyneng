ask_ip = input("Enter the ip in (A.B.C.D/n) notation: " )

ip_str,mask= ask_ip.split('/')

ip_list = ip_str.split('.')

int_ip = [int(ip) for ip in ip_list]

bin_ip = f"{int_ip[0]:08b}{int_ip[1]:08b}{int_ip[2]:08b}{int_ip[3]:08b}"

mask = int(mask)



net_mask = '1'*mask + '0'*(32-mask)

net_id = bin_ip[:mask]+'0'*(32-mask)

bcast_id = bin_ip[:mask]+'1'*(32-mask)



dec_bcast_id = [int(bcast_id[:8],2),int(bcast_id[8:16],2),int(bcast_id[16:24],2),int(bcast_id[24:32],2)]

dec_net_id = [int(net_id[:8],2),int(net_id[8:16],2),int(net_id[16:24],2),int(net_id[24:32],2)]

dec_mask_id = [int(net_mask[:8],2),int(net_mask[8:16],2),int(net_mask[16:24],2),int(net_mask[24:32],2)]



code_out = f'''

            Network/Prefix:

            {dec_net_id[0]:<8} . {dec_net_id[1]:<8} . {dec_net_id[2]:<8} . {dec_net_id[3]:<8}

            {dec_net_id[0]:<08b} . {dec_net_id[1]:<08b} . {dec_net_id[2]:<08b} . {dec_net_id[3]:<08b}



            Mask/Prefix-Length:

            /{mask}

            {dec_mask_id[0]:<8} . {dec_mask_id[1]:<8} . {dec_mask_id[2]:<8} . {dec_mask_id[3]:<8}

            {dec_mask_id[0]:<08b} . {dec_mask_id[1]:<08b} . {dec_mask_id[2]:<08b} . {dec_mask_id[3]:<08b}

    

           Broadcast id:

            {dec_bcast_id[0]:<8} . {dec_bcast_id[1]:<8} . {dec_bcast_id[2]:<8} . {dec_bcast_id[3]:<8}

           '''

print(code_out)



