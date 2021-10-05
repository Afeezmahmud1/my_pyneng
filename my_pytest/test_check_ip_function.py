import ipaddress
from check_ip_function import check_ip

def test_check_ip ():
    assert check_ip ( '10.1.1.1' ) == True , ' With the correct IP, the function should return True '
    assert check_ip ( '500.1.1.1' ) == False , 'If the address is incorrect, function should return False '

