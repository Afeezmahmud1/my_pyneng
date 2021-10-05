import re
from pprint import pprint
def generate_description_from_cdp(filename):
    with open (filename) as f:
        nei_desc = {}
        for line in f:
            cmd = re.search(r'(\S+)'
             r' +(\D+ \S+)'
             r' +\d+ +([RSI ]+)\S+ +'
             r'(\D+ \S+)'
             ,line)
            if cmd:
                value = re.sub(r'(\S+)'
                         r' +(\D+ \S+)'
                         r' +\d+ +([RSI ]+)\S+ +'
                         r'(\D+ \S+)'
                         ,r'Description Connected to  \1 port \4',line)
                nei_desc[cmd.group(2)] = value
    return nei_desc
if __name__ == "__main__":
    code_out = generate_description_from_cdp('sh_cdp_n_sw1.txt')
    pprint(code_out)

