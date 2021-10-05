out_range = False
while not out_range:
    not_integer=False
    while not not_integer:
        ip_add = input("Enter ip (A.B.C.D) :")
        try:
            ip_list = ip_add.split('.')
            ip_int = [int(ip) for ip in ip_list]
            a,b,c,d = ip_int
        except ValueError:
            print ("One of the Ip Value is not a Number or contains more than four Octet")
        else:
            not_integer = True
    if ( a not in range(0,256) or b not in range(0,256) or c not in range(0,256) or d not in range(0,256) ):
        print("One of the Ip Octet is Greater than 255")
    else:
        print("Ip meets all requirements")
        out_range=True
if (a in range (1,224)):
    print(f"Ip Address : {ip_add} you entered is a UNICAST ADDRESS")
elif (a in range (224,240)):
    print("Ip Address : {} you entered is a MULTICAST ADDRESS".format(ip_add))
elif (a==b==c==d==255):
    print("{} ip address you entered is a BROADCAST ADDRESS".format(ip_add))
elif (a==b==c==d==0):
    print("{} ip address you entered is UNASSIGNED ADDRESS".format(ip_add))
else:
    print(f"{ip_add} ip address is UNUSED")

