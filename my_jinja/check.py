import yaml
from pprint import pprint
with open ('check.yml') as f:
    x = yaml.safe_load(f)
pprint(x['ospf'])
pprint(x)

for networks in x['ospf']:
    print(networks['network'])
    print(networks['area'])
    break


