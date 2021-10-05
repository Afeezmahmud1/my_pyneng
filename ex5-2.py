
ip_address = input("Enter the Ip network in the format A.B.C.D/Z : ")

ip_mask = ip_address.split('/')

ip1,ip2,ip3,ip4 = [int(ip) for ip in ip_mask[0].split('.')]

mask_len = int(ip_mask[1])

mask = '1'*mask_len + '0'*(32-mask_len)

m1_bin,m2_bin,m3_bin,m4_bin = mask[:8],mask[8:16],mask[16:24],mask[24:32]

m1_int,m2_int,m3_int,m4_int = int(m1_bin,2),int(m2_bin,2),int(m3_bin,2),int(m4_bin,2)



net_out = f'''

          Network:

          {ip1:<8} {ip2:<8}  {ip3:<8}  {ip4:<8} 

          {ip1:<08b} {ip2:<08b}  {ip3:<08b}  {ip4:<08b}



          Mask:

          /{mask_len}

          {m1_int:<8}  {m2_int:<8}  {m3_int:<8}  {m4_int:<8}

          {m1_int:<08b}  {m2_int:<08b}  {m3_int:<08b}  {m4_int:<08b}

          '''

print(net_out)

