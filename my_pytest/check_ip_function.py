import ipaddress

def check_ip(ip):
    #return False
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError as err:
        return False
def test_check_ip ():
    assert check_ip ( '10.1.1.1' ) == True , ' With the correct IP, the function should return True '
    assert check_ip ( '500.1.1.1' ) == False , 'If the address is incorrect, function should return False '

if __name__ =="__main__":
    print(check_ip('10.1.1.'))

