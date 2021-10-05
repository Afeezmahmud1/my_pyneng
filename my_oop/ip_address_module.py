

class IPAddress():
    def __init__(self,ip_mask):
        self.ip,self.mask = self._confirm_ip(ip_mask)
    def _confirm_ip(self,ip_mask):
        try:
            ip,mask = ip_mask.split('/')
            x_lst = ip.split('.')
            x_list = [int(x) for x in x_lst]
            mask = int(mask)
            a,b,c,d = x_list
        except ValueError:
            print("ValueError: Incorrect IPv4 address")
            return
        if not all (x in range(0,256) for x in x_list):
            raise ValueError("ValueError: Incorrect IPv4 Address ")
        if mask not in range(8,33):
            raise ValueError("ValueError: Incorrect Network Mask")
        return ip,mask
    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"
    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"
if __name__ == "__main__":
    ip = IPAddress('10.1.1.4/14')
    print(ip)
    ip

